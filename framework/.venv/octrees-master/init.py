import json
import os
from octrees import *
from skyfield.api import load, EarthSatellite

Scene = None

class Satellite:
  # TODO: figure out what timescale is for.
  ts = load.timescale()

  @staticmethod
  def get_timescale():
    return Satellite.ts
  
  def generate_satellite(self):
    ts = Satellite.ts
    line1, line2 = self.TLE
    satellite = EarthSatellite(line1, line2, self.name, ts)
    return satellite

  def __init__(self, name, TLE):
    self.name = name
    self.TLE = TLE
    self.satellite = self.generate_satellite()
    
  #returns [x, y, z]
  def get_pos(self, t):
    return self.satellite.at(t).position.km


def getScene():
  return Scene



def main():
  global Scene
  # Get the json data containing celestial objects orbiting earth in TLE format.
  
  
  current_directory = os.getcwd()
  print(f"The current working directory is: {current_directory}")
  final_path = 'src/datasets/final.json'
  with open(final_path, 'r') as f:
    celestial_data = json.load(f)

  # Generate satellite objects from TLE data and store them in a list (for now).
  ts = Satellite.get_timescale()
  # satellites = []
  # ts = Satellite.get_timescale()
  # now = ts.now()
  satellites = []
  for name, lines in celestial_data.items():
    line1 = lines['line1']
    line2 = lines['line2']
    TLE = (line1, line2)
    satellite = Satellite(name, TLE)
    satellites.append(satellite)
  # for name, lines in celestial_data.items():
  #   line1 = lines['line1']
  #   line2 = lines['line2']
  #   TLE = (line1, line2)
  #   earth_satellite = EarthSatellite(line1, line2, name, ts)
  #   print(earth_satellite.at(now).position.km)
  #   path = lambda t: earth_satellite.at(t).position.km
  #   satellite = Satellite(name, TLE, path)
  #   satellites.append(satellite)
  #print(satellites)

  bounds = ((-100,100),(-100,100),(-100,100))
  scene = Octree(bounds)

  initialTime = ts.now()
  for sat in satellites:
    # print(f'{sat.name} : {sat.get_pos(initialTime)}')
    initialPos = sat.get_pos(initialTime)
    p = (initialPos[0]/1000, initialPos[1]/1000, initialPos[2]/1000)
    
    try:
      scene.insert(p,sat)
    except:
      continue

  Scene=scene
  


    



  
main()

#print(Scene)