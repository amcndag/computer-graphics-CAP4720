# Assignment 2
# 

import glfw
import moderngl
import numpy
from random import random
import time

glfw.init()

window = glfw.create_window(1280, 720, "Assignment 2: Amanda Go", None, None)
if not window:
    print("Failed to create GLFW window")
    glfw.terminate()
else:
    glfw.make_context_current(window)
    ctx = moderngl.create_context()
    if not ctx:
        print("ModernGL could not create hook onto the current context")
        glfw.destroy_window(window)
        glfw.terminate()
    else:
        width, height = glfw.get_framebuffer_size(window)
        ctx.viewport = (0, 0, width, height)

#1. Keyinput callback
def key_callback(window, key, scancode, action, mods):
  if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
      glfw.set_window_should_close(window, True)

glfw.set_key_callback(window, key_callback)

#2. Window resize callback
def framebuffer_size_callback(window, w, h):
    global width, height
    width = w
    height = h
    # 1. Update the ModernGL viewport size
    ctx.viewport = (0, 0, width, height)
    
    # 2. Avoid division by zero if window is minimized
    if height == 0:
        height = 1
    #aspect_ratio = width / height
    
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

triangle_vertices = numpy.array([
     0.0,  0.8,  # Top
    -0.8, -0.8,  # Bottom left
     0.8, -0.8   # Bottom right
], dtype='f4')

triangle_vbo = ctx.buffer(triangle_vertices)

# vertex shader
vShader_code = '''
#version 330 core
in vec3 position;
void main(){
    gl_Position = vec4(position, 1);
}
'''

fShader_code = '''
#version 330 core
uniform vec3 color;
out vec4 out_color;
void main(){
    out_color = vec4(color, 1);
}
'''
shader_program = ctx.program(vertex_shader = vShader_code, fragment_shader = fShader_code)

triangle_vao = ctx.vertex_array(shader_program, [(triangle_vbo, "2f", "position")])

FPS = 5
RENDER_INTERVAL = 1/FPS
last_render_time = 0.0
# Main render loop
while not glfw.window_should_close(window):
    glfw.wait_events_timeout(RENDER_INTERVAL) # glfw.poll_events()
    current_time = time.perf_counter()
    if current_time - last_render_time >= RENDER_INTERVAL:
        last_render_time = current_time
        
        ctx.clear(0.2, 0.2, 0.2)

        shader_program["color"] = (random(), random(), random())
        triangle_vao.render()
        

        glfw.swap_buffers(window)
