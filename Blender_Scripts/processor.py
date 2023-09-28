'''
Author: Manu Gond (ESR11)
Created on: 03-Oct-2022
Objective: Given the files created from blender script, this script puts the images
in correct order of sub-apertures for LF network created for 360 Images. Hence the index goes as follows:-
           Right --> Left (0->7->14->21->28->35->42)
           Top --> Bottom (6->5->4->3->2->1->0)
'''

from operator import sub
import os
from turtle import back
import shutil
from numpy import source


'''
Information about base directory where all scenes are stored.
Target directory and image prefix 
'''
BASE_DIR = "./base_dataset/"
PREFIX_DIR = "/Data/360/"
POSTFIX_DIR = "/7_1_7/"
TARGET_DIR = "./processed_dataset/"
TARGET_IMG_PREFIX = "/LF"
file_lists = os.listdir(BASE_DIR)
print(file_lists)


'''
Define Top Left, Top Right, Bottom Left, Bottom Right indices
which will be used to rearrange the images
'''
GRID_SIZE = 7
TOP_L = GRID_SIZE-1
TOP_R = (GRID_SIZE*GRID_SIZE)-1
BOTTOM_L = 0
BOTTOM_R = (GRID_SIZE*GRID_SIZE)-GRID_SIZE
count = 0

def createSingleSet(fileList,indexList,prefix):
    targetFolder = TARGET_DIR+TARGET_IMG_PREFIX+str(prefix).zfill(3)
    if not os.path.exists(targetFolder):
        os.makedirs(targetFolder)

    for i in range(len(fileList)):
        sourceFile = fileList[i]
        sourceIndex_i = indexList[i][0]
        sourceIndex_j = indexList[i][1]
        targetFile = targetFolder + "/" + "LF"+str(prefix)+"_"+str(sourceIndex_i)+"_"+str(sourceIndex_j)+".png"
        shutil.move(sourceFile, targetFile)

for dir_scene in file_lists:
    dir_scene_poses = os.listdir(BASE_DIR+dir_scene+PREFIX_DIR)
    print("=========================================================")
    print("Status: Moving for scene '"+dir_scene+"'")
    print("_________________________________________________________")
    for scene_poses in dir_scene_poses:
        prefix_dir = "/"+os.listdir(BASE_DIR+dir_scene+PREFIX_DIR+scene_poses)[0]
        sub_aperture_files = BASE_DIR+dir_scene+PREFIX_DIR+scene_poses+prefix_dir+POSTFIX_DIR
        all_files = os.listdir(sub_aperture_files)
        fileList = []
        indexList = []
        idx_ui = 0
        for i in range(TOP_L, BOTTOM_L-1, -1):
            idx_uj = 0
            print_str = ""
            print_str_idx = ""
            idx_j = i
            for j in range(GRID_SIZE):
                print_str = print_str+", "+str(idx_j)
                print_str_idx = print_str_idx+", ("+str(idx_ui)+","+str(idx_uj)+")"
                fileList.append(sub_aperture_files+str(idx_j).zfill(5)+"_000.png")
                indexList.append([idx_ui,idx_uj])

                idx_j = idx_j+GRID_SIZE
                idx_uj += 1
            idx_ui += 1
            #print(print_str+"\t|"+print_str_idx)
        createSingleSet(fileList, indexList, count)
        count += 1
        print("Status: Moving the files "+str(count))