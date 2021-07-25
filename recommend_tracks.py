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
import random
from dotenv import load_dotenv

from cosine_matrix import CosineMatrix, recommendations

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:8500/'
SCOPE =  'user-top-read'
SHOW_DIALOG = True

class RecommendTracks:
    def __init__(self, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG):
        self.SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID
        self.SPOTIPY_CLIENT_SECRET = SPOTIPY_CLIENT_SECRET
        self.REDIRECT_URI = REDIRECT_URI
        self.SCOPE = SCOPE
        self.SHOW_DIALOG = SHOW_DIALOG
        logging.info('Spotify credentials is set and instanciated')

    def get_sp_instance(self):
        sp_oauth=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
                              client_secret=self.SPOTIPY_CLIENT_SECRET,
                              redirect_uri=self.REDIRECT_URI,
                              scope=self.SCOPE)

        token_info = sp_oauth.get_cached_token()

        logging.info('Token: '+ str(token_info))

        if not token_info:
            sp = spotipy.Spotify(auth_manager=sp_oauth)
        elif sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            token = token_info['access_token']
            sp = spotipy.Spotify(auth=token)
        else:
            sp = spotipy.Spotify(auth=token_info['access_token'])

        return sp

    def get_batch_list(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def col_to_list(self, user_track_prof):
        up_track_artist_id = reduce(operator.concat, user_track_prof['track_artist_id'].values.tolist())
        up_album_artist_id = reduce(operator.concat, user_track_prof['album_artist_id'].values.tolist())
        up_unique_artists_id = list(set().union(up_track_artist_id, up_album_artist_id))
        batch_list_ids = self.get_batch_list(up_unique_artists_id,50)
        return batch_list_ids

    def top_tracks(self, artists):
        tracks_arr = []
        sp = self.get_sp_instance()
        for artist in artists:
            tracks_result = sp.artist_top_tracks(artist)
            for i, item in enumerate(tracks_result['tracks']):
                tracks_arr.append(item['id'])
        return tracks_arr

    def suppress_tracks(self, user_profile, artists):
        top_tracks = self.top_tracks(artists)
        user_profile_tracks = list(user_profile['track_id'])
        sup_tracks = [x for x in top_tracks if x not in user_profile_tracks]
        return sup_tracks

    def recommended_tracks(self):
        cos_sim = CosineMatrix()
        indices, cosine_sim, features, user_profile = cos_sim.similarity_matrix(self.SPOTIPY_CLIENT_ID, self.SPOTIPY_CLIENT_SECRET, self.REDIRECT_URI, self.SCOPE, self.SHOW_DIALOG)
        random_artist = random.choice(list(features.index.values))
        logging.info(f"Recommendations for artist ID : {random_artist}")
        recomm_artists = recommendations(random_artist, indices, cosine_sim, features)
        tracks = self.suppress_tracks(user_profile,recomm_artists)
        return tracks


# if __name__ == '__main__':
#     # cos_sim = CosineMatrix()
#     # indices, cosine_sim, features, user_profile = cos_sim.similarity_matrix(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG)
#     # random_artist = random.choice(list(features.index.values))
#     # recomm_artists = recommendations(random_artist, indices, cosine_sim, features)
#     recommend = RecommendTracks(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG)
#     print(recommend.recommended_tracks())
