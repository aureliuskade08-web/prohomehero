"""Procedural kitchen for the Home Hero finishes designer, rendered with Cycles.
Usage: python3 kitchen.py VIEW COUNTER MODE OUT [W H SAMPLES]
  VIEW    A | B
  COUNTER quartz | granite | slate
  MODE    beauty | mask   (mask: R=cabinets, G=island, B=hardware)
Everything is built from boxes and primitives with procedural materials, no downloaded assets."""
import sys, math, random
import bpy, bmesh
from mathutils import Vector, Euler

VIEW, COUNTER, MODE, OUT = sys.argv[1:5]
W = int(sys.argv[5]) if len(sys.argv) > 5 else 1280
H = int(sys.argv[6]) if len(sys.argv) > 6 else 800
SAMPLES = int(sys.argv[7]) if len(sys.argv) > 7 else 96
random.seed(7)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = SAMPLES if MODE == "beauty" else 8
scene.cycles.use_denoising = MODE == "beauty"
scene.cycles.max_bounces = 6
scene.cycles.diffuse_bounces = 3
scene.cycles.glossy_bounces = 3
scene.cycles.transmission_bounces = 2
scene.cycles.sample_clamp_indirect = 8
scene.render.resolution_x, scene.render.resolution_y = W, H
scene.render.resolution_percentage = 100
scene.render.filter_size = 1.2
if MODE == "beauty":
    scene.view_settings.view_transform = "AgX"
    try: scene.view_settings.look = "AgX - Medium High Contrast"
    except Exception: pass
    scene.view_settings.exposure = -0.45
else:
    scene.view_settings.view_transform = "Standard"
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.filepath = OUT

# ---------------------------------------------------------------- materials
def mat(name, color=(0.8, 0.8, 0.8), rough=0.5, metal=0.0, spec=0.5, emit=None, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bs = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bs.inputs["Base Color"].default_value = (*color, 1)
    bs.inputs["Roughness"].default_value = rough
    bs.inputs["Metallic"].default_value = metal
    for k in ("Specular IOR Level", "Specular"):
        if k in bs.inputs: bs.inputs[k].default_value = spec; break
    if coat:
        for k in ("Coat Weight", "Clearcoat"):
            if k in bs.inputs: bs.inputs[k].default_value = coat; break
    if emit:
        bs.inputs["Emission Color"].default_value = (*emit[0], 1)
        bs.inputs["Emission Strength"].default_value = emit[1]
    nt.links.new(bs.outputs[0], out.inputs[0])
    return m, bs, nt

def nodes(nt):
    return nt.nodes, nt.links

def add_coord(nt, scale=(1, 1, 1), rot=(0, 0, 0)):
    n, l = nodes(nt)
    tc = n.new("ShaderNodeTexCoord")
    mp = n.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = scale
    mp.inputs["Rotation"].default_value = rot
    l.new(tc.outputs["Object"], mp.inputs["Vector"])
    return mp

def ramp(nt, stops, interp="LINEAR"):
    n, _ = nodes(nt)
    r = n.new("ShaderNodeValToRGB")
    r.color_ramp.interpolation = interp
    el = r.color_ramp.elements
    while len(el) > 2: el.remove(el[-1])
    el[0].position, el[0].color = stops[0][0], (*stops[0][1], 1)
    el[1].position, el[1].color = stops[1][0], (*stops[1][1], 1)
    for p, c in stops[2:]:
        e = el.new(p); e.color = (*c, 1)
    return r

# paint, cabinet whites (tinted later by the page), oak floor
M = {}
M["paint"] = mat("paint", (0.93, 0.90, 0.85), 0.92, spec=0.2)[0]
M["white"] = mat("white", (0.92, 0.92, 0.9), 0.5, spec=0.3)[0]
M["cab"] = mat("cab", (0.88, 0.88, 0.87), 0.38, spec=0.45, coat=0.15)[0]
M["island"] = mat("island", (0.88, 0.88, 0.87), 0.38, spec=0.45, coat=0.15)[0]
M["brass"] = mat("brass", (0.83, 0.62, 0.30), 0.22, metal=1.0)[0]
M["steel"] = mat("steel", (0.74, 0.75, 0.77), 0.30, metal=1.0)[0]
M["black"] = mat("black", (0.02, 0.02, 0.022), 0.35, spec=0.5)[0]
M["glass_dark"] = mat("glass_dark", (0.01, 0.01, 0.012), 0.06, spec=0.8)[0]
M["linen"] = mat("linen", (0.80, 0.74, 0.64), 0.95, spec=0.1)[0]
M["ceramic"] = mat("ceramic", (0.94, 0.92, 0.88), 0.18, spec=0.6)[0]
M["lemon"] = mat("lemon", (0.95, 0.78, 0.10), 0.35, spec=0.5)[0]
M["leaf"] = mat("leaf", (0.36, 0.45, 0.36), 0.55)[0]
M["wood_dark"] = mat("wood_dark", (0.42, 0.29, 0.19), 0.45)[0]
M["terracotta"] = mat("terracotta", (0.66, 0.38, 0.27), 0.7)[0]
M["lamp"] = mat("lamp", (1, 0.93, 0.80), 0.3, emit=((1, 0.86, 0.66), 4.5))[0]
M["can"] = mat("can", (1, 0.9, 0.75), 0.3, emit=((1, 0.85, 0.62), 40))[0]
M["sky"] = mat("sky", (1, 1, 1), 1.0)[0]

# sky plane outside windows
m, bs, nt = mat("sky2")
n, l = nodes(nt); n.clear()
out = n.new("ShaderNodeOutputMaterial"); em = n.new("ShaderNodeEmission")
mp = add_coord(nt, (0.28, 0.28, 0.28), (0, math.pi / 2, 0))
gr = n.new("ShaderNodeTexGradient")
l.new(mp.outputs[0], gr.inputs[0])
r = ramp(nt, [(0.0, (0.20, 0.30, 0.14)), (0.35, (0.55, 0.68, 0.45)), (0.5, (0.97, 0.96, 0.94)), (1.0, (0.78, 0.88, 1.0))])
l.new(gr.outputs[0], r.inputs[0]); l.new(r.outputs[0], em.inputs[0]); em.inputs[1].default_value = 5.0
l.new(em.outputs[0], out.inputs[0]); M["sky2"] = m

def gradient_axis(mt, axis_rot):  # helper to rotate gradient
    pass

# oak floor
m, bs, nt = mat("floor", (0.7, 0.55, 0.38), 0.42, spec=0.5)
n, l = nodes(nt)
mp = add_coord(nt, (1, 1, 1))
br = n.new("ShaderNodeTexBrick")
br.offset = 0.5; br.offset_frequency = 2
br.inputs["Scale"].default_value = 1.0; br.inputs["Mortar Size"].default_value = 0.004
br.inputs["Brick Width"].default_value = 1.3; br.inputs["Row Height"].default_value = 0.19
br.inputs["Color1"].default_value = (0.74, 0.58, 0.40, 1); br.inputs["Color2"].default_value = (0.66, 0.50, 0.34, 1)
br.inputs["Mortar"].default_value = (0.30, 0.22, 0.15, 1)
l.new(mp.outputs[0], br.inputs["Vector"])
mp2 = add_coord(nt, (2.2, 55, 2.2))
nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.0; nz.inputs["Detail"].default_value = 6
l.new(mp2.outputs[0], nz.inputs["Vector"])
mix = n.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "OVERLAY"; mix.inputs[0].default_value = 0.45
l.new(br.outputs["Color"], mix.inputs[6]); l.new(nz.outputs["Color"], mix.inputs[7])
l.new(mix.outputs[2], bs.inputs["Base Color"])
bump = n.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.25
l.new(nz.outputs["Fac"], bump.inputs["Height"]); l.new(bump.outputs[0], bs.inputs["Normal"])
M["floor"] = m

# subway tile
m, bs, nt = mat("tile", (0.93, 0.92, 0.90), 0.12, spec=0.6)
n, l = nodes(nt)
mp = add_coord(nt, (1, 1, 1), (math.pi / 2, 0, 0))
br = n.new("ShaderNodeTexBrick")
br.offset = 0.5; br.offset_frequency = 2
br.inputs["Scale"].default_value = 1.0; br.inputs["Mortar Size"].default_value = 0.0035
br.inputs["Brick Width"].default_value = 0.15; br.inputs["Row Height"].default_value = 0.075
br.inputs["Color1"].default_value = (0.95, 0.94, 0.92, 1); br.inputs["Color2"].default_value = (0.91, 0.90, 0.87, 1)
br.inputs["Mortar"].default_value = (0.62, 0.60, 0.56, 1)
l.new(mp.outputs[0], br.inputs["Vector"]); l.new(br.outputs["Color"], bs.inputs["Base Color"])
inv = n.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0
l.new(br.outputs["Fac"], inv.inputs[1])
bump = n.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.6; bump.inputs["Distance"].default_value = 0.004
l.new(br.outputs["Fac"], bump.inputs["Height"]); l.new(bump.outputs[0], bs.inputs["Normal"])
M["tile"] = m

# worktops
def counter_material(kind):
    m, bs, nt = mat("counter_" + kind, (0.9, 0.9, 0.9), 0.14, spec=0.6, coat=0.2)
    n, l = nodes(nt)
    if kind == "quartz":
        mp = add_coord(nt, (0.9, 0.9, 0.9))
        wv = n.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"
        wv.inputs["Scale"].default_value = 1.1; wv.inputs["Distortion"].default_value = 9
        wv.inputs["Detail"].default_value = 4; wv.inputs["Detail Scale"].default_value = 1.4
        l.new(mp.outputs[0], wv.inputs["Vector"])
        r = ramp(nt, [(0.0, (0.93, 0.93, 0.92)), (0.40, (0.93, 0.93, 0.92)), (0.47, (0.50, 0.50, 0.53)), (0.52, (0.93, 0.93, 0.92))])
        l.new(wv.outputs["Fac"], r.inputs["Fac"])
        mp2 = add_coord(nt, (5, 5, 5))
        nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.0; nz.inputs["Detail"].default_value = 8
        l.new(mp2.outputs[0], nz.inputs["Vector"])
        mix = n.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"; mix.inputs[0].default_value = 0.25
        l.new(r.outputs[0], mix.inputs[6]); l.new(nz.outputs["Color"], mix.inputs[7])
        l.new(mix.outputs[2], bs.inputs["Base Color"])
    elif kind == "granite":
        mp = add_coord(nt, (150, 150, 150))
        nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.0; nz.inputs["Detail"].default_value = 1.0; nz.inputs["Roughness"].default_value = 0.8
        l.new(mp.outputs[0], nz.inputs["Vector"])
        r1 = ramp(nt, [(0.0, (0.50, 0.40, 0.30)), (0.34, (0.78, 0.70, 0.56)), (0.52, (0.12, 0.10, 0.085)), (0.60, (0.88, 0.82, 0.72)), (0.80, (0.42, 0.34, 0.26))], "CONSTANT")
        l.new(nz.outputs["Fac"], r1.inputs["Fac"])
        mp2 = add_coord(nt, (3, 3, 3))
        nz2 = n.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value = 1.0; nz2.inputs["Detail"].default_value = 4
        l.new(mp2.outputs[0], nz2.inputs["Vector"])
        mixs = n.new("ShaderNodeMix"); mixs.data_type = "RGBA"; mixs.blend_type = "OVERLAY"; mixs.inputs[0].default_value = 0.35
        l.new(r1.outputs[0], mixs.inputs[6]); l.new(nz2.outputs["Color"], mixs.inputs[7])
        l.new(mixs.outputs[2], bs.inputs["Base Color"])
        bs.inputs["Roughness"].default_value = 0.2
    else:  # slate / soapstone
        mp = add_coord(nt, (1.3, 1.3, 1.3))
        wv = n.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"
        wv.inputs["Scale"].default_value = 1.4; wv.inputs["Distortion"].default_value = 12
        wv.inputs["Detail"].default_value = 3
        l.new(mp.outputs[0], wv.inputs["Vector"])
        r = ramp(nt, [(0.0, (0.055, 0.057, 0.06)), (0.45, (0.055, 0.057, 0.06)), (0.5, (0.20, 0.21, 0.22)), (0.55, (0.055, 0.057, 0.06))])
        l.new(wv.outputs["Fac"], r.inputs["Fac"]); l.new(r.outputs[0], bs.inputs["Base Color"])
        bs.inputs["Roughness"].default_value = 0.34
    return m

# rugs and fabric
m, bs, nt = mat("rug", (0.85, 0.80, 0.72), 0.95, spec=0.1)
n, l = nodes(nt)
mp = add_coord(nt, (1, 1, 1))
wv = n.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Y"
wv.inputs["Scale"].default_value = 9; wv.inputs["Distortion"].default_value = 0
l.new(mp.outputs[0], wv.inputs["Vector"])
r = ramp(nt, [(0.0, (0.84, 0.79, 0.70)), (0.45, (0.84, 0.79, 0.70)), (0.5, (0.55, 0.60, 0.50)), (0.6, (0.55, 0.60, 0.50)), (0.65, (0.84, 0.79, 0.70))], "CONSTANT")
l.new(wv.outputs["Fac"], r.inputs["Fac"]); l.new(r.outputs[0], bs.inputs["Base Color"])
M["rug"] = m

# ---------------------------------------------------------------- geometry helpers
ALL = []
def new_obj(name, me, material, bevel=0.0, smooth=False):
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(material)
    if smooth:
        for p in me.polygons: p.use_smooth = True
    if bevel:
        bm = ob.modifiers.new("bev", "BEVEL"); bm.width = bevel; bm.segments = 2; bm.limit_method = "ANGLE"
    ALL.append(ob)
    return ob

def box(name, x0, x1, y0, y1, z0, z1, material, bevel=0.003):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update()
    return new_obj(name, me, material, bevel)

def cyl(name, cx, cy, z0, z1, r, material, axis="Z", seg=32, r2=None):
    bm = bmesh.new()
    if axis == "Z":
        bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=(r if r2 is None else r2), depth=z1 - z0)
        bmesh.ops.translate(bm, vec=(cx, cy, (z0 + z1) / 2), verts=bm.verts)
    else:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=(r if r2 is None else r2), depth=z1 - z0)
        rot = {"X": Euler((0, math.pi / 2, 0)), "Y": Euler((math.pi / 2, 0, 0))}[axis]
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=rot.to_matrix(), verts=bm.verts)
        # for X/Y axes the 'z0..z1' range is the length centred at (cx, cy, z0)
        mid = (z0 + z1) / 2 if False else 0
        if axis == "X": bmesh.ops.translate(bm, vec=(cx, cy, z0), verts=bm.verts)
        else: bmesh.ops.translate(bm, vec=(cx, cy, z0), verts=bm.verts)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    return new_obj(name, me, material, 0.0, smooth=True)

def sph(name, cx, cy, cz, rx, ry, rz, material, seg=32):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * rx + cx, v.co.y * ry + cy, v.co.z * rz + cz))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    return new_obj(name, me, material, 0.0, smooth=True)

HW = []        # hardware objects (mask B)
CAB = []       # cabinet objects (mask R)
ISL = []       # island objects (mask G)
CTR = []       # counter objects

def shaker(name, x0, x1, z0, z1, yf, material, bucket, frame=0.065, d=0.014):
    t = 0.016
    o = [box(name + "_s", x0, x1, yf - t, yf, z0, z1, material, 0.002)]
    o.append(box(name + "_l", x0, x0 + frame, yf, yf + d, z0, z1, material, 0.0015))
    o.append(box(name + "_r", x1 - frame, x1, yf, yf + d, z0, z1, material, 0.0015))
    o.append(box(name + "_b", x0 + frame, x1 - frame, yf, yf + d, z0, z0 + frame, material, 0.0015))
    o.append(box(name + "_t", x0 + frame, x1 - frame, yf, yf + d, z1 - frame, z1, material, 0.0015))
    bucket.extend(o)

def pull_bar(name, cx, z, yf, length=0.14, vertical=False):
    r = 0.006
    y = yf + 0.034
    if vertical:
        HW.append(cyl(name + "_bar", cx, y, z - length / 2, z + length / 2, r, M["brass"], "Z", 16))
        HW.append(cyl(name + "_p1", cx, yf + 0.016, z + length / 2 - 0.012, z + length / 2 - 0.012 + 0.0001, 0.0001, M["brass"], "Z", 4))
    else:
        o = cyl(name + "_bar", cx, y, 0, 0, r, M["brass"], "X", 16)  # placeholder replaced below
        bpy.data.objects.remove(o)
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=r, radius2=r, depth=length)
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Euler((0, math.pi / 2, 0)).to_matrix(), verts=bm.verts)
        bmesh.ops.translate(bm, vec=(cx, y, z), verts=bm.verts)
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        HW.append(new_obj(name + "_bar", me, M["brass"], 0, True))
        for s in (-1, 1):
            HW.append(box(name + "_post%d" % s, cx + s * (length / 2 - 0.016) - 0.004, cx + s * (length / 2 - 0.016) + 0.004, yf, y, z - 0.004, z + 0.004, M["brass"], 0.001))

def knob(name, cx, z, yf):
    HW.append(cyl(name, cx, yf + 0.015, z, z, 0.014, M["brass"], "Y", 20))
    HW[-1].location = (0, 0, 0)
    # a short cylinder pointing out of the door
    bpy.data.objects.remove(HW.pop())
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.006, radius2=0.006, depth=0.03)
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Euler((math.pi / 2, 0, 0)).to_matrix(), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(cx, yf + 0.016, z), verts=bm.verts)
    me = bpy.data.meshes.new(name + "_stem"); bm.to_mesh(me); bm.free()
    HW.append(new_obj(name + "_stem", me, M["brass"], 0, True))
    HW.append(sph(name + "_head", cx, yf + 0.033, z, 0.016, 0.011, 0.016, M["brass"], 24))

# ---------------------------------------------------------------- the room
CEIL = 2.7
# floor
box("floor", -0.2, 5.6, -0.2, 6.4, -0.03, 0.0, M["floor"], 0)
# ceiling
box("ceiling", -0.2, 5.6, -0.2, 6.4, CEIL, CEIL + 0.05, M["paint"], 0)
# back wall around the window (window x 2.15..3.05, z 1.05..2.15), paint above/around, tile behind the run
y0, y1 = -0.16, 0.0
def wall(x0, x1, z0, z1, m):
    box("wall", x0, x1, y0, y1, z0, z1, m, 0)
wall(-0.2, 5.6, 0.0, 0.94, M["paint"])
wall(-0.2, 0.9, 0.94, CEIL, M["paint"])
wall(4.9, 5.6, 0.94, CEIL, M["paint"])
wall(0.9, 4.9, 2.55, CEIL, M["paint"])
# tiled zone with a window cut-out
def tile(x0, x1, z0, z1):
    box("tile", x0, x1, 0.0, 0.012, z0, z1, M["tile"], 0)
    wall(x0, x1, z0, z1, M["paint"])
tile(0.9, 2.15, 0.94, 2.55); tile(3.05, 4.9, 0.94, 2.55); tile(2.15, 3.05, 0.94, 1.05); tile(2.15, 3.05, 2.15, 2.55)
# window frame + sill + mullions
fr = M["white"]
box("w_sill", 2.07, 3.13, -0.02, 0.12, 1.02, 1.06, fr, 0.003)
box("w_l", 2.15, 2.19, -0.12, 0.0, 1.05, 2.15, fr, 0.002); box("w_r", 3.01, 3.05, -0.12, 0.0, 1.05, 2.15, fr, 0.002)
box("w_t", 2.15, 3.05, -0.12, 0.0, 2.11, 2.15, fr, 0.002)
box("w_mv", 2.59, 2.61, -0.08, -0.03, 1.05, 2.15, fr, 0.001)
box("w_mh", 2.15, 3.05, -0.08, -0.03, 1.58, 1.62, fr, 0.001)
if VIEW == "B":
    box("rwall", 5.6, 5.76, -0.2, 6.4, 0.0, CEIL, M["paint"], 0)
# left wall with a big window
def lwall(y0_, y1_, z0, z1):
    box("lwall", -0.16, 0.0, y0_, y1_, z0, z1, M["paint"], 0)
lwall(-0.2, 6.4, 0.0, 0.8); lwall(-0.2, 6.4, 2.2, CEIL)
lwall(-0.2, 1.4, 0.8, 2.2); lwall(3.4, 6.4, 0.8, 2.2)
box("lw_t", -0.12, 0.0, 1.4, 3.4, 2.16, 2.2, fr, 0.002); box("lw_b", -0.12, 0.0, 1.4, 3.4, 0.8, 0.84, fr, 0.002)
box("lw_a", -0.12, 0.0, 1.4, 1.44, 0.84, 2.16, fr, 0.002); box("lw_c", -0.12, 0.0, 3.36, 3.4, 0.84, 2.16, fr, 0.002)
box("lw_m", -0.08, -0.03, 2.38, 2.42, 0.84, 2.16, fr, 0.001)
box("lw_mh", -0.08, -0.03, 1.44, 3.36, 1.5, 1.54, fr, 0.001)
# sky outside
sky = box("sky_back", -2.0, 7.0, -2.6, -2.55, 0.0, 3.6, M["sky2"], 0)
sky.rotation_euler = (0, 0, 0)
skyL = box("sky_left", -2.6, -2.55, -2.0, 7.0, 0.0, 3.6, M["sky2"], 0)
for ob in (sky, skyL):
    ob.visible_shadow = False

# rug runner between island and range
box("rug", 1.1, 3.9, 0.95, 1.55, 0.0, 0.01, M["rug"], 0)

# ---------------------------------------------------------------- back run
YF = 0.60
# toe kick + carcass
carc = box("carc", 0.9, 4.9, 0.0, 0.575, 0.0, 0.9, M["cab"], 0.002); CAB.append(carc)
# panel-ready fridge (cabinet panels, brass bar pulls) and cabinet above it
shaker("fr_low", 0.10, 0.90, 0.02, 0.60, 0.70, M["cab"], CAB, frame=0.065)
shaker("fr_hi", 0.10, 0.90, 0.605, 1.85, 0.70, M["cab"], CAB, frame=0.065)
box("fr_carc", 0.10, 0.90, 0.0, 0.684, 0.0, 1.85, M["cab"], 0.002); CAB.append(ALL[-1])
pull_bar("frp1", 0.82, 0.90, 0.70, 0.30, True); pull_bar("frp2", 0.82, 1.28, 0.70, 0.30, True)
shaker("fridge_up", 0.10, 0.90, 1.90, 2.55, 0.62, M["cab"], CAB, frame=0.06)
box("fridge_up_c", 0.10, 0.90, 0.0, 0.60, 1.90, 2.55, M["cab"], 0.002); CAB.append(ALL[-1])
knob("frk", 0.84, 1.96, 0.62)
# base modules
shaker("A1", 0.90, 1.50, 0.10, 0.895, YF, M["cab"], CAB); knob("A1k", 1.45, 0.82, YF)
# drawer stack under counter between 3.1 and 3.7 (three drawers)
dz = [(0.10, 0.37), (0.375, 0.64), (0.645, 0.895)]
for i, (a, b) in enumerate(dz):
    shaker("D3_%d" % i, 3.10, 3.70, a, b, YF, M["cab"], CAB, frame=0.05); pull_bar("D3p%d" % i, 3.40, (a + b) / 2, YF, 0.14)
# dishwasher
shaker("DW", 1.50, 2.10, 0.10, 0.895, YF, M["cab"], CAB, frame=0.05); pull_bar("DWp", 1.80, 0.80, YF, 0.30)
# sink base
shaker("S1", 2.10, 2.60, 0.10, 0.895, YF, M["cab"], CAB, frame=0.06); shaker("S2", 2.60, 3.10, 0.10, 0.895, YF, M["cab"], CAB, frame=0.06)
knob("S1k", 2.55, 0.82, YF); knob("S2k", 2.65, 0.82, YF)
# filler
shaker("F1", 4.60, 4.90, 0.10, 0.895, YF, M["cab"], CAB, frame=0.05); pull_bar("F1p", 4.75, 0.78, YF, 0.14, True)
# range
box("range", 3.70, 4.60, 0.0, 0.66, 0.02, 0.92, M["steel"], 0.004)
box("range_door", 3.70, 4.60, 0.66, 0.68, 0.06, 0.74, M["steel"], 0.003)
box("range_win", 3.82, 4.48, 0.68, 0.682, 0.22, 0.62, M["glass_dark"], 0)
box("range_hb", 3.78, 4.52, 0.74, 0.78, 0.776, 0.786, M["brass"], 0.003); HW.append(bpy.data.objects[-1] if False else ALL[-1])
for s in (-1, 1):
    HW.append(box("range_hp%d" % s, 4.15 + s * 0.30 - 0.006, 4.15 + s * 0.30 + 0.006, 0.68, 0.74, 0.778, 0.784, M["brass"], 0.001))
for i in range(5):
    HW.append(cyl("range_kn%d" % i, 3.84 + i * 0.18, 0.69, 0.83, 0.83, 0.017, M["brass"], "Y", 24))
    # replace placeholder zero-length cylinder with a short barrel
    ob = HW.pop(); bpy.data.objects.remove(ob)
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.017, radius2=0.017, depth=0.03)
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Euler((math.pi / 2, 0, 0)).to_matrix(), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(3.84 + i * 0.18, 0.675, 0.83), verts=bm.verts)
    me = bpy.data.meshes.new("kn"); bm.to_mesh(me); bm.free()
    HW.append(new_obj("kn%d" % i, me, M["brass"], 0, True))
box("cooktop", 3.72, 4.58, 0.02, 0.64, 0.92, 0.926, M["glass_dark"], 0.001)
for cx, cy in ((3.97, 0.20), (4.33, 0.20), (3.97, 0.46), (4.33, 0.46)):
    cyl("burner", cx, cy, 0.926, 0.932, 0.075, M["black"], "Z", 32)
    cyl("burner_c", cx, cy, 0.932, 0.940, 0.03, M["steel"], "Z", 24)
for cx, cy in ((3.97, 0.33), (4.33, 0.33)):
    box("grate", cx - 0.15, cx + 0.15, cy - 0.006, cy + 0.006, 0.94, 0.96, M["black"], 0.001)
# hood (plaster, follows cabinet mask) + brass band
def frustum(name, b, t, z0, z1, material, bucket):
    (bx0, bx1, by0, by1), (tx0, tx1, ty0, ty1) = b, t
    v = [(bx0, by0, z0), (bx1, by0, z0), (bx1, by1, z0), (bx0, by1, z0), (tx0, ty0, z1), (tx1, ty0, z1), (tx1, ty1, z1), (tx0, ty1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update()
    for p in me.polygons: p.use_smooth = False
    bucket.append(new_obj(name, me, material, 0.004))
frustum("hood", (3.62, 4.68, 0.0, 0.56), (3.97, 4.33, 0.0, 0.34), 1.50, 1.98, M["cab"], CAB)
box("hood_ch", 3.97, 4.33, 0.0, 0.34, 1.98, CEIL, M["cab"], 0.004); CAB.append(ALL[-1])
HW.append(box("hood_band", 3.60, 4.70, -0.0, 0.58, 1.48, 1.51, M["brass"], 0.003))
# uppers
shaker("U1", 0.90, 1.50, 1.45, 2.30, 0.34, M["cab"], CAB, frame=0.055); knob("U1k", 1.45, 1.52, 0.34)
shaker("U2", 1.50, 2.10, 1.45, 2.30, 0.34, M["cab"], CAB, frame=0.055); knob("U2k", 1.55, 1.52, 0.34)
shaker("U3", 3.10, 3.60, 1.45, 2.30, 0.34, M["cab"], CAB, frame=0.055); knob("U3k", 3.15, 1.52, 0.34)
box("U_carc", 0.90, 2.10, 0.0, 0.325, 1.45, 2.30, M["cab"], 0.002); CAB.append(ALL[-1])
box("U_carc2", 3.10, 3.60, 0.0, 0.325, 1.45, 2.30, M["cab"], 0.002); CAB.append(ALL[-1])
# open shelf above window gap? floating brass-edge shelf at 2.35
box("shelf", 2.15, 3.05, 0.0, 0.18, 2.30, 2.33, M["wood_dark"], 0.003)
# counters (waterfall island + back run), with the sink cut-out built from pieces
M["counter"] = M["white"]
def ctr(name, x0, x1, y0, y1, z0, z1):
    CTR.append(box(name, x0, x1, y0, y1, z0, z1, M["counter"], 0.004))
CT0, CT1 = 0.9, 0.94
ctr("c1", 0.9, 2.3, 0.0, 0.64, CT0, CT1); ctr("c2", 2.3, 2.9, 0.0, 0.10, CT0, CT1); ctr("c3", 2.3, 2.9, 0.50, 0.64, CT0, CT1)
ctr("c4", 2.9, 3.7, 0.0, 0.64, CT0, CT1); ctr("c5", 4.6, 4.9, 0.0, 0.64, CT0, CT1)
# undermount sink basin (inside, steel)
box("sink_f", 2.32, 2.88, 0.12, 0.48, 0.64, 0.66, M["steel"], 0.002)
box("sink_l", 2.30, 2.32, 0.10, 0.50, 0.64, 0.90, M["steel"], 0.002); box("sink_r", 2.88, 2.90, 0.10, 0.50, 0.64, 0.90, M["steel"], 0.002)
box("sink_b", 2.30, 2.90, 0.10, 0.12, 0.64, 0.90, M["steel"], 0.002); box("sink_fr", 2.30, 2.90, 0.48, 0.50, 0.64, 0.90, M["steel"], 0.002)
# faucet: gooseneck, brass
cu = bpy.data.curves.new("faucet", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.011; cu.bevel_resolution = 6
sp = cu.splines.new("NURBS")
pts = [(2.6, 0.07, 0.94), (2.6, 0.07, 1.10), (2.6, 0.07, 1.30), (2.6, 0.12, 1.40), (2.6, 0.24, 1.40), (2.6, 0.31, 1.32), (2.6, 0.31, 1.20)]
sp.points.add(len(pts) - 1)
for p, c in zip(sp.points, pts): p.co = (*c, 1)
sp.order_u = 4; sp.use_endpoint_u = True
fo = bpy.data.objects.new("faucet", cu); bpy.context.collection.objects.link(fo); cu.materials.append(M["brass"]); HW.append(fo); ALL.append(fo)
cyl("f_base", 2.6, 0.07, 0.94, 0.955, 0.03, M["brass"], "Z", 24); HW.append(ALL[-1])
# soap pump + brass dish tray
cyl("pump", 2.2, 0.10, 0.94, 1.02, 0.025, M["ceramic"], "Z", 24)

# ---------------------------------------------------------------- the island (waterfall, panelled, with stools)
IX0, IX1 = 1.25, 3.85
BY0, BY1 = 2.50, 3.20          # cabinet body, panelled on the +y (camera) side
TY0, TY1 = 2.15, 3.23          # top, overhanging toward the range for stools
box("isl_body", IX0 + 0.04, IX1 - 0.04, BY0, BY1 - 0.02, 0.0, 0.9, M["island"], 0.002); ISL.append(ALL[-1])
n_panels = 4
pw = (IX1 - IX0 - 0.08) / n_panels
for i in range(n_panels):
    x0 = IX0 + 0.04 + i * pw + 0.004; x1 = IX0 + 0.04 + (i + 1) * pw - 0.004
    shaker("IB%d" % i, x0, x1, 0.06, 0.895, BY1, M["island"], ISL, frame=0.06)
    pull_bar("IBp%d" % i, (x0 + x1) / 2, 0.80, BY1, 0.14)
# post under the overhang
for sx in (IX0 + 0.10, IX1 - 0.10):
    box("isl_post", sx - 0.04, sx + 0.04, TY0 + 0.08, TY0 + 0.16, 0.0, 0.9, M["island"], 0.002); ISL.append(ALL[-1])
box("isl_toe", IX0 + 0.04, IX1 - 0.04, BY0 - 0.01, BY1 - 0.01, 0.0, 0.06, M["island"], 0.0); ISL.append(ALL[-1])
ctr("i_top", IX0, IX1, TY0, TY1, 0.90, 0.94)
ctr("i_wl", IX0, IX0 + 0.04, TY0, TY1, 0.0, 0.90); ctr("i_wr", IX1 - 0.04, IX1, TY0, TY1, 0.0, 0.90)
# stools tucked under the overhang on the range side
def stool(cx, cy):
    cyl("st_seat", cx, cy, 0.62, 0.68, 0.20, M["linen"], "Z", 40)
    cyl("st_ring", cx, cy, 0.60, 0.62, 0.20, M["wood_dark"], "Z", 40)
    for a_ in range(4):
        ang = math.pi / 4 + a_ * math.pi / 2
        lx, ly = cx + 0.13 * math.cos(ang), cy + 0.13 * math.sin(ang)
        cyl("st_leg", lx, ly, 0.0, 0.60, 0.022, M["wood_dark"], "Z", 12, r2=0.016)
    cyl("st_rail", cx, cy, 0.24, 0.25, 0.14, M["wood_dark"], "Z", 32)
for cx in (1.95, 2.55, 3.15): stool(cx, TY0 - 0.12)

# pendants over the island
for cx in (1.9, 2.55, 3.2):
    cyl("cord", cx, 2.68, 1.70, CEIL, 0.004, M["black"], "Z", 8)
    sph("dome", cx, 2.68, 1.60, 0.17, 0.17, 0.14, M["lamp"], 36)
    cyl("cap", cx, 2.68, 1.72, 1.78, 0.04, M["brass"], "Z", 16); HW.append(ALL[-1])
# recessed cans
for cx in (1.2, 2.5, 3.8):
    for cy in (1.0, 3.0, 4.4):
        cyl("can", cx, cy, CEIL - 0.004, CEIL, 0.07, M["can"], "Z", 24)

# island dressing
sph("bowl", 2.55, 2.72, 0.99, 0.19, 0.19, 0.075, M["ceramic"], 40)
for i, (dx, dy, dz) in enumerate([(-0.05, 0.02, 0.0), (0.06, -0.03, 0.0), (0.0, 0.06, 0.02), (0.02, -0.07, 0.025)]):
    sph("lemon", 2.55 + dx, 2.72 + dy, 1.04 + dz, 0.036, 0.034, 0.034, M["lemon"], 20)
box("board", 1.50, 1.90, 2.55, 2.75, 0.94, 0.96, M["wood_dark"], 0.004)
box("bk1", 3.05, 3.45, 2.60, 2.82, 0.94, 0.965, M["white"], 0.002); box("bk2", 3.07, 3.43, 2.62, 2.80, 0.965, 0.985, M["terracotta"], 0.002)
cyl("vase", 3.25, 2.95, 0.985, 1.12, 0.045, M["ceramic"], "Z", 32, r2=0.03)
for k in range(9):
    a = k * 0.7; length = 0.38 + 0.16 * random.random(); tilt = 0.25 + 0.35 * random.random()
    ex = 3.25 + math.cos(a) * math.sin(tilt) * length * 0.55; ey = 2.95 + math.sin(a) * math.sin(tilt) * length * 0.55
    ez = 1.12 + math.cos(tilt) * length
    cu2 = bpy.data.curves.new("stem", "CURVE"); cu2.dimensions = "3D"; cu2.bevel_depth = 0.0025
    s2 = cu2.splines.new("POLY"); s2.points.add(1)
    s2.points[0].co = (3.25, 2.95, 1.10, 1); s2.points[1].co = (ex, ey, ez, 1)
    so = bpy.data.objects.new("stem", cu2); bpy.context.collection.objects.link(so); cu2.materials.append(M["leaf"]); ALL.append(so)
    for j in range(5):
        t = 0.35 + j * 0.15
        px = 3.25 + (ex - 3.25) * t; py = 2.95 + (ey - 2.95) * t; pz = 1.10 + (ez - 1.10) * t
        sph("leaf", px, py, pz, 0.028, 0.012, 0.018, M["leaf"], 12)
# back counter props: canisters, herb pot, cutting board leaning on the tile
for i, h in enumerate((0.20, 0.16, 0.13)):
    cyl("canister", 4.78 + 0.0, 0.14 + i * 0.0, 0.94, 0.94 + h, 0.0, M["ceramic"], "Z", 4); bpy.data.objects.remove(ALL.pop())
for i, (cx, h) in enumerate(((3.25, 0.21), (3.45, 0.17), (3.62, 0.13))):
    cyl("canister", cx, 0.16, 0.94, 0.94 + h, 0.06 if i == 0 else 0.05, M["ceramic"], "Z", 32)
    cyl("canister_lid", cx, 0.16, 0.94 + h, 0.94 + h + 0.012, 0.062 if i == 0 else 0.052, M["wood_dark"], "Z", 32)
cyl("herb_pot", 2.95, 0.12, 1.06, 1.14, 0.045, M["terracotta"], "Z", 24, r2=0.036)
for k in range(10):
    sph("herb", 2.95 + 0.03 * math.cos(k), 0.12 + 0.03 * math.sin(k), 1.18 + 0.02 * (k % 4), 0.032, 0.032, 0.022, M["leaf"], 12)
box("c_board", 1.05, 1.45, 0.02, 0.05, 0.94, 1.32, M["wood_dark"], 0.004).rotation_euler = (0, 0, 0)
cyl("c_board_h", 1.25, 0.04, 1.32, 1.32, 0, M["wood_dark"], "Z", 4); bpy.data.objects.remove(ALL.pop())
# runner end stool prop: folded towel on the oven handle
box("towel", 4.20, 4.34, 0.785, 0.80, 0.55, 0.78, M["linen"], 0.004)

# ---------------------------------------------------------------- lights and world
bpy.ops.object.light_add(type="SUN"); sun = bpy.context.object
sun.data.energy = 5.0; sun.data.angle = math.radians(1.5); sun.data.color = (1.0, 0.93, 0.82)
d = Vector((1.0, 0.35, -0.55)).normalized(); sun.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
w = bpy.data.worlds.new("w"); scene.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.97, 0.94, 0.90, 1); bg.inputs[1].default_value = 0.45
# soft fill from the open front of the room
bpy.ops.object.light_add(type="AREA"); fill = bpy.context.object
fill.data.size = 4.0; fill.data.size_y = 2.0; fill.data.energy = 160; fill.data.color = (1.0, 0.93, 0.86)
fill.location = (2.6, 6.2, 2.4); fill.rotation_euler = (math.radians(-110), 0, 0)

bpy.ops.object.light_add(type="AREA"); fl = bpy.context.object
fl.data.size = 2.5; fl.data.size_y = 1.6; fl.data.energy = 140; fl.data.color = (1.0, 0.94, 0.88)
fl.location = (2.2, 5.9, 1.9); fl.rotation_euler = (Vector((-2.0, -1.4, -0.4))).to_track_quat("-Z", "Y").to_euler()
# ---------------------------------------------------------------- finish materials: counter, and the mask pass
def _alive(lst):
    out = []
    for o in lst:
        try:
            o.name; out.append(o)
        except ReferenceError:
            pass
    return out
ALL[:] = _alive(ALL); HW[:] = _alive(HW); CAB[:] = _alive(CAB); ISL[:] = _alive(ISL); CTR[:] = _alive(CTR)
CM = counter_material(COUNTER)
M["counter"] = CM
for ob in CTR: ob.data.materials[0] = CM

if MODE == "mask":
    def flat(name, c):
        m = bpy.data.materials.new("mask_" + name); m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
        em.inputs[0].default_value = (*c, 1); em.inputs[1].default_value = 1.0
        nt.links.new(em.outputs[0], out.inputs[0]); return m
    mk = {"cab": flat("r", (1, 0, 0)), "isl": flat("g", (0, 1, 0)), "hw": flat("b", (0, 0, 1)), "none": flat("k", (0, 0, 0))}
    cab_ids = {o.name for o in CAB}; isl_ids = {o.name for o in ISL}; hw_ids = {o.name for o in HW}
    for ob in ALL:
        if ob.name in hw_ids: m_ = mk["hw"]
        elif ob.name in isl_ids: m_ = mk["isl"]
        elif ob.name in cab_ids: m_ = mk["cab"]
        else: m_ = mk["none"]
        ob.data.materials[0] = m_
    # sky and lamps are emissive: keep them black in the mask
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.0
    for L in [o for o in bpy.data.objects if o.type == "LIGHT"]: bpy.data.objects.remove(L)
    scene.cycles.use_denoising = False
    scene.cycles.samples = 24

# ---------------------------------------------------------------- cameras
cam_data = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_data); bpy.context.collection.objects.link(cam)
if VIEW == "A":
    cam.location = (4.55, 5.35, 1.38); target = Vector((2.35, 0.9, 1.05)); cam_data.lens = 24
else:
    cam.location = (0.75, 4.95, 1.30); target = Vector((2.65, 1.5, 0.95)); cam_data.lens = 26
cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
cam_data.sensor_width = 36
scene.camera = cam
bpy.ops.render.render(write_still=True)
