# coding: utf-8
from typing import Dict, List, Union


BuildObj = Dict[str, Union[str, int]]
YearObj = List[BuildObj]
StatResponse = Dict[str, YearObj]


def generate_stat(buildings: List) -> StatResponse:
    """
    Возвращает статистику по всем существующим домам с группировкой по датам.

    Формирует JSON с информацией:
     - сколько в каждом доме лежит кирпичей;
     - адрес дома.

    :param buildings: список всех домов
    :return: {
        'year': [
            {
                'id': building.id,
                'address': building.address,
                'count_bricks': building.bricks.count_bricks,
            },
            ...
        ]
        ...
    }
    """
    print(buildings)
    result = dict()
    for building in buildings:
        year = building.year_construction
        building_info = {
            'id': building.id,
            'address': building.address,
            'count_bricks': building.bricks.count_bricks,
        }
        if result.get(year) is None:
            result[year] = [building_info]
        else:
            result[year].append(building_info)

    return result
