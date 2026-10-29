from OpenGL import GL as gl
import pyopencl as cl
import sdl2 as sdl

from .window import Window

class Renderer:
  def __init__(self, win: Window):
    self.gl_ctx = sdl.SDL_GL_CreateContext(win.win)
    self.dim = (win.width, win.height)
    self.tex_id = gl.GLuint()
    self.fbo_id = gl.GLuint()
    
  def __enter__(self) -> Renderer:
    gl.glCreateTextures(gl.GL_TEXTURE_2D, 1, self.tex_id)
    gl.glTextureStorage2D(self.tex_id.value, 1, gl.GL_RGBA32F, *self.dim)
    gl.glCreateFramebuffers(1, self.fbo_id)
    gl.glNamedFramebufferTexture(self.fbo_id.value, gl.GL_COLOR_ATTACHMENT0, self.tex_id.value, 0)
    
    return self
  
  def __exit__(self, exc_type, exc, tb):
    if self.fbo_id: gl.glDeleteFramebuffers(1, self.fbo_id)
    if self.tex_id: gl.glDeleteTextures(1, self.tex_id)