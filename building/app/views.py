# coding: utf-8
import json
from flask import request
from typing import Tuple

from . import app
from . import db
from .exceptions import BodyNotFound, DBError, ParamError
from .controllers import generate_stat
from .models import Bricks, Building
from .validated import get_data, BricksValidator, BuildingsValidator


BuildingResponse = Tuple[str, int]


@app.route('/')
def index_view():
    return 'Hello, building project!'


@app.route('/building', methods=['POST', ])
def building_view() -> BuildingResponse:
    # "{\"address\":\"Москва\", \"year\":\"2020\"}"
    if not request.get_data():
        raise BodyNotFound(message='Body objects not found')

    data = json.loads(request.get_json(force=True))
    # валидация данных (просто проверю, что поля переданы)
    serialized = get_data(data, schema=BuildingsValidator())

    for build in serialized:
        building = Building(address=build['address'], year_construction=build['year'])
        db.session.add(building)

    try:
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        return f'Not created: {err}', 501

    return 'Created', 201


@app.route('/building/<int:build_id>/add-bricks', methods=['POST', ])
def bricks_view(build_id: int) -> BuildingResponse:
    # "{\"count_bricks\":\"600\"}"
    building = Building.query.get(build_id)
    if building is None:  # если такого здания нет, то добавить кирпичи не можем
        raise DBError(message=f'Building with id={build_id} not such')

    if not request.get_data():
        raise BodyNotFound(message='Body objects not found')

    data = json.loads(request.get_json(force=True))
    serialized = get_data(data, schema=BricksValidator())
    try:
        count_bricks = int(serialized['count_bricks'])
    except ValueError:
        raise ParamError(field_name='count_bricks', message='The number of bricks must be a number')

    curr_bricks = Bricks.query.get(build_id)
    if curr_bricks is not None:
        Bricks.query.filter_by(id=build_id).update({'count_bricks': count_bricks})
    else:
        bricks = Bricks(id=building.id, count_bricks=count_bricks)
        db.session.add(bricks)

    try:
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        return f'Not created: {err}', 501

    return f'/building/{build_id}/add-bricks/', 201


@app.route('/stats', methods=['GET', ])
def stats_view():
    buildings = Building.query.join(Bricks, Bricks.id == Building.id).all()

    return generate_stat(buildings)
