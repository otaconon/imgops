from OpenGL import GL as gl
import pyopencl as cl

from .window import Window


class Renderer:
  def __init__(self, win: Window):
    self.gl_ctx = win.create_gl_ctx()
    self.dim = (win.width, win.height)
    self.tex_id = gl.GLuint()
    self.fbo_id = gl.GLuint()
    self.cl_tex: cl.GLTexture | None = None
    self.cl_queue: cl.CommandQueue | None = None
    
  def __enter__(self) -> Renderer:
    gl.glCreateTextures(gl.GL_TEXTURE_2D, 1, self.tex_id)
    gl.glTextureStorage2D(self.tex_id.value, 1, gl.GL_RGBA32F, *self.dim)
    gl.glCreateFramebuffers(1, self.fbo_id)
    gl.glNamedFramebufferTexture(self.fbo_id.value, gl.GL_COLOR_ATTACHMENT0, self.tex_id.value, 0)
    return self
  
  def __exit__(self, exc_type, exc, tb):
    if self.cl_queue: self.cl_queue.finish()
    if self.cl_tex: self.cl_tex.release()
    if self.fbo_id: gl.glDeleteFramebuffers(1, self.fbo_id)
    if self.tex_id: gl.glDeleteTextures(1, self.tex_id)
    
  def set_cl_context(self, cl_ctx: cl.Context):
    self.cl_queue = cl.CommandQueue(cl_ctx)
    self.cl_tex = cl.GLTexture(cl_ctx, cl.mem_flags.READ_WRITE, gl.GL_TEXTURE_2D, 0, int(self.tex_id.value), 2)
    