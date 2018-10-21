# /src/views/SatelliteView.py

from flask import request, json, Response, Blueprint, g
from ..models.SatelliteModel import SatelliteModel, SatelliteSchema

satellite_api = Blueprint('satellites', __name__)
satellite_schema = SatelliteSchema()

@satellite_api.route('/create', methods=['POST'])
def create():
    """
    Create a Satellite
    """
    req_data = request.get_json()
    data, error = satellite_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    # check if satellite already exists in the db
    sat_in_db = Satellite.get_one_satellite(data.get('satellite_id'))
    if sat_in_db:
        message = {'exists': 'Satellite already exists'}
        return custom_response(message, 400)

    satellite = SatelliteModel(data)
    satellite.save()

    ser_data = satellite_schema.dump(satellite).data

    return custom_response({'data': ser_data})


@satellite_api.route('/', methods=['GET'])
def get_all():
    """
    Get all Satellites
    """
    satellites = SatelliteModel.get_all_satellites()
    ser_users = satellite_schema.dump(satellites, many=True).data
    return custom_response(ser_users, 200)

@satellite_api.route('/update', methods=['PUT'])
def update():
    """
    Update Satellite
    """
    req_data = request.get_json()
    data, error = satellite_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)

    satellite = SatelliteModel.get_one_satellite(g.user.get('id'))
    satellite.update(data)
    ser_data = satellite_schema.dump(satellite).data
    return custom_response(ser_data, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Reponse(
            mimetype='application/json',
            response=json.dumps(res),
            status=status_code
    )

