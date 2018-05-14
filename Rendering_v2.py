import bpy, os, math, mathutils, sys, pdb, re
from PIL import Image
from numpy import random as rand
import xml.etree.cElementTree as ET
from random import *

def pixel_area():
	return bpy.context.scene.render.resolution_x * bpy.context.scene.render.resolution_y


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


def point_camera_to_target(cam, position):
    # we want to point the camera towards the positon(x,y,z), we rotate around the z-axis

    dx = position[0] - cam.location.x
    dy = position[1] - cam.location.y
    dz = position[2] - cam.location.z
    xRad = (math.pi / 2.) + math.atan2(dz, math.sqrt(dy ** 2 + dx ** 2))
    zRad = math.atan2(dy, dx) - (math.pi / 2.)

    cam.rotation_euler = mathutils.Euler((xRad, 0, zRad), 'XYZ')


def rotate_camera_by_angle(camera, radians_angle, obj):
    camera_location_rotation = mathutils.Matrix.Rotation(radians_angle, 4, 'Z')
    camera.location.rotate(camera_location_rotation)
    rand_index = rand.randint(0,2)

    position = ((obj.location.x, obj.location.y, obj.location.z))
    rand_x = rand.randint(-4,4)
    rand_y = rand.randint(-4,4)
    rand_z = rand.randint(-4,4)
    if rand_index == 0:
        # point towards object center
        pass
    elif rand_index == 1:
        position = ((obj.location.x + rand_x, obj.location.y + rand_y, obj.location.z + rand_z))

    point_camera_to_target(camera, position)


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
    bpy.ops.object.lamp_add(type='HEMI', radius=3, view_align=False, location=(meshObjectPos.x, meshObjectPos.y, 10),
                            layers=(
                                True, False, False, False, False, False, False, False, False, False, False, False,
                                False,
                                False, False, False,
                                False, False, False, False))

def reset_camera_location(camera_pos_index, camera_object):
    if camera_pos_index == 1: # Default blender camera position
        camera_object.location = (18.44144, -17.26113, 13.67201)
    elif camera_pos_index == 2:
        camera_object.location = (camera_object.location.x, camera_object.location.y, camera_object.location.z + 5)
    elif camera_pos_index == 3:
        camera_object.location = (camera_object.location.x, camera_object.location.y, camera_object.location.z - 5)
    elif camera_pos_index == 4:
        camera_object.location = (camera_object.location.x, camera_object.location.y, camera_object.location.z - 10)
    else:
        pass


def change_camera_location(camera_pos_index, camera_object):
    if camera_pos_index == 1: # Default blender camera position
        camera_object.location = (18.44144, -17.26113, 13.67201)
    elif camera_pos_index == 2:
        camera_object.location = (camera_object.location.x, camera_object.location.y, camera_object.location.z - 5)
    elif camera_pos_index == 3:
        camera_object.location = (camera_object.location.x, camera_object.location.y, camera_object.location.z + 5)
    elif camera_pos_index == 4:
        camera_object.location = (camera_object.location.x, camera_object.location.y, camera_object.location.z + 10)
    else:
        pass


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


def write_to_xml(saving_image_path, render_res, scene, cam_obj, render_obj):
    xml_filename = saving_image_path[:-5]+ '.xml'
    fname = os.path.basename(saving_image_path)
    folder =  os.path.basename(os.path.dirname(saving_image_path))
    width = render_res[0]
    height = render_res[1]
    #creating the tree
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = folder
    ET.SubElement(annotation, "filename").text = fname
    ET.SubElement(annotation, "path").text = saving_image_path
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    ET.SubElement(annotation, "segmented").text = "0"

    tmp_obj_name, _ = os.path.splitext(bpy.path.basename(bpy.context.blend_data.filepath))
    if render_obj.name.lower() == tmp_obj_name.lower():
        obj_node = ET.SubElement(annotation, "object")
        ET.SubElement(obj_node, "name").text = render_obj.name
        ET.SubElement(obj_node, "pose").text = "Unspecified"

        (xmin, ymin, width, height) = parse_bb_box(str(camera_view_bounds_2d(scene, cam_obj, render_obj)))
        ymax = int(ymin) + int(height)
        xmax = int(xmin) + int(width)
        truncated = check_truncated(xmin, xmax, ymin, ymax, render_res)
        if truncated:
            ET.SubElement(obj_node, "truncated").text = "1"
        else:
            ET.SubElement(obj_node, "truncated").text = "0"
        ET.SubElement(obj_node, "difficult").text = "0"
        bbox =  ET.SubElement(obj_node, "bndbox")


        ET.SubElement(bbox, "xmin").text = xmin
        ET.SubElement(bbox, "ymin").text = ymin
        ET.SubElement(bbox, "xmax").text = str(xmax)
        ET.SubElement(bbox, "ymax").text = str(ymax)
    else:
        print("object name do not match file name, {} ,{}".format(tmp_obj_name, render_obj.name))
        exit(1)
    tree = ET.ElementTree(annotation)
    tree.write(xml_filename)

def check_truncated(xmin, ymin, xmax, ymax, image_resolution):
    width = image_resolution[0]
    height = image_resolution[1]
    truncated = False
    if (int(xmin) <= 1 or int(ymin) <= 1 or int(xmax) >= width or int(ymax) >= height):
        truncated = True
    return truncated

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
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]

    background_folder_path = argv[0]
    background_folder_full_path = os.path.abspath(background_folder_path)
    texture_folder_path = argv[1]
    texture_folder_full_path = os.path.abspath(texture_folder_path)
    saving_folder = argv[2]
    os.makedirs(saving_folder, exist_ok=True)
    blend_file = argv[3]
    blend_file_name = os.path.basename(os.path.splitext(blend_file)[0])

    render_resolution()
    render_res =(bpy.context.scene.render.resolution_x,
        bpy.context.scene.render.resolution_y)

    camera = bpy.data.objects["Camera"]
    camera.rotation_mode = 'XYZ'
    scene = bpy.context.scene

    counter = 0
    degree = 36
    rotate_angle = math.radians(degree)
    number_of_frames = int(360 / degree)
    image_area = pixel_area()

    list_of_texture = os.listdir(texture_folder_full_path)

    object_dictionary = {}
    # Save all mesh object == render object in a dictionary for easy access
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            render_object = obj
            #object_dictionary[obj.name] = obj

    #Setting the background
    for background in os.listdir(background_folder_full_path):
        background_path = os.path.join(background_folder_full_path, background)
        add_background(background_path)
        for index in range(0,3):
            change_camera_location(index, camera)
            for frame in range( 0, number_of_frames):
                delta_x, delta_y, delta_z = change_postion(render_object)
                for texture in list_of_texture:
                    fname = os.path.join(texture_folder_full_path, texture)
                    add_texture_to_object(render_object, fname)
                    scale_factor = 0.1*render_object.scale[0]
                    choice = rand.randint(0,3)
                    change_scale_of_object(render_object, choice, scale_factor, image_area, scene, camera)
                    rotate_camera_by_angle(camera, rotate_angle, render_object)
                    saving_path = os.path.join(saving_folder, ("%s_image_%d.jpeg") % (blend_file_name, counter))
                    counter += 1
                    bpy.context.scene.render.filepath = saving_path
                    bpy.ops.render.render(write_still=True, use_viewport=True)
                    write_to_xml(saving_path,render_res, scene, camera, render_object)
                    reset_scale(render_object,choice, scale_factor)
                reset_pos(render_object, delta_x, delta_y, delta_z)
            reset_camera_location(index, camera)
def reset_pos(obj, delta_x, delta_y, delta_z):
    obj.location.y = obj.location.y - delta_x
    obj.location.x = obj.location.x - delta_y
    obj.location.z = obj.location.z - delta_z

def change_postion(render_object):
    delta_x = randint(-4,4)
    delta_y = randint(-4,4)
    delta_z = randint(-2,2)
    render_object.location.y = render_object.location.y + delta_x
    render_object.location.x = render_object.location.x + delta_y
    render_object.location.z = render_object.location.z + delta_z
    return delta_x, delta_y, delta_z

def add_texture_to_all_objects(object_dict, list_of_texture, texture_folder_full_path):
    for key in object_dict:
        render_object= object_dict[key]
        rand_texture = rand.choice(list_of_texture)



#Add texture to object
def add_texture_to_object(obj,texture_full_path):
    mat = material_for_texture(texture_full_path)
    if len(obj.data.materials) < 1:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat


#Change the scale of object
def change_scale_of_object(obj, index, scale_factor, image_area, scene, cam_obj):
    (_, _, width, height) = parse_bb_box(str(camera_view_bounds_2d(scene, cam_obj, obj)))
    obj_area_rel_to_image = int(width) * int(height)
    ratio = obj_area_rel_to_image / image_area
    print('ratio:{}, obj_area_rel_to_image: {}, image_area: {}'.format(ratio, obj_area_rel_to_image, image_area))
    x_scale = obj.scale[0]
    y_scale = obj.scale[1]
    z_scale = obj.scale[2]
    if index == 0:
        obj.scale[0] = x_scale + 2*scale_factor
        obj.scale[1] = y_scale + 2*scale_factor
        obj.scale[2] = z_scale + 2*scale_factor
    elif index == 1:
        obj.scale[0] = x_scale + 1*scale_factor
        obj.scale[1] = y_scale + 1*scale_factor
        obj.scale[2] = z_scale + 1*scale_factor
    elif index == 2:
        obj.scale[0] = x_scale + 1.5*scale_factor
        obj.scale[1] = y_scale + 1.5*scale_factor
        obj.scale[2] = z_scale + 1.5*scale_factor
    else:
        pass

#Reset scale of object
def reset_scale(obj,index, scale_factor):
    x_scale = obj.scale[0]
    y_scale = obj.scale[1]
    z_scale = obj.scale[2]
    if index == 0:
        obj.scale[0] = x_scale - 2*scale_factor
        obj.scale[1] = y_scale - 2*scale_factor
        obj.scale[2] = z_scale - 2*scale_factor
    elif index == 1:
        obj.scale[0] = x_scale - 1*scale_factor
        obj.scale[1] = y_scale - 1*scale_factor
        obj.scale[2] = z_scale - 1*scale_factor
    elif index == 2:
        obj.scale[0] = x_scale - 1.5*scale_factor
        obj.scale[1] = y_scale - 1.5*scale_factor
        obj.scale[2] = z_scale - 1.5*scale_factor
    else:
        pass


if __name__ == "__main__":
    main(sys)

