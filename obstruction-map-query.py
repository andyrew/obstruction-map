import numpy
import imageio

# Function to find the index of the list item nearest to the value provided 
def findnearest(value, paramlist):
	return(min(range(len(paramlist)), key=lambda i: abs(paramlist[i]-value)))

# Defining an obstruction map class
class obstructionMap:
	def __init__(self, filename):
		self.filename = filename
		self.image = imageio.imread(self.filename)
		if len(self.image) == 360 and len(self.image[0]) == 360:
			self.size = 'full'
			self.winAzimuthRange = list(numpy.arange(-89.75, 90, 0.5))
			self.winProfileRange = list(numpy.arange(89.75, -90, -0.5))
		elif len(self.image) == 180 and len(self.image[0]) == 360:
			self.size = 'half'
			self.winAzimuthRange = list(numpy.arange(-89.75, 90, 0.5))
			self.winProfileRange = list(numpy.arange(89.75, 0, -0.5))
		else:
			print("unsupported image size")
			return -1

	def isObstructed(self, winAzimuth, winProfile):
		x = findnearest(winAzimuth, self.winAzimuthRange)
		y = findnearest(winProfile, self.winProfileRange)
		return( self.image[y][x][0] < 5 )

# Instantiating an obstruction map object
LA_Obsmap = obstructionMap('images/LA_obsmap.png')

# Querying an obstruction map
result = LA_Obsmap.isObstructed(-35, 30)
print("querying window azimuth: -35, profile: 30; obstructed = {0}".format(result))

result = LA_Obsmap.isObstructed(0, 20)
print("querying window azimuth: 0, profile: 20; obstructed = {0}".format(result))
