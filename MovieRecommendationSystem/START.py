# import TkinterGUI.movieInfo_window
import tkinter as tk
import GlobalVar
import TkinterGUI.browseFootprints
import TkinterGUI.main_window
import TkinterGUI.search_window
#测试movieinfo_window.py页
# Root = GlobalVar.BigWindow
# Root.geometry('800x900')
# Frame = tk.Frame(Root,width=800,height=900)
# Frame.place(x=0,y=0,anchor="nw")
# TkinterGUI.movieInfo_window.movieinfo_window(Root, Frame, 1, 1)
# Root.mainloop()

#测试browserFootprints.py页
# Root = GlobalVar.BigWindow
# Root.geometry('800x900')
# Frame = tk.Frame(Root,width=800,height=900)
# Frame.place(x=0,y=0,anchor="nw")
# TkinterGUI.browseFootprints.BrowseFootprints(Root,Frame,1,194)
# Root.mainloop()

#测试main_window
Root = GlobalVar.BigWindow
Root.geometry('800x900')
Frame = tk.Frame(Root,width=800,height=900)
Frame.place(x=0,y=0,anchor="nw")
TkinterGUI.main_window.Main_window(Root,Frame,1,None)
# TkinterGUI.main_window.Main_window(Root,Frame,1,2)
Root.mainloop()

#测试搜索页面
# Root = GlobalVar.BigWindow
# Root.geometry('800x900')
# Frame = tk.Frame(Root,width=800,height=900)
# Frame.place(x=0,y=0,anchor="nw")
# TkinterGUI.search_window.Search_window(Root,Frame,1,None)
# Root.mainloop()


