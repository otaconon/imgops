from OpenGL import GL as gl
import pyopencl as cl
import pyopencl.tools
import sdl2 as sdl

class CLContext:
  tex:cl.GLTexture
  
  def __init__(self):
    gl_props = pyopencl.tools.get_gl_sharing_context_properties()
    for platform in cl.get_platforms():
      try: 
        cl_ctx = cl.Context(properties=[(cl.context_properties.PLATFORM, platform)] + gl_props) #type: ignore
        break
      except cl.RuntimeError: continue
    self.ctx = cl_ctx
    self.queue = cl.CommandQueue(self.ctx)
    
  def set_texture(self, tex_id):
    self.tex = cl.GLTexture(self.ctx, cl.mem_flags.READ_WRITE, gl.GL_TEXTURE_2D, 0, int(tex_id.value), 2)