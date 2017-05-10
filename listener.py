#!/usr/env python
# -*- coding: utf-8 -*-

# Inspirado em https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/

import config
import json
import tweepy
from pprint import pprint
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)
api = tweepy.API(auth)
 
class TwitterListener(StreamListener):
    def on_data(self, data):
        _data = json.loads(data)
        _user_data = {
            'text': _data['text'],
            'user': {
                'name': _data['user']['name'],
                'location': _data['user']['location'],
                'url': _data['user']['url'],
                'profile_image_url': _data['user']['profile_image_url']
            }
        }

        try:
            # Os dados são armazenados no arquivo `data.json`
            with open('data.json', 'a') as f:
                f.write(data + ",")

            if '#moroorgulhobrasileiro' in _data['text'].lower():
                m = open('moro.json', 'a')
                m.write(json.dumps(_user_data) + "\n")

            if '#brasilcomlula' in _data['text'].lower():
                l = open('lula.json', 'a')
                l.write(json.dumps(_user_data) + "\n")

            print('Novo registro adicionado')
            return True
        except BaseException as e:
            print('Error on_data: %s' % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        time.sleep(5)
        return True
if __name__ == '__main__':
    twitter_stream = Stream(auth, TwitterListener())
    twitter_stream.filter(track=['#MoroOrgulhoBrasileiro', '#BrasilComLula'])