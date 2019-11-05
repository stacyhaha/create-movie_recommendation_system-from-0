#preWork_SVD中包括：
#根据ratings.csv文件得到协同过滤矩阵
#SVD进行分解，保留5个纬度，基于item进行协同过滤
#得到余弦相似度矩阵
#得到movie_similar_svd矩阵，将相似度大于0.88的电影存入
#得到offline_recommend_svd矩阵，根据预测后的评分，每个用户保留前100个电影

#这篇文档中的工作应该在程序启动前完成
#实际运行程序时，会将处理好的数据直接导入mysql中


import pandas as pd
import numpy as np
import GlobalVar
import pickle


#根据rating.csv得到协同过滤矩阵
ratings = pd.read_csv("{}".format(GlobalVar.pathrating))
rating_dict = {}
for i in range(ratings.shape[0]):
    line = ratings.loc[i,:]
    if line.userId in rating_dict:
        rating_dict[line.userId][line.movieId] = line.rating
    else:
        rating_dict[line.userId] = {line.movieId:line.rating}
rating_matrix = pd.DataFrame(rating_dict).T
rating_matrix_fillzero = rating_matrix.fillna(0)

#使用SVD进行分解
U,sigma,Vt = np.linalg.svd(rating_matrix_fillzero)

#基于item的svd协同过滤
#对数据进行降维
reduced_matrix = (U[:,:5].dot(np.eye(5)*sigma[:5])).T.dot(rating_matrix_fillzero)
#对降维后的电影矩阵进行归一化处理
std_matrix = ((reduced_matrix.T - reduced_matrix.T.mean(axis=0))/reduced_matrix.T.std(axis=0)).T
#计算余弦相似度矩阵
upfactor = std_matrix.T.dot(std_matrix)#分子
downfactor = (np.linalg.norm(std_matrix,axis=0).reshape(-1,1)).dot(np.linalg.norm(std_matrix,axis=0).reshape(1,-1))
cosSim = (upfactor/downfactor + 1)/2#在原本余弦相似度的基础上进行小小修改，将值定在0～1之间
with open(GlobalVar.pathcosSim,"wb") as file:
    pickle.dump(cosSim,file)

#把相似度大于0.88的电影，以movieId,similarId,similarDegree的格式进行保存，数字过小，信息量太大
movieIdList = rating_matrix.columns
movie_similar_svd = pd.DataFrame()

for i in range(cosSim.shape[0]):
    movieId = movieIdList[i]
    similarlist = movieIdList[cosSim[i,:]>=0.88]
    similardegreelist = cosSim[i,:][cosSim[i,:]>=0.88]
    if len(similardegreelist)>26:
        index = np.argsort(similardegreelist)[::-1]
        index = index[:26]
        similarlist = similarlist[index]
        similardegreelist = similardegreelist[index]
    movie_similar_svd = pd.concat([movie_similar_svd,pd.DataFrame({'movieId':movieId,'similarId':similarlist,'similarDegree':similardegreelist})])
movie_similar_svd = movie_similar_svd.loc[movie_similar_svd.movieId != movie_similar_svd.similarId,:]#删除自己与自己的相似度
movie_similar_svd.to_csv(GlobalVar.pathmovie_similar_svd,index=False)

#离线推荐系统
#预测用户未评分的电影评分
#对于每个用户取预测评分最高的50部电影，存入predict_matrix中
predict_matrix = pd.DataFrame()
userIdlist = rating_matrix.index
movieIdList = rating_matrix.columns
for user in range(rating_matrix.shape[0]):
    userId = userIdlist[user]
    unrate = np.isnan(rating_matrix.values[user,:])
    haverated = ~unrate
    predict_Val=(cosSim[unrate,:][:,haverated]).dot(rating_matrix.values[user,:][haverated])/np.sum(cosSim[unrate,:][:,haverated],axis=1)
    recommendId = movieIdList[unrate]
    print(userId)
    if len(predict_Val>100):
        index = np.argsort(predict_Val)[::-1]
        index = index[:100]
        predict_Val = predict_Val[index]
        recommendId = recommendId[index]
    predict_matrix = pd.concat([predict_matrix,pd.DataFrame({'userId':userId,'recommendId':recommendId,'predictScore':predict_Val})])
predict_matrix.to_csv(GlobalVar.pathoffline_recommend_svd,index=False)




