import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(
                    prog='stitch_by_ref',
                    description='Stitches images together using a reference')

parser.add_argument('image_files', nargs='+', help='files to be cropped')
parser.add_argument('-r', '--reference', help='file whose position must be defined')
parser.add_argument('-v', '--verbose', action='store_true', help='print more stuff')

args = parser.parse_args()


# Load the images
image_1 = cv2.imread(args.image_files[0])
image_2 = cv2.imread(args.image_files[1])
ref    = cv2.imread(args.reference)

method = cv2.TM_SQDIFF_NORMED

# Read the images from the file

result_1 = cv2.matchTemplate(ref, image_1, method)
mn_1,mx_1,mnLoc_1,mxLoc_1 = cv2.minMaxLoc(result_1)
print(mn_1,mx_1,mnLoc_1,mxLoc_1)

result_2 = cv2.matchTemplate(ref, image_2, method)
mn_2,mx_2,mnLoc_2,mxLoc_2 = cv2.minMaxLoc(result_2)
print(mn_2,mx_2,mnLoc_2,mxLoc_2)

x1, y1 = mnLoc_1
x2, y2 = mnLoc_2

print(x1, y1, x2, y2)


# Calculate the size of the output image
height1, width1 = image_1.shape[:2]
height2, width2 = image_2.shape[:2]

top_left_image_1 = (max(0, x2 - x1), max(0, y2 - y1)) # Determine the top-left corner 
top_left_image_2 = (max(0, x1 - x2), max(0, y1 - y2)) # of each image in the resulting canvas

canvas_width = max(top_left_image_1[0] + width1, top_left_image_2[0] + width2)
canvas_height = max(top_left_image_1[1] + height1, top_left_image_2[1] + height2)

# Create a blank canvas
canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

# Place images on the canvas
canvas[top_left_image_1[1]:top_left_image_1[1]+height1, top_left_image_1[0]:top_left_image_1[0]+width1] = image_1
canvas[top_left_image_2[1]:top_left_image_2[1]+height2, top_left_image_2[0]:top_left_image_2[0]+width2] = image_2

cv2.imwrite('stitched_image.png', canvas)
