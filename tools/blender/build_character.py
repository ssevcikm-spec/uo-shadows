# -*- coding: utf-8 -*-
"""
Stavba lidské postavy + rig + chůze (4 framy) + izometrická kamera (45°).
Render vrstev (body/torso/legs/weapon) x 4 směry x 4 framy s alfa kanálem.

Spuštění (preview jednoho snímku):
  blender -b -P build_character.py -- --preview
Plný render:
  blender -b -P build_character.py
"""
import bpy, os, sys, math
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)

PREVIEW = "--preview" in sys.argv
WALKTEST = "--walktest" in sys.argv

# ----------------------------------------------------------------------------
# Základní scéna
# ----------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '8'
scene.render.image_settings.compression = 15

# Svět (ambient)
world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.40, 0.42, 0.45, 1.0)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.6

# ----------------------------------------------------------------------------
# Pomocné funkce
# ----------------------------------------------------------------------------
def mat(name, rgb, roughness=0.6, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf is None:
        bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m

MAT = {
    "skin":    mat("skin",    (0.86, 0.68, 0.55), roughness=0.55),
    "shorts":  mat("shorts",  (0.30, 0.25, 0.22), roughness=0.8),
    "tunic":   mat("tunic",   (0.20, 0.36, 0.56), roughness=0.7),
    "pants":   mat("pants",   (0.38, 0.30, 0.20), roughness=0.75),
    "blade":   mat("blade",   (0.72, 0.75, 0.80), roughness=0.22, metallic=1.0),
    "grip":    mat("grip",    (0.30, 0.22, 0.16), roughness=0.7),
    "guard":   mat("guard",   (0.74, 0.55, 0.25), roughness=0.35, metallic=0.8),
}

def _finish(obj, name, layer, material):
    obj.name = name
    obj["layer"] = layer
    if material:
        obj.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return obj

def sphere(name, layer, material, r, loc):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=r, location=loc)
    return _finish(bpy.context.object, name, layer, material)

def cyl(name, layer, material, r, h, loc):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=r, depth=h, location=loc)
    return _finish(bpy.context.object, name, layer, material)

def box(name, layer, material, size, loc):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, name, layer, material)

def bind(obj, armature, bone_name):
    vg = obj.vertex_groups.new(name=bone_name)
    vg.add(list(range(len(obj.data.vertices))), 1.0, 'REPLACE')
    mod = obj.modifiers.new(name="Arm", type='ARMATURE')
    mod.object = armature

# ----------------------------------------------------------------------------
# Postava (primitiva)
# ----------------------------------------------------------------------------
# Hlava / trup (layer body)
sphere("head",      "body", MAT["skin"],   0.125, (0, 0, 1.65))
cyl("neck",         "body", MAT["skin"],   0.05,  0.14, (0, 0, 1.49))
cyl("torso",        "body", MAT["skin"],   0.15,  0.46, (0, 0, 1.19))
sphere("pelvis",    "body", MAT["skin"],   0.14,  (0, 0, 0.97))
cyl("shorts",       "body", MAT["shorts"], 0.17,  0.18, (0, 0, 0.90))

# Končetiny (layer body)
for side, sx in (("L", 0.20), ("R", -0.20)):
    cyl(f"upper_arm.{side}", "body", MAT["skin"], 0.05,  0.30, (sx, 0, 1.26))
    cyl(f"fore_arm.{side}",  "body", MAT["skin"], 0.042, 0.32, (sx, 0, 0.97))
    sphere(f"hand.{side}",   "body", MAT["skin"], 0.05,  (sx, 0, 0.74))

for side, sx in (("L", 0.075), ("R", -0.075)):
    cyl(f"thigh.{side}", "body", MAT["skin"], 0.07,  0.44, (sx, 0, 0.75))
    cyl(f"shin.{side}",  "body", MAT["skin"], 0.055, 0.44, (sx, 0, 0.35))
    box(f"foot.{side}",  "body", MAT["skin"], (0.10, 0.22, 0.07), (sx, 0.11, 0.035))

# Zbroj (trup) – tunika
cyl("tunic", "torso", MAT["tunic"], 0.19, 0.44, (0, 0, 1.17))

# Kalhoty (legs)
for side, sx in (("L", 0.075), ("R", -0.075)):
    cyl(f"pants_thigh.{side}", "legs", MAT["pants"], 0.085, 0.46, (sx, 0, 0.75))
    cyl(f"pants_shin.{side}",  "legs", MAT["pants"], 0.065, 0.46, (sx, 0, 0.35))

# Meč (weapon) – v pravé ruce (x=-0.20), čepel dolů
hx = -0.20
cyl("sword_grip",  "weapon", MAT["grip"],  0.022, 0.14, (hx, 0, 0.74))
box("sword_guard", "weapon", MAT["guard"], (0.16, 0.03, 0.04), (hx, 0, 0.82))
box("sword_blade", "weapon", MAT["blade"], (0.02, 0.055, 0.48), (hx, 0, 0.53))
sphere("sword_pommel", "weapon", MAT["guard"], 0.03, (hx, 0, 0.66))

# ----------------------------------------------------------------------------
# Rig
# ----------------------------------------------------------------------------
arm_data = bpy.data.armatures.new("Rig")
arm = bpy.data.objects.new("Rig", arm_data)
bpy.context.collection.objects.link(arm)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='EDIT')
eb = arm_data.edit_bones

def bone(name, head, tail, parent=None):
    b = eb.new(name)
    b.head = head
    b.tail = tail
    if parent:
        b.parent = parent
    return b

root = bone("root", (0, 0, 0.95), (0, 0, 1.42))
neck = bone("neck", (0, 0, 1.42), (0, 0, 1.56), root)
bone("head", (0, 0, 1.56), (0, 0, 1.74), neck)

for side, sx in (("L", 0.20), ("R", -0.20)):
    ua = bone(f"upper_arm.{side}", (sx, 0, 1.40), (sx, 0, 1.12), root)
    fa = bone(f"fore_arm.{side}",  (sx, 0, 1.12), (sx, 0, 0.82), ua)
    bone(f"hand.{side}",           (sx, 0, 0.82), (sx, 0, 0.74), fa)

for side, sx in (("L", 0.075), ("R", -0.075)):
    th = bone(f"thigh.{side}", (sx, 0, 0.95), (sx, 0, 0.55), root)
    sh = bone(f"shin.{side}",  (sx, 0, 0.55), (sx, 0, 0.15), th)
    bone(f"foot.{side}",       (sx, 0, 0.15), (sx, 0.18, 0.03), sh)

bpy.ops.object.mode_set(mode='OBJECT')

# Svázat meshe s kostmi
BINDING = {
    "head": "head", "neck": "neck", "torso": "root", "pelvis": "root",
    "shorts": "root", "tunic": "root",
    "sword_grip": "hand.R", "sword_guard": "hand.R", "sword_blade": "hand.R",
    "sword_pommel": "hand.R",
}
for side in ("L", "R"):
    BINDING[f"upper_arm.{side}"] = f"upper_arm.{side}"
    BINDING[f"fore_arm.{side}"] = f"fore_arm.{side}"
    BINDING[f"hand.{side}"] = f"hand.{side}"
    BINDING[f"thigh.{side}"] = f"thigh.{side}"
    BINDING[f"shin.{side}"] = f"shin.{side}"
    BINDING[f"foot.{side}"] = f"foot.{side}"
    BINDING[f"pants_thigh.{side}"] = f"thigh.{side}"
    BINDING[f"pants_shin.{side}"] = f"shin.{side}"

for o in list(scene.objects):
    if o.type == 'MESH' and o.name in BINDING:
        bind(o, arm, BINDING[o.name])

bound = [o.name for o in scene.objects if o.type == 'MESH' and o.modifiers.get("Arm")]
print("BOUND_MESHES", len(bound))

# ----------------------------------------------------------------------------
# Kamera (orto, 45°) + světla
# ----------------------------------------------------------------------------
cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
scene.collection.objects.link(cam)
cam_data.type = 'ORTHO'
cam_data.ortho_scale = 2.4
scene.camera = cam
TARGET = Vector((0, 0, 1.0))

def aim_cam(azimuth):
    d = 3.0
    cam.location = (d * math.sin(azimuth), d * math.cos(azimuth), 1.0 + d)
    direction = (TARGET - Vector(cam.location)).normalized()
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

aim_cam(0.0)

def add_sun(name, energy, rot):
    bpy.ops.object.light_add(type='SUN', rotation=rot)
    l = bpy.context.object
    l.name = name
    l.data.energy = energy
    l.data.color = (1.0, 1.0, 1.0)

add_sun("Key",  3.6, (-0.7, 0.0, 0.3))
add_sun("Fill", 1.3, (0.5, 0.0, -2.8))
add_sun("Rim",  1.8, (-1.3, 0.0, -3.0))

# ----------------------------------------------------------------------------
# Chůze (8 framů, 2-kostní IK nohy → kolena se ohýbají)
# ----------------------------------------------------------------------------
FRAMES = 8
THIGH_LEN = 0.40
SHIN_LEN = 0.40
HIP_Z = 0.95
ANKLE_Z = 0.15   # výška kotníku při stoji (konec holeně)
STRIDE = 0.45    # rozsah chodidla vpřed/vzad
LIFT = 0.09      # zdvih chodidla při švihu

def solve_leg(fy, fz, hip_z):
    """2-kostní IK: kyčel v (0,0,hip_z), kotník v (0, fy, fz).
    Vrací (thigh_x, shin_x) – rotace kolem X, kladné = vpřed."""
    down = hip_z - fz
    d = math.hypot(fy, down)
    L1, L2 = THIGH_LEN, SHIN_LEN
    foot_dir = math.atan2(fy, down)                 # úhel od svislice, kladný vpřed
    if d >= L1 + L2 - 1e-6:
        return foot_dir, 0.0                        # rovná noha (bez singularity)
    d = max(abs(L1 - L2) + 1e-6, d)
    cos_knee = (L1 * L1 + L2 * L2 - d * d) / (2 * L1 * L2)
    cos_knee = max(-1.0, min(1.0, cos_knee))
    knee_interior = math.acos(cos_knee)             # π = rovná noha, 0 = skrčená
    # úhel mezi spojnicí kyčel→kotník a stehnem (kosinová věta, kolena vpřed)
    cos_alpha = (d * d + L1 * L1 - L2 * L2) / (2.0 * d * L1)
    cos_alpha = max(-1.0, min(1.0, cos_alpha))
    alpha = math.acos(cos_alpha)
    thigh_x = foot_dir + alpha
    knee_bend = math.pi - knee_interior             # 0 = rovně, >0 = ohnuto
    return thigh_x, -knee_bend

def apply_walk(f):
    pb = arm.pose.bones
    for b in pb:
        b.rotation_mode = 'XYZ'
    t = 2.0 * math.pi * f / FRAMES
    bob = 0.02 * math.cos(2 * t)
    hip_z = HIP_Z + bob
    Aarm = 0.50

    def r(name, x):
        pb[name].rotation_euler = (x, 0.0, 0.0)

    # dráha kotníků: švih (zdvižené) t=0..π, stojná (na zemi) t=π..2π
    fyL = -STRIDE / 2.0 * math.cos(t)
    fzL = ANKLE_Z + LIFT * max(0.0, math.sin(t))
    fyR = -STRIDE / 2.0 * math.cos(t + math.pi)
    fzR = ANKLE_Z + LIFT * max(0.0, math.sin(t + math.pi))

    tl, sl = solve_leg(fyL, fzL, hip_z)
    tr, sr = solve_leg(fyR, fzR, hip_z)
    r("thigh.L", tl)
    r("shin.L", sl)
    r("thigh.R", tr)
    r("shin.R", sr)
    # chodidlo drží směr špičky (dopředu), bez proti-rotace
    r("foot.L", 0.0)
    r("foot.R", 0.0)

    # paže švihají opačně než nohy
    r("upper_arm.L", Aarm * math.cos(t))
    r("upper_arm.R", -Aarm * math.cos(t))
    r("fore_arm.L", 0.25)
    r("fore_arm.R", 0.25)

    # náklon trupu vpřed a lehké pohupování
    pb["root"].rotation_euler = (-0.05, 0.04 * math.sin(t), 0.02 * math.sin(t))
    pb["root"].location = (0, 0, bob)

# ----------------------------------------------------------------------------
# Viditelnost vrstev
# ----------------------------------------------------------------------------
LAYERS = ["body", "torso", "legs", "weapon"]
def set_layer(layer):
    for o in scene.objects:
        if o.type == 'MESH':
            o.hide_render = (o.get("layer") != layer)

# ----------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------
if PREVIEW:
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    set_layer("body")
    apply_walk(0)
    out = os.path.join(HERE, "preview.png")
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    for mn in ("skin", "tunic", "pants"):
        n = bpy.data.materials[mn].node_tree.nodes.get("Principled BSDF")
        if n:
            print("MAT", mn, tuple(round(c, 3) for c in n.inputs["Base Color"].default_value)[:3])
    print("PREVIEW_OK", out)
elif WALKTEST:
    # body, bokorys (d1), 8 framů → strip pro vizuální kontrolu chůze
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    set_layer("body")
    aim_cam(math.pi / 2.0)
    for f in range(FRAMES):
        apply_walk(f)
        out = os.path.join(RAW, f"walktest_f{f}.png")
        scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
    print("WALKTEST_OK", FRAMES, "frames ->", RAW)
else:
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    for layer in LAYERS:
        set_layer(layer)
        for d in range(4):
            aim_cam(d * math.pi / 2.0)
            for f in range(FRAMES):
                apply_walk(f)
                out = os.path.join(RAW, f"{layer}_d{d}_f{f}.png")
                scene.render.filepath = out
                bpy.ops.render.render(write_still=True)
                print("RENDERED", out)

print("DONE")
