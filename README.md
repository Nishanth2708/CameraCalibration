# CameraCalibration

This Repository includes Scripts for Camera Calibration using Zhangs Method where a standard checkerboard is used as a reference.

# Prerequisites

OpenCv, Numpy and glob or an alternative to read images from a directory 

# Motivation

Not all Pinhole Camera Models are accurate, especially when using a lens along with the camera. This always induces the common distortions such as Barrel and Tangential Distortion.
In this regard, the pixels would be curved or distorted on image and will not be squared. This impact, plays a significant role for various application where precision must be robust.

Hence, inorder to correct the distortions that are internal to the camera, I have developed this repository which works for any camera modules as a reference to zhangs method.\

# Steps to Run

1. Clone the repository using ``` git clone https://github.com/Nishanth2708/CameraCalibration.git  ``` 
   
    # Generating Data
2. Run, the script GetImages.py using ```python3 GetImages.py``` and this would  Capture 100 images of checkerboard along different orientations and translations
   
       1. All your images will be saved onto raw_images folder
       2. Once capturing the images are done, all the frames in raw_images folders are displayed one by one
       3. Now choose, 25-30 best frames for calibration based on keypress(space bar) and ignore the ones that are bad
       4. All your saved images will be saved into SavedImages folder

  # Calibration 
3. Calibrate your camera with ```python3 main.py```

       1. This Imports script from Calibration.py
       2. Iterates through the images in SavedImages folder -- Camera
       3. Calibration of Camera starts and generates CameraData in save.yml file

       ## Undistort ## 
       4. Takes first image from, Saved folder and undistort and saves it as "calibrated.png" into it's root directory.
    
    
    
