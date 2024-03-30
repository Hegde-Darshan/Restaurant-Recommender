from scipy import sparse as sparse
import numpy as np
import pandas as pd

import pickle as pkl


#___________Load Objects__________#
restaurants = pd.read_csv(r'models/restaurants.csv', usecols=['Restaurant Name','Cuisine','Rating','Location','Revised Rating'])

SIMILARITIES = sparse.load_npz("models/sparse_sim.npz")
print(type(SIMILARITIES))

#SIMILARITIES = SIMILARITIES.toarray()

def get_recommendations(curr_location : str, restaurant: str, recommend : int = 8) -> pd.DataFrame:
    """
    Returns a frame of recommended restaurants based on the cosine similarity of restaurants in the area

    curr_location - Current location selected
    restaurant - restaurant name previously ordered in the location
    recommend - number of items to recommend
    """
    restaurant_idx  = restaurants[(restaurants['Restaurant Name'] == restaurant) & (restaurants['Location'] == curr_location)].index[0]
    restaurants_in_area = restaurants[(restaurants['Location'] == curr_location)].index

    #list of tuples (idx, similarity value)
    print(SIMILARITIES.getrow(restaurant_idx).toarray()[0])
    similarity_for_X = list(enumerate(SIMILARITIES.getrow(restaurant_idx).toarray()[0]))

    #list of only those tuples from the same location
    similarity_in_area = [ x for x in similarity_for_X if x[0] in restaurants_in_area]
    #sort by similarity values
    similarity_in_area = sorted(similarity_in_area, key= lambda x: x[1], reverse=True)

    return restaurants.iloc[[item[0] for item in similarity_in_area[:recommend]]].sample(4).reset_index(drop=True)

n_recommends = get_recommendations(curr_location="Bangalore", restaurant="Starbucks Coffee")

print(n_recommends)
