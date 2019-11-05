import tkinter as tk
import GlobalFun
import threading
import TkinterGUI.metaFrame
import TkinterGUI.main_window
import TkinterGUI.metaButtons
global Images
Images=[]

class BrowseFootprints():

    def __init__(self,root,window,movieid,userid,):
        self.movieid = movieid
        self.userid = userid
        self.window = window#铺的纸
        self.root = root

        navbar_Frame = tk.Frame(self.window, width=800, height=20)  # 导航栏
        navbar_Frame.pack_propagate(False)
        navbar_Frame.place(x=0, y=0, anchor="nw")
        TkinterGUI.metaButtons.NavigationBar(self.root, self.window, navbar_Frame, self.movieid, self.userid, type="B")

        #从mysql中提取用户的浏览记录
        conn,cur = GlobalFun.ConnectSql()
        sql = "select movieid,rating,timestamp from movierecommender.ratings where userid={}  order by timestamp desc limit 15;".format(self.userid)
        cur.execute(sql)
        data = cur.fetchall()#记录用户的打分情况
        sql = "select count(rating) from movierecommender.ratings where userid={};".format(self.userid)
        cur.execute(sql)
        num_rated_movie = cur.fetchall()[0][0]
        GlobalFun.Closesql(conn,cur)
        #显示用户投票了几部电影
        if num_rated_movie <= 1:
            tk.Label(self.window,text="You have rate {} movie,we only show the recent 15 movies".format(num_rated_movie)).place(x=0,y=20,anchor='nw')
        else:
            tk.Label(self.window, text="You have rate {} movies,we only show the recent 15 movies".format(num_rated_movie)).place(x=0,y=20,anchor='nw')

        #电影展示页面
        if num_rated_movie == 0:
            tk.Label(self.window,text="No movies you have rated",font=('',20)).place(x=250,y=156,anchor="nw")
        if num_rated_movie > 0:
            #只显示一行
            self.list1_Frame = tk.Frame(self.window)
            self.list1_Frame.place(x=15,y=130)
            movielist1 = data[:5]
            for tup in movielist1:
                t=threading.Thread(target=self.job,args=(self.list1_Frame,tup[0],tup[1],tup[2]))
                t.start()


        if num_rated_movie >5:
            self.list2_Frame = tk.Frame(self.window)
            self.list2_Frame.place(x=15, y=363)
            movielist2 = data[5:10]
            for tup in movielist2:
                t=threading.Thread(target=self.job,args=(self.list2_Frame,tup[0],tup[1],tup[2]))
                t.start()


        if num_rated_movie >10:
            #再显示一行
            self.list3_Frame = tk.Frame(self.window)
            self.list3_Frame.place(x=15, y=590)
            movielist3 = data[10:15]
            for tup in movielist3:
                t=threading.Thread(target=self.job,args=(self.list3_Frame,tup[0],tup[1],tup[2]))
                t.start()


    def job(self,Frame,movieid,rating,timestamp):
        temp = TkinterGUI.metaFrame.metaFrame(movieid, self.userid, Frame, self.window, self.root,type='browse',timestamp=timestamp,rate=rating)
        Images.append(temp.tk_image)
        temp.frm.pack(side='left')



