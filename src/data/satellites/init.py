import json
import sys
sys.path.append('../../')

from octrees import *
from skyfield.api import load, EarthSatellite

Scene = None

class Satellite:
  # TODO: figure out what timescale is for.
  ts = load.timescale()

  @staticmethod
  def get_timescale():
    return Satellite.ts

  def __init__(self, name, TLE, path):
    self.name = name
    self.TLE = TLE
    self.path = path
    
  #returns [x, y, z]
  def get_pos(self, t):
    return self.path(t)







def main():
  global Scene
  # Get the json data containing celestial objects orbiting earth in TLE format.
  data_path = '../datasets'
  final_path = data_path + '/final.json'
  with open(final_path, 'r') as f:
    celestial_data = json.load(f)

  # Generate satellite objects from TLE data and store them in a list (for now).
  ts = Satellite.get_timescale()
  satellites = []
  for name, lines in celestial_data.items():
    line1 = lines['line1']
    line2 = lines['line2']
    TLE = (line1, line2)
    earth_satellite = EarthSatellite(line1, line2, name, ts)
    path = lambda t: earth_satellite.at(t).position.km
    satellite = Satellite(name, TLE, path)
    satellites.append(satellite)

  bounds = ((-1000,1000),(-1000,1000),(-1000,1000))
  scene = Octree(bounds)

  initialTime = ts.now()
  for sat in satellites:
    initialPos = sat.path(initialTime)
    scene.insert(initialPos,sat)
  

  Scene=scene


    



main()