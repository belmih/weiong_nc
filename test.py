import json

def read_json():
  with open('data.json', encoding='utf-8') as read_file:
    data = json.load(read_file)
  return data

def g_line(n, line):
  tmp = "N{0} {1}\n".format(str(n).zfill(2), line)  
  return tmp

def get_points(fl, fw, fm):
  fm2 = fm  
  if fw == 140:
    if fm == 61 : fm2 = 35
    if fm == 70 : fm2 = 44
    
  points = []
  points.append((fm2,fm))
  points.append((fm2,fl-fm))
  points.append((fw-fm2,fl-fm))
  points.append((fw-fm2,fm))
  points.append((fm2,fm))    
  return points


  
def make_gcode(fasad, freza):
  flength = fasad[0]
  fwidth = fasad[1]
  fmargin = freza['отступ']
  points = get_points(flength, fwidth, fmargin)
  gcode =  'G00 G90 Z10.0000 \n'
  gcode += 'G00 X{} Y{} S{} M03 \n'.format(points[0][0], points[0][1], freza['шпиндель'])
  gcode += 'G00 Z1.000 \n'
  gcode += 'G04 P4000 \n'
  for depth in freza['глубина']:
    for point in points:  
      gcode += 'G01 X{} Y{} Z-{}.000 F{} S{} \n'.format(point[0], point[1], depth, freza['подача'], freza['шпиндель'])
  gcode += 'G00 Z10.000 \n'
  gcode += 'M05 M30 \n'
  return gcode
  
def num_gcode(gcode):
  n = 0
  tmp = ""
  for line in gcode.split('\n'):
    if len(line) > 0:
      n += 1
      tmp += "N{:02} {}\n".format(n, line)
  return tmp

def make_nc_file(fasad, freza):
  gcode = ""
  gcode = make_gcode(fasad, freza)
  gcode = num_gcode(gcode)
  filename = "{0}x{1}_{2}.nc".format(fasad[0], fasad[1], freza['имя'])
  print(filename)
  f = open(filename, 'w')
  f.write(gcode)
  f.close()


def make_gcode_file(data):
  for freza in data['фрезы']:
    for fasad in data['фасады']:
      make_nc_file(fasad, freza)

 
def main():
  json_data = read_json()
  make_gcode_file(json_data)

	
if __name__ == "__main__":
  main()
