import bpy
import math
from bpy.types import Operator

body = []
overlap = 0.3


def create_color_mat(name, color):
    mat = bpy.data.materials.get(name)

    if not mat:
        mat = bpy.data.materials.new(name=name)

    bpy.data.materials[name].diffuse_color = color

    return mat


def add_mat_to_active_object(material):
    active = bpy.context.active_object
    active.data.materials.append(material)


def calc_point_on_ball_from_angles(radius, vert, hor):
    s = math.radians(hor)
    t = math.radians(vert)
    x = radius * math.cos(s) * math.sin(t)
    y = radius * math.sin(s) * math.sin(t)
    z = radius * math.cos(t)

    return (x, y, z)


class CreateBody(Operator):
    """Create main snowman body"""
    bl_idname = "snow.create_body"
    bl_label = "Create main snowman body"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        del body[:]
        scene = context.scene
        snow = scene.snow

        material = create_color_mat("white", (1, 1, 1))

        ball_amount = snow.ball_amount

        bottom_radius = 10

        delta = (bottom_radius/2)/(ball_amount-1)
        previous_radius = 0
        z_position = 0
        for ball_number in range(ball_amount):
            radius = bottom_radius - (delta * ball_number)
            z_position += 0 if previous_radius == 0 else previous_radius + radius - (overlap * previous_radius)
            bpy.ops.mesh.primitive_uv_sphere_add(size=radius, location=(0, 0, z_position))
            active = context.active_object
            add_mat_to_active_object(material)
            obj = bpy.data.objects[active.name]
            body.append(obj)

            previous_radius = radius

        return {'FINISHED'}


class CreateFace(Operator):
    """Add face to snowman"""
    bl_idname = "snow.create_face"
    bl_label = "Add face to snowman"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(body) > 0

    def execute(self, context):
        scene = context.scene
        snow = scene.snow
        head = body[-1]
        head_location_z = head.location.z

        # nose
        material = create_color_mat("orange", (1, 0.216036, 0))
        nose_z = head_location_z
        nose_radius = 1
        nose_length = snow.nose_length
        nose_y = -nose_length/2

        bpy.ops.mesh.primitive_cone_add(radius1=nose_radius, depth=nose_length, location=(0, nose_y, nose_z), rotation=(1.5708, 0, 0))
        add_mat_to_active_object(material)

        # eyes
        material = create_color_mat("black", (0, 0, 0))

        x, y, z = calc_point_on_ball_from_angles(5, 70, 70)
        z += head_location_z

        bpy.ops.mesh.primitive_uv_sphere_add(size=0.5, location=(x, -y, z))
        add_mat_to_active_object(material)

        bpy.ops.mesh.primitive_uv_sphere_add(size=0.5, location=(-x, -y, z))
        add_mat_to_active_object(material)

        return {'FINISHED'}


class CreateButtons(Operator):
    """Add buttons to snowman"""
    bl_idname = "snow.create_buttons"
    bl_label = "Add buttons to snowman"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(body) > 0

    def execute(self, context):
        scene = context.scene
        snow = scene.snow

        material = create_color_mat("black", (0, 0, 0))

        hor = 90
        button_amount = snow.button_amount
        start_angle = 45
        delta_angle = (135 - 45) / (button_amount - 1)
        for ball in body[:-1]:
            radius = ball.dimensions.x/2
            ball_z_location = ball.location.z
            for button_number in range(button_amount):
                vert = start_angle + button_number*delta_angle
                x, y, z = calc_point_on_ball_from_angles(radius, vert, hor)
                z += ball_z_location

                bpy.ops.mesh.primitive_uv_sphere_add(size=0.5, location=(x, -y, z))
                add_mat_to_active_object(material)

        return {'FINISHED'}


class CreateHat(Operator):
    """Add hat to snowman"""
    bl_idname = "snow.create_hat"
    bl_label = "Add hat to snowman"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(body) > 0

    def execute(self, context):
        head = body[-1]
        head_location_z = head.location.z
        radius = head.dimensions.x/2

        hat_z_location = head_location_z + radius - overlap * radius

        top_hat_height = 6
        top_hat_z_location = hat_z_location + top_hat_height/2

        bpy.ops.mesh.primitive_cylinder_add(radius=3, depth=top_hat_height,
                                            location=(0, 0, top_hat_z_location))

        material = create_color_mat('red', (0.55, 0, 0))
        add_mat_to_active_object(material)

        bottom_hat_height = 1
        bottom_hat_z_location = hat_z_location + bottom_hat_height/2 - 0.1
        bpy.ops.mesh.primitive_cylinder_add(radius=6, depth=bottom_hat_height,
                                            location=(0, 0, bottom_hat_z_location))

        add_mat_to_active_object(material)

        return {'FINISHED'}
