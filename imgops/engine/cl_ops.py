import pyopencl as cl
import pyopencl.tools

def create_ctx() -> cl.Context:
  gl_props = pyopencl.tools.get_gl_sharing_context_properties()
  for platform in cl.get_platforms():
    try: return cl.Context(properties=[(cl.context_properties.PLATFORM, platform)] + gl_props) #type: ignore
    except cl.RuntimeError: pass
  raise RuntimeError("No OpenCL platform supports GL sharing")