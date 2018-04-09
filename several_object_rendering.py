import bpy, os, math, mathutils, sys, pdb
from PIL import Image
from numpy import random

# camera.location = (7.4811, -6.5076, 5.3437) original camera position in blender
# (2.03913, -1.55791, 1.26075)
def render_resolution():
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512

def add_background(filepath):
    img = bpy.data.images.load(filepath)
    render_resolution()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space_data = area.spaces.active
            background = space_data.background_images.new()
            background.image = img
            space_data.show_background_images = True
            background.view_axis = 'CAMERA'
            break
    texture_name = os.path.splitext(filepath)[0]       
    texture = bpy.data.textures.new(texture_name, 'IMAGE')
    texture.image = img
    bpy.data.worlds['World'].active_texture = texture
    bpy.context.scene.world.texture_slots[0].use_map_horizon = True
    bpy.context.scene.world.use_sky_paper = True


def material_for_texture(fname):
    img = bpy.data.images.load(fname)

    tex = bpy.data.textures.new(fname, 'IMAGE')
    tex.image = img

    mat = bpy.data.materials.new(fname)
    mat.texture_slots.add()
    ts = mat.texture_slots[0]

    ts.texture = tex
    ts.texture_coords = 'ORCO'

    return mat


def point_camera_to_target(cam, object):
    # we want to point the camera towards the object.location(x,y,z), we rotate around the z-axis
    dx = object.location.x - cam.location.x
    dy = object.location.y - cam.location.y
    dz = object.location.z - cam.location.z
    xRad = (math.pi / 2.) + math.atan2(dz, math.sqrt(dy ** 2 + dx ** 2))
    zRad = math.atan2(dy, dx) - (math.pi / 2.)

    cam.rotation_euler = mathutils.Euler((xRad, 0, zRad), 'XYZ')

def rotate_camera_by_angle(camera, radians_angle, object):
    camera_location_rotation = mathutils.Matrix.Rotation(radians_angle, 4, 'Z')
    camera.location.rotate(camera_location_rotation)
    point_camera_to_target(camera, object)

def look_at(cam, point):
    loc_camera = cam.matrix_world.to_translation()

    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()

def delete_and_add_correct_light_source(meshObjectPos):
    # deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # selection % delete
    for obj in bpy.data.objects:
        if obj.type == 'LAMP':
            bpy.data.objects[obj.name].select = True
            bpy.ops.object.delete()

    # Add lamp object, type HEMI
    bpy.ops.object.lamp_add(type='HEMI', radius=1, view_align=False, location=(meshObjectPos.x, meshObjectPos.y, 10),
                            layers=(
                                True, False, False, False, False, False, False, False, False, False, False, False,
                                False,
                                False, False, False,
                                False, False, False, False))

def change_camera_location(camera_pos_index, camera_object, obj):
    if camera_pos_index == 1: # Default blender camera position 
        camera_object.location = (7.4811, -6.5076, 5.3437)
    elif camera_pos_index == 2:
        camera_object.location = (camera_object.location.x, camera_object.location.y, camera_object.location.z - 7)
    elif camera_pos_index == 3:
        camera_object.location = (camera_object.location.x, camera_object.location.y, camera_object.location.z + 7)
    else:
        camera_object.location = (obj.location.x + 5, obj.location.y + 5, 10)

class Box:

    dim_x = 1
    dim_y = 1

    def __init__(self, min_x, min_y, max_x, max_y, dim_x=dim_x, dim_y=dim_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.dim_x = dim_x
        self.dim_y = dim_y

    @property
    def x(self):
        return round(self.min_x * self.dim_x)

    @property
    def y(self):
        return round(self.dim_y - self.max_y * self.dim_y)

    @property
    def width(self):
        return round((self.max_x - self.min_x) * self.dim_x)

    @property
    def height(self):
        return round((self.max_y - self.min_y) * self.dim_y)

    def __str__(self):
        return "<Box, x=%i, y=%i, width=%i, height=%i>" % \
               (self.x, self.y, self.width, self.height)

    def to_tuple(self):
        if self.width == 0 or self.height == 0:
            return (0, 0, 0, 0)
        return (self.x, self.y, self.width, self.height)

def camera_view_bounds_2d(scene, cam_ob, me_ob):
    """
    Returns camera space bounding box of mesh object.

    Negative 'z' value means the point is behind the camera.

    Takes shift-x/y, lens angle and sensor size into account
    as well as perspective/ortho projections.

    :arg scene: Scene to use for frame size.
    :type scene: :class:`bpy.types.Scene`
    :arg obj: Camera object.
    :type obj: :class:`bpy.types.Object`
    :arg me: Untransformed Mesh.
    :type me: :class:`bpy.types.Mesh´
    :return: a Box object (call its to_tuple() method to get x, y, width and height)
    :rtype: :class:`Box`
    """

    mat = cam_ob.matrix_world.normalized().inverted()
    me = me_ob.to_mesh(scene, True, 'PREVIEW')
    me.transform(me_ob.matrix_world)
    me.transform(mat)

    camera = cam_ob.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)
            # Does it make any sense to drop these?
            #if z <= 0.0:
            #    continue
            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    bpy.data.meshes.remove(me)

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    return Box(min_x, min_y, max_x, max_y, dim_x, dim_y)

def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

def write_to_xml(saving_folder, saving_image_path, render_res, scene, cam_obj, obj_list)
    pdb.set_trace()
    fname = os.path.basename(saving_image_path)
    folder = 
    width = render_res.x
    height = render_res.y
    #creating the tree
    annotation = ET.Element("annontation")
    ET.SubElement(annotation, "folder").text = "folder"
    ET.SubElement(annotation, "filename").text = "fname"
    ET.SubElement(annotation, "path").text = "saving_image_path"
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"
    size = ET.SubElement(annotation, "size")
    ET.SubElement(annotation, "segmented").text = "0"
    # loop for each object
    for obj in obj_list:
        obj_node = ET.SubElement(annotation, "object")

        ET.SubElement(obj_node, "name").text = obj.name
        ET.SubElement(obj_node, "pose").text = "Unspecified"
        ET.SubElement(obj_node, "truncated").text = "1"
        ET.SubElement(obj_node, "difficult").text = "0"
        bbox =  ET.SubElement(obj_node, "bndbox")  
        (xmin, ymin, width, height) = parse_bb_box(camera_view_bounds_2d(scene, cam_obj, obj))
        ymax = ymin + height
        xmax = xmin + width
        ET.SubElement(bbox, "xmin").text = xmin
        ET.SubElement(bbox, "ymin").text = ymin
        ET.SubElement(bbox, "xmax").text = xmax
        ET.SubElement(bbox, "ymax").text = ymax
    tree = ET.ElementTree(annotation)  
    sav_path = os.path.join(sav_path, fname)
    sav_path = sav_path + '.xml'
    tree.write(sav_path)  

def parse_bb_box(bbox):
    xmin = get_xmin(bbox)
    width = get_width(bbox)
    ymin = get_ymin(bbox)
    height = get_height(bbox)

    return xmin, ymin, width, height

def get_xmin(line):
    find = re.compile('x=(?=)(\d*)(?<=),')
    xmin = re.search(find, line).group(1)
    return xmin

def get_ymin(line):
    find = re.compile('y=(?=)(\d*)(?<=),')
    ymin = re.search(find, line).group(1)
    return ymin

def get_width(line):
    find = re.compile('width=(?=)(\d*)(?<=),')
    xmax = re.search(find, line).group(1)
    return xmax

def get_height(line):
    find = re.compile('height=(?=)(\d*)(?<=)')
    ymax = re.search(find, line).group(1)
    return ymax


def main(sys):
    print("starting rendering")
    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    render_resolution()
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
  
    background_folder_path = argv[0]
    background_folder_full_path = os.path.abspath(background_folder_path)
    texture_folder_path = argv[1]
    texture_folder_full_path = os.path.abspath(texture_folder_path)
    saving_folder = argv[2]
    os.makedirs(saving_folder, exist_ok=True)
    blend_file = argv[3]
    blend_file_name = os.path.splitext(blend_file)[0]


    camera = bpy.data.objects["Camera"]
    camera.rotation_mode = 'XYZ'

    x = 0
    degree = 150
    rotate_angle = math.radians(degree)
    number_of_frames = int(360 / degree)

    list_of_texture = os.listdir(texture_folder_full_path)

    #Adding texture to all objects
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            delete_and_add_correct_light_source(obj.location)

            rand_texture = random.choice(list_of_texture)
            fname = os.path.join(texture_folder_full_path, rand_texture)
            texture_name = os.path.splitext(rand_texture)[0]
            mat = material_for_texture(fname)
            if len(obj.data.materials) < 1:
                obj.data.materials.append(mat)
            else:
                obj.data.materials[0] = mat
    
    #Setting the background
    for background in os.listdir(background_folder_full_path):
        background_path = os.path.join(background_folder_full_path, background)
        add_background(background_path)
        background_name = os.path.splitext(background)[0]
            
        saving_path = os.path.join(saving_folder, ("%s_%d.jpeg") % (blend_file_name, x))
        x = x +1        

        bpy.context.scene.render.filepath = saving_path
        bpy.ops.render.render(write_still=True, use_viewport=True)

def change_scale_of_object(obj, index):
    x_scale = obj.scale[0]
    y_scale = obj.scale[1]
    z_scale = obj.scale[2]
    
    if index == 1:
        scale_factor = x_scale * 0.4
        obj.scale[0] = x_scale - scale_factor
        obj.scale[1] = y_scale - scale_factor
        obj.scale[2] = z_scale - scale_factor
    else: 
        scale_factor = x_scale * 0.6
        obj.scale[0] = x_scale - scale_factor
        obj.scale[1] = y_scale - scale_factor
        obj.scale[2] = z_scale - scale_factor
      

if __name__ == "__main__":
    main(sys)

"""
 for obj in bpy.data.objects:
        if obj.type == 'MESH':
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            delete_and_add_correct_light_source(obj.location)
            bpy.context.scene.objects.active = obj

           
            for scale_index in range(1,3):
                change_scale_of_object(obj, scale_index)

                for background in os.listdir(background_folder_full_path):

                    background_path = os.path.join(background_folder_full_path, background)
                    add_background(background_path)
                    background_name = os.path.splitext(background)[0]
                
                    for file in os.listdir(texture_folder_full_path):
                        fname = os.path.join(texture_folder_full_path, file)
                        texture_name = os.path.splitext(file)[0]

                        if (texture_name == "white" and background_name != "black") or (background_name == "black" and texture_name != "white"):
                            continue
                        obj = bpy.context.active_object
                        mat = material_for_texture(fname)
                        if len(obj.data.materials) < 1:
                            obj.data.materials.append(mat)
                        else:
                            obj.data.materials[0] = mat
                        for index in range(1, 3):
                            change_camera_location(index, camera, obj)

                            for x in range(1, number_of_frames):
                                rotate_camera_by_angle(camera, rotate_angle, obj)
                                if (texture_name == "white" and background_name == "black"):
                                    saving_path = os.path.join(saving_folder, ("groundTruth/%s/%s%s%sCameraPose%dScale%dFrame%d.jpeg") % (obj.name, obj.name, background_name, texture_name, index, scale_index, x))
                                else:
                                    #saving_path = os.path.join(saving_folder,("%s/%s%s%sCameraPose%dScale%dFrame%d.jpeg") % (obj.name, obj.name, background_name, texture_name, index,scale_index,  x))
                                    saving_path= os.path.join(saving_folder,)                                
"""
