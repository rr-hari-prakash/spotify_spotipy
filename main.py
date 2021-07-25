import sys
import os
import numpy as np
import pandas as pd
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.oauth2 as oauth2
from recommend_tracks import RecommendTracks
import streamlit as st
import streamlit.components.v1 as components
import random
import time
from dotenv import load_dotenv
load_dotenv()


SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:8500/'
SCOPE =  'user-top-read'
SHOW_DIALOG = True

st.title('Spotify Recommendation App')
'''
Powered by _NLP_.
'''

st.markdown('#')
p = st.button('Go')

if p:
    recommend = RecommendTracks(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG)
    track_ids = recommend.recommended_tracks()
    st.balloons()
    st.write('Our personialised recommendations for you...')
    for track in random.sample(track_ids, 10):
        components.iframe(f"https://open.spotify.com/embed/track/{track}", width=600, height=80)


