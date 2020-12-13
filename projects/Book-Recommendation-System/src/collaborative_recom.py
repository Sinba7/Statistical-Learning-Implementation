import pandas as pd
from surprise import Dataset, Reader, KNNWithMeans
from load_data import rating_df 


def collab_recommender(train_data, test_data, user_based=True):
    """
    Input: 
    - train_data: n*3, 'userid','movieid','rating'
    - test_data: n*2, 'userid', 'movieid'
    Output:
    - pred_rating: n*2, 'movieid', 'rating'
    """
    reader = Reader(rating_scale=(1,5))
    data = Dataset.load_from_df(train_data, reader)

    sim_options = {
        'name':'cosine', 
        'user_based': user_based
    }
    algo = KNNWithMeans(sim_options=sim_options)

    train_set = data.build_full_trainset()
    algo.fit(train_set)

    pred_rating = {'movieid':[], 'rating':[]}
    for idx in test_data.index:
        pred_rating['movieid'].append(test_data.loc[idx, 'movieid'])
        pred = algo.predict(test_data.loc[idx, 'userid'], test_data.loc[idx, 'movieid'])
        pred_rating['rating'].append(pred.est)
        
    return pd.DataFrame(pred_rating)
    