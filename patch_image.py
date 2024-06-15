import cv2
import argparse

parser = argparse.ArgumentParser(description='Patch an image with another image at specified coordinates.')
parser.add_argument('image2', help='Path to the image to be patched')
parser.add_argument('-r', '--reference', help='file whose position must be defined')

args = parser.parse_args()


image_2 = cv2.imread(args.image2)
ref     = cv2.imread(args.reference)

method = cv2.TM_SQDIFF_NORMED

result_2 = cv2.matchTemplate(ref, image_2, method)
mn_2,mx_2,mnLoc_2,mxLoc_2 = cv2.minMaxLoc(result_2)
x2, y2 = mnLoc_2

# Get the dimensions of the images
height1, width1 = ref.shape[:2]
height2, width2 = image_2.shape[:2]

# Calculate the region in image2 where image1 will be placed
start_x = x2
start_y = y2
end_x = x2 + width1
end_y = y2 + height1

# Ensure the region is within the bounds of image2
if end_x > width2:  end_x = width2
if end_y > height2: end_y = height2

# Calculate the dimensions of the overlapping area
overlap_width = end_x - start_x
overlap_height = end_y - start_y


patch = ref[0:overlap_height, 0:overlap_width] # Extract the overlapping region from image1
image_2[start_y:end_y, start_x:end_x] = patch  # Place the patch in the corresponding region of image2

cv2.imwrite('patched_image.jpg', image_2)
