import maya.cmds as cmds
import math
import random
import sys

cmds.select(all=True) 
cmds.delete()


"""
2010 MDDN 311 Final Project (Updated 2014)
Using Maya, the script draws 3D objects linearly using an L-system. 

I am unable to find the original 2010 reference material used to guide elements of the script. 
If I recollect correctly, the guide project drew the object in 2D and I expanded it to 3D. 

"""

"""
A rule dictionary for adding object transformation rules as characters
"""
class LSystem:
	ruleDictionary = {}
	
	#clears dict
	def __init__(self):
			self.ruleDictionary = {}
	
	def setBase( self, aBase ):
		self.systemBase = aBase
		print 'Base %s' % aBase
	
	def addRule( self, aReplace, aWith ):
		# Add the rule to tuple array
		self.ruleDictionary[ aReplace ] = aWith



	#returns the rules. 
	def iterate( self, aBase, aIterations ):
		if aIterations > 0:
			replaced = ""
			for i in aBase:		
				replaced = replaced + self.ruleDictionary.get(i,i)
				#print 'i: %s replace: %s' % (i, replaced)
			aBase = replaced
			return self.iterate( aBase, aIterations-1 )
		else:
			return aBase
            
"""
World Co-ordinates
"""
class Point3D():
	def __init__(self, field1, field2, field3):
		self.x = field1
		self.y = field2
		self.z = field3

"""
Maya line draw
"""
def drawLine( aStartPoint, aEndPoint ):
	cmds.curve( d=1, p=[(aStartPoint.x, aStartPoint.y, aStartPoint.z),(aEndPoint.x, aEndPoint.y, aEndPoint.z)] )
	return

"""
Calculates vector for next object to draw
"""
def calculateVector( aLength, aRotationZ, aRotationX):
	# +- z axis, LR y axis.
    
	"""
	Using 3D Camera calculations as a model:
    
	x = zoom * cos(tilt) * sin(rotation)
	y = zoom * sin(tilt)
	z = zoom * cos(tilt) * cos(rotation)
    
    radiansZ is tilt
    radiansx is rotation
    zoom is magnitude of the vector (aLength)
    
	The direction is different for the line segement vector as it follows
	the y axis. It rearranges the directions values to the following:
    
    x ==> aLength * (math.sin(radiansZ))
	y ==> aLength * (math.cos(radiansZ) * math.cos(radiansX))
	z ==> aLength * (math.cos(radiansZ) * math.sin(radiansX))
    
	"""

	radiansX = math.pi * aRotationX / 180
	radiansZ = math.pi * aRotationZ / 180
    
	return Point3D( aLength * math.sin(radiansZ), aLength * (math.cos(radiansZ) * math.cos(radiansX)) , 
						aLength * (math.cos(radiansZ) * math.sin(radiansX)) )	


"""
Visualises L-system 
Loops through string input, drawing and transforming based on input characters
"""	
def visualizeLSystem( aString ):
	
	mass =  cmds.spaceLocator()
	mass = mass[0]

	inputString = aString
	index = 0	# Where at the input string we start from
	angle = 0
	zAngle = 0	# Degrees, nor radians
	xAngle = 0
	turn = 30	# How much we turn
	length = 1.0		# Unit length of an advancement
	currentPoint = Point3D( 0.0, 0.0, 0.0 )
	coordinateStack = []	# Stack where to store coordinates
	vertAngleStack = []		# Stack to store angles
	horizAngleStack = []

	while ( index < len( inputString ) ):
		if inputString[index] == 'F':
			vector = calculateVector( length, zAngle, xAngle )
			newPoint = Point3D( currentPoint.x + vector.x, currentPoint.y + vector.y,
								currentPoint.z + vector.z )
			#drawLine( currentPoint, newPoint )
			currentPoint = newPoint
			
			origin = cmds.polyCylinder(	r=0.125 , sx=2, sy=2,
										h = length+0.25, ax=(vector.x,vector.y,vector.z), 
										cuv=1, ch=1)
			shpereRef = origin [0]
			cmds.parent(shpereRef, mass)
			
			x= currentPoint.x - vector.x/2
			y= currentPoint.y - vector.y/2
			z= currentPoint.z - vector.z/2

			cmds.setAttr ('%s.translateX' % shpereRef, x)
			cmds.setAttr ('%s.translateY' % shpereRef, y)
			cmds.setAttr ('%s.translateZ' % shpereRef, z)


		#Function to draw geometry for line in here
		elif (inputString[index] == '-'):
			zAngle -= turn
		elif (inputString[index] == '+'):
			zAngle +=  turn
		elif (inputString[index] == 'L'):
			xAngle -= turn
		elif (inputString[index] == 'R'):
			xAngle += turn
		elif (inputString[index] == '['):
			coordinateStack.append( currentPoint )
			vertAngleStack.append( angle )
			horizAngleStack.append( angle )			

			junction = cmds.polySphere(r=0.3, sx=4, sy=4, ax=(0,1,0), cuv=2, ch=1)
			junctRef = junction [0]
			x= currentPoint.x
			y= currentPoint.y
			z= currentPoint.z
			cmds.setAttr ('%s.translateX' % junctRef, x)
			cmds.setAttr ('%s.translateY' % junctRef, y)
			cmds.setAttr ('%s.translateZ' % junctRef, z)
			cmds.parent(junctRef, mass)

			#Function to draw geometry for junction in here
		elif inputString[index] == ']':
			currentPoint = coordinateStack.pop()
			horizAngle = horizAngleStack.pop()
			vertAngle = vertAngleStack.pop()
			
		elif (inputString[index] == 'S'):
			thesphere = cmds.polyCube (w=0.4, h=0.4, d=1)
			cosmo = thesphere [0]
			cmds.parent(cosmo, mass)

			x= currentPoint.x
			y= currentPoint.y
			z= currentPoint.z-0.5
			
			cmds.setAttr ('%s.tx' % cosmo, x)
			cmds.setAttr ('%s.ty' % cosmo, y)
			cmds.setAttr ('%s.tz' % cosmo, z)
		else:
			print inputString[index] + ": ignored"

		# Move to the next drawing directive
		index = index + 1

	return mass


### Example Usage (+or-)(L or R)( ###
# create dictionery, add commands #
system = LSystem()
system.addRule( "A", "---F" )
system.addRule( "B", "RRRF" )
"""
system.addRule( "C", "FFFFLLFFLFF[][]FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]++++++FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]++++++FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]++++++F+F+F+F+F+F+F+F+F+F+F+F+F-F-F-F-F-F-F-F-F-F-F-F-F[][]LLLF[][][][][]" )
system.addRule( "D", "FFFFLLFFLFF[][]FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]++++++FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]++++++FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]++++++F+F+F+F+F+F+F+F+F+F+F+F+F-F-F-F-F-F-F-F-F-F-F-F-F[]" )
system.addRule( "E", "F+++FS+++F+++F[F+++FS+++FS]LLLF[]FS+++FS+++F+++F[F+++FS+++F]LLLF[]F+++F+++F[][LLLLLF[]]+++++++++F[F[][LLLLLF[]]F+++F]LLLLLF[]+++FS+FS+FS+FS+FS+FS+FSFS+FS+FS+FS+FS+FS+FS[]RRRFF[][RF][]+++FFS+FFS+FFS+FFS+FFS[][[]LLLF[]FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]++++++FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]][]++++++++FFS+FFSFFS+FFS[][[]LLLF[]FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-SFS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]LLLF[]++++++FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS+FS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS-FS[]][]-FFS+FFS+FSF+FFS+FF" )
"""

iterations =1
# command rule index #
axiomA = "A"
axiomB = "B"
"""
axiomC = "C"
axiomD = "D"
axiomE = "E"
"""

# input rules to visualisation #
print 'Base %s' % system.iterate( axiomA, iterations )
A= visualizeLSystem( system.iterate( axiomA, iterations ) )
B= visualizeLSystem( system.iterate( axiomB, iterations ) )
"""
C= visualizeLSystem( system.iterate( axiomC, iterations ) )
D= visualizeLSystem( system.iterate( axiomD, iterations ) )
E= visualizeLSystem( system.iterate( axiomE, iterations ) )
"""
"""
# extra ornamental rotations #
cmds.setAttr ('%s.rotateX' % A, 90)
cmds.setAttr ('%s.rotateX' % B, 90)
cmds.setAttr ('%s.rotateX' % D, 90)
cmds.setAttr ('%s.rotateX' % E, 270)
"""
