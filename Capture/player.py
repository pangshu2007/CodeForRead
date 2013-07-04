'''
(*)~----------------------------------------------------------------------------------
 Pupil - eye tracking platform
 Copyright (C) 2012-2013  Moritz Kassner & William Patera

 Distributed under the terms of the CC BY-NC-SA License.
 License details are in the file license.txt, distributed as part of this software.
----------------------------------------------------------------------------------~(*)
'''
import os, sys
import OpenGL.GL as gl
from glfw import *
import numpy as np
import cv2
from methods import Temp
from uvc_capture import autoCreateCapture
from time import sleep
from glob import glob
from gl_utils import adjust_gl_view, draw_gl_texture, clear_gl_screen


def make_grid(dim=(11,4)):
    """
    this function generates the structure for an asymetrical circle grid
    centerd around 0 width=1, height scaled accordinly
    """
    x,y = range(dim[0]),range(dim[1])
    p = np.array([[[s,i] for s in x] for i in y], dtype=np.float32)
    p[:,1::2,1] += 0.5
    p = np.reshape(p, (-1,2), 'F')

    ###scale height = 1
    x_scale =  1./(np.amax(p[:,0])-np.amin(p[:,0]))
    y_scale =  1./(np.amax(p[:,1])-np.amin(p[:,1]))

    p *=x_scale,x_scale/.5

    ###center x,y around (0,0)
    x_offset = (np.amax(p[:,0])-np.amin(p[:,0]))/2.
    y_offset = (np.amax(p[:,1])-np.amin(p[:,1]))/2.
    p -= x_offset,y_offset
    return p

def player(g_pool,size):
    """player
        - Shows 9 point calibration pattern
        - Plays a source video synchronized with world process
        - Get src videos from directory (glob)
        - Iterate through videos on each record event
    """


    grid = make_grid()
    grid *=2.5###scale to fit
    # player object
    player = Temp()
    player.play_list = glob('src_video/*')
    path_parent = os.path.dirname( os.path.abspath(sys.argv[0]))
    player.playlist = [os.path.join(path_parent, path) for path in player.play_list]
    player.captures = [autoCreateCapture(src) for src in player.playlist]
    print "Player found %i videos in src_video"%len(player.captures)
    player.captures =  [c for c in player.captures if c is not None]
    print "Player sucessfully loaded %i videos in src_video"%len(player.captures)
    # for c in player.captures: c.auto_rewind = False
    player.current_video = 0

    # Callbacks
    def on_resize(w, h):
        adjust_gl_view(w,h)

    def on_key(key, pressed):
        if key == GLFW_KEY_ESC:
                on_close()
    def on_char(char, pressed):
        if char  == ord('9'):
            g_pool.cal9.value = True
            g_pool.calibrate.value = True



    def on_close():
        g_pool.quit.value = True
        print "Player Process closing from window"


    # initialize glfw
    glfwInit()
    glfwOpenWindow(size[0], size[1], 0, 0, 0, 8, 0, 0, GLFW_WINDOW)
    glfwSetWindowTitle("Player")
    glfwSetWindowPos(100,0)
    glfwDisable(GLFW_AUTO_POLL_EVENTS)


    #Callbacks
    glfwSetWindowSizeCallback(on_resize)
    glfwSetWindowCloseCallback(on_close)
    glfwSetKeyCallback(on_key)
    glfwSetCharCallback(on_char)


    #gl state settings
    gl.glEnable( gl.GL_BLEND )
    gl.glEnable(gl.GL_POINT_SMOOTH)
    gl.glClearColor(1.,1.,1.,0.)


    while glfwGetWindowParam(GLFW_OPENED) and not g_pool.quit.value:

        glfwPollEvents()

        if g_pool.player_refresh.wait(0.01):
            g_pool.player_refresh.clear()

            clear_gl_screen()
            if g_pool.cal9.value:
                circle_id,step = g_pool.cal9_circle_id.value,g_pool.cal9_step.value
                gl.glColor4f(0.0,0.0,0.0,1.0)
                gl.glPointSize(40)
                gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
                gl.glBegin(gl.GL_POINTS)
                for p in grid:
                    gl.glVertex3f(p[0],p[1],0.0)
                gl.glEnd()

                ###display the animated target dot
                gl.glPointSize((40)*(1.01-(step+1)/80.0))
                gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ZERO)
                if g_pool.ref_x.value or g_pool.ref_y.value: ###if pattern detected
                    gl.glColor4f(0.0,0.5,0.0,1.0)
                else:
                    gl.glColor4f(0.5,0.0,0.0,1.0)
                gl.glBegin(gl.GL_POINTS)
                gl.glVertex3f(grid[circle_id][0],grid[circle_id][1],0.0)
                gl.glEnd()

            elif g_pool.play.value:
                s, img = player.captures[player.current_video].read_RGB()
                if s:
                    draw_gl_texture(image)
                else:
                    player.captures[player.current_video].rewind()
                    player.current_video +=1
                    if player.current_video >= len(player.captures):
                        player.current_video = 0
                    g_pool.play.value = False
            glfwSwapBuffers()

    glfwCloseWindow()
    glfwTerminate()
    print "PLAYER Process closed"

if __name__ == '__main__':
    print make_grid()
