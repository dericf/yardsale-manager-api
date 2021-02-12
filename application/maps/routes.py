from flask import request, redirect
from . import maps_blueprint

@maps_blueprint.route('/address-for-lat-long', methods=['POST'])
def get_address():
    data = request.get_json()
    print('DATA: ', data)

    reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
    print('\nRoute Reverse Geocode Result')
    print(reverse_geocode_result)
    return {
        "result": reverse_geocode_result
    }