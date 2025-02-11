import bpy

pid = -1

def run(cmd):
    import subprocess, shlex
    return subprocess.Popen(shlex.split(cmd), check=True)

def document(m, path):
    import pdoc, os
    
    doc = pdoc.doc.Module(m)
    out = pdoc.render.html_module(module=doc, all_modules={m.__name__: doc})
    rel_path = os.path.join(path, 'docs', f"{m.__name__}.html")
    with open(rel_path, "w") as f:
        f.write(out)

def list_submodules(package):
    
    import pkgutil, importlib
    
    """List all submodules of a given package without importing them."""
    submodules = []
    for _, name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
        submodules.append(importlib.import_module(name))
        if is_pkg:
            submodules.extend(list_submodules(importlib.import_module(name)))
    return submodules

def generate(**kwargs):
    import importlib
    import os
    import inspect
    import sys
   
    mod = importlib.import_module(kwargs['module_name'])
    modules = list_submodules(mod)
    if kwargs['target_dir'] == "":
        script_dir = os.path.dirname(inspect.getfile(mod))
        path = os.path.join(script_dir, "docs")
        os.makedirs(path, exist_ok=True)
    else:
        path = os.path.join(kwargs['target_dir'], kwargs['module_name'])
        os.makedirs(path, exist_ok=True)
    
    document(mod, path)
    for m in modules:
        document(m, path)

    if kwargs['server']:
        exe = sys.executable
        port = kwargs['port']
        cmd = f"{exe} -m http.server -d{path} {port}"
        pid = run(cmd)
        url = f"http://localhost:{port}"
        bpy.ops.wm.url_open(url=url)

    return path


class KillServerOperator(bpy.types.Operator):
    """Kill the server process if one was started previously"""
    bl_idname = "pdoc.kill"
    bl_label = "Generate Documentation"
    pid : bpy.props.IntProperty(name="pid")
    def execute(self, context):
        import signal, os
        if self.pid > -1:
            os.kill(self.pid, signal.SIGTERM)
            return {"FINISHED"}
        return {"CANCELLED"}

class DocumentationOperator(bpy.types.Operator):
    """Generates Documentation with pdoc for the given module and its submodules"""
    bl_idname = "pdoc.generate"
    bl_label = "Generate Documentation"
    module_name : bpy.props.StringProperty(name="module_name")
    server: bpy.props.BoolProperty(name="server", default=False)
    port: bpy.props.IntProperty(name="port", min=0, max=65535, default=8000)
    target: bpy.props.StringProperty(name="target", default="")

    def execute(self, context):
        if self.module_name != "":
            generate(module_name=self.module_name, target_dir=self.target, server=self.server, port=self.port)
            self.report({'INFO'}, "Documentation generated")
            return {'FINISHED'}
        self.report({'ERROR'}, "Please specify a module name")
        return {'CANCELLED'}

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(DocumentationOperator)
    bpy.utils.register_class(KillServerOperator)

def unregister():
    bpy.utils.unregister_class(KillServerOperator)
    bpy.utils.unregister_class(DocumentationOperator)
