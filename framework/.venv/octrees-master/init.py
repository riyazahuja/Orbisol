import json
from octrees import *
from skyfield.api import load, EarthSatellite

Scene = None

class Satellite:
  # TODO: figure out what timescale is for.
  ts = load.timescale()
  pos_scale = 1000
  time_scale = 0.
  delta_time_scale = 0.00001

  @staticmethod
  def get_timescale():
    return Satellite.ts
  
  def generate_satellite(self):
    ts = Satellite.ts
    line1, line2 = self.TLE
    satellite = EarthSatellite(line1, line2, self.name, ts)
    return satellite

  def __init__(self, name, TLE, t):
    self.name = name
    self.TLE = TLE
    self.type = t
    self.satellite = self.generate_satellite()
    
  #returns (x, y, z)
  def get_pos(self, t):
    pos_scale = Satellite.pos_scale
    pos = self.satellite.at(t).position.km / pos_scale
    pos = (pos[0], pos[1], pos[2])
    return pos


def getScene():
  return Scene



def main():
  global Scene
  # Get the json data containing celestial objects orbiting earth in TLE format.
  
  

  final_path = 'src/datasets/final_half.json'
  with open(final_path, 'r') as f:
    celestial_data = json.load(f)

  # Generate satellite objects from TLE data and store them in a list (for now).
  ts = Satellite.get_timescale()
  satellites = []
  for name, lines in celestial_data.items():
    line1 = lines['line1']
    line2 = lines['line2']
    t = lines['type']
    TLE = (line1, line2)
    satellite = Satellite(name, TLE,t)
    satellites.append(satellite)


  bounds = ((-100,100),(-100,100),(-100,100))
  scene = Octree(bounds)

  initialTime = ts.now()
  for sat in satellites:
    initialPos = sat.get_pos(initialTime)
    
    try:
      scene.insert(initialPos, sat)
    except:
      continue

  Scene=scene
  


    



  
main()

#print(Scene)
