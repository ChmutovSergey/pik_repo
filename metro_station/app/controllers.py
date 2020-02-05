# coding: utf-8
import json
from requests import get
from typing import List, Set

from .exceptions import StructApiException


ListStations = List[str]
SetStations = Set[str]


def get_stations(req) -> SetStations:
    """
    Возвращает множество станций переданных по HTTP

    :param req: объект HTTP-запроса Flask
    :return: {"Станция 1", ..., "Станция N"}
    """
    body = req.get_data()

    return set(json.loads(req.get_json(force=True))) if body else set()


def get_api_stations(url: str) -> SetStations:
    """
    Возвращает множество станций запрашиваемых по API

    :param url: url-адрес для обращения по API
    :return: {"Станция 1", ..., "Станция N"}
    """
    api_station = get(url).json()
    try:
        station = {
            station_info['name']
            for line in api_station['lines']
            for station_info in line['stations']
        }
    except KeyError as err:
        raise StructApiException(field_name=err, message="The field does't exist on API response")

    return station


def get_intersection(first_set: SetStations, second_set: SetStations) -> ListStations:
    """
    Возвращает список с результатом пересечения двух множеств

    :param first_set: первое множество
    :param second_set: второе множество
    :return: ["Элемент 1", ..., "Элемент 1"]
    """
    return list(first_set.intersection(second_set))


def get_difference(first_set: SetStations, second_set: SetStations) -> ListStations:
    """
    Возвращает список с результатом разности двух множеств

    :param first_set: первое множество
    :param second_set: второе множество
    :return: ["Элемент 1", ..., "Элемент 1"]
    """
    return list(first_set.difference(second_set))
