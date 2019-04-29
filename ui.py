from bpy.types import Panel


class Snowman(Panel):
    bl_idname = "snowman_object"
    bl_label = "Snowman creation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Snowman"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        snow = scene.snow

        box = layout.box()
        rowsub = box.row(align=True)
        rowsub.label("Balls:")
        rowsub.prop(snow, "ball_amount", text="")

        rowsub = box.row(align=True)
        rowsub.operator("snow.create_body", text="Create body")

        rowsub = box.row(align=True)
        rowsub.label("Nose length:")
        rowsub.prop(snow, "nose_length", text="")

        rowsub = box.row(align=True)
        rowsub.operator("snow.create_face", text="Create face")

        rowsub = box.row(align=True)
        rowsub.label("Buttons:")
        rowsub.prop(snow, "button_amount", text="")

        rowsub = box.row(align=True)
        rowsub.operator("snow.create_buttons", text="Create buttons")

        rowsub = box.row(align=True)
        rowsub.operator("snow.create_hat", text="Create hat")


