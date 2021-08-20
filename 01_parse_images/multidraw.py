# Write Python code here
# import the necessary packages
import cv2

def shape_selection(event, x, y, flags, param):
	# grab references to the global variables
	global roi_points, ref_points #, crop

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being performed
	if event == cv2.EVENT_LBUTTONDOWN:
		roi_points = [(x, y)]

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		roi_points.append((x, y))

		# draw a rectangle around the region of interest
		cv2.rectangle(image, roi_points[-2], roi_points[-1], (0, 255, 0), 2)
		cv2.imshow("image", image)

	elif event == cv2.EVENT_RBUTTONDOWN:
		ref_points = [(x, y)]

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_RBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		ref_points.append((x, y))

		ref_points[0] = (ref_points[0][0], roi_points[0][1])
		ref_points[1] = (ref_points[1][0], roi_points[1][1])

		# draw a rectangle around the region of interest
		cv2.rectangle(image, ref_points[-2], ref_points[-1], (0, 0, 255), 2)
		cv2.imshow("image", image)

# now let's initialize the list of reference point
roi_points = []
ref_points = []

src_img = 'demo.jpg'

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(src_img)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", shape_selection)


# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF

	# press 'r' to reset the window
	if key == ord("r"):
		roi_points = []
		image = clone.copy()

	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

	elif key == ord("s"):
		print('wear track points', roi_points)
		print('reference points', ref_points)

		break

# close all open windows
cv2.destroyAllWindows()
def draw_segmentation_areas(img_src):
	pass

# if __name__ == "__main__":
# 	# define image src
# 	img_src = 'demo.jpg'
#
# 	draw_segmentation_areas(img_src)