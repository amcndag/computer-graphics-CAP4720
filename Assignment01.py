# Assignment 1
# create a display window that changes color one fps

import glfw
import moderngl
import numpy
from random import random
import time

glfw.init()
window = glfw.create_window(1280, 720, "Assignment 1: Amanda Go", None, None)
if not window:
    print("Failed to create GLFW window")
    glfw.terminate()
else:
    major = glfw.get_window_attrib(window,glfw.CONTEXT_VERSION_MAJOR)
    minor = glfw.get_window_attrib(window,glfw.CONTEXT_VERSION_MINOR)
    print(f"Window supports OpenGL {major}.{minor}")
    glfw.make_context_current(window)
    
    ctx = moderngl.create_context()
    # added during the 8/27 lecture
    width, height = glfw.get_framebuffer_size(window)
    ctx.viewport = (0, 0, width, height)
    
    if not ctx:
        print("ModernGL could not create hook onto the current context")
        glfw.destroy_window(window)
        glfw.terminate()

def framebuffer_size_callback(window, w, h):
    global width, height
    ctx.viewport = (0, 0, width, height)

    if height == 0:
        height = 1
    aspect_ratio = width / height

def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
glfw.set_key_callback(window, key_callback)

FPS = 1
frame_duration = 1/FPS
last_frame_time = 0

# Main render loop

while not glfw.window_should_close(window):
    glfw.wait_events_timeout(frame_duration)
    current_time = time.perf_counter()
    time_elapsed = current_time - last_frame_time

    if time_elapsed >= frame_duration:
        last_frame_time = current_time
        r = random()
        g = random()
        b = random()
        ctx.clear(r, g, b)
        glfw.swap_buffers(window)

# Clean up when finished
glfw.destroy_window(window)
glfw.terminate()