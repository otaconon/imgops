import sdl2 as sdl
from typing import Any

class Window:
  win: Any
  
  def __init__(self, name: str, width: int, height: int):
    self.name = name
    self.width = width
    self.height = height
    
  def __enter__(self) -> Window:
    sdl.SDL_Init(sdl.SDL_INIT_VIDEO)
    sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MAJOR_VERSION, 4)
    sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MINOR_VERSION, 5)
    sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_PROFILE_MASK, sdl.SDL_GL_CONTEXT_PROFILE_CORE)
    self.win = sdl.SDL_CreateWindow(self.name.encode(), sdl.SDL_WINDOWPOS_CENTERED, sdl.SDL_WINDOWPOS_CENTERED, self.width, self.height, sdl.SDL_WINDOW_OPENGL | sdl.SDL_WINDOW_SHOWN)
    return self
    
  def __exit__(self, exc_type, exc_value, traceback):
    if self.win != None: sdl.SDL_DestroyWindow(self.win)
    
  def set_gl_ctx(self, gl_ctx):
    sdl.SDL_GL_MakeCurrent(self.win, gl_ctx)
    sdl.SDL_GL_SetSwapInterval(1)