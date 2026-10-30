from imgops import engine
import sdl2 as sdl
from OpenGL import GL as gl
import pyopencl as cl
import pyopencl.array as cl_array
import numpy as np
from imgui_bundle import imgui
from imgui_bundle.python_backends.sdl2_backend import SDL2Renderer
from PIL import Image

def main():
  with open("imgops/kernels/process_image.c") as f:
    kernel_src = f.read()
  
  with (engine.Window("App", 900, 900) as win, engine.Renderer(win) as renderer):
    win.set_gl_ctx(renderer.gl_ctx)
    cl_ctx = engine.CLContext()
    cl_ctx.set_texture(renderer.tex_id)
    
    imgui.create_context()
    imgui_renderer = SDL2Renderer(win.win)
    
    running = True
    event = sdl.SDL_Event()
    
    prg = cl.Program(cl_ctx.ctx, kernel_src).build()
    kernel = prg.process_image
    
    with Image.open("data/colors/vertical_stripes.png") as im:
      img_arr = np.ascontiguousarray(np.asarray(im.convert("RGBA"), dtype=np.float32) / 255)
      
    d_img = cl.image_from_array(cl_ctx.ctx, np.ascontiguousarray(img_arr[:renderer.dim[0], :renderer.dim[1], :]), num_channels=4)
    color_mult = np.array([1.0, 0.5, 0.2, 1.0], dtype=np.float32)
    
    while running:
      while sdl.SDL_PollEvent(event) != 0:
        imgui_renderer.process_event(event)
        if event.type == sdl.SDL_QUIT: running = False
        
      imgui_renderer.process_inputs()
      imgui.new_frame()
        
      imgui.begin("Kernel Parameters")
      _, color_mult[0] = imgui.slider_float("Color mult: r", color_mult[0], 0.1, 10.0)
      _, color_mult[1] = imgui.slider_float("Color mult: g", color_mult[1], 0.1, 10.0)
      _, color_mult[2] = imgui.slider_float("Color mult: b", color_mult[2], 0.1, 10.0)
      imgui.end()
      
      gl.glFinish()
      cl.enqueue_acquire_gl_objects(cl_ctx.queue, [cl_ctx.tex])
      kernel(cl_ctx.queue, renderer.dim, None, d_img, cl_ctx.tex, color_mult)
      cl.enqueue_release_gl_objects(cl_ctx.queue, [cl_ctx.tex])
      cl_ctx.queue.finish()

      gl.glBlitNamedFramebuffer(renderer.fbo_id.value, 0, 0, 0, *renderer.dim, 0, 0, *renderer.dim, gl.GL_COLOR_BUFFER_BIT, gl.GL_NEAREST)
      
      imgui.render()
      imgui_renderer.render(imgui.get_draw_data())
      sdl.SDL_GL_SwapWindow(win.win)

if __name__ == "__main__":
  main()