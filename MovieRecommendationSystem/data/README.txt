原始数据集说明：
原始数据集来自http://movielens.org[MovieLens]电影推荐网站，采集自1996-3-29到2018-9-24，一共包含610名用户对于9742部电影的100836条评分数据。

原始数据集：
* links.csv
* movies.csv

**links.csv文件内容：**  
对于links.csv文件来说，一共是三列特征:
* moviedId:为https://movielens.org 网站使用的电影的标识符  
* imdbld:为http://www.imdb.com 网站使用的电影标识符
* tmdbld:为https://www.themoviedb.org 网站使用的电影标识符号

以movieId=1为例
可以得到：  
在movielens中的网站信息为https://movielens.org/movies/1  
在imdbld中的网站信息为http://www.imdb.com/title/tt0114709/  
在tmdbld中的网站信息为https://www.themoviedb.org/movie/862  

**links.csv文件规模:**  
含有9742部电影的信息  
其中imdbid存在8个缺失值

**links.csv文件应用:**  
关于这个文件，目前想到的就是可以得到对应网站的相关介绍


**movies文件内容**  
一共包含3个特征:
* movieId:电影在MovieLens网站上使用的电影ID
* title:电影名称，并且包含上映时间
* genres:电影类型  

**movies数据规模**  
共包含9742电影的信息,一共是20种类别，比数据说明文件中多IMAX这个类别


**ratings文件内容**  
一共包含4个特征  
* userId:用户id
* moviedId:电影id
* rating:用户评分，评分以5星级为标准，以半星级递增
* timestamp:评分时间戳  

**ratings文件规模**  
一共包含100836条评分记录9742部电影的评分，有评分的电影占总电影数的99.8%

