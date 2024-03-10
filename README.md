# Restaurant Recommendation System

This project is aimed at building a content based recommender system for restaurant recommendations. 

The system provides 2 kinds of recommendations :
- ### Content based filtering based on previous order
    Recommends M restaurants sampled from the top-N restaurants in the same locality considering the previous order (Location, Cuisines and Ratings)

- ### Content based filtering for best rated restaurant in the locality
    Recommends top-N restaurants in the same locality the user is in based solely on a rating metric calculated from Number of Ratings and Average Rating given by the users


### Rating Metric 
Calculated based on Number of Ratings (N) and Average ratings (R) given by users, under a presumption of a minimum Number of Ratings (Th) required to calculate this metric. A is the average rating of the dataset

Revised Rating = (N * R)/(N + Th) + (Th * A)/(N + Th)

