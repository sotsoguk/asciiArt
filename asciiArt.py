import sys, random, argparse
import numpy as np
import math
from PIL import Image


# setup grayscale codes

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# 10 levels of gray
gscale2 = '@%#*+=-:. '

def computeMeanValue(image):
	#convert image to np array
	im = np.array(image)
	w,h = im.shape
	# reshape into vector (w*h,1) matrix and compute mean value
	return np.average(im.reshape(w*h))

def convertImToAscii(fileName, cols, scale, moreShades, invert):

	global gscale1, gscale1
	# load image to grayscale
	image = Image.open(fileName).convert('L')
	# Image dimensions
	W, H = image.size[0], image.size[1]
	# compute size of subtiles
	w = W / cols
	h = w / scale
	# number of rows in ouput image
	rows = int(H/h)
	print "input image:  %d x %d " %(W,H)
	print "output image: %d x %d " %(cols,rows)

	# check if image is too small
	if cols > W or rows > H:
		print("Image 2 small!")
		exit(0)
	# init string for image
	asciiImg = []
	# compute list of tile dimensions
	for j in range(rows):
		y1 = int( j * h )
		y2 = int( (j+1) * h )
		#correct last tile
		if j == rows - 1:
			y2 = H
		#append empty string
		asciiImg.append("")
		for i in range(cols):
			#crop image to fit tile
			x1 = int(i*w)
			x2 = int( (i+1) * w)
			#correct last tile again
			if i == cols - 1:
				x2 = W
			# extract tile
			img = image.crop( (x1,y1, x2,y2))
			# compute avg brightness of tile
			avg = computeMeanValue(img)
			if invert:
				avg = 255- avg
			# lookup ASCII Value
			if moreShades:
				gsval = gscale1[int( (avg*69)/255) ]
			else:
				gsval = gscale2[int( (avg*9)/255) ]
			# "add" ascii Pixel
			asciiImg[j] += gsval

	return asciiImg


def main():
	# parse arguments

	parser = argparse.ArgumentParser(description='asciiArt Generator')
	parser.add_argument('--file', dest='imgFile',required=True)
	parser.add_argument('--out', dest='outFile',required=False)
	parser.add_argument('--cols', dest='cols',required=False)
	parser.add_argument('--scale',dest='scale',required=False)
	parser.add_argument('--ms', dest='moreShades', action='store_true')
	parser.add_argument('--inv',dest='invert',action='store_true')

	args = parser.parse_args()
	# eval arguments
	outFile = 'out.txt'
	if args.outFile:
		outFile = args.outFile

	scale =0.43
	if args.scale:
		scale = float(args.scale)

	cols = 80
	if args.cols:
		cols = int(args.cols)
	outImg = convertImToAscii(args.imgFile,cols,scale,args.moreShades,args.invert)

	# write output
	f = open(outFile,'w')
	for row in outImg:
		f.write(row+ '\n')
	f.close()

	print "Haha, work is done!"


if __name__ == '__main__':
	main()