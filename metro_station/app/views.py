# coding: utf-8
from flask import request
from typing import Dict, List

from . import app
from .controllers import get_stations, get_api_stations, get_intersection, get_difference


API_URL = 'https://api.hh.ru/metro/1'
ListStations = List[str]
RespVerification = Dict[str, ListStations]


@app.route('/')
def index():
    return "Hello, Verification metro stations!"


@app.route('/api/v1/metro/verificate', methods=['POST', ])
def station_verification() -> RespVerification:
    post_stations = get_stations(request)  # множество станций полученных из запроса
    stations = get_api_stations(API_URL)  # множество станций полученных по API

    return {
        'unchanged': get_intersection(stations, post_stations),
        'update': get_difference(post_stations, stations),
        'deleted': get_difference(stations, post_stations),
    }
