
'''Todo ----> This Part of Code needs to be tuned by getting
            the depth estimate for N number of points assumed, followed
            by measuring extrnisic parameters wrt the world frame and camera
            coordinate system.
             '''
import numpy as np
from Calibration import load_coefficients
import cv2, os

# global writeValues

writeValues = True

if os.path.isdir('camera_data'):

    def Convert2dtoXYZ (savedir="camera_data/", width = 9, height = 6) :

        '''

            Converting the 2D Image Cooridnates to 3D World Coordinates

        " Using the Multiview Geometry and the application of Perspective Transformation with the following formula

         "    1. ( S*[ U V 1 ].T * inv(NewCamMat) - t ) * inv(R) = [ X Y Z ].T
              2. Scaling Factor S     --->
              3. [U V 1 ]             ---> Image Coordinates
              4. NewCamMat            ---> Intrinisic Matrix of Camera after Undistorting the Image
              5. Rotational Matrix R  ---> Rotational Matrix after the Solving Pnp (Perspective n Point Transformation)
              6. Translation Matrix t ---> Translation Matrix after the Solving Pnp (Perspective n Point Transformation)
              7. [X Y Z ]             ---> Real world coordinates

        '''

        camera_matrix, distortion_matrix = load_coefficients('/save.yml')
        new_camera_matrix =  np.load(savedir+'newcam_mtx.npy')
        roi =  np.load(savedir +'roi.npy')

        # load center points from New Camera matrix
        cx = new_camera_matrix[0, 2]
        cy = new_camera_matrix[1, 2]
        fx = new_camera_matrix[0, 0]
        fy = new_camera_matrix[1, 1]


        print("cx: " + str(cx) + ",cy " + str(cy) + ",fx " + str(fx),",fy " + str(fy))

        total_points = int(width * height)

        image_points = np.load(savedir + 'imagepoints_one.npy')
        print(image_points)

        world_points = np.load(savedir + 'worldpoints_one.npy')
        # print(world_points.shape,world_points)

        worldPoints = np.array([
                                [21.5, 0, 0],
                                [43, 0, 0],
                                [64.5, 0, 0],
                                [21.5*4, 0, 0],
                                [21.5*5, 0, 0],
                                [21.5*6, 0, 0],
                                [21.5*7, 0, 0],
                                [21.5*8, 0, 0],
                               ], dtype=np.float32)
        imgPoints = np.array([[173.71376, 142.48972],

          [215.16212,142.72597],

          [256.37875,143.1675 ],

          [296.69202,143.25449],

          [337.10135,143.55455],

          [377.21487,143.83162],

          [416.9865 ,144.08597],

          [456.19937,144.4007 ],],dtype=np.float32)

        ret, rvec1, tvec1 = cv2.solvePnP(worldPoints,imgPoints,new_camera_matrix,distortion_matrix)

        print("pnp rvec1 - Rotation")
        print(rvec1)
        if writeValues == True: np.save(savedir + 'rvec1.npy', rvec1)

        print("pnp tvec1 - Translation")
        print(tvec1)
        if writeValues == True: np.save(savedir + 'tvec1.npy', tvec1)

        R_mtx, jac = cv2.Rodrigues(rvec1)
        print("R_mtx:",R_mtx)

        Rt = np.column_stack((R_mtx, tvec1))

        P_mtx = new_camera_matrix.dot(Rt)

        s_arr = np.array([0], dtype=np.float32)
        s_describe = np.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=np.float32)

        total_points_used = 1

        test_image_points = np.array([imgPoints[0,0], imgPoints[0,1],1],dtype=np.float32)

        for i in range(0, total_points_used):

            print("=======POINT # " + str(i) + " =========================")

            lefsidemat_1  = np.linalg.inv(R_mtx).dot(np.linalg.inv(new_camera_matrix))
            lefsidemat = lefsidemat_1.dot(test_image_points.T)
            print("leftsidemat:\n",lefsidemat,"leftsidematshape:",lefsidemat.shape)

            rightsidemat = np.linalg.inv(R_mtx).dot(tvec1)
            print("rightsidemat:\n", rightsidemat,"rightsidematshape:",rightsidemat.shape)

            s = 700 + (rightsidemat[2]/lefsidemat[2])

            test = s*(np.linalg.inv(new_camera_matrix))
            sr = test.dot(test_image_points.T)
            world_point = np.linalg.inv(R_mtx).dot(sr)

            print(world_point)



        #     print("Forward: From World Points, Find Image Pixel")
        #     XYZ1 = np.array([[worldPoints[i, 0], worldPoints[i, 1], worldPoints[i, 2], 1]], dtype=np.float32)
        #     XYZ1 = XYZ1.T
        #     print("{{-- XYZ1")
        #     print(XYZ1)
        #     suv1 = P_mtx.dot(XYZ1)
        #     print("//-- suv1")
        #     print(suv1)
        #     s = suv1[2, 0]
        #     uv1 = suv1 / s
        #     print(">==> uv1 - Image Points")
        #     print(uv1)
        #     print(">==> s - Scaling Factor")
        #     print(s)
        #     s_arr = np.array([s / total_points_used + s_arr[0]], dtype=np.float32)
        #     s_describe[i] = s
        #     if writeValues == True: np.save(savedir + 's_arr.npy', s_arr)
        #
        #     print("Solve: From Image Pixels, find World Points")
        #
        #     uv_1 = np.array([[imgPoints[i, 0], imgPoints[i, 1], 1]], dtype=np.float32)
        #     uv_1 = uv_1.T
        #     print(">==> uv1")
        #     print(uv_1)
        #     suv_1 = s * uv_1
        #     print("//-- suv1")
        #     print(suv_1)
        #
        #     print("get camera coordinates, multiply by inverse Camera Matrix, subtract tvec1")
        #     xyz_c = np.linalg.inv(new_camera_matrix).dot(suv_1)
        #     xyz_c = xyz_c - tvec1
        #     print("      xyz_c")
        #     inverse_R_mtx = np.linalg.inv(R_mtx)
        #     XYZ = inverse_R_mtx.dot(xyz_c)
        #     print("{{-- XYZ")
        #     print(XYZ)
        #
        #     # if calculatefromCam == True:
        #     #     cXYZ = cameraXYZ.calculate_XYZ(imagePoints[i, 0], imagePoints[i, 1])
        #     #     print("camXYZ")
        #     #     print(cXYZ)
        #
        # s_mean, s_std = np.mean(s_describe), np.std(s_describe)
        #
        # print(">>>>>>>>>>>>>>>>>>>>> S RESULTS")
        # print("Mean: " + str(s_mean))
        # # print("Average: " + str(s_arr[0]))
        # print("Std: " + str(s_std))
        #
        # print(">>>>>> S Error by Point")
        #
        # for i in range(0, total_points_used):
        #     print("Point " + str(i))
        #     print("S: " + str(s_describe[i]) + " Mean: " + str(s_mean) + " Error: " + str(s_describe[i] - s_mean))


    Convert2dtoXYZ()