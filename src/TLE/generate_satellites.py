import json

from skyfield.api import load, EarthSatellite
from functools import partial

class Satellite:
  ts = load.timescale()

  def __init__(self, name, TLE, path):
    self.name = name
    self.type = type
    self.TLE = TLE
    self.path = path

  def get_timescale(self):
    return ts

  def get_pos(self, t):
    return self.path(t)
  
# Get the json data containing celestial objects orbiting earth in TLE format.
data_path = '../datasets'
final_path = data_path + '/final.json'
with open(final_path, 'r') as f:
  celestial_data = json.load(f)

# TODO: Create an octree of 
ts = Satellite.ts
satellites = []
for name, lines in celestial_data.items():
  line1 = lines['line1']
  line2 = lines['line2']
  TLE = (line1, line2)
  satellite = EarthSatellite(line1, line2, name, ts)
  path = partial(satellite.at)
  satellite = Satellite(name, TLE, path)
  satellites.append(satellite)
