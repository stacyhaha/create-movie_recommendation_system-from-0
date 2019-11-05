#preWork_ALS中包括：
#根据ratings.csv文件得到协同过滤矩阵
#基于ALS将矩阵进行分解，保留5个纬度，基于item进行协同过滤
#得到余弦相似度矩阵
#得到movie_similar_svd矩阵，将相似度大于0.88的电影存入
#得到offline_recommend_als矩阵，根据预测后的评分，每个用户保留前100个电影

#这篇文档中的工作应该在程序启动前完成
#实际运行程序时，会将处理好的数据直接导入mysql中
#
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
# rating_matrix_fillzero = rating_matrix.fillna(0)
#
# #进行模型的评价
# rating_train = pickle.load(open("/Users/stacy/code/try movie recommend system/test_data/test_data.pkl",'rb'))
# val = pickle.load(open("/Users/stacy/code/try movie recommend system/test_data/val.pkl",'rb'))
# test_loc = pickle.load(open("/Users/stacy/code/try movie recommend system/test_data/test_loc.pkl","rb"))
# test_row,test_col = zip(*test_loc)
#
# def vec_grad_desc(R,max_iter=5000,lamda=0.004,K=2,alpha=0.0002):
#     max_r2 = 0.224882
#
#     P = np.random.rand(R.shape[0],K)
#     Q = np.random.rand(K,R.shape[1])
#
#     for _ in range(max_iter):
#         for u in range(R.shape[0]):
#             r = np.nonzero(R[u, :] != 0)[0]
#             P[u, :] = P[u, :] - 2 * alpha * (-Q[:,r].dot(R[u, :][r]) + Q[:, r].dot(Q[:, r].T).dot(P[u, :]) + lamda * P[u, :])
#         for i in range(R.shape[1]):
#             r = np.nonzero(R[:, i] != 0)[0]
#             Q[:, i] = Q[:, i] - 2 * alpha * (-P[r,:].T.dot(R[:, i][r]) + P[r, :].T.dot(P[r, :]).dot(Q[:, i]) + lamda * Q[:, i])
#
#         cost = 0
#         predR = np.dot(P,Q)
#         cost += np.sum((R - predR * (R!=0))**2)
#         cost += lamda * (np.sum(P**2)+np.sum(Q**2))
#
#         if _%10 == 0:
#             print()
#             print("num_iter:{},cost:{}".format(_,cost))
#             predData = P.dot(Q)
#             predictVal = predData[test_row, test_col]
#             r2 = 1 - np.sum((val - predictVal) ** 2) / np.sum((val - val.mean()) ** 2)
#             print("r2=%f" % r2)
#             if max_r2<r2:
#                 max_r2=r2
#                 print('load in the better P & Q')
#                 with open('/Users/stacy/code/P_k12_best.pickle', 'wb') as file:
#                     pickle.dump(P, file)
#                 with open('/Users/stacy/code/Q_k12_best.pickle', 'wb') as file:
#                     pickle.dump(Q, file)
#
#         if cost<0.001:
#             break
#
#     return P,Q,cost
#
# P,Q,cost = vec_grad_desc(rating_train,max_iter=1000,lamda=0.0004,K=12,alpha=0.0002)

#计算余弦相似矩阵
Q = pickle.load(open('/Users/stacy/code/Q_k12_best.pickle', 'rb'))
upfactor = Q.T.dot(Q)
normlist = np.linalg.norm(Q,axis=0)
downfactor = normlist.reshape(-1,1).dot(normlist.reshape(1,-1))
cosSim = (upfactor/(2*downfactor))+0.5
# with open('/Users/stacy/code/cosSim_ALS.pickle','wb') as file:
#     pickle.dump(cosSim,file)

#把相似度大于0.88的电影的前25部电影，以movieId,similarId,similarDegree的格式进行保存，
# movieIdList = rating_matrix.columns
# movie_similar_als = pd.DataFrame()
# for i in range(cosSim.shape[0]):
#     movieId = movieIdList[i]
#     print("the movie {} is counting".format(movieId))
#     similarlist = movieIdList[cosSim[i,:]>=0.88]
#     similardegreelist = cosSim[i,:][cosSim[i,:]>=0.88]
#     if len(similardegreelist)>26:
#         index = np.argsort(similardegreelist)[::-1]
#         index = index[:26]
#         similarlist = similarlist[index]
#         similardegreelist = similardegreelist[index]
#     movie_similar_als = pd.concat([movie_similar_als,pd.DataFrame({'movieId':movieId,'similarId':similarlist,'similarDegree':similardegreelist})])
# movie_similar_als = movie_similar_als.loc[movie_similar_als.movieId != movie_similar_als.similarId,:]#删除自己与自己的相似度
# movie_similar_als.to_csv(GlobalVar.pathmovie_similar_als,index=False)

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
predict_matrix.to_csv(GlobalVar.pathoffline_recommend_als,index=False)

#把电影列表保存下来，方便后面调用
with open(GlobalVar.pathmovieidlist,'wb') as file:
    pickle.dump(movieIdList,file)