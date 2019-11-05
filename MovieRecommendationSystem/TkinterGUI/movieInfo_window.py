import tkinter as tk
import GlobalFun
import threading
import metaFun_GUI
import TkinterGUI.metaFrame
import TkinterGUI.metaButtons
global Images
Images=[]

class movieinfo_window():

    def __init__(self,root,window,movieid,userid):
        self.movieid=movieid
        self.userid=userid
        self.window=window
        self.root = root

        navbar_Frame = tk.Frame(self.window, width=800, height=20)  # 导航栏
        navbar_Frame.pack_propagate(False)
        navbar_Frame.place(x=0, y=0, anchor="nw")
        TkinterGUI.metaButtons.NavigationBar(self.root, self.window, navbar_Frame, self.movieid, self.userid, type="I")

        self.frm_content = tk.Frame(self.window,width=800,height=500,bg="white")#电影相关内容
        self.frm_content.place(x=0,y=20)
        self.url_imdbid = metaFun_GUI.get_movie_url(movieid=self.movieid)
        self.src,self.title,self.date,self.genres,self.briefinfo = metaFun_GUI.get_src(self.url_imdbid,self.movieid)
        self.tk_image=metaFun_GUI.get_image(self.src,w_box=300,h_box=300)
        Images.append(self.tk_image)#为了在tkinter中显示图片，无所不用其极

        #放海报
        self.frm_content_l = tk.Frame(self.frm_content,width=375,height=500,bg="white")
        self.frm_content_l.place(x=0,y=0,anchor="nw")
        tk.Label(self.frm_content_l,image=self.tk_image).place(x=130,y=17,anchor="nw")

        #获取评分数据
        self.score,self.times = self.get_score()
        tk.Label(self.frm_content_l, text="Score:{:.2f}/5\tTimes:{}".format(self.score, self.times)).place(x=115, y=330, anchor="nw")

        #用户打分
        if self.userid is not None:
            metaFun_GUI.basedFrame(self.frm_content_l, self.userid, self.movieid)

        #放内容
        self.frm_content_r = tk.Frame(self.frm_content, bg="white", height=500, width=500)
        self.frm_content_r.place(x=380, y=0, anchor="nw")
        tk.Label(self.frm_content_r, text="TITLE:{}".format(self.title), font=("", 15), height=1).place(x=0, y=17)  # title行
        tk.Label(self.frm_content_r, text="DATE:{}".format(self.date), font=("", 15), height=1).place(x=0, y=50)  # date行
        self.genres = self.genres.strip('""').replace(",", "").replace('"', "").replace(" ", '')
        tk.Label(self.frm_content_r, text="GENRES:\n" + self.genres, font=("", 15)).place(x=0, y=85)
        tk.Label(self.frm_content_r, text="DESCRIPTION:\n" + self.briefinfo.replace('\\u0027', '\''), font=("", 15),
                 wraplength=300, justify="left", height=10).place(x=0, y=220)

        # 基于SVD显示5部相似电影
        # 从mysql中movie_similar_svd中提取相似电影
        tk.Label(self.window, text="Similar Movies Based on SVD").place(x=25, y=445, anchor="nw")
        self.data_SVD = metaFun_GUI.get_similar_movie_list(self.movieid,type="SVD")
        self.frm_svd = tk.Frame(self.window, bg="green")
        self.frm_svd.place(x=15, y=470, anchor="nw")
        for tup in self.data_SVD:
            t = threading.Thread(target=self.job,args=(tup[0],tup[1],self.frm_svd))
            t.start()

        # 基于ALS显示5部相似电影
        # 从mysql中movie_similar_als中提取相似电影
        tk.Label(self.window, text="Similar Movies Based on ALS").place(x=25, y=650, anchor="nw")
        self.data_ALS = metaFun_GUI.get_similar_movie_list(self.movieid,type="ALS")
        self.frm_als = tk.Frame(self.window, bg="green")
        self.frm_als.place(x=15, y=670, anchor="nw")
        for tup in self.data_ALS:
            t = threading.Thread(target=self.job, args=(tup[0], tup[1], self.frm_als))
            t.start()

    def get_score(self):
        #获取评分数据
        conn,cur = GlobalFun.ConnectSql()
        sql = "select score,times from movierecommender.movie_score_info where movieid={};".format(self.movieid)
        cur.execute(sql)
        data = cur.fetchall()
        score = data[0][0]#电影的平均
        times = data[0][1]#电影被点评的次数
        return score,times

    def job(self,movieid,similarDegree,frm):
        temp = TkinterGUI.metaFrame.metaFrame(movieid, self.userid, frm, self.window, self.root,type="similarDegree",similarDegree=similarDegree)
        Images.append(temp.tk_image)
        temp.frm.pack(side='left')
