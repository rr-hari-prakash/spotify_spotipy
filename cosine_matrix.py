import sys
import os
import logging
import numpy as np
import pandas as pd
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy.oauth2 as oauth2
from functools import reduce
import operator
import time
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from get_sp_data import SpotifyData, Artists, PrepareFeatures

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:8500/'
SCOPE =  'user-top-read'
SHOW_DIALOG = True

class CosineMatrix:
    """Build Cosine similarity matrix"""

    def get_features(self, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG):
        get_sp_data = SpotifyData(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG)
        user_profile = get_sp_data.get_user_top_tracks()
        logging.info('user_profile')
        get_artists = Artists(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG)
        artist_related_artists = get_artists.related_artists(user_profile)
        artists_genres = get_artists.up_artists_genres(user_profile)
        logging.info('artist_related_artists')
        logging.info('artists_genres')
        prepare_features = PrepareFeatures()
        artists_features = prepare_features.bag_of_words(related_artists_df=artist_related_artists, up_artists_genres_df=artists_genres)
        logging.info('artists_features')
        return artists_features, user_profile

    def similarity_matrix(self, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG):
        features, user_profile = self.get_features(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG)
        count = CountVectorizer()
        count_matrix = count.fit_transform(features['bag_of_words'])
        indices = pd.Series(features.index)
        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        return indices, cosine_sim, features, user_profile


def recommendations(title, indices, cosine_sim, df):
    recommended_artists = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indexes = list(score_series.iloc[1:6].index)
    for i in top_10_indexes:
        recommended_artists.append(list(df.index)[i])
    return recommended_artists

# if __name__ == '__main__':
#     cos_sim = CosineMatrix()
#     indices, cosine_sim, features, user_profile = cos_sim.similarity_matrix(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG)
#     recomm = recommendations('2wPsNCwhEGb0KvChZ5DD52', indices, cosine_sim, features)
#     print(recomm)
