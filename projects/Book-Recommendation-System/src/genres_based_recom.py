import pandas as pd
from load_data import rating_df, movie_df


# get n_reviewers and average rating
movie_rating_df = movie_df.copy()
movie_rating_df['n_reviewers'] = rating_df.groupby('movieid')['rating'].count().reset_index()['rating']
movie_rating_df['avg_rating'] = rating_df.groupby('movieid')['rating'].mean().reset_index()['rating']

# recommend functions
# recommend most popular movies, measure for "most popular": viewed/rated by most users. 
def top_popular_movie(genres):
    genres_filter = movie_rating_df['genres'].apply(lambda x: genres in x)
    rating_theshold = 3 #movie_rating[genres_filter]['n_reviewers'].mean()
    rating_filter = movie_rating_df['avg_rating']>rating_theshold
    sorted_filtered_movies = movie_rating_df[genres_filter&rating_filter].sort_values(by='n_reviewers', ascending=False)
    return sorted_filtered_movies[['movieid', 'title']] #.to_list()

# recommend high-rated movies, measure for "highly-rating": sorted by avg rating, but only movies with more than certain number of viewers will be considered. 
def top_high_rated_movie(genres):
    genres_filter = movie_rating_df['genres'].apply(lambda x: genres in x)
    nreviewers_theshold = 100 # movie_rating[genres_filter]['n_reviewers'].mean()
    nreviewers_filter = movie_rating_df['n_reviewers'] > nreviewers_theshold
    sorted_filtered_movies = movie_rating_df[genres_filter&nreviewers_filter].sort_values(by='avg_rating', ascending=False)
    return sorted_filtered_movies[['movieid', 'title']] #.to_list()

# evaluate results
assert len(top_popular_movie(genres = 'Animation')) == 71
assert len(top_high_rated_movie(genres = 'Animation')) == 64

