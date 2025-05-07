import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import uniform
from OpenGL.GL import *

stars = []
for a in range(500):
    stars.append([uniform(-5, 5), uniform(-5, 5)])

def init():
    pygame.init()
    display = (900, 700)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glTranslatef(0, 0, -2)
    glMatrixMode(GL_MODELVIEW)

def draw(rotationMatrix):

    # Cube
    glPushMatrix()

    vertices = (
        (.25, .25, .25),
        (.25, -.25, .25),
        (-.25, -.25, .25),
        (-.25, .25, .25),

        (.25, .25, -.25),
        (.25, -.25, -.25),
        (-.25, -.25, -.25),
        (-.25, .25, -.25)

        )
    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),

        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),

        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7)
    )

    glColor3fv((0.0, 1.0, 0.0))
    glLineWidth(5)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glMultMatrixf(rotationMatrix)
    glColor3fv((1.0, 1.0, 1.0))
    glPointSize(2.0)
    glBegin(GL_POINTS)
    for c in stars:
        glVertex3f(c[0], c[1], -5)
        glVertex3f(c[0], c[1], 5)
        glVertex3f(5, c[0], c[1])
        glVertex3f(-5, c[0], c[1])
        glVertex3f(c[0], 5, c[1])
        glVertex3f(c[0], -5, c[1])
    glEnd()
    glPopMatrix()

def main():
    global angle_x, angle_y
    init()
    clock = pygame.time.Clock()

    rotationMatrix = (GLfloat * 16)(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    while True:
        for event in pygame.event.get():
            # Check if the Player Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        glPushMatrix()
        glLoadIdentity()
        angle_y = (keys[pygame.K_d] - keys[pygame.K_a]) * 0.5
        angle_x = (keys[pygame.K_s] - keys[pygame.K_w]) * 0.5
        glRotatef(-angle_x, 1, 0, 0)
        glRotatef(-angle_y, 0, 1, 0)
        glMultMatrixf(rotationMatrix)
        glGetFloatv(GL_MODELVIEW_MATRIX, rotationMatrix)
        glPopMatrix()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw(rotationMatrix)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()