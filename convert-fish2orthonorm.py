import imageio
import math
import numpy as np

fisheye_center = [ 1136, 972 ]							# Center of circle in image pixel coordinates
fisheye_radius = 900									# Fisheye radius in image pixels
angular_distortion = [ -0.4339, 0.5808, -0.1185, 0.9661, 0 ]	# Angular distortion polynomial coefficients
output_resolution = [ 900, 900 ]
filename = 'images/inputL.jpg'
camera_rotation = 0.14									# Rotation angle of the camera for this image
output_filename = 'images/outputL.jpg'

# Function to correct image angular distortion
def undistortangle( pixelcoord ):
	distance = math.sqrt( 
				( pixelcoord[0] - fisheye_center[0] )**2 + ( pixelcoord[1] - fisheye_center[1] )**2 
						)
	norm_distance = distance / fisheye_radius
	norm_distance_quadlist = [ norm_distance**4, norm_distance**3, norm_distance**2, 
							norm_distance**1, norm_distance**0 ]
	undistort_distance = sum(i[0] * i[1] for i in zip(angular_distortion,norm_distance_quadlist))
	
	if camera_rotation == 0:
		rotated_pixelcoord = pixelcoord
	else:
		pixel_angle = math.atan2( 
							pixelcoord[1] - fisheye_center[1], 
							pixelcoord[0] - fisheye_center[0] 
						) + math.radians( camera_rotation )
		pixel_dist = math.sqrt( 
						math.pow( pixelcoord[0] - fisheye_center[0], 2) + math.pow(pixelcoord[1] - fisheye_center[1],2)
					)
		rotated_pixelcoord = [ fisheye_center[0] + pixel_dist * math.cos(pixel_angle),
								fisheye_center[1] + pixel_dist * math.sin(pixel_angle) ]

	if norm_distance == 0: 
		undistort_pixelcoord=[0,0]
	else:
		undistort_pixelcoord = [ 	int( ( rotated_pixelcoord[0] - fisheye_center[0] ) * 
									undistort_distance / norm_distance + fisheye_center[0] ),
							int( (rotated_pixelcoord[1]-fisheye_center[1] ) * 
									undistort_distance / norm_distance + fisheye_center[1] ) ]
	return( undistort_pixelcoord )

# Function to convert from real world XYZ vector to angular fisheye pixel coordinates
def convert_XYZ_2_AF( vector ):
	phi = math.atan2(vector[2],vector[0])
	theta = math.acos(vector[1])
	x = int( fisheye_center[0] + theta / (math.pi / 2) * fisheye_radius * math.cos(phi))
	y = int( fisheye_center[1] + theta / (math.pi / 2) * fisheye_radius * math.sin(phi))
	return( [x, y] )

# Function to convert from orthonormal pixel coordinates to real world XYZ vector, 
# where Y is perpendicular to the image view, Z is up and X is right.
def convert_orthonormal_2_XYZ( vector ):
	azi = (math.pi) * (vector[0] / output_resolution[0] - 0.5)
	pro = (math.pi) * (vector[1] / output_resolution[1] - 0.5)
	alt = math.atan( math.tan(pro) * math.cos(azi) )
	X = math.cos(alt) * math.sin(azi)
	Y = math.cos(alt) * math.cos(azi)
	Z = math.sin(alt)
	return( [X, Y, Z] )

# Read Image
fisheye_image = imageio.imread(filename)

# Create up a blank array for the remapped output image
remap_img = np.zeros( shape = ( output_resolution[0], output_resolution[1], 3 ), dtype = float, order='C')
# Iterate over pixels in output image
for y in range(len(remap_img)):
	for x in range(len(remap_img[y])):
		# Find input fisheye pixel coordinates that are coincident with the current pixel in the orthonormal 
		AF = undistortangle( convert_XYZ_2_AF( convert_orthonormal_2_XYZ( [ x, y ] ) ) )
		# Assign the pixel value of the angular fisheye to the current pixel of the orthonormal 
		remap_img[y][x] += fisheye_image[AF[1]][AF[0]]

# Write the output image
imageio.imsave( output_filename, remap_img )
