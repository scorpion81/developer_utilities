from . import edit_operator_source
from . import edit_addon_source
from . import python_text_api_lookup
import bpy 
from bpy.types import AddonPreferences


class DeveloperUtilitiesPreferences(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    use_external : BoolProperty(
            name="Use External Editor",
            default=False,
            )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "use_external")

def register():
    bpy.utils.register_class(DeveloperUtilitiesPreferences)
    edit_operator_source.register()
    edit_addon_source.register()
    python_text_api_lookup.register()

def unregister():
    edit_operator_source.unregister()
    edit_addon_source.unregister()
    python_text_api_lookup.unregister()
    bpy.utils.unregister_class(DeveloperUtilitiesPreferences)
