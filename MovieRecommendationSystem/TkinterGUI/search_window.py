#建立搜索页面，基本类似于broserFootprints的构建
#唯一不同是从数据库movies中检索信息

import tkinter as tk
import GlobalFun
import threading
import TkinterGUI.metaFrame
import TkinterGUI.main_window
import TkinterGUI.metaButtons
global Images
Images=[]

class Search_window():

    def __init__(self,root,window,movieid,userid):
        self.movieid = movieid
        self.userid = userid
        self.window = window#铺的纸
        self.root = root

        navbar_Frame = tk.Frame(self.window, width=800, height=20)  # 导航栏
        navbar_Frame.pack_propagate(False)
        navbar_Frame.place(x=0, y=0, anchor="nw")
        TkinterGUI.metaButtons.NavigationBar(self.root, self.window, navbar_Frame, self.movieid, self.userid, type="S")

        self.searchcontent = tk.StringVar()
        tk.Entry(self.window,textvariable=self.searchcontent).place(x=58,y=48,anchor='nw')
        tk.Button(self.window,text="Search",command=self.get_search).place(x=249,y=48)

        self.result_Frame = tk.Frame(self.window,width=800,height=700)
        self.result_Frame.pack_propagate(False)
        self.result_Frame.place(x=0,y=90,anchor='nw')

    def get_search(self):
        self.result_Frame.destroy()
        self.result_Frame = tk.Frame(self.window, width=800, height=700)
        self.result_Frame.pack_propagate(False)
        self.result_Frame.place(x=0, y=90, anchor='nw')

        searchcontent = self.searchcontent.get()

        #从mysql中搜索相关结果
        conn,cur = GlobalFun.ConnectSql()
        sql = "select movieid from movierecommender.movies where title like '%{}%';".format(searchcontent)
        cur.execute(sql)
        data = cur.fetchall()#记录用户的打分情况
        GlobalFun.Closesql(conn,cur)

        #显示搜索结果
        tk.Label(self.result_Frame, text="We have found {} movies,and only show the recent 15 movies".format(len(data))).place(x=58,y=0,anchor='nw')

        #清空之前的搜索结果

        #电影展示页面
        if len(data) == 0:
            tk.Label(self.result_Frame,text="Sorry,we don't have similar movies",font=('',20)).place(x=250,y=60,anchor="nw")
        if len(data) > 0:
            #只显示一行
            list1_Frame = tk.Frame(self.result_Frame)
            list1_Frame.place(x=15,y=50)
            movielist1 = data[:5]
            for tup in movielist1:
                t=threading.Thread(target=self.job,args=(list1_Frame,tup[0]))
                t.start()


        if len(data) >5:
            list2_Frame = tk.Frame(self.result_Frame)
            list2_Frame.place(x=15, y=258)
            movielist2 = data[5:10]
            for tup in movielist2:
                t=threading.Thread(target=self.job,args=(list2_Frame,tup[0]))
                t.start()


        if len(data) >10:
            #再显示一行
            list3_Frame = tk.Frame(self.result_Frame)
            list3_Frame.place(x=15, y=465)
            movielist3 = data[10:15]
            for tup in movielist3:
                t=threading.Thread(target=self.job,args=(list3_Frame,tup[0]))
                t.start()


    def job(self,Frame,movieid):
        temp = TkinterGUI.metaFrame.metaFrame(movieid, self.userid, Frame, self.window, self.root)
        Images.append(temp.tk_image)
        temp.frm.pack(side='left')



