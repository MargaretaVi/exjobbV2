import cv2
import sys

def main(sys):

    # Playing video from file:
    vidcap  = cv2.VideoCapture(sys.argv[1])
    output_path = sys.argv[2]
    ret,image = vidcap.read()
    # image is an array of array of [R,G,B] values

    count = 0;
    while vidcap.isOpened() and count <= 1000:
        success,image = vidcap.read()
        name = "{}/frame{}.jpeg".format(output_path,count)
        cv2.imwrite(name, image)     # save frame as JPEG file

        if cv2.waitKey(10) == 27:                     # exit if Escape is hit
            break

        count += 1


if __name__ == '__main__':
      main(sys)
