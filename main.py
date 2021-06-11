import glob
from Calibration import *
from GetImages import SaveImages
from PerspectiveCalibration import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Camera calibration')


    # parser.add_argument('--image_dir', type=str, required=True, help='image directory path')
    # parser.add_argument('--image_format', type=str, required=True,  help='image format, png/jpg')
    # parser.add_argument('--prefix', type=str, required=True, help='image prefix')


    # parser.add_argument('--square_size', type=float, required=False, help='chessboard square size')
    # parser.add_argument('--width', type=int, required=False, help='chessboard width size, default is 9')


    # parser.add_argument('--height', type=int, required=False, help='chessboard height size, default is 6')
    # parser.add_argument('--save_file', type=str, required=True, help='YML file to save calibration matrices')

    #SavedImages()
    ret, mtx, dist, rvecs, tvecs, imgpoints, objpoints = calibrate(width=9, height=6)
    print("Calibration is finished. RMS: ", ret)


    new_camera_matrix, roi = undistort('save.yml')
    save_coefficients(mtx, dist,'save.yml')

    print("Calibration is finished. RMS: ", ret)

    for img in glob.glob('./calibrated.png'):
        TextonImage(img)


    # Convert2dtoXYZ()
   #
   #  # image = str(image)

