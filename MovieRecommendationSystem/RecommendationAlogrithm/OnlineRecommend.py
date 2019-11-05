import pandas as pd
import numpy as np
import GlobalVar
import GlobalFun
import pickle

def prework():
    res_svd = pd.read_csv(GlobalVar.pathoffline_recommend_svd)
    res_als = pd.read_csv(GlobalVar.pathoffline_recommend_als)
    mix = pd.concat([res_als,res_svd])
    mix = mix.sort_values(by=['userId', 'predictScore'], ascending=[True, False])
    mix = mix.loc[~mix.duplicated(subset=['recommendId', 'userId']), :]
    useridlist = mix.userId.unique()
    mix_svd_als = pd.DataFrame()
    for userid in useridlist:
        temp = mix.loc[mix.userId == userid, :].sort_values(by='predictScore', ascending=False)[:50]
        mix_svd_als = pd.concat([mix_svd_als, temp])
    pd.DataFrame({'userId':mix_svd_als['userId'],'recommendId':mix_svd_als['recommendId']}).to_csv(GlobalVar.pathonline_recommend,index=False)

def updateonline(userid,nowmovieid):
    '''
    当老用户对新电影进行投票后，按投票分数更新online_recommend的值
    :param userid:
    :param nowmovieid:
    :return:
    '''
    conn,cur = GlobalFun.ConnectSql()
    cur.execute('select movieid from movierecommender.online_recommend where userid = {}'.format(userid))
    optionallist = cur.fetchall()
    cur.execute('select similarid from movierecommender.movie_similar_svd where movieid = {}'.format(nowmovieid))
    similarlist = cur.fetchall()
    cur.execute("select * from movierecommender.ratings where userid = {}".format(userid))
    ratingdata = cur.fetchall()
    ratingdata = np.array(ratingdata)
    mix_list = set(optionallist)|set(similarlist)
    mix_list = np.array([mix[0] for mix in mix_list])
    mix_list = np.array(list(set(mix_list) - set(ratingdata[:, 1])))

    movieIdlist = pickle.load(open(GlobalVar.pathmovieidlist,'rb')).values
    movieIdlist = [*map(int,movieIdlist)]


    cosSim = pickle.load(open(GlobalVar.pathcosSim_svd,'rb'))
    cosSim = pd.DataFrame(cosSim,columns=movieIdlist,index=movieIdlist,copy=True)


    recentmovie = ratingdata[np.argsort(ratingdata[:,-1])[::-1][:5],:]#选取最近评分的五部电影
    preVal1 = cosSim.loc[mix_list,recentmovie[:,1]].values.dot(recentmovie[:,2])/np.sum(cosSim.loc[mix_list,recentmovie[:,1]].values,axis=1)
    highratemovie = recentmovie[:,2]>3
    lowratemovie = recentmovie[:,2]<3
    preVal2 = np.log(np.sum((cosSim.loc[mix_list, recentmovie[:, 1]].values > 0.8) * highratemovie,axis=1)+1)#增强因子
    preVal3 = np.log(np.sum((cosSim.loc[mix_list, recentmovie[:, 1]].values > 0.8) * lowratemovie,axis=1)+1)#减弱因子
    preScore = preVal1+preVal2-preVal3
    newrecommend = mix_list[np.argsort(preScore)[::-1][:50]]
    useridlist = np.array([userid]*len(newrecommend))
    newrecommendValue = ','.join(map(str,[*zip(useridlist,newrecommend)]))
    sqls = ['delete from movierecommender.online_recommend where userid = {}'.format(userid),
            'insert into movierecommender.online_recommend values {}'.format(newrecommendValue)]
    for sql in sqls:
        cur.execute(sql)
        conn.commit()
    GlobalFun.Closesql(conn,cur)
    print('online well done!!!')

def insertnewuser(userid):
    '''
    当新用户注册后，在online_recommend中建立新用户的推荐榜单，初始时，推荐榜单为热门电影的前50
    :param userid:
    :return:
    '''
    conn,cur = GlobalFun.ConnectSql()
    sql = 'insert into movierecommender.online_recommend select {},movieid from movierecommender.movie_score_info order by times desc limit 50;'.format(userid)
    cur.execute(sql)
    conn.commit()
    GlobalFun.Closesql(conn,cur)


if __name__ == "__main__":
    updateonline(2,3)
