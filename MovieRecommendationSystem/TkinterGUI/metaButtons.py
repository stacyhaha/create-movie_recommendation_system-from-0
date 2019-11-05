#将所有主页上涉及到的按钮统一在这个模块中
#一共是分为4种页面
# IMBS
# I：电影信息页
# M：推荐主页
# B：用户浏览页
# S：搜索页面

import TkinterGUI.browseFootprints
import TkinterGUI.main_window
import TkinterGUI.movieInfo_window
import TkinterGUI.search_window
import RecommendationAlogrithm.OnlineRecommend
import tkinter as tk
import GlobalVar
import GlobalFun
import tkinter.messagebox

class Login_register_Button():
    def __init__(self,root , window ,nagvibar, movieid , userid ,type="M"):
        self.movieid = movieid
        self.userid = userid
        self.window = window #当前的主幕布
        self.nagvibar = nagvibar#当前的小幕布
        self.root = root #窗口根目录
        self.type = type #确定所在的页面种类，方便刷新页面"M" "B" "I"
        s = tk.StringVar()
        if self.userid is None:
            s.set('Login|Register')
        else:
            s.set('Logout')
        self.Button = tk.Button(self.nagvibar,textvariable=s,command=self.trigger)

    def trigger(self):
        if self.userid is None:
            self.login()
        else:
            #开启毁灭模式
            print("I am destroying the Main_Frame")
            print('Prepare to create a new window')
            self.userid = None
            self.update()#刷新页面
            print('Well Done!')

    def login(self):#登陆的那一套
        self.window_sign_up = tk.Toplevel(self.root)
        self.window_sign_up.geometry("459x345")
        self.window_sign_up.title('Login|Register')

        self.name = tk.StringVar()
        self.name.set("1~610")
        tk.Label(self.window_sign_up,text="UserId:").place(x=50,y=57)
        tk.Entry(self.window_sign_up,textvariable=self.name).place(x=103,y=57)

        self.password = tk.StringVar()
        tk.Label(self.window_sign_up,text="Password:").place(x=34,y=117)
        tk.Entry(self.window_sign_up,textvariable=self.password,show='*').place(x=103,y=117)

        #温馨提示
        tk.Label(self.window_sign_up,text="The recorded userId is from 1 to 610\nPassword is identical to  userId\nIf you want to register a new user,\nplease start from 611.",justify='left').place(x=103,y=166)
        tk.Button(self.window_sign_up,text="Login/register",command=self.comfirm).place(x=282,y=253)

    def comfirm(self):
        #判断userid是否异常
        try:
            name = eval(self.name.get())
        except:
            tk.messagebox.showerror(message="The user name must be integer")
            return
        if not isinstance(name,int):
            tk.messagebox.showerror(message="The user name must be integer")
            return
        conn,cur = GlobalFun.ConnectSql()
        cur.execute("select password from movierecommender.users where userid={}".format(self.name.get()))
        data = cur.fetchall()
        if len(data)==0:
            #记录新用户
            cur.execute("insert into movierecommender.users values({},{})".format(self.name.get(),self.password.get()))
            conn.commit()
            tk.messagebox.showinfo(message="Welcome :>\nNew User:{}".format(self.name.get()))
            self.window_sign_up.destroy()
            self.userid = eval(self.name.get())

            #触发online_recommend添加上新用户的推荐列表
            RecommendationAlogrithm.OnlineRecommend.insertnewuser(self.userid)
            self.update()#刷新页面

        else:
            if data[0][0] == self.password.get():
                tk.messagebox.showinfo(message="Welcome :D\n User:{}".format(self.name.get()))
                self.window_sign_up.destroy()
                self.userid = eval(self.name.get())
                self.update()
            else:
                tk.messagebox.showerror(message="Sorry :<\nThe password is wrong")

    def update(self):
        self.window.destroy()
        self.newFrame = tk.Frame(self.root, width=800, height=900)
        self.newFrame.place(x=0, y=0, anchor='nw')
        if self.type == "M" or self.type == "B":
            TkinterGUI.main_window.Main_window(self.root, self.newFrame, self.movieid, self.userid)
        elif self.type == "I":
            TkinterGUI.movieInfo_window.movieinfo_window(self.root, self.newFrame, self.movieid, self.userid)
        else:
            TkinterGUI.search_window.Search_window(self.root,self.newFrame,self.movieid,self.userid)

class Search_Button():
    def __init__(self , root , window , nagvibar, movieid, userid):
        self.movieid = movieid
        self.userid = userid
        self.nagvibar = nagvibar#当前的小幕布
        self.window = window  # 当前的主幕布
        self.root = root  # 窗口根目录
        self.Button = tk.Button(self.nagvibar, text="Search", command=self.turn2search)

    def turn2search(self):
        print("I am destroying the browseFootprints")
        self.window.destroy()
        print('I am creating a new Frame for Main_window')
        self.newFrame = tk.Frame(self.root, width=800, height=900)
        self.newFrame.place(x=0, y=0, anchor='nw')
        print('Prepare to create Search window')
        TkinterGUI.search_window.Search_window(self.root, self.newFrame, self.movieid, self.userid)
        print('Well Done!')


class Main_window_Button():
    def __init__(self , root , window , nagvibar, movieid, userid):
        self.movieid = movieid
        self.userid = userid
        self.nagvibar = nagvibar#当前的小幕布
        self.window = window  # 当前的主幕布
        self.root = root  # 窗口根目录
        self.Button = tk.Button(self.nagvibar, text="Main Window", command=self.turn2main)

    def turn2main(self):
        print("I am destroying the browseFootprints")
        self.window.destroy()
        print('I am creating a new Frame for Main_window')
        self.newFrame = tk.Frame(self.root, width=800, height=900)
        self.newFrame.place(x=0, y=0, anchor='nw')
        print('Prepare to create Main Window')
        TkinterGUI.main_window.Main_window(self.root, self.newFrame, self.movieid, self.userid)
        print('Well Done!')


class Browse_Button():
    def __init__(self , root , window ,nagvibar, movieid, userid):
        self.movieid = movieid
        self.userid = userid
        self.nagvibar = nagvibar#当前的小幕布
        self.window = window  # 当前的幕布
        self.root = root  # 窗口根目录
        self.Button = tk.Button(self.nagvibar, text="BrowseFootprints", command=self.turn2Browse)

    def turn2Browse(self):
        print("I am destroying the Main_Frame")
        self.window.destroy()
        print('I am creating a new Frame for BrowseFootprint')
        self.newFrame = tk.Frame(self.root, width=800, height=900)
        self.newFrame.place(x=0, y=0, anchor='nw')
        print('Prepare to create BrowseFootprint window')
        TkinterGUI.browseFootprints.BrowseFootprints(self.root, self.newFrame, self.movieid, self.userid)
        print('Well Done!')


class NavigationBar():
    def __init__(self , root , window , nagvibar, movieid, userid , type):
        self.movieid = movieid
        self.userid = userid
        self.nagvibar = nagvibar
        self.window = window  # 当前的幕布
        self.root = root  # 窗口根目录
        self.type = type

        if userid is not None:#在登陆状态
            tk.Label(self.nagvibar, text='Welcome :D\tUser:{}'.format(self.userid), font=('', 15)).pack(side='left')
            Login_register_Button(self.root, self.window, self.nagvibar, self.movieid, self.userid,
                                  self.type).Button.pack(side="right")
            if self.type == "I" or self.type == "M" or self.type == "S":
                Browse_Button(self.root,self.window,self.nagvibar,self.movieid,self.userid).Button.pack(side="right")

            if self.type == "I" or self.type == "B" or self.type == "S":
                Main_window_Button(self.root,self.window,self.nagvibar,self.movieid,self.userid).Button.pack(side='right')

            if self.type != 'S':
                Search_Button(self.root, self.window, self.nagvibar, self.movieid, self.userid).Button.pack(
                    side="right")

        else:#非登陆状态
            Login_register_Button(self.root, self.window, self.nagvibar, self.movieid, self.userid,
                                  self.type).Button.pack(side="right")
            if self.type == "I" or self.type == "S":
                Main_window_Button(self.root, self.window,self.nagvibar, self.movieid, self.userid).Button.pack(side="right")
            if self.type != 'S':
                Search_Button(self.root, self.window,self.nagvibar, self.movieid, self.userid).Button.pack(side="right")

if __name__ == "__main__":
    Root = GlobalVar.BigWindow
    Root.geometry('800x900')
    Frame = tk.Frame(Root,width=800,height=20,bg='black')
    Frame.pack_propagate(False)
    Frame.pack()
    # a = Login_register_Button(Root,Frame,1,1,type='B')
    NavigationBar(Root, Frame,Frame, 1, 1, type='I')
    # a = NavigationBar(Root, Frame, 1, None, type='B')

    Root.mainloop()
