import sys
import os
import numpy as np
import pandas as pd
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.oauth2 as oauth2
import streamlit as st
import time
from dotenv import load_dotenv
load_dotenv()

st.title('Spotify Recommendation App')
'''
Powered by _NLP_.
'''

# @st.cache
# class get_spotify_data:
#     """
#     To retrieve data from Spotify using their API
#     """
    
#     def __init__(self, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG):
#         self.SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID
#         self.SPOTIPY_CLIENT_SECRET = SPOTIPY_CLIENT_SECRET
#         self.REDIRECT_URI = REDIRECT_URI
#         self.SCOPE = SCOPE
#         self.SHOW_DIALOG = SHOW_DIALOG
#         self.get_permission()
#         st.text('Spotify credentials is set and instanciated')

#     def get_permission(self):
#         client_credentials_manager = SpotifyClientCredentials(client_id=self.SPOTIPY_CLIENT_ID, client_secret=self.SPOTIPY_CLIENT_SECRET)
#         sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#     def get_user_top_tracks(self):
#         st.text(self.SPOTIPY_CLIENT_ID)
#         auth_manager=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
#                                   client_secret=self.SPOTIPY_CLIENT_SECRET,
#                                   redirect_uri=self.REDIRECT_URI,
#                                   scope=self.SCOPE,
#                                   show_dialog=self.SHOW_DIALOG)
#         sp = spotipy.Spotify(auth_manager=auth_manager)
#         time_ranges = ['short_term', 'medium_term', 'long_term']
#         for r in time_ranges:
#             for i in range(0,100,49):
#                 track_results = sp.current_user_top_tracks(time_range=r, limit=48, offset=i)
#                 for i, item in enumerate(track_results['items']):  
#                     st.text(item['artists'][0]['name'])
#                     # st.text(i, item['name'], '//', item['artists'][0]['name'])     


class get_spotify_data:
    """
    To retrieve data from Spotify using their API
    """
    
    def __init__(self, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG):
        self.SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID
        self.SPOTIPY_CLIENT_SECRET = SPOTIPY_CLIENT_SECRET
        self.REDIRECT_URI = REDIRECT_URI
        self.SCOPE = SCOPE
        self.SHOW_DIALOG = SHOW_DIALOG
#         self.get_permission()
        print('Spotify credentials is set and instanciated')
        st.text('Spotify credentials is set and instanciated')

    def get_permission(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=self.SPOTIPY_CLIENT_ID, client_secret=self.SPOTIPY_CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        print("Default permissions set")

    def get_user_top_tracks(self):
#         auth_manager=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
#                                   client_secret=self.SPOTIPY_CLIENT_SECRET,
#                                   redirect_uri=self.REDIRECT_URI,
#                                   scope=self.SCOPE,
#                                   show_dialog=self.SHOW_DIALOG)
#         sp = spotipy.Spotify(auth_manager=auth_manager)
        time_ranges = ['short_term', 'medium_term', 'long_term']
        sp_feature_data = self.arr_dec()
        sp = self.get_sp_instance()
        for r in time_ranges:
            for i in range(0,100,49):
                try:                    
                    track_results = sp.current_user_top_tracks(time_range=r, limit=50, offset=i)
#                     break
                except:
                    print(sys.exc_info()[0])
                    break
                else:
                    for i, item in enumerate(track_results['items']): 
                        sp_feature_data['index'].append(i)
                        sp_feature_data['dur_range'].append(r)
                        sp_feature_data['track_name'].append(item['name'])
                        sp_feature_data['track_popularity'].append(item['popularity'])
                        sp_feature_data['track_number'].append(item['track_number'])
                        sp_feature_data['track_type'].append(item['type'])
                        sp_feature_data['track_uri'].append(item['uri'])
                        sp_feature_data['duration_ms'].append(item['duration_ms'])
        df_tracks = pd.DataFrame.from_dict(sp_feature_data)
        st.text(sp.me())
        return df_tracks
    
    def get_sp_instance(self):
        sp_oauth=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
                              client_secret=self.SPOTIPY_CLIENT_SECRET,
                              redirect_uri=self.REDIRECT_URI,
                              scope=self.SCOPE)
#         sp = spotipy.Spotify(auth_manager=sp_oauth)
        
        token_info = sp_oauth.get_cached_token() 
        
        print('Token: ', token_info)

        if not token_info:
            st.text(token_info)
            sp = spotipy.Spotify(auth_manager=sp_oauth)
        elif sp_oauth.is_token_expired(token_info):
            st.text(sp_oauth.is_token_expired(token_info))
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            token = token_info['access_token']
            sp = spotipy.Spotify(auth=token)
        else:
            st.text(token_info)
            sp = spotipy.Spotify(auth=token_info['access_token'])

        return sp
        
                    
    def arr_dec(self):
        sp_feature_names = ['index','dur_range','track_name','track_popularity','track_number','track_type',
                           'track_uri','duration_ms']
        sp_feature_data = {}
        for i in sp_feature_names:
            sp_feature_data[i] = []
        return sp_feature_data
                                            

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:8500/'
SCOPE =  'user-read-private'
SHOW_DIALOG = True

get_sp_data = get_spotify_data(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG)

df_tracks = get_sp_data.get_user_top_tracks()
st.text(df_tracks.head())