from flask import Blueprint

# import googlemaps

from config import CONFIG as conf

CONFIG = conf()

# gmaps = googlemaps.Client(key=CONFIG.GOOGLE_MAPS_API_KEY)

# Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = [] # gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)

# print('\nReverse Geocode Result')
# print(reverse_geocode_result)

maps_blueprint = Blueprint(__name__, 'maps_blueprint')


from . import routes