from imgops import engine
import sdl2 as sdl
from OpenGL import GL as gl
import pyopencl as cl
import numpy as np

def main():
  with open("imgops/kernels/process_image.c") as f:
    kernel_src = f.read()
  
  with (engine.Window("App", 900, 900) as win, engine.Renderer(win) as renderer):
    win.set_gl_ctx(renderer.gl_ctx)
    cl_ctx = engine.CLContext()
    cl_ctx.set_texture(renderer.tex_id)
    
    running = True
    event = sdl.SDL_Event()
    
    prg = cl.Program(cl_ctx.ctx, kernel_src).build()
    kernel = prg.process_image
    
    #mf = cl.mem_flags
    #in_buf = cl.Buffer(cl_ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.zeros((renderer.dim[0]*renderer.dim[1], 4), dtype=np.float32))
    
    while running:
      while sdl.SDL_PollEvent(event) != 0:
        if event.type == sdl.SDL_QUIT: running = False

      gl.glFinish()
      cl.enqueue_acquire_gl_objects(cl_ctx.queue, [cl_ctx.tex])
      kernel(cl_ctx.queue, renderer.dim, None, cl_ctx.tex)
      cl.enqueue_release_gl_objects(cl_ctx.queue, [cl_ctx.tex])
      cl_ctx.queue.finish()

      gl.glBlitNamedFramebuffer(
        renderer.fbo_id.value, 0,
        0, 0, *renderer.dim,
        0, 0, *renderer.dim,
        gl.GL_COLOR_BUFFER_BIT,
        gl.GL_NEAREST,
      )
      sdl.SDL_GL_SwapWindow(win.win)

if __name__ == "__main__":
  main()