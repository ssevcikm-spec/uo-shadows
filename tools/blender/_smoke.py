import bpy, os, sys

# Minimal smoke test: sphere on transparent bg, EEVEE, write RGBA PNG.
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(0, 0, 0.3))
bpy.context.active_object.name = "smoke_sphere"

scn = bpy.context.scene
scn.render.engine = 'BLENDER_EEVEE'
scn.render.film_transparent = True
scn.render.image_settings.file_format = 'PNG'
scn.render.image_settings.color_mode = 'RGBA'

cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
scn.collection.objects.link(cam)
cam.location = (3, -3, 2)
cam.rotation_euler = (1.0, 0, 0.8)
scn.camera = cam

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_smoke.png")
scn.render.filepath = out
scn.render.resolution_x = 256
scn.render.resolution_y = 256
bpy.ops.render.render(write_still=True)
print("SMOKE_OK", out, "exists=", os.path.exists(out))
