"""
photomosaic.py

Creates a photomosaic given a target image and a folder of input images

Author: Mahesh Venkitachalam
"""

import os, random, argparse
from PIL import Image
import numpy as np
from scipy.spatial import KDTree
import timeit

def getAverageRGBOld(image):
  """
  Given PIL Image, return average value of color as (r, g, b)
  """
  # no. of pixels in image
  npixels = image.size[0]*image.size[1]
  # get colors as [(cnt1, (r1, g1, b1)), ...]
  cols = image.getcolors(npixels)
  # get [(c1*r1, c1*g1, c1*g2),...]
  sumRGB = [(x[0]*x[1][0], x[0]*x[1][1], x[0]*x[1][2]) for x in cols] 
  # calculate (sum(ci*ri)/np, sum(ci*gi)/np, sum(ci*bi)/np)
  # the zip gives us [(c1*r1, c2*r2, ..), (c1*g1, c1*g2,...)...]
  avg = tuple([int(sum(x)/npixels) for x in zip(*sumRGB)])
  return avg

def getAverageRGB(image):
  """
  Given PIL Image, return average value of color as (r, g, b)
  """
  # get image as numpy array
  im = np.array(image)
  # get shape
  w,h,d = im.shape
  # get average
  return tuple(np.average(im.reshape(w*h, d), axis=0))

def splitImage(image, size):
  """
  Given Image and dims (rows, cols) returns an m*n list of Images 
  """
  W, H = image.size[0], image.size[1]
  m, n = size
  w, h = int(W/n), int(H/m)
  # image list
  imgs = []
  # generate list of images
  for j in range(m):
    for i in range(n):
      # append cropped image
      imgs.append(image.crop((i*w, j*h, (i+1)*w, (j+1)*h)))
  return imgs

def getImages(imageDir):
  """
  given a directory of images, return a list of Images
  """
  files = os.listdir(imageDir)
  images = []
  for file in files:
    filePath = os.path.abspath(os.path.join(imageDir, file))
    try:
      # explicit load so we don't run into resource crunch
      fp = open(filePath, "rb")
      im = Image.open(fp)
      images.append(im)
      # force loading image data from file
      im.load() 
      # close the file
      fp.close() 
    except:
      # skip
      print("Invalid image: %s" % (filePath,))
  return images

def getBestMatchIndex(input_avg, avgs):
  """
  return index of best Image match based on RGB value distance
  """

  # input image average
  avg = input_avg
  
  # get the closest RGB value to input, based on x/y/z distance
  index = 0
  min_index = 0
  min_dist = float("inf")
  for val in avgs:
    dist = ((val[0] - avg[0])*(val[0] - avg[0]) +
            (val[1] - avg[1])*(val[1] - avg[1]) +
            (val[2] - avg[2])*(val[2] - avg[2]))
    if dist < min_dist:
      min_dist = dist
      min_index = index
    index += 1

  return min_index

def getBestMatchIndicesKDT(qavgs, kdtree):
    """
    return indices of best Image matches based on RGB value distance.
    Uses a k-d tree.
    """
    # eg. [array([2.]), array([9], dtype=int64)]
    res = list(kdtree.query(qavgs, k=1))
    #print("res: ", res)
    min_indices = res[1]
    return min_indices

def createImageGrid(images, dims):
  """
  Given a list of images and a grid size (m, n), create 
  a grid of images. 
  """
  m, n = dims

  # sanity check
  assert m*n == len(images)

  # get max height and width of images
  # ie, not assuming they are all equal
  width = max([img.size[0] for img in images])
  height = max([img.size[1] for img in images])

  # create output image
  grid_img = Image.new('RGB', (n*width, m*height))
  
  # paste images
  for index in range(len(images)):
    row = int(index/n)
    col = index - n*row
    grid_img.paste(images[index], (col*width, row*height))
    
  return grid_img


def createPhotomosaic(target_image, input_images, grid_size,
                      reuse_images, use_kdt):
  """
  Creates photomosaic given target and input images.
  """

  print('splitting input image...')
  # split target image 
  target_images = splitImage(target_image, grid_size)

  print('finding image matches...')
  # for each target image, pick one from input
  output_images = []
  # for user feedback
  count = 0
  batch_size = int(len(target_images)/10)

  # calculate input image averages
  avgs = []
  for img in input_images:
    avgs.append(getAverageRGB(img))

  # compute target averages 
  avgs_target = []
  for img in target_images:
    # target sub-image average
    avgs_target.append(getAverageRGB(img))
  
  # use k-d tree for average match?
  if use_kdt:
    # create k-d tree
    kdtree = KDTree(avgs)
    # query k-d tree
    match_indices = getBestMatchIndicesKDT(avgs_target, kdtree)

    # process matches
    for match_index in match_indices:
        output_images.append(input_images[match_index])
  else:
    # use linear search
    for avg in avgs_target:
        # find match index
        match_index = getBestMatchIndex(avg, avgs)
        output_images.append(input_images[match_index])
        # user feedback
        if count > 0 and batch_size > 10 and count % batch_size == 0:
          print('processed {} of {}...'.format(count, len(target_images)))
        count += 1
        # remove selected image from input if flag set
        if not reuse_images:
          input_images.remove(match)

  print('creating mosaic...')
  # draw mosaic to image
  mosaic_image = createImageGrid(output_images, grid_size)

  # return mosaic
  return mosaic_image

# Gather our code in a main() function
def main():
  # Command line args are in sys.argv[1], sys.argv[2] ..
  # sys.argv[0] is the script name itself and can be ignored

  # parse arguments
  parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
  # add arguments
  parser.add_argument('--target-image', dest='target_image', required=True)
  parser.add_argument('--input-folder', dest='input_folder', required=True)
  parser.add_argument('--grid-size', nargs=2, dest='grid_size', required=True)
  parser.add_argument('--output-file', dest='outfile', required=False)
  parser.add_argument('--kdt', action='store_true', required=False)
  
  args = parser.parse_args()

  # start timing
  start = timeit.default_timer()

  ###### INPUTS ######

  # target image
  target_image = Image.open(args.target_image)

  # input images
  print('reading input folder...')
  input_images = getImages(args.input_folder)

  # check if any valid input images found  
  if input_images == []:
      print('No input images found in %s. Exiting.' % (args.input_folder, ))
      exit()

  # shuffle list - to get a more varied output?
  random.shuffle(input_images)

  # size of grid
  grid_size = (int(args.grid_size[0]), int(args.grid_size[1]))

  # output
  output_filename = 'mosaic.png'
  if args.outfile:
    output_filename = args.outfile
  
  # re-use any image in input
  reuse_images = True

  # resize the input to fit original image size?
  resize_input = True

  # use k-d trees for matching
  use_kdt = False
  if args.kdt:
      use_kdt = True

  ##### END INPUTS #####

  print('starting photomosaic creation...')
  
  # if images can't be reused, ensure m*n <= num_of_images 
  if not reuse_images:
    if grid_size[0]*grid_size[1] > len(input_images):
      print('grid size less than number of images')
      exit()
  
  # resizing input
  if resize_input:
    print('resizing images...')
    # for given grid size, compute max dims w,h of tiles
    dims = (int(target_image.size[0]/grid_size[1]), 
            int(target_image.size[1]/grid_size[0])) 
    print("max tile dims: %s" % (dims,))
    # resize
    for img in input_images:
      img.thumbnail(dims)

  # setup time
  t1 = timeit.default_timer()

  # create photomosaic
  mosaic_image = createPhotomosaic(target_image, input_images, grid_size,
                                   reuse_images, use_kdt)

  # write out mosaic
  mosaic_image.save(output_filename, 'PNG')

  print("saved output to %s" % (output_filename,))
  print('done.')
  
  # creation time
  t2 = timeit.default_timer()

  print('Execution time:    setup: %f seconds' % (t1 - start, ))
  print('Execution time: creation: %f seconds' % (t2 - t1, ))
  print('Execution time:    total: %f seconds' % (t2 - start, ))

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()