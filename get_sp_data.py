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

load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:8500/'
SCOPE =  'user-top-read'
SHOW_DIALOG = True


class SpotifyData:
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
        logging.info('Spotify credentials is set and instanciated')

    def get_permission(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=self.SPOTIPY_CLIENT_ID, client_secret=self.SPOTIPY_CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        logging.info("Default permissions set")

    def get_user_top_tracks(self):
        time_ranges = ['short_term', 'medium_term', 'long_term']
        sp_feature_data = self.arr_dec()
        sp = self.get_sp_instance()
        for r in time_ranges:
            for i in range(0,100,49):
                try:
                    track_results = sp.current_user_top_tracks(time_range=r, limit=50, offset=i)
                except:
                    logging.error(sys.exc_info()[0])
                    break
                else:
                    for i, item in enumerate(track_results['items']):
                        sp_feature_data['index'].append(i)
                        sp_feature_data['dur_range'].append(r)
                        sp_feature_data['track_id'].append(item['id'])
                        sp_feature_data['track_uri'].append(item['uri'])
                        sp_feature_data['track_name'].append(item['name'])
                        sp_feature_data['preview_url'].append(item['preview_url'])

                        sp_feature_data['album_type'].append(item['album']['type'])
                        sp_feature_data['album_id'].append(item['album']['id'])
                        sp_feature_data['album_uri'].append(item['album']['uri'])
                        sp_feature_data['album_release_date'].append(item['album']['release_date'])
                        sp_feature_data['album_name'].append(item['album']['name'])
                        sp_feature_data['total_tracks_in_album'].append(item['album']['total_tracks'])

                        list1, list2, list3, list4 = ([] for i in range(4))
                        for inn_item in item['album']['artists']:
                            list1.append(inn_item['id'])
                            list2.append(inn_item['uri'])
                            list3.append(inn_item['name'])
                            list4.append(inn_item['type'])

                        sp_feature_data['album_artist_id'].append(list1)
                        sp_feature_data['album_artist_uri'].append(list2)
                        sp_feature_data['album_artist_name'].append(list3)
                        sp_feature_data['album_artist_type'].append(list4)

                        list5, list6, list7, list8 = ([] for i in range(4))
                        for inn_item in item['artists']:
                            list5.append(inn_item['id'])
                            list6.append(inn_item['uri'])
                            list7.append(inn_item['name'])
                            list8.append(inn_item['type'])

                        sp_feature_data['track_artist_id'].append(list5)
                        sp_feature_data['track_artist_uri'].append(list6)
                        sp_feature_data['track_artist_name'].append(list7)
                        sp_feature_data['track_artist_type'].append(list8)
        df_tracks = pd.DataFrame.from_dict(sp_feature_data)
        return df_tracks

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


    def arr_dec(self):
        sp_feature_names = ['index','dur_range','track_id','track_uri','track_name','preview_url',
                           'album_type','album_id','album_uri','album_release_date','album_name',
                           'total_tracks_in_album',
                           'album_artist_id','album_artist_uri','album_artist_name','album_artist_type',
                           'track_artist_id','track_artist_uri','track_artist_name','track_artist_type']
        sp_feature_data = {}
        for i in sp_feature_names:
            sp_feature_data[i] = []
        return sp_feature_data



class Artists:
    """
    Function to convert id to lists and pull artists related artists
    """

    def __init__(self, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG):
        self.SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID
        self.SPOTIPY_CLIENT_SECRET = SPOTIPY_CLIENT_SECRET
        self.REDIRECT_URI = REDIRECT_URI
        self.SCOPE = SCOPE
        self.SHOW_DIALOG = SHOW_DIALOG
    #         self.get_permission()
        print('Spotify credentials is set and instanciated')

    def get_sp_instance(self):
        sp_oauth=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
                              client_secret=self.SPOTIPY_CLIENT_SECRET,
                              redirect_uri=self.REDIRECT_URI,
                              scope=self.SCOPE)
    #         sp = spotipy.Spotify(auth_manager=sp_oauth)
        token_info = sp_oauth.get_cached_token()
        print('Token: ', token_info)
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

    def arr_dec(self):
        sp_feature_names_1 = ['index','artist_id','related_artist_id','related_artist_uri',
                            'related_artist_name','related_artist_popularity',
                            'related_artist_followers','related_artist_genres']
        sp_feature_names_2 = ['index','artist_id','artist_uri',
                            'artist_name','artist_popularity',
                            'artist_followers','artist_genres']
        sp_feature_data_1 = {}
        sp_feature_data_2 = {}
        for i in sp_feature_names_1:
            sp_feature_data_1[i] = []
        for i in sp_feature_names_2:
            sp_feature_data_2[i] = []
        return sp_feature_data_1,sp_feature_data_2

    def related_artists(self, user_track_prof):
        artist_ids = self.col_to_list(user_track_prof)
        sp = self.get_sp_instance()
        sp_feature_data = self.arr_dec()[0]
        for batch in artist_ids:
            for i in batch:
                try:
                    related_artists = sp.artist_related_artists(i)
                except:
                    print(sys.exc_info()[0])
                    break
                else:
                    for j, item in enumerate(related_artists['artists']):
                        sp_feature_data['index'].append(j)
                        sp_feature_data['artist_id'].append(i)
                        sp_feature_data['related_artist_id'].append(item['id'])
                        sp_feature_data['related_artist_uri'].append(item['uri'])
                        sp_feature_data['related_artist_name'].append(item['name'])
                        sp_feature_data['related_artist_popularity'].append(item['popularity'])
                        sp_feature_data['related_artist_followers'].append(item['followers']['total'])
                        sp_feature_data['related_artist_genres'].append(item['genres'])
        df_related_artists = pd.DataFrame.from_dict(sp_feature_data)
        return df_related_artists

    def up_artists_genres(self, user_track_prof):
        artist_ids = self.col_to_list(user_track_prof)
        sp = self.get_sp_instance()
        sp_feature_data = self.arr_dec()[1]
        for batch in artist_ids:
            try:
                artists = sp.artists(batch)
            except:
                print(sys.exc_info()[0])
                break
            else:
                for i, item in enumerate(artists['artists']):
                    sp_feature_data['index'].append(i)
                    sp_feature_data['artist_id'].append(item['id'])
                    sp_feature_data['artist_uri'].append(item['uri'])
                    sp_feature_data['artist_name'].append(item['name'])
                    sp_feature_data['artist_popularity'].append(item['popularity'])
                    sp_feature_data['artist_followers'].append(item['followers']['total'])
                    sp_feature_data['artist_genres'].append(item['genres'])
        df_artists = pd.DataFrame.from_dict(sp_feature_data)
        return df_artists


class PrepareFeatures:
    def unique_artist_id(self, related_artists_df, up_artists_genres_df):
        up_related_artist_id = related_artists_df.drop_duplicates('related_artist_id')
        up_artist_id = up_artists_genres_df.drop_duplicates('artist_id')
        related_artists_df_drop = up_related_artist_id[['related_artist_id','related_artist_uri',
                        'related_artist_name','related_artist_popularity',
                        'related_artist_followers','related_artist_genres']]
        up_artists_genres_df_drop = up_artist_id[['artist_id','artist_uri',
                                    'artist_name','artist_popularity',
                                    'artist_followers','artist_genres']]
        up_artists_concat = pd.concat([
                   up_artists_genres_df_drop,
                   related_artists_df_drop.rename(columns=
                                                  {
                                                      'related_artist_id':'artist_id',
                                                      'related_artist_uri':'artist_uri',
                                                      'related_artist_name':'artist_name',
                                                      'related_artist_popularity':'artist_popularity',
                                                      'related_artist_followers':'artist_followers',
                                                      'related_artist_genres':'artist_genres'
                                                  })], ignore_index=True)
        up_unique_artists = up_artists_concat.drop_duplicates('artist_id').reset_index(drop=True)
        return up_unique_artists

    def bag_of_words(self, related_artists_df, up_artists_genres_df):
        artists = self.unique_artist_id(related_artists_df, up_artists_genres_df)
        artists = artists.set_index('artist_id')
        artists['artist_name'] = artists['artist_name'].map(lambda x: x.replace(' ', '').replace('.', '').lower())
        artists['bag_of_words'] = ''
        for index, row in artists.iterrows():
            words = ''
            for col in ['artist_name','artist_genres']:
                words = words + ''.join(row[col])+ ' '
            artists.loc[index, 'bag_of_words'] = words
        artists.drop(columns = [col for col in artists.columns if col!= 'bag_of_words'], inplace = True)
        return artists



# if __name__ == '__main__':
#     get_sp_data = SpotifyData(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG)
#     user_profile = get_sp_data.get_user_top_tracks()
#     logging.info('user_profile')
#     print(user_profile.head())
#     get_artists = Artists(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI, SCOPE, SHOW_DIALOG)
#     artist_related_artists = get_artists.related_artists(user_profile)
#     artists_genres = get_artists.up_artists_genres(user_profile)
#     logging.info('artist_related_artists')
#     print(artist_related_artists.head())
#     logging.info('artists_genres')
#     print(artists_genres.head())
#     prepare_features = PrepareFeatures()
#     artists_features = prepare_features.bag_of_words(related_artists_df=artist_related_artists, up_artists_genres_df=artists_genres)
#     logging.info('artists_features')
#     print(artists_features.head())
