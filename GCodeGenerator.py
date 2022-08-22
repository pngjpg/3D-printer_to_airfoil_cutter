# -*- coding: utf-8 -*-
"""
Created on Fri May 20 12:17:18 2022

@author: Brian
"""

import matplotlib.pyplot as plt
import math

#csv file with points from http://airfoiltools.com/plotter/index
airfoil_file = "clarky-il.csv"

#output file
output_file_name = "output clark y"

#the distance to shift the profile upward from 0,0 to avoid hitting the bed
vertical_offset = 7

#feedrate. 50 is slow, but reliable
feedrate_max = 75

#distance from leading edge to trailing edge. major_chord same as root chord
major_chord = 160
minor_chord = major_chord

#the length of the wing segment to cut. Does not matter unless you have taper
wing_span = 400

#the distance away from the leading edge to start the cut
leadin_distance = 10

#the angle of attack of the minor profile. This probably won't give the desired results
twist_angle = 0

#sweep angle in degrees
sweep_angle = 0

#Mirror the wing in order to cut an airfoil for the opposite side of the aircraft
mirror_wing = False

#if a sweep angle is not specified and the major and minor chords are different, define the behavior
allign_leading_edge = True

#============= Step 1: Load CSV =============

f = open(airfoil_file).readlines()[9:]
chords = [[float(b) for b in a] for a in [x.replace('\n', '').split(',') for x in f[:f.index(',\n')]]]

#compute the coordinates of the major cross section (root)
major_chord_ratio = major_chord/max([x[0] for x in chords])
major_scaled_chords = [[(major_chord_ratio*b) for b in a] for a in chords]
x_major = [abs(x[0]-(major_chord+leadin_distance)) for x in major_scaled_chords]
y_major = [y[1]+vertical_offset for y in major_scaled_chords]

#compute the coordinates of the minor cross section (tip)
minor_chord_ratio = minor_chord/max([x[0] for x in chords])
minor_scaled_chords = [[(minor_chord_ratio*b) for b in a] for a in chords]
temp_transform = 0

if allign_leading_edge and sweep_angle == 0: 
    temp_transform = major_chord - minor_chord
elif sweep_angle != 0: 
    temp_transform = (major_chord - minor_chord)-(wing_span*math.tan(math.radians(sweep_angle)))

x_minor = [abs(x[0]-(minor_chord+leadin_distance)-temp_transform) for x in minor_scaled_chords]
y_minor = [y[1]+vertical_offset for y in minor_scaled_chords]

plt.rcParams['figure.dpi'] = 200
plt.scatter(x_major, y_major, 1, c="b")
plt.scatter(x_minor, y_minor, 1, c="b")
plt.scatter([0.001], [0.001], 10, c="r")
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.margins(x=0.1, y=0.5)
plt.gca().set_aspect("equal")
plt.show()

print("Airfoil Stats")
print("Min Wire Height: " + str(min(y_major)))
print("Max Wire Height: " + str(max(y_major)))
print("Wing Thickness: " + str(max(y_major)-min(y_major)))
#print(x_major)

'''
Map of plt  coords to printer coords:
    X -> Y
    Y -> Z
'''

# for x1, y1, x2, y2 in zip(x_major, y_major, x_minor, y_minor):
#     output_file.write('G1 X' + str(x1) + ' Y' + str(y1) + ' Z0\n')
#     output_file.write('G1 X' + str(x2) + ' Y' + str(y2) + ' Z400' +' E' + str(extruder) + '\n')
#     extruder +=100

# previous_location = (0,0)
output_file = open(output_file_name + '.gcode', 'w')
output_file.write('M203 Y' + str(feedrate_max) + ' Z' + str(feedrate_max) + '/n')
output_file.write('G1 X10 Y0' + ' Z' + str(y_major[0]) + '\n')

for x1, y1 in zip(x_major, y_major):
    output_file.write('G1 Y' + str(x1) + ' Z' + str(y1) + '\n')
    
output_file.write('G1 Y0' + ' Z' + str(y_major[0]) + '\n')

    
output_file.close()
