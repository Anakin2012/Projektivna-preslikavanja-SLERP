import numpy as np
import sys

import math

from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *

def draw_debug_coosys(size):
    glDisable(GL_LIGHTING);
    glBegin(GL_LINES);
    glColor3f(1, 0, 0);
    glVertex3f(size, 0, 0);
    glVertex3f(0, 0, 0);

    glColor3f(0, 1, 0);
    glVertex3f(0, size, 0);
    glVertex3f(0, 0, 0);

    glColor3f(0, 0, 1);
    glVertex3f(0, 0, size);
    glVertex3f(0, 0, 0);
    glEnd();
    glEnable(GL_LIGHTING);

def alpha(a):
    return np.array([ [1,0,0],
                      [0, math.cos(a), -math.sin(a)],
                      [0, math.sin(a), math.cos(a)] ])

def beta(b):
    return np.array([ [math.cos(b), 0, math.sin(b)],
                      [0, 1, 0],
                      [-math.sin(b), 0, math.cos(b)] ])

def gamma(c):
    return np.array([ [math.cos(c), -math.sin(c), 0],
                      [math.sin(c), math.cos(c), 0],
                      [0,0,1] ])

def normalizeVec(vec):

    length = math.sqrt(vec[0][0]*vec[0][0]+vec[1][0]*vec[1][0]+vec[2][0]*vec[2][0]);
    newvec = vec/length;

    return newvec;

def eulerToA(phi, theta, psi):
    return (gamma(psi).dot(beta(theta))).dot(alpha(phi))


def AxisAngle(matrixA):

    one = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    ap = matrixA-one;

    axis = np.cross(ap[0], ap[1]);
    n = math.sqrt(axis[0]*axis[0] + axis[1]*axis[1] + axis[2]*axis[2])
    axis = axis/n

    trace = ap[1]
    n1 = math.sqrt(trace[0]*trace[0] + trace[1]*trace[1] + trace[2]*trace[2])
    tracep = matrixA.dot(trace)
    np1 = math.sqrt(tracep[0]*tracep[0] + tracep[1]*tracep[1] + tracep[2]*tracep[2])


    angle = math.acos((trace.dot(tracep) / (n1*np1)))

    d = np.linalg.det(np.array([trace, tracep, axis]))
    if(d < 0):
        angle = -angle;

    return axis, angle;

def rodrigez(vec, angle):

   cos = math.cos(angle)
   sin = math.sin(angle)

   one = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
   vec = np.resize(vec, (3, 1))

   return vec.dot(np.transpose(vec)) + cos*(one - (vec.dot(np.transpose(vec)))) + sin*np.array([ [0, -vec[2], vec[1]], [vec[2], 0, -vec[0]], [-vec[1], vec[0], 0] ])

def aToEuler(matrixA):

    a31 = matrixA[2][0]
    if a31 < 1:
        if a31 > -1:
            angle3 = math.atan2(matrixA[1][0],matrixA[0][0])
            angle2 = math.asin(-a31)
            angle1 = math.atan2(matrixA[2][1],matrixA[2][2])
        else:
            angle3 = math.atan2(-matrixA[0][1],matrixA[1][1]);
            angle2 = math.pi/2;
            angle1 = 0;
    else:
        angle3 = math.atan2(-matrixA[0][1],matrixA[1][1])
        angle2 = math.pi / 2
        angle1 = 0

    return angle1, angle2, angle3

def axisAngle2Q(vec, angle):

    rotation = rodrigez(vec, angle);
    angles = aToEuler(rotation);

    calpha = math.cos(angles[0] * 0.5);
    salpha = math.sin(angles[0] * 0.5);

    cbeta = math.cos(angles[1] * 0.5);
    sbeta = math.sin(angles[1] * 0.5);

    cgama = math.cos(angles[2] * 0.5);
    sgama = math.sin(angles[2] * 0.5);

    return np.array([salpha * cbeta * cgama - calpha * sbeta * sgama,
                     calpha * sbeta * cgama + salpha * cbeta * sgama,
                     calpha * cbeta * sgama - salpha * sbeta * cgama,
                     calpha * cbeta * cgama + salpha * sbeta * sgama])

def q2AxisAngle(q):
    angles = np.array([math.atan(2*(q[3]*q[0]+q[1]*q[2])/(1-2*(q[0]*q[0]+q[1]*q[1]))),
                       math.asin(2*(q[3]*q[1]-q[2]*q[0])),
                       math.atan(2*(q[3]*q[2]+q[0]*q[1])/(1-2*(q[1]*q[1]+q[2]*q[2]))) ])

    return AxisAngle(eulerToA(angles[0], angles[1], angles[2]))

def normalizeQ(q):
    qn = 0
    for i in q:
        qn += i*i
    qn = math.sqrt(qn)

    return qn


def slerp(tm, t):

    global q1
    global q2

    qn1 = normalizeQ(q1)
    qn2 = normalizeQ(q2)

    cos = q1.dot(q2)
    if(cos < 0):
        q1 = -q1
        cos = -cos

    if(cos > 0.95):
        return q1

    angle = math.acos(cos)
    a = math.sin(angle*(1-t/tm))/ math.sin(angle)
    b = math.sin(angle*t/tm)/ math.sin(angle)

    qs = a*q1 + b*q2

    return qs

animation_parameter = 0
animation_ongoing = 0
angles1 = np.array([math.pi/6, 2*math.pi/3, 5*math.pi/4])
position1 = np.array([-0.2, 0.5, 0])

angles2 = np.array([-5*math.pi/3, math.pi/4, 5*math.pi/6])
position2 = np.array([1, -0.2, -1]);

m1 = eulerToA(angles1[0],angles1[1],angles1[2])
m2 = eulerToA(angles2[0],angles2[1],angles2[2])
axis1, angle1 = AxisAngle(m1)
axis2, angle2 = AxisAngle(m2)
q1 = axisAngle2Q(axis1, angle1)
q2 = axisAngle2Q(axis2, angle2)

def animate():

    global animation_parameter
    t = animation_parameter

    if animation_parameter < 1:
        qs = slerp(1, animation_parameter)
        axis, angle = q2AxisAngle(qs)
        matrixA = rodrigez(axis, angle)
        phi, theta, psi = aToEuler(matrixA)

        glColor3f(1, 0.5, 0.5)
        glPushMatrix()
        glDisable(GL_LIGHTING)

        glTranslatef((1-t)*position1[0] + t*position2[0], (1-t)*position1[1] + t*position2[1], (1-t)*position1[2] + t*position2[2])

        glScalef(0.2, 0.3, 0.2)

        glRotatef(psi*57.2958, 0, 0, 1)
        glRotatef(theta*57.2958, 0, 1, 0)
        glRotatef(phi*57.2958, 1, 0, 0)

        glutWireCube(1)
        glEnable(GL_LIGHTING)
        glPopMatrix()
    #    glEnable(GL_LIGHTING)

    else:
        animation_parameter = 0


def keyboard(*args):
    global animation_ongoing
    if ord(args[0]) == 27:
        exit()
    elif ord(args[0]) == 103:
        if not animation_ongoing:
            animation_ongoing = 1
            glutTimerFunc(50,timer,0)
    elif ord(args[0]) == 115:
        animation_ongoing = 0
    elif ord(args[0]) == 114:
        global animation_parameter
        animation_parameter = 0

def display():

    light_position = [ 1, 1, 1, 0 ]

#    angles1 = np.array([math.pi/6, 2*math.pi/3, 5*math.pi/4])
#    position1 = np.array([-0.2, 0.5, 0])

    #angles2 = np.array([-5*math.pi/3, math.pi/4, 5*math.pi/6])
#    position2 = np.array([1, -0.2, -1]);

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(2, 1, 2, 0, 0, 0, 0, 1, 0)

    draw_debug_coosys(2)

    glDisable(GL_LIGHTING)
    glColor3f(1, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(position1[0], position1[1], position1[2])
    glScalef(0.2, 0.3, 0.2)
    glRotatef(angles1[2]*57.2958, 0, 0, 1)
    glRotatef(angles1[1]*57.2958, 0, 1, 0)
    glRotatef(angles1[0]*57.2958, 1, 0, 0)

    glutWireCube(1)
    draw_debug_coosys(1)
    glPopMatrix()
    glEnable(GL_LIGHTING)

    glDisable(GL_LIGHTING)
    glColor3f(1, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(position2[0], position2[1], position2[2])
    glScalef(0.2, 0.3, 0.2)
    glRotatef(angles2[2]*57.2958, 0, 0, 1)
    glRotatef(angles2[1]*57.2958, 0, 1, 0)
    glRotatef(angles2[0]*57.2958, 1, 0, 0)


    glutWireCube(1)
    draw_debug_coosys(1)
    glPopMatrix()
    glEnable(GL_LIGHTING)

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    animate()

    glutSwapBuffers()


def main():

    glutInit(sys.argv)

    light_ambient = [0.1,0.1,0.1,1]
    light_diffuse = [0.7,0.7,0.7,1]
    light_specular = [0.9,0.9,0.9,1]

    ambient_coeffs = [0.3,0.3,0.4,1]
    diffuse_coeffs = [0.6,0.6,0.85,1]
    specular_coeffs = [0.6,0.6,0.6,1]
    shininess = 30;

    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
    glutInitWindowSize(300, 300)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("animation")

    glutKeyboardFunc(keyboard)
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse);
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_coeffs);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_coeffs);
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular_coeffs);
    glMaterialf(GL_FRONT, GL_SHININESS, shininess);

    glutMainLoop();


def timer(value):
    if value != 0:
        return
    global animation_parameter
    global animation_ongoing

    animation_parameter+=0.01
    glutPostRedisplay()

    if animation_ongoing:
        glutTimerFunc(50 , timer, 0);


def reshape(width, height):

    glViewport(0, 0, width, height);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(60, float(width) / height, 1, 100);


if __name__ == "__main__":
    main()
