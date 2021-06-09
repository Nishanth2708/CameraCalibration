import cv2
import time,glob
import os,sys,argparse


def get_images(folder ='raw_images '):

    video = cv2.VideoCapture(0)
    print("[INFO]: Video Starting........")

    try:

        os.mkdir(folder)

        if os.path.isdir(folder):
            print("[INFO]: Directory Created \n")
        else:
            print("[INFO]: Directory all ready in the Project folder")
            # sys.exit()

    except:

        print("[ERROR]: Dir already exists")
        time.sleep(1)
        print("[INFO]: Remove or Rename Directory and Run again")
        sys.exit()

    try:

        count = 0
        images = []

        while count < 10:

            print("[INFO]: Reading image {:0}".format(count))
            ok, frame = video.read()

            if not ok:
                print("[ERROR]: Could not read the Image")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("image", gray)

            images.append(gray)
            time.sleep(0.5)

            k = cv2.waitKey(1)
            count += 1

            if k == 27:
                break

    except:

        print("[ERROR]: Could not open the Camera or Camera is not working")
        sys.exit()

    i = 0

    for img in images:
        cv2.imwrite(os.path.join('./raw_images/image_{:>02}.jpg'.format(i)), img)
        i += 1

    print("[INFO]: All Images Saved in {} folder \n".format(str(folder)))


    return folder

def SavedImages(folder = 'SavedImages'):


    try:

        os.mkdir(folder)

        if os.path.isdir(folder):
            print("[INFO]: Directory Created \n")
        else:
            print("[INFO]: Directory all ready in the Project folder")
            # sys.exit()

    except:

        print("[ERROR]: Dir already exists")
        time.sleep(1)
        print("[INFO]: Remove or Rename Directory and Run again")
        sys.exit()

    path = get_images()
    print("[INFO]: Loading Images from {} folder".format(str(path)))

    images = glob.glob('raw_images/*.jpg')
    img_counter = 0

    for img in images:

        img = cv2.imread(img)
        cv2.imshow('image',img)
        k = cv2.waitKey(0)

        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

        elif k % 256 == 32:
            # SPACE pressed
            img_name = "saved_frame_{}.png".format(img_counter)
            cv2.imwrite(os.path.join("./SavedImages/""saved_frame_{}.png".format(img_counter)), img)
            print("{} written!".format(img_name))
            img_counter += 1

    return


