import warnings
import GlobalVar
import GlobalFun

def inputdata():
    warnings.filters
    #创建连接
    conn,cur = GlobalFun.ConnectSql()

    #新建MovieRecommender数据库
    sql_creatDatabase = ["drop database if exists MovieRecommender;",
                        "create database MovieRecommender;",
                         "use MovieRecommender;",
                         ]
    for sql in sql_creatDatabase:
        cur.execute(sql)

    # 把data中的数据导入到mysql中
    #导入数据links.csv(links.csv数据在导入前，将空值写为NULL)
    sql_inputlinks = ["create table links(movieId int,imdbId int,tmdbId int);",
                       r'''load data infile '{}' into table links fields terminated by ',' optionally enclosed by '"' lines terminated by '\n'  ignore 1 lines;'''.format(GlobalVar.pathlink)
                       ]
    for sql in sql_inputlinks:
        cur.execute(sql)



    #导入数据movies.csv
    sql_inputmovies = ["create table movies(movieId int,title varchar(200),genres varchar(100));",
                       r'''load data infile "{}" into table movies fields terminated by ',' optionally enclosed by '"' escaped by '"' lines terminated by '\n' ignore 1 lines;'''.format(GlobalVar.pathmovie),
                       ]
    for sql in sql_inputmovies:
        cur.execute(sql)

    #导入数据ratings
    sql_inputratings = ["create table ratings(userId int,movieId int,rating float,timestamp int)",
                        r'''load data infile "{}" into table ratings fields terminated by ',' lines terminated by '\n' ignore 1 lines'''.format(GlobalVar.pathrating)
                        ]
    for sql in sql_inputratings:
        cur.execute(sql)

    conn.commit()

    #导入数据movie_similar_svd
    sql_inputmovie_similar_svd = ["create table movie_similar_svd(movieId int,similarId int,similarDegree float)",
                                  r'''load data infile "{}" into table movie_similar_svd fields terminated by',' lines terminated by '\n' ignore 1 lines'''.format(GlobalVar.pathmovie_similar_svd)]
    for sql in sql_inputmovie_similar_svd:
        cur.execute(sql)
    conn.commit()

    #导入数据offline_recommend_svd
    sql_inputoffline_recommend_svd = ["create table offline_recommend_svd(userId int,recommendId int,predictScore float)",
                                      r'''load data infile "{}" into table offline_recommend_svd fields terminated by',' lines terminated by '\n' ignore 1 lines'''.format(GlobalVar.pathoffline_recommend_svd)]
    for sql in sql_inputoffline_recommend_svd:
        cur.execute(sql)
    conn.commit()



    #导入数据users
    sql_inputusers = ['create table users (userid int,password varchar(10))',
                      r'''load data infile "{}" into table users fields terminated by ',' lines terminated by '\n' ignore 1 lines'''.format(GlobalVar.pathusers)]
    for sql in sql_inputusers:
        cur.execute(sql)
    conn.commit()

    #导入数据movie_similar_als
    sql_inputmovie_similar_als = ["create table movie_similar_als(movieId int,similarId int,similarDegree float)",
                                  r'''load data infile "{}" into table movie_similar_als fields terminated by ',' lines terminated by '\n' ignore 1 lines'''.format(GlobalVar.pathmovie_similar_als)]
    for sql in sql_inputmovie_similar_als:
        cur.execute(sql)
    conn.commit()

    #导入数据offline_recommend_als
    sql_inputoffline_recommend_als = [
        "create table offline_recommend_als(userId int,recommendId int,predictScore float)",
        r'''load data infile "{}" into table offline_recommend_als fields terminated by',' lines terminated by '\n' ignore 1 lines'''.format(
            GlobalVar.pathoffline_recommend_als)]
    for sql in sql_inputoffline_recommend_als:
        cur.execute(sql)
    conn.commit()


    #导入数据online_recommend
    sql_inputonline_recommend = [
        "create table online_recommend (userId int,movieId int);",
        r'''load data infile "{}" into table online_recommend fields terminated by ',' lines terminated by '\n' ignore 1 lines'''.format(GlobalVar.pathonline_recommend)
    ]
    for sql in sql_inputonline_recommend:
        cur.execute(sql)
    conn.commit()

    GlobalFun.Closesql(conn, cur)

def get_new_table_statistically():
    warnings.filters
    conn, cur = GlobalFun.ConnectSql()
    sql_ = ["use MovieRecommender;",
           "create table movie_score_info select movieId,avg(rating) score,count(*) times from ratings group by movieId;"
           ]
    for sql in sql_:
        cur.execute(sql)
    conn.commit()

    GlobalFun.Closesql(conn, cur)

if __name__ == '__main__':
    inputdata()
    get_new_table_statistically()
