import json

def read_json():
  with open('data.json', encoding='utf-8') as read_file:
    data = json.load(read_file)
  return data

def g_line(n, line):
  tmp = "N{0} {1}\n".format(str(n).zfill(2), line)  
  return tmp

def get_points(fl,fw,fm):
  fm2 = fm  
  if fw==140:
    if fm==61 : fm2=35
    if fm==70 : fm2=44
    
  points = []
  points.append((fm2,fm))
  points.append((fm2,fl-fm))
  points.append((fw-fm2,fl-fm))
  points.append((fw-fm2,fm))
  points.append((fm2,fm))    
  return points


def make_gcode(points, depths, feed, spindle):
  gcode =  'G00 G90 Z5.0000 \n'
  gcode += 'G00 X{} Y{} S{} M03 \n'.format(points[0][0], points[0][1], spindle)
  gcode += 'G00 Z1.000 \n'.format(points[0][0], points[0][1])
  gcode += 'G04 P4000 \n'
  for depth in depths:
    for point in points:  
      gcode += 'G01 X{} Y{} Z-{}.000 F{} S{} \n'.format(point[0], point[1], depth, feed, spindle)
      
  gcode += 'G00 X{} Y{} Z5.000\n'.format(points[0][0], points[0][1])
  gcode += 'M05 M30 \n'
  return gcode
  

def make_nc_file(freza, fasad):
  points = get_points(fasad[0],fasad[1],freza['отступ'])
  gcode = make_gcode(points, freza['глубина'], freza['подача'], freza['шпиндель'])  
  filename = "{0}x{1}_{2}.nc".format(fasad[0],fasad[1],freza['имя'])
  print(filename)
  f = open(filename, 'w')
  f.write(gcode)
  f.close()

  


def make_gcode_file(data):
  for fasad in data['фасады']:
    for freza in data['фрезы']:
      make_nc_file(freza, fasad)

 
def main():
  json_data = read_json()
  make_gcode_file(json_data)
	
if __name__ == "__main__":
  main()
