import tkinter as tk
import TkinterGUI.movieInfo_window
import metaFun_GUI
import time
class metaFrame():
    """
    形成一个小的Frame单元
    """
    def __init__(self,movieId, userId ,window,Bigwindow,Allwindow,type="base",**kw):
        self.movieId = movieId
        self.userId = userId
        self.window = window
        self.Bigwindow = Bigwindow
        self.Allwindow = Allwindow
        self.url_imdbid = metaFun_GUI.get_movie_url(movieid=self.movieId)  # 得到imbd网站中对应的url
        self.src, self.title, self.date, self.genres, self.briefinfo = metaFun_GUI.get_src(self.url_imdbid,self.movieId)  # 爬得电影海报的scr等信息

        # 建立主框架
        self.frm = tk.Frame(self.window, width=90, height=120)

        # 根据不同的type进行样式的小修改
        if type == "browse":
            tk.Label(self.frm, text='Your rate:{}'.format(kw['rate']), font=('', 10)).pack()
            tk.Label(self.frm,text='Rate Time:{}'.format(time.strftime('%Y-%m-%d',time.localtime(kw['timestamp']))),font=('',10)).pack()

        if type == "similarDegree":
            tk.Label(self.frm,text='Similar Degree:{:.2f}'.format(kw['similarDegree']),font=('',9)).pack()

        # 获得电影海报
        self.tk_image = metaFun_GUI.get_image(self.src)
        self.button = tk.Button(self.frm, image=self.tk_image, width=80, height=120, bg="brown",command=self.createmovieinfo)
        self.button.pack()

        # 获取电影名称和上映时间
        tk.Label(self.frm, text="{}".format(self.title), width=20, height=1, font=('', 10)).pack()
        tk.Label(self.frm, text="{}".format(self.date), width=20, height=1, font=('', 10)).pack()


    def createmovieinfo(self):
        print("I am destroying the Frame")
        self.Bigwindow.destroy()
        print('I am creating a new Frame')
        self.Frame = tk.Frame(self.Allwindow, width=800, height=900)
        self.Frame.place(x=0, y=0, anchor="nw")
        print('prepare to create a new movie info window')
        TkinterGUI.movieInfo_window.movieinfo_window(self.Allwindow, self.Frame, self.movieId, self.userId)
        print("Done!")
