'''
Author: Manu Gond
Created on: 03-Oct-2022
'''
from operator import ge
import bpy
import bpy_extras
from mathutils import Matrix
from mathutils import Vector
import sys
import numpy as np
import os
import argparse
import time
import pathlib
import time
import random

'''
Basic parameters related to scene.
1. SCENE_NAME & CAMERA_NAME will depend names in blender.
2. Increase or decrease SAMPLING based on how noisy image is.
3. XYZ MIN MAX defines the bounds between which any random point for camera
placement will result in usable view.
'''
DEFAULT_ROOT = 'lone_monk'
SCENE_NAME = "monk"
CAMERA_NAME = 'Camera_front'
SCENE_KEY = 'daylight'
SAMPLING = 2000
X_MIN, X_MAX = 13, 26
Y_MIN, Y_MAX = 15, 25
Z_MIN, Z_MAX = 0.5, 2.5

'''
Global Parameters realted to rendering, irrespective of scene
'''
DATA_DIR = "./Data/360/"
LOG_DIR = "./Logs/360/"
WIDTH = 2048
HEIGHT = 1024
offset_val = 0.01  # Displacement interval for camera when capturing each image
grid_val = 7  # Used to calculate max value of coordinate
num_scenes = 30  # Numer of random points where camera grid will be placed in scene
grid_size = [(7, 1, 7)] # Define grid sizes in list, here we are only rendering 7x1x7 grid
logList = []


def render_eva_dataset(base_dir,
                       x_min=0, x_max=1,
                       y_min=0, y_max=1,
                       z_min=0, z_max=1,
                       CAM_type='PANO', start_ind=0, presets=[(3, 1, 3)]):
    '''
    Main Author: Kai Gu (ESR7)
    Modified By: Manu Gond (ESR11)

    Objective: Given Mix, Max XYZ bounds this script renders images defined on grid.

    :param base_dir: directory where scene will be saved
    :param x_min, x_max, y_min, y_max, z_min, z_max: Min and Max value of coordinates in each axis
    :param CAM_type: Default is panormic camera, the types "Equirectangular, Fisheye-Equisolid, Fisheye-Equidistant needs to be
                     selected in Blender, as parameters there will overwrite whatever type is selected here"
    :param start_ind: In case few images were preivously rendered, set the start index to resume from that index.
                       For example: In case of 7x1x7 if 10/49 were already created, then start index = 10
    :param presets: List of grid size.
    :return: None
    '''

    print("Executing: Render Eva Dataset")
    print("Cam Type: ", CAM_type)
    # logList.append("Executing: Render Eva Dataset")
    bpy.data.scenes[0].render.engine = "CYCLES"
    bpy.context.preferences.addons[
        "cycles"
    ].preferences.compute_device_type = "CUDA"  # or "OPENCL"
    bpy.context.scene.cycles.device = "GPU"
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d["use"] = 1  # Using all devices, include GPU and CPU
        sysout(d["name"], d["use"])

    bpy.data.scenes[SCENE_KEY].cycles.samples = SAMPLING
    bpy.data.scenes[SCENE_KEY].render.resolution_x = WIDTH
    bpy.data.scenes[SCENE_KEY].render.resolution_y = HEIGHT

    cam = bpy.data.objects[CAMERA_NAME]
    if CAM_type == 'PANO':
        cam.data.cycles.equirectangular = 12.5
        cam.data.cycles.equirectangular_fov = 360.0 / 180.0 * np.pi
        cam.data.type = CAM_type
    else:
        cam.data.lens = 12.5

    psis = np.array([0, 1 / 2, 1, 3 / 2]) * np.pi
    theta = np.pi / 2
    phi = 0

    if CAM_type == 'PANO':
        psis = psis[::4]

    config_folder = f'w{WIDTH}_s{SAMPLING}_' + CAM_type
    total_digits = 5
    hwf = np.array([WIDTH, HEIGHT, 12.5])
    for preset_i in presets:
        x_step, y_step, z_step = preset_i
        folder_name = f'{x_step}_{y_step}_{z_step}'

        path = os.path.join(base_dir, config_folder, folder_name)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            if os.path.isfile(os.path.join(path, 'pose.npz')):
                sysout(folder_name + ' finished, skipped')
                continue
        x = np.linspace(x_min, x_max, x_step, endpoint=True)
        y = np.linspace(y_min, y_max, y_step, endpoint=True)
        z = np.linspace(z_min, z_max, z_step, endpoint=True)

        meshgrid = np.meshgrid(x, y, z)
        xx, yy, zz = meshgrid
        xx, yy, zz = xx.flatten(), yy.flatten(), zz.flatten()
        img_index = 0
        c2ws = []

        for x, y, z in zip(xx, yy, zz):
            for psi in psis:
                psi_degree = int(psi / np.pi * 180)
                name = f'{img_index:0>{total_digits}}_{psi_degree:0>{3}}'
                pose = render_single_image(name, path, cam, x, y, z, theta, phi, psi, )
                c2ws.append(pose)
            img_index += 1
        np.savez(os.path.join(path, 'pose'), c2ws=np.array(c2ws), hwf=hwf)
    pass


def render_single_image(name, path, cam, x, y, z, theta, phi, psi, pose_only=False, overwrite_exist=False):
    '''
    Objective: Given relevant parameters this function renders a single image
    :param name: Name of image to be rendered
    :param path: Full path where rendered image is strored
    :param cam: Camera object created in parent function
    :param x, y, z: X,Y,Z coordinatese where camera is stored
    :param theta, phi, psi: Rotation angles
    :param pose_only: Just return pose information instead of rendering
    :param overwrite_exist: True if want to overwrite an existing image
    :return: None
    '''
    # print("Executing: Render Single Image")
    str_xyz = "x: " + str(x) + ", y: " + str(y) + ", z: " + str(z) + ", theta: " + str(theta) + ", phi: " + str(
        phi) + ", psi: " + str(psi) + ", time: " + str(time.time()) + ", name: " + name
    # logList.append("Executing: Render Single Image")
    logList.append(str_xyz)
    cam.location = Vector((x, y, z))

    cam.rotation_euler[0] = theta
    cam.rotation_euler[1] = phi
    cam.rotation_euler[2] = psi

    bpy.context.scene.camera = cam

    bpy.context.view_layer.update()

    pose = np.array(cam.matrix_world)
    if pose_only:
        return pose
    file_path = os.path.join(path, name + '.png')
    if os.path.isfile(file_path) and (not overwrite_exist):
        sysout(name, ' rendered, skipped')
        return pose
    bpy.context.scene.render.filepath = os.path.join(path, name + '.png')
    bpy.ops.render.render(write_still=True)

    return pose


def if_file_exist(file_name):
    return os.path.isfile(file_name)


def sysout(*msg):
    print(*msg, file=sys.stderr)


def generateRandom(low, high):
    x = random.uniform(low, high)
    y = '{:.2f}'.format(x)
    return float(y)


if __name__ == '__main__':

    if(not os.path.exists(DATA_DIR)):
        os.makedirs(DATA_DIR)

    if (not os.path.exists(LOG_DIR)):
        os.makedirs(LOG_DIR)

    x_min_list = [13.0, 13.0, 13.0, 13.0, 26.0, 26.0, 26.0, 26.0, 20.0, 20.0,
                  20.0, 20.0, 15.0, 15.0, 15.0, 15.0, 22.0, 22.0, 22.0, 22.0,
                  20.0, 20.0, 22.0, 22.0, 22.0, 22.0, 18.0, 18.0, 18.0, 18.0]

    y_min_list = [15.0, 15.0, 25.0, 25.0, 15.0, 15.0, 25.0, 25.0, 25.0, 25.0,
                  15.0, 15.0, 25.0, 25.0, 15.0, 15.0, 25.0, 25.0, 15.0, 15.0,
                  12.0, 12.0, 15.0, 15.0, 17.0, 17.0, 15.0, 15.0, 17.0, 17.0]

    z_min_list = [1.0,  2.5,  1.0,  2.5,  1.0,  2.5,  1.0,  2.5,  2.5,  1.0,
                  2.5,  1.0,  2.5,  1.0,  2.5,  1.0,  2.5,  1.0,  2.5,  1.0,
                  2.5,  1.5,  1.0,  2.5,  1.0,  2.5,  1.0,  2.5,  1.0,  2.5]

    # x = 13, 26.0
    # y = 15, 25.0
    # z = 1.0, 2.5

    for idx in range(num_scenes):
        #x_min = generateRandom(X_MIN, X_MAX)
        #y_min = generateRandom(Y_MIN, Y_MAX)
        #z_min = generateRandom(Z_MIN, Z_MAX)

        x_min = x_min_list[idx]
        y_min = y_min_list[idx]
        z_min = z_min_list[idx]

        x_max = x_min + (grid_val * offset_val)-offset_val
        y_max = y_min + (grid_val * offset_val)-offset_val
        z_max = z_min + (grid_val * offset_val)-offset_val

        render_eva_dataset(DATA_DIR + str(idx) + SCENE_NAME,
                           x_min, x_max,
                           y_min, y_max,
                           z_min, z_max,
                           CAM_type='PANO',
                           start_ind=0,
                           presets=grid_size)

        with open(LOG_DIR + str(idx) + '_logFile.txt', 'w') as ptr:
            ptr.write('\n'.join(logList))
        logList.clear()
