import streamlit as st
import pandas as pd
import pickle as pk


#___________Load Objects__________#
restaurants = pd.read_csv(r'models/restaurants.csv', usecols=['Restaurant Name','Cuisine','Rating','Location','Revised Rating'])

with open(r'models/restaurant_sim.pkl', 'rb') as f:
    SIMILARITIES = pk.load(f)

ALL_LOCATIONS = pd.Series(restaurants['Location'].unique())

#____________Functions___________#
def get_restaurants(curr_location):
    return restaurants[restaurants['Location'] == curr_location]['Restaurant Name']


def get_topN(curr_location):
    # Candidate ranking
    candidates = restaurants[restaurants['Location'] == curr_location].sort_values(by='Revised Rating', ascending=False)
    ranked = candidates[['Restaurant Name', 'Cuisine', 'Rating']].head(10)
    return ranked.sample(4).reset_index(drop=True)


def get_recommendations(curr_location, restaurant, top_n : int = 8) -> pd.DataFrame:
    """
    Returns a frame of recommended restaurants based on the cosine similarity of restaurants in the area
    1. recommend - number of items to recommend
    """
    restaurant_idx  = restaurants[(restaurants['Restaurant Name'] == restaurant) & (restaurants['Location'] == curr_location)].index[0]
    restaurants_in_area = restaurants[(restaurants['Location'] == curr_location)].index

    #list of tuples (idx, similarity value)
    similarity_for_X = list(enumerate(SIMILARITIES[restaurant_idx]))

    #list of only those tuples from the same location
    similarity_in_area = [ x for x in similarity_for_X if x[0] in restaurants_in_area]
    #sort by similarity values
    similarity_in_area = sorted(similarity_in_area, key= lambda x: x[1], reverse=True)

    return restaurants.iloc[[item[0] for item in similarity_in_area[:top_n]]].sample(4).reset_index(drop=True)


#___________________page____________________#

font_ = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">New image</p>'

note_container = st.container()
header_container = st.container()
title_div, select_div = st.columns([5,1])

with header_container:
    title_div.title("Restaurant Recommender")

    current_location = select_div.selectbox('Your Location', ALL_LOCATIONS, int(ALL_LOCATIONS[ALL_LOCATIONS == 'Bangalore'].index[0]),
                                            key='location_select')

    

with note_container:
        st.toast('Your current location is set to {}'.format(current_location))

st.divider()

st.subheader(
    'Top rated restaurants near you'
)

#get topN recommendations
topN = get_topN(curr_location = current_location)
top1, top2, top3, top4 = st.columns([1,1,1,1], gap='medium')

with top1:
    st.markdown('<p style="font-size: 18px;">{}</p>'.format(topN.loc[0, 'Restaurant Name']), unsafe_allow_html=True)
    st.image(r'images/r2.jpg')
    st.caption('{}:star: Ratings'.format(topN.loc[0, 'Rating']), unsafe_allow_html=True)

with top2:
    st.markdown('<p style="font-size: 18px;">{}</p>'.format(topN.loc[1, 'Restaurant Name']), unsafe_allow_html=True)
    st.image(r'images/r1.jpg')
    st.caption('{}:star: Ratings'.format(topN.loc[1, 'Rating']), unsafe_allow_html=True)

with top3:
    st.markdown('<p style="font-size: 18px;">{}</p>'.format(topN.loc[2, 'Restaurant Name']), unsafe_allow_html=True)
    st.image(r'images/r3.jpg')
    st.caption('{}:star: Ratings'.format(topN.loc[2, 'Rating']), unsafe_allow_html=True)

with top4:
    st.markdown('<p style="font-size: 18px;">{}</p>'.format(topN.loc[3, 'Restaurant Name']), unsafe_allow_html=True)
    st.image(r'images/r4.jpg')
    st.caption('{}:star: Ratings'.format(topN.loc[3, 'Rating']), unsafe_allow_html=True)

st.divider()

st.subheader(
    'Based on your previous orders'
)

restaurants_at_loc = get_restaurants(current_location) 
prev_order = st.selectbox('You previously ordered at', restaurants_at_loc, key='restaurant_select')

st.caption('We recommend')

n_recommends = get_recommendations(curr_location=current_location, restaurant=prev_order)
recommend1, recommend2, recommend3, recommend4 = st.columns([1,1,1,1], gap='medium')

with recommend1:
    st.markdown('<p style="font-size: 18px;">{}</p>'.format(n_recommends.loc[0, 'Restaurant Name']), unsafe_allow_html=True)
    st.image(r'images/r5.jpg')
    st.caption('{}:star: Ratings'.format(n_recommends.loc[0, 'Rating']), unsafe_allow_html=True)

with recommend2:
    st.markdown('<p style="font-size: 18px;">{}</p>'.format(n_recommends.loc[1, 'Restaurant Name']), unsafe_allow_html=True)
    st.image(r'images/r6.jpg')
    st.caption('{}:star: Ratings'.format(n_recommends.loc[1, 'Rating']), unsafe_allow_html=True)
     
with recommend3:
    st.markdown('<p style="font-size: 18px;">{}</p>'.format(n_recommends.loc[2, 'Restaurant Name']), unsafe_allow_html=True)
    st.image(r'images/r7.jpg')
    st.caption('{}:star: Ratings'.format(n_recommends.loc[2, 'Rating']), unsafe_allow_html=True)
     
with recommend4:
    st.markdown('<p style="font-size: 18px;">{}</p>'.format(n_recommends.loc[3, 'Restaurant Name']), unsafe_allow_html=True)
    st.image(r'images/r8.jpg')
    st.caption('{}:star: Ratings'.format(n_recommends.loc[3, 'Rating']), unsafe_allow_html=True)
