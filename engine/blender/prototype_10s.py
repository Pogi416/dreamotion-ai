"""Render a self-contained 10-second procedural 3D motion-graphics scene."""
import os
import math
import bpy
from mathutils import Vector

OUT = os.path.abspath(os.environ.get("OUTPUT_DIR", "output"))
TOPIC = os.environ.get("STUDIO_TOPIC", "DREAMOTION AI")
os.makedirs(OUT, exist_ok=True)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
try:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    scene.render.engine = "BLENDER_EEVEE"
if hasattr(scene, "eevee"):
    scene.eevee.taa_render_samples = 24
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 240
scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
scene.render.filepath = os.path.join(OUT, "dreamotion_3d_silent.mp4")
scene.world.color = (0.012, 0.016, 0.035)
scene.view_settings.view_transform = "AgX"

def mat(name, color, metallic=0.0, roughness=0.35, emission=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = (*color, 1)
    bs.inputs["Metallic"].default_value = metallic
    bs.inputs["Roughness"].default_value = roughness
    if emission:
        bs.inputs["Emission Color"].default_value = (*color, 1)
        bs.inputs["Emission Strength"].default_value = emission
    return m

midnight = mat("Midnight enamel", (0.018, 0.035, 0.09), 0.72, 0.22)
cyan = mat("Electric cyan", (0.015, 0.62, 0.95), 0.45, 0.2, 1.4)
violet = mat("Ultraviolet", (0.28, 0.08, 0.8), 0.4, 0.24, 0.8)
white = mat("Porcelain", (0.82, 0.9, 1.0), 0.12, 0.28, 0.18)
dark = mat("Backdrop", (0.006, 0.01, 0.026), 0.1, 0.7)

bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -1.65))
bpy.context.object.name = "Infinite dark stage"
bpy.context.object.data.materials.append(dark)

bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.18, location=(0, 0, 0))
orb = bpy.context.object
for p in orb.data.polygons: p.use_smooth = True
orb.name = "Core luminous sphere"
orb.data.materials.append(midnight)
orb.rotation_euler = (0.25, 0.15, 0)
orb.keyframe_insert(data_path="rotation_euler", frame=1)
orb.rotation_euler.z = math.tau
orb.keyframe_insert(data_path="rotation_euler", frame=240)

for idx, (radius, tilt, material) in enumerate(((1.72, 0.45, cyan), (2.0, -0.62, violet), (2.28, 0.95, white))):
    bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=0.018 if idx != 2 else 0.01, major_segments=128, minor_segments=12)
    ring = bpy.context.object
    for p in ring.data.polygons: p.use_smooth = True
    ring.name = f"Orbital ring {idx+1}"
    ring.rotation_euler = (tilt, 0.2 * idx, 0)
    ring.data.materials.append(material)
    ring.keyframe_insert(data_path="rotation_euler", frame=1)
    ring.rotation_euler.z = math.tau
    ring.keyframe_insert(data_path="rotation_euler", frame=240)

for i in range(9):
    a = math.tau * i / 9
    radius = 2.5 + (i % 3) * 0.22
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.075 + (i % 3)*0.025, location=(radius*math.cos(a), radius*math.sin(a), 0.18*math.sin(2*a)))
    sat = bpy.context.object
    for p in sat.data.polygons: p.use_smooth = True
    sat.name = f"Satellite {i+1:02d}"
    sat.data.materials.append(cyan if i % 2 == 0 else violet)
    sat.keyframe_insert(data_path="location", frame=1)
    sat.location.x = radius*math.cos(a + 1.2)
    sat.location.y = radius*math.sin(a + 1.2)
    sat.keyframe_insert(data_path="location", frame=240)

def add_text(body, name, size, location, material):
    curve = bpy.data.curves.new(name, "FONT")
    curve.body = body
    curve.size = size
    curve.align_x = "CENTER"
    curve.extrude = 0.002
    obj = bpy.data.objects.new(name, curve)
    scene.collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(material)
    obj.rotation_euler = (math.radians(72), 0, 0)
    return obj

headline = add_text(TOPIC[:42].upper(), "Topic title", 0.56, (0, -0.02, 2.05), white)
headline.keyframe_insert(data_path="scale", frame=1)
headline.scale = (1.04, 1.04, 1.04)
headline.keyframe_insert(data_path="scale", frame=240)
add_text("A PROCEDURAL 3D MOTION STUDY", "Subtitle", 0.18, (0, -0.04, 1.52), cyan)

bpy.ops.object.camera_add(location=(7.2, -10.5, 6.1))
cam = bpy.context.object
cam.name = "Cinematic camera"
scene.camera = cam
target = Vector((0, 0, 0.2))
cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
cam.data.lens = 48
cam.keyframe_insert(data_path="location", frame=1)
cam.location = (6.3, -9.0, 5.1)
cam.keyframe_insert(data_path="location", frame=240)
cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()

def area_light(name, loc, energy, color, size):
    bpy.ops.object.light_add(type="AREA", location=loc)
    light = bpy.context.object
    light.name = name
    light.data.energy = energy
    light.data.color = color
    light.data.shape = "DISK"
    light.data.size = size
    light.rotation_euler = (Vector((0,0,0)) - light.location).to_track_quat("-Z","Y").to_euler()

area_light("Cool key", (2, -4, 6), 1250, (0.25, 0.65, 1.0), 5)
area_light("Violet rim", (-4, 2, 3), 1600, (0.38, 0.12, 1.0), 4)
area_light("Soft fill", (4, 3, 1), 700, (0.2, 0.8, 1.0), 3)

scene.use_nodes = True
nodes = scene.node_tree.nodes
nodes.clear()
rl = nodes.new("CompositorNodeRLayers")
glare = nodes.new("CompositorNodeGlare")
glare.glare_type = "FOG_GLOW"
glare.quality = "MEDIUM"
glare.threshold = 1.2
composite = nodes.new("CompositorNodeComposite")
scene.node_tree.links.new(rl.outputs["Image"], glare.inputs["Image"])
scene.node_tree.links.new(glare.outputs["Image"], composite.inputs["Image"])

for obj in scene.objects:
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for key in fc.keyframe_points:
                key.interpolation = "BEZIER"

scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "dreamotion_3d_prototype.blend"))
bpy.ops.render.render(animation=True)
print("RENDER_COMPLETE", scene.render.filepath)
