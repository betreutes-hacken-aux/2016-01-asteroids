#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Author: Moritz Laudahn
# First Version: 27.03.2016
# Current Version: 23.06.2016
# Status: work in progress
#


import math  # degrees, radians, sin, cos
import random
import os    # linesep
import sys   # exit, args
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT

debug = True
prMatrices = False
numAstroids = 5
freeze = True

class point(object):
	def __init__(self, x, y):
		self._x = x
		self._y = y
	
	def __str__(self):
		return "point("+str(self._x)+", "+str(self._y)+")"

class PlayerShip(object):
	def __init__(self):
		self.hitpoints = 1

	def paint(self):
		GL.glPushMatrix()
		GL.glBegin(GL.GL_QUADS)
		if self.hitpoints < 0:
			GL.glColor3f(0.9, 0.2, 0.2)
		else:
			GL.glColor3f(0.5, 0.5, 0.5)
		GL.glVertex3d(5.0, 30.0, 0.0)
		GL.glVertex3d(-5.0, 30.0, 0.0)
		GL.glVertex3d(-15.0, -15.0, 0.0)
		GL.glVertex3d(15.0, -15.0, 0.0)
		
		GL.glColor3f(0.8, 0.8, 0.8)
		GL.glVertex3d(15.0, -15.0, 0.0)
		GL.glVertex3d(-15.0, -15.0, 0.0)
		GL.glVertex3d(-25.0, -25.0, 0.0)
		GL.glVertex3d(25.0, -25.0, 0.0)
		GL.glEnd()
		
		GL.glBegin(GL.GL_TRIANGLES)
		GL.glColor3f(0.8, 0.8, 0.8)
		GL.glVertex3d(0.0, 50.0, 0.0)
		GL.glColor3f(0.6, 0.6, 0.6)
		GL.glVertex3d(-5.0, 30.0, 0.0)
		GL.glVertex3d(5.0, 30.0, 0.0)
		
		GL.glColor3f(0.8, 0.8, 0.8)
		GL.glVertex3d(0.0, 50.0, 0.0)
		GL.glVertex3d(-25.0, -25.0, 0.0)
		GL.glColor3f(0.5, 0.5, 0.5)
		GL.glVertex3d(-5.0, 30.0, 0.0)
		
		GL.glColor3f(0.5, 0.5, 0.5)
		GL.glVertex3d(5.0, 30.0, 0.0)
		GL.glColor3f(0.8, 0.8, 0.8)
		GL.glVertex3d(25.0, -25.0, 0.0)
		GL.glVertex3d(0.0, 50.0, 0.0)
		
		GL.glColor3f(0.5, 0.5, 0.5)
		GL.glVertex3d(-15.0, -15.0, 0.0)
		GL.glVertex3d(-5.0, 30.0, 0.0)
		GL.glColor3f(0.8, 0.8, 0.8)
		GL.glVertex3d(-25.0, -25.0, 0.0)
		
		GL.glColor3f(0.5, 0.5, 0.5)
		GL.glVertex3d(5.0, 30.0, 0.0)
		GL.glVertex3d(15.0, -15.0, 0.0)
		GL.glColor3f(0.8, 0.8, 0.8)
		GL.glVertex3d(25.0, -25.0, 0.0)
		GL.glEnd()
		GL.glPopMatrix()

class Asteroid(object):
	def __init__(self):
		self._vertices = [point(-100.0, 100.0),
		                  point(-100.0, -100.0),
		                  point(100.0, -50.0),
		                  point(100.0, 100.0),
		                  point(50.0, 110.0)]

	def paint(self):
		GL.glPushMatrix()
		GL.glBegin(GL.GL_POLYGON)
		GL.glColor3f(0.0, 0.0, 1.0)
		for p in self._vertices:
			GL.glVertex3d(p._x, p._y, 0.0)
		GL.glEnd()
		GL.glPopMatrix()

distance = 1000
ship = PlayerShip()
astroids = []
astroids.append(Asteroid())

def display():
	global debug
	global distance
	global ship
	global astroids
	
	GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
	GL.glMatrixMode(GL.GL_MODELVIEW)
	GL.glLoadIdentity()
	
	GL.glDisable(GL.GL_DEPTH_TEST)
	
	### Objekte in der Welt
	GL.glPushMatrix()
	GL.glTranslated(0.0, 0.0, -distance)
	
	for astroid in astroids:
		astroid.paint()
	ship.paint()
	
	### weitere Objekte in der Welt
	# ...
	
	GL.glPopMatrix()
	
	GL.glDisable(GL.GL_DEPTH_TEST);
	### Objekte mit fester Position im Fenster (immer im Vordergrund)
	# ...
	
	GL.glEnable(GL.GL_DEPTH_TEST);

	GLUT.glutSwapBuffers()


def displayStop():
	GLUT.glutPostRedisplay()

def init():
	# Bedienungsanleitung ausgeben:
	print("Keine Steuerung.")
	
	# Einstellungen festlegen:
	GL.glClearColor(0.0, 0.0, 0.0, 0.0) # Hintergrundfarbe
	GL.glShadeModel(GL.GL_SMOOTH)

def reshape(w, h):
	global debug
	GL.glViewport(0, 0, w, h)
	GL.glMatrixMode(GL.GL_PROJECTION)
	GL.glLoadIdentity()
	GLU.gluPerspective(
		45, # field of view in degrees
		w/h, # aspect ratio
		1, # near clipping plane
		30000, # far clipping plane
	)
	if debug:
		print("Projection Matrix: " + os.linesep + str(GL.glGetFloatv(GL.GL_PROJECTION_MATRIX)))
	GL.glMatrixMode(GL.GL_MODELVIEW)
	GL.glLoadIdentity()

def moveDisplay():
	GLUT.glutPostRedisplay()

def mouse(button, state, x, y):
	global distance
	
	if button == 3 and state == GLUT.GLUT_DOWN:
		if distance < 10000:
			distance += 100
	elif button == 4 and state == GLUT.GLUT_DOWN:
		if distance > 100:
			distance -= 100

def keyboard(key, x, y):
	if key == chr(27):
		sys.exit(0)

if __name__ == '__main__':
	GLUT.glutInit(sys.argv)
	GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB  | GLUT.GLUT_DEPTH)
	GLUT.glutInitWindowSize(300, 300)
	GLUT.glutInitWindowPosition(100, 100)
	GLUT.glutCreateWindow('Asteroids Template #1')
	init()
	GLUT.glutDisplayFunc(display)
	GLUT.glutReshapeFunc(reshape)
	GLUT.glutMouseFunc(mouse)
	GLUT.glutKeyboardFunc(keyboard)
	GLUT.glutIdleFunc(displayStop)
	GLUT.glutMainLoop()
