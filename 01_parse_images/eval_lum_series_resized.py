import cv2
import os
import numpy as np
import data_handling as dh
import datetime
from time import sleep


def shape_selection(event, x, y, flags, param):
	# grab references to the global variables
	# global roi_points, ref_points, pol_points, poltref_points #, crop
	global roi_points, ref_points, pol_points, poltref_points
	is_polref_computed = False

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being performed
	if event == cv2.EVENT_LBUTTONDOWN:
		roi_points.append((x, y))

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		roi_points.append((x, y))

		# draw a rectangle around the region of interest
		cv2.rectangle(resized, roi_points[-2], roi_points[-1], (0, 255, 0), 2)
		cv2.imshow("image", resized)

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
		cv2.rectangle(resized, ref_points[-2], ref_points[-1], (0, 0, 255), 2)
		cv2.imshow("image", resized)

	elif event == cv2.EVENT_MBUTTONDOWN:
		pol_points = [(x, y)]

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_MBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		pol_points.append((x, y))

		pol_points[0] = (roi_points[0][0], pol_points[0][1])
		pol_points[1] = (roi_points[1][0], pol_points[1][1])

		# draw a rectangle around the region of interest
		cv2.rectangle(resized, pol_points[-2], pol_points[-1], (255, 0, 0), 2)
		cv2.imshow("image", resized)

	elif roi_points and ref_points and pol_points and not is_polref_computed:
		polref_points = []
		polref_points.append((ref_points[0][0], pol_points[0][1]))
		polref_points.append((ref_points[1][0], pol_points[1][1]))
		cv2.rectangle(resized, polref_points[-2], polref_points[-1], (0, 0, 0), 2)
		is_polref_computed = True


def draw_segmentation_areas(src_img, scale_percent = 100):
	# now let's initialize the list of reference point
	# scale_percent = percent of original size

	global image, resized, roi_points, ref_points

	roi_points = []
	ref_points = []

	# load the image, clone it, and setup the mouse callback function
	image = cv2.imread(f'{master_src}/{image_folder}/{data_src}/{src_img}', cv2.IMREAD_UNCHANGED)
	print(type(image))
	# scale image
	print('Original Dimensions : ', image.shape)
	width = int(image.shape[1] * scale_percent / 100)
	height = int(image.shape[0] * scale_percent / 100)
	dim = (width, height)
	resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
	print('Resized Dimensions : ', resized.shape)

	clone_orig = image.copy()
	clone_resized = resized.copy()

	cv2.namedWindow("image")
	cv2.setMouseCallback("image", shape_selection)


	# keep looping until the 'q' key is pressed
	while True:
		# display the image and wait for a keypress
		# cv2.resizeWindow('image', 1500, 500)
		cv2.imshow("image", resized)
		key = cv2.waitKey(1) & 0xFF

		# press 'r' to reset the window
		if key == ord("r"):
			roi_points = []
			resized = clone_resized.copy()

		# if the 'c' key is pressed, break from the loop
		elif key == ord("c"):
			print("script aborted!")
			exit()

		elif key == ord("s"):
			# print('wear track points', roi_points)
			# print('reference points', ref_points)
			#
			# break
			cv2.destroyAllWindows()
			return {
					'roi': roi_points,
					'ref': ref_points,
			}

	# close all open windows
	cv2.destroyAllWindows()
	def draw_segmentation_areas(img_src):
		pass

# def convert_to_gray(src, dst):
# 	"https://imagemagick.org/script/color-management.php"
# 	import os
# 	cmd = f'{src} -set colorspace Gray {dst}'
# 	os.system(cmd)

def crop_image(coordinates, src_img):
	image = cv2.imread(src_img)
	if len(coordinates) == 2:
		crop_img = image.copy()[coordinates[0][1]:coordinates[1][1], coordinates[0][0]:
															coordinates[1][0]]
		# cv2.imshow("crop_img", crop_img)
		# cv2.waitKey(0)
	return crop_img

def write_xts(df, filename, plot = True):
	# col1 = x pos in mm
	# col2 = time in seconds
	# col3 = lum
	# 1 new lines needed for next line

	fn = filename + '_L-roi.xt.dat'
	with open(fn,'w+') as fout:
		for iw in range(len(df['width_pos'])):
			for it in range(len(df['elapsed_time'])):
				fout.write(f"{df['width_pos'][iw]}\t{df['elapsed_time'][it]}\t{df['roi_line'][it][iw]}\n")
			fout.write('\n')

	# plot in Gnuplot
	if plot == True:
		plot_gnuplot(fn)

def plot_gnuplot(fn):
	from shutil import copyfile
	src = 'template.gnp'
	dst = fn[:fn.rfind(".")+1] + 'gnp'
	filename = fn[fn.rfind("/")+1:fn.rfind(".xt")]

	copyfile(src, dst)
	with open(dst,'a') as f:
		f.write(f"set output '{filename}.3d.png'\n")
		f.write(f"splot '{filename}.xt.dat' u 1:2:3 w pm3d\n")
		f.write(f"set view map\n")
		f.write(f"set output '{filename}.map.png'\n")
		f.write("unset zlabel\n")
		f.write("set xtics offset 0,0\n")
		f.write("set ytics offset 0,0\n")
		f.write("set yrange [0:20.0]\n")
		f.write("set ylabel 't / h' offset -2,0 font 'Times-New-Roman, 24'\n")
		f.write("replot\n")
	wd = os.getcwd()
	os.chdir(fn[:fn.rfind("/")+1])
	os.system(f'gnuplot {fn[fn.rfind("/")+1:fn.rfind(".")] + ".gnp"}')
	os.chdir(wd)



def write_data_files(df, filename):
	with open(f'{filename}_singles.txt','w+') as fout:
		fout.write('L-roi_single [1]\tL-ref_single [1]\troi_single_rel [%]\n')
		for i in range(len(lum_data['roi_single'])):
			fout.write(f"{lum_data['roi_single'][i]}\t{lum_data['ref_single'][i]}\t{lum_data['roi_single_rel'][i]}\n")
	with open(f'{filename}_lines.txt', 'w+') as fout:
		for j in range(len(lum_data['roi_line'])):
			fout.write(f"{lum_data['roi_line'][i]}\n")

def plot_py(data, filename = 'unnamed'):
	import matplotlib.pyplot as plt
	x = np.linspace(0,20,len(data['roi_single']))

	plt.figure()
	plt.plot(x, data['roi_single'])
	plt.plot(x, data['ref_single'])
	plt.savefig(filename + '_L-roi_L-ref.jpg')

	plt.figure()
	plt.plot(x, data['roi_single_rel'])
	plt.ylabel('Relative Luminance [%]')
	plt.xlabel('sliding duration [h]')
	plt.savefig(filename + '_L-rel.jpg')


if __name__ == "__main__":
	# define image src
	first_image = True	# If True, selection window is opened
	scale_percent = 70
	# master_src = r"W:\11_Technologie\11.8_eval_lum_series\data"
	master_src = r"C:\Users\jim\Documents\Python_projects\jbc_tools\data"
	# data_src = '00546214'
	data_src = '00548671'
	# data_src = 'test'
	filename = data_src
	image_folder = 'image_data'
	test_folder = 'wear_test_ids'
	set_folder = 'wear_test_set_ids'


	img_srcs = dh.get_list_of_filenames(src = f'{master_src}/{image_folder}/{data_src}', ext = 'jpg')
	check_id = int(len(img_srcs)*0.7)
	# print(img_srcs)
	roi_width = 4 	# wear track width in mm
	roi_width_step = False
	duration_total = 20
	duration_step = False
	# duration = 20	# test duration

	lum_data = {
		'roi_line': 	[],
		'roi_single':	[],
		'ref_single':	[],
	}
	for i in range(0, len(img_srcs), 50):
		img_src = img_srcs[i]
		print(f'Processing ({i+1}/{len(img_srcs)}) {img_src}...')
		if first_image == True:
			coords = draw_segmentation_areas(img_srcs[check_id], scale_percent = scale_percent)
			first_image = False
			time_first = datetime.datetime.now()

			# correct coordinates to orignal image
			print("uncorrected coords", coords)
			scale = scale_percent / 100
			coords['roi'] = [(int(coords['roi'][0][0] / scale), int(coords['roi'][0][1] / scale)),\
							(int(coords['roi'][1][0] / scale), int(coords['roi'][1][1] / scale))]
			coords['ref'] = [(int(coords['ref'][0][0] / scale), int(coords['ref'][0][1] / scale)),\
							(int(coords['ref'][1][0] / scale), int(coords['ref'][1][1] / scale))]
			print("corrected coords", coords)

		# crop images
		img_roi_crop = crop_image(coords['roi'], f'{master_src}/{image_folder}/{data_src}/{img_src}')
		img_ref_crop = crop_image(coords['ref'], f'{master_src}/{image_folder}/{data_src}/{img_src}')

		# convert images to grayscale
		img_roi_crop_gray = cv2.cvtColor(img_roi_crop, cv2.COLOR_BGR2GRAY)
		img_ref_crop_gray = cv2.cvtColor(img_ref_crop, cv2.COLOR_BGR2GRAY)

		# compute average line and single point data
		img_roi_crop_gray_avg_line = img_roi_crop_gray.mean(axis = 0) # get column average of roi
		img_roi_crop_gray_avg_single = img_roi_crop_gray.mean()  # get average roi of the whole matrix
		img_ref_crop_gray_avg_single = img_ref_crop_gray.mean()  # get average ref of the whole matrix

		# save to lum_data variable
		lum_data['roi_line'].append(img_roi_crop_gray_avg_line)
		lum_data['roi_single'].append(img_roi_crop_gray_avg_single)
		lum_data['ref_single'].append(img_ref_crop_gray_avg_single)
		lum_data['roi_single_rel'] = (np.divide(lum_data['roi_single'], lum_data['ref_single']) - 1) * 100

	# generate time and roi width data
	if duration_step == False:
		duration_step = True
		lum_data['elapsed_time'] = np.linspace(0, duration_total, len(lum_data['roi_single']))
	if roi_width_step == False:
		roi_width_step = roi_width/ len(lum_data['roi_line'][0])
		print('ROI WIDTH STEP',roi_width_step)
		lum_data['width_pos'] = np.linspace(0, roi_width, len(lum_data['roi_line'][0]))

	## saving procedures


	# print(f'{master_src}/{test_folder}/{data_src}')

	# if not os.path.exists(f'{master_src}/{test_folder}/{data_src}'):
	# 	os.mkdir(f'{master_src}/{test_folder}/{data_src}')
	# 	print("Directory ", f'{master_src}/{test_folder}/{data_src}', " Created ")
	# else:
	# 	print("Directory ", f'{master_src}/{test_folder}/{data_src}', " already exists")

	# save files
	# write_data_files(lum_data, filename=f'{master_src}/{test_folder}/{data_src}/{filename}')

	# write xt files
	# write_xts(lum_data, filename=f'{master_src}/{test_folder}/{data_src}/{filename}')

	# plot_py(lum_data, filename=f'{master_src}/{test_folder}/{data_src}/{filename}')
	plot_py(lum_data, filename=f'test.jpg')
	print('Time needed:', (datetime.datetime.now()-time_first).total_seconds(), 's')