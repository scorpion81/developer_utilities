from . import edit_operator_source
from . import edit_addon_source
from . import python_text_api_lookup
from . import document_addon

def register():
    document_addon.register()
    edit_operator_source.register()
    edit_addon_source.register()
    python_text_api_lookup.register()

def unregister():
    edit_operator_source.unregister()
    edit_addon_source.unregister()
    python_text_api_lookup.unregister()
    document_addon.unregister()
