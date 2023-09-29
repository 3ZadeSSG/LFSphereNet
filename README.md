# LFSphereNet: Real Time Spherical Light Field Reconstruction from a Single Omnidirectional Image 

This repo contains the dataset scripts and the actual dataset used in paper **"LFSphereNet: Real Time Spherical Light Field Reconstruction from a Single Omnidirectional Image"**

### Dataset Links:-
1. **Spherical Light Field Dataset (~14 GB)** [Download URL will be made available soon]
2. **Real Photographic Light Field Data (~1.18 GB)** [Download URL will be made available soon]


Supplementary Video can be accessed from here: [Video URL]("https://github.com/3ZadeSSG/LFSphereNet/blob/main/assets/LFSphereNet%20_CVMP_Supplemental_Materials.mp4")


## Generating the dataset using the Blender Scripts

The scripts in `Blender_Scripts` can be used to generate Light Field dataset with any X,Y,Z grid size. For example 7x1x7.

### Blender Setup
The following camera properties are used:-
```
Camera Type: Panorma
Projection: Equirectangular
Image Width: 2048px
Image Height: 1024px
```

### Code Setup

Depending on the scene 3 major setup changes are required in code

1. ```SCENE_KEY for example: '_mainScene'```
2. ```CAMERA_NAME for example: 'Camera.001'```
3. ```grid_size = [(X,Y,Z)] for example: to render 7x1x7 put [(7,1,7)]```


### Output Folder Structure:-
The template folder structure with following parameters
```
Grid size: 7x1x7
Image Width: 1024
Sampling: 1000
```
```
Scene_name/
|-Data/
    |-360/
        |-0SceneName/
            |-w1024_s1000_PANO/
                |-7_1_7/
                    |- 00000_000.png
                    |- 00001_000.png
                    .
                    .
                    |-00048_000.png

|-Logs/
    |-360/
        |- 0_logFile.txt
        |- 1_logFile.txt
        .
        .
        |- 14_logFile.txt
```

### How to run?

1. Start blender app, or use terminal ```blender``` to launch it
2. Load the scene
3. Open the script window
4. Select open file and then select the python file which corresponds to that scene
5. Modify `DEFAULT_ROOT, SCENE_NAME, SCENE_KEY, SAMPLING` according to scene which is loaded (if you add your own custom camera or scene key is different from the one which is already in script)
6. Run the script from blender
7. After generating all scenes, use `processor.py` to generate the order of files as used in `Spherical_Light_Field_Dataset`. You will need to copy each folder into a new `base_dataset` folder first.

### Scenes
The scene files can be found on blender's official website under demos section. URL: https://www.blender.org/download/demo-files/
1. Classroom 
2. Lone Monk
3. Barbershop
4. Italian Flat
5. Barcelona

### References
The initial code for the scenes has been taken from the paper [Omni-NeRF: Neural Radiance Field from 360° Image Captures](https://ieeexplore.ieee.org/document/9859817).


If you plan to use the dataset please make sure to cite our paper:-

```
@INPROCEEDINGS{gond2023lfspherenet,
  author={Gond, Manu and Zerman, Emin and Knorr, Sebastian and Sjöström, Mårten},
  booktitle={ACM SIGGRAPH European Conference on Visual Media Production (CVMP)}, 
  title={{LFSphereNet}: Real Time Spherical Light Field Reconstruction from a Single Omnidirectional Image}, 
  year={2023}
  }
```
<p float="center">
    <img src="https://github.com/3ZadeSSG/LFSphereNet/blob/main/assets/miun_logo.png" width="200" />
    <img src="https://github.com/3ZadeSSG/LFSphereNet/blob/main/assets/plenoptima.png" width="200" />
</p>
