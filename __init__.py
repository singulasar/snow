bl_info = {
    "name": "Snowman",
    "author": "Jam",
    "blender": (2, 79, 0),
    "location": "3D View > Toolbox",
    "description": "Creation of snowmen",
    "warning": "",
    "category": "Mesh"}


if "bpy" in locals():
    import importlib
    importlib.reload(ui)
else:
    import bpy
    from bpy.props import (
            StringProperty,
            PointerProperty,
            IntProperty,
            BoolProperty,
            FloatProperty
            )
    from bpy.types import (
            AddonPreferences,
            PropertyGroup,
            )
    from . import (
        ui
    )
    from .operators import operators


def update_panel(self, context):
    panel = ui.Snowman
    if "bl_rna" in panel.__dict__:
        bpy.utils.unregister_class(panel)
    panel.bl_category = context.user_preferences.addons[__name__].preferences.category
    bpy.utils.register_class(panel)


class preferences(AddonPreferences):
    bl_idname = __name__

    category = StringProperty(
                name="Tab Category",
                description="Choose a name for the category of the panel",
                default="Snowman",
                update=update_panel
                )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()

        col.label(text="Tab Category:")
        col.prop(self, "category", text="")


class SnowSettings(PropertyGroup):
    ball_amount = IntProperty(
        description="Number of balls",
        min=1, max=10,
        default=3
    )
    nose_length = FloatProperty(
        description="Nose length",
        min=1, default=10
    )
    button_amount = IntProperty(
        description="Number of buttons",
        min=2, max=10,
        default=3
    )

classes = (
    operators.CreateBody,
    operators.CreateFace,
    operators.CreateButtons,
    operators.CreateHat,

    SnowSettings,
    preferences,
    )


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    update_panel(None, bpy.context)
    bpy.types.Scene.snow = PointerProperty(type=SnowSettings)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
