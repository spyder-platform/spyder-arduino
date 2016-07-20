#!/usr/bin/python
# coding=utf-8

import requests

API_ENDPOINT = 'http://176.31.127.127:3000/api'
ACCOUNT_LOGIN_ENDPOINT = API_ENDPOINT + '/account/login'
MOVEMENT_CREATE_ENDPOINT = API_ENDPOINT + '/movement'


def login(email, password):
    params = {'email': email, 'password': password}
    response = requests.post(ACCOUNT_LOGIN_ENDPOINT, json=params)
    return response.json()


def create_movement(filepath, token):
    url = MOVEMENT_CREATE_ENDPOINT + '?token=' + token
    photo = open(filepath, 'rb').read()
    files = {'photo': ('photo.jpg', photo, 'image/jpeg')}
    response = requests.post(url, files=files)
    return response.json()
