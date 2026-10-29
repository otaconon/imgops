import sdl2 as sdl
from typing import Any

class Window:
  def __init__(self, name: str, width: int, height: int):
    self.name = name
    self.width = width
    self.height = height
    self.win: Any | None
    
  def __enter__(self) -> Window:
    sdl.SDL_Init(sdl.SDL_INIT_VIDEO)
    sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MAJOR_VERSION, 4)
    sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MINOR_VERSION, 5)
    sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_PROFILE_MASK, sdl.SDL_GL_CONTEXT_PROFILE_CORE)
    self.win = sdl.SDL_CreateWindow(self.name.encode(), sdl.SDL_WINDOWPOS_CENTERED, sdl.SDL_WINDOWPOS_CENTERED, self.width, self.height, sdl.SDL_WINDOW_OPENGL | sdl.SDL_WINDOW_SHOWN)
    return self
    
  def __exit__(self, exc_type, exc_value, traceback):
    if self.win: sdl.SDL_DestroyWindow(self.win)
    
  def create_gl_ctx(self):
    gl_context = sdl.SDL_GL_CreateContext(self.win)
    sdl.SDL_GL_MakeCurrent(self.win, gl_context)
    sdl.SDL_GL_SetSwapInterval(1)
    return gl_context