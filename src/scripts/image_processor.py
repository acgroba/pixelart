#!/usr/bin/env python3

import numpy as np
import re
import cv2
import sys
import json

PIXEL_SIZE = 40
# Open our JSON file and load it into python
input_file = open ('img.json')
json_array = json.load(input_file)

# Determine sizde
size = len(json_array ) * PIXEL_SIZE

# Create numpy array of BGR triplets
im = np.zeros((size,size,3), dtype=np.uint8) 

for row in range (0,size, PIXEL_SIZE):
    for col in range(0, size, PIXEL_SIZE):
    	row_input=int(row/PIXEL_SIZE)
    	col_input=int(col/PIXEL_SIZE)    	
    	R = int(json_array[row_input][col_input][1:3],16) 
    	G = int(json_array[row_input][col_input][3:5],16)
    	B = int(json_array[row_input][col_input][5:],16)
    	for i in range (PIXEL_SIZE):
    		for j in range (PIXEL_SIZE):    	
    			im[row+i][col+j] = (B,G,R)

# Save to disk
cv2.imwrite('result.png', im)