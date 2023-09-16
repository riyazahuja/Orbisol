import json

from skyfield.api import load, EarthSatellite
from functools import partial

# Get the json data containing celestial objects orbiting earth in TLE format.
data_path = '../datasets'
final_path = data_path + '/final.json'
with open(final_path, 'r') as f:
  celestial_data = json.load(f)

# Define a timescale.
# TODO: decide whether a timescale should be passed as an argument to this
# file, or this file creates a timescale and passes it to our struct thingy.
ts = load.timescale() # Don't even know what timescale is tbh.

# TODO: Create an octree of paths. (Right now it's all lists)
satellites = []
for name, lines in celestial_data.items():
  line1, line2 = lines
  satellite = EarthSatellite(line1, line2, name, ts)
  path = partial(satellite.at)
  satellites.append(path)
