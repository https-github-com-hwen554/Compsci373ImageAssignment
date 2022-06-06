import math
import sys
from pathlib import Path
import time # used to display program's runtime
from matplotlib import pyplot
from matplotlib.patches import Rectangle

# import our basic, light-weight png reader library
# this is our module that performs the reading of a png image
import imageIO.png

# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
# a useful shortcut method to create a list of lists based array representation for an image, initialized with a value

# Creates a two dimensional array representing an image as a very simple (not very efficient) list of lists
# datastructure.
# The outer list is covering all the image rows. Each row is an inner list covering the columns of the image.
def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_pixel_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_pixel_array
def computeStandardDeviationImage5x5RepeatBorder(pixel_array, image_width, image_height):
    new = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(image_height):
        for x in range(image_width):
            ret = 0
            catch_list = []
            for m in range(-2,3):
                for n in range(-2,3):
                    catch_list.append(pixel_array[max(min(y+n,image_height-1),0)][max(min(x+m,image_width-1),0)])
            average = sum(catch_list)/len(catch_list)
            for i in catch_list:
                ret+=(i-average)**2
            new[y][x] = math.sqrt(ret/len(catch_list))
    return new
def computeThresholdGE(pixel_array, threshold_value, image_width, image_height):
    new_im = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            if pixel_array[i][j]<threshold_value:
                new_im[i][j] = 0
            else:
                new_im[i][j] = 255
    return new_im
"""
FROM CODERUNNER - SCALING THE GREYSCALE ARRAY TO 0-255 RANGE
"""
def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):
    #min_val, max_val = computeMinAndMaxValues(pixel_array, image_width, image_height)
    new = createInitializedGreyscalePixelArray(image_width, image_height)
    minim = pixel_array[0][0]
    maxim = pixel_array[0][0]

    for i in pixel_array:
        for j in i:
            if j>maxim:
                maxim=j
            if j<minim:
                minim = j
    original_range = maxim - minim
    if original_range ==0:
        original_range +=1
    for i in range(image_height):
        for j in range(image_width):
            new[i][j]=round(255*(pixel_array[i][j]-minim)/original_range)
    return new
def computeHistogram(pixel_array, image_width, image_height, nr_bins):
    seen = []
    for x in range(nr_bins):
        seen.append(0)
    for i in pixel_array:
        for j in i:
            seen[j]+=1
    return seen
def computeAdaptiveThreshold(pixel_array,image_width,image_height,iterations=10):
    current_iter = 0
    theta = 0
    index = 0
    histogram = computeHistogram(pixel_array,image_width,image_height,256)
    for i in histogram:
        theta += i*index
        index+=1
    theta /= sum(histogram)
    while current_iter<iterations:
        theta_bg = 0
        theta_ob = 0
        theta_bg_count = 0
        theta_ob_count = 0
        index = 0
        for i in histogram:
            if index<theta:
                theta_bg+=i*index
                theta_bg_count+=i
            else:
                theta_ob+=i*index
                theta_ob_count+=i
            index += 1
        theta_bg /= max(theta_bg_count,1)
        theta_ob /= max(theta_ob_count,1)
        theta = (theta_bg+theta_ob)/2
        current_iter+=1
    return theta+85
"""
FROM CODERUNNER - EROSION
"""
def computeErosion8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    new = createInitializedGreyscalePixelArray(image_width, image_height)
    ct_list = []
    for y in range(image_height):
        for x in range(image_width):
            for m in range(-1, 2):
                for n in range(-1, 2):
                    if (x + m < 0) or (x + m >= image_width) or (y + n < 0) or (y + n >= image_height):
                        ct_list.append(0)
                    else:
                        ct_list.append(pixel_array[y + n][x + m])
            ct_list.sort()
            new[y][x] = min(1, ct_list[0])
            ct_list = []
    return new

"""
FROM CODERUNNER - DILATION
"""
def computeDilation8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    new = createInitializedGreyscalePixelArray(image_width, image_height)
    ct_list = []
    for y in range(image_height):
        for x in range(image_width):
            for m in range(-1,2):
                for n in range(-1,2):
                    if (x+m<0) or (x+m>=image_width) or (y+n<0) or (y+n>=image_height):
                        ct_list.append(0)
                    else:
                        ct_list.append(pixel_array[y+n][x+m])
            ct_list.sort()
            new[y][x] = min(1,ct_list[-1])
            ct_list = []
    return new

"""
FROM CODERUNNER - CONNECTED COMPONENT ANALYSIS
"""
def computeConnectedComponentLabeling(pixel_array, image_width, image_height):
    # keep track of pixels that have been visited
    visited = [[0 for x in range(image_width)] for y in range(image_height)]
    # keep track of labels per pixel -- shows the different components later
    labels = [[0 for x in range(image_width)] for y in range(image_height)]
    # keep track of the number of components and their pixel counts
    num_pixel_counts = {}
    current_label = 1

    for i in range(image_height):
        for j in range(image_width):

            # if pixel not visited AND NOT a background pixel
            if pixel_array[i][j] > 0 and visited[i][j] == 0:
                q = Queue()
                num_pixel_counts[current_label] = 0
                q.enqueue([i, j])
                visited[i][j] = 1  # mark as visited

                while bool(q.isEmpty()) == False:  # while queue isn't empty
                    new_pixel = q.dequeue()  # new_pixel == [row,col], RETURNS INDICES OF THE DEQUEUED PIXEL
                    # get the indices of the dequeued pixel
                    row = new_pixel[0]
                    col = new_pixel[1]
                    labels[row][col] = current_label  # assign current pixel with label
                    num_pixel_counts[current_label] += 1  # increment because dequeued pixel has been labelled

                    # get the neighbours of the current dequeued pixel
                    left = pixel_array[row][col - 1]
                    right = pixel_array[row][col + 1]
                    top = pixel_array[row - 1][col]
                    bottom = pixel_array[row + 1][col]

                    # ASSIGN LABELS TO NEIGHBOURS THAT haven't BEEN VISITED

                    # LEFT NEIGHBOUR
                    if (row < image_height) and ((col - 1) < image_width) and (left > 0 and visited[row][col - 1] == 0):
                        q.enqueue([row, col - 1])
                        visited[row][col - 1] = 1
                        labels[row][col - 1] = current_label

                    # RIGHT NEIGHBOUR
                    if (row < image_height) and ((col + 1) < image_width) and (
                            right > 0 and visited[row][col + 1] == 0):
                        q.enqueue([row, col + 1])
                        visited[row][col + 1] = 1
                        labels[row][col + 1] = current_label

                    # TOP NEIGHBOUR
                    if ((row - 1) < image_height) and (col < image_width) and (top > 0 and visited[row - 1][col] == 0):
                        q.enqueue([row - 1, col])
                        visited[row - 1][col] = 1
                        labels[row - 1][col] = current_label

                    # BOTTOM NEIGHBOUR
                    if ((row + 1) < image_height) and (col < image_width) and (
                            bottom > 0 and visited[row + 1][col] == 0):
                        q.enqueue([row + 1, col])
                        visited[row + 1][col] = 1
                        labels[row + 1][col] = current_label
                current_label += 1
            else:
                continue

    return labels, num_pixel_counts
# returns the pixel array and their connected components, as well as a dictionary displaying number of pixels per component
"""
FROM CODERUNNER - CONVERTING INTO GREYSCALE PIXEL ARRAY
"""
def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)

    # STUDENT CODE HERE
    for i in range(image_height):
        for j in range(image_width):
            greyscale_pixel_array[i][j] = round(
                0.299 * pixel_array_r[i][j] + 0.587 * pixel_array_g[i][j] + 0.114 * pixel_array_b[i][j])

    return greyscale_pixel_array












def setTheBoundry(connect_array,image_width,image_height,connect_dictionary):
    max_connect = 1
    print(connect_dictionary)
    for i in connect_dictionary.keys():
        if connect_dictionary.get(i)>connect_dictionary.get(max_connect):
            max_connect = i
    minX = image_width
    minY = image_height
    maxX = 0
    maxY = 0
    for y in range(image_height):
        for x in range(image_width):
            if (connect_array[y][x]==max_connect):
                minX = min(x,minX)
                minY = min(y,minY)
                maxX = max(x,maxX)
                maxY = max(y,maxY)
    return minX,maxX,minY,maxY
# This is our code skeleton that performs the license plate detection.
# Feel free to try it on your own images of cars, but keep in mind that with our algorithm developed in this lecture,
# we won't detect arbitrary or difficult to detect license plates!
def main():

    total_time = time.time()
    start_time = time.time()
    command_line_arguments = sys.argv[1:]

    SHOW_DEBUG_FIGURES = True

    # this is the default input image filename
    input_filename = "numberplate1.png"

    if command_line_arguments != []:
        input_filename = command_line_arguments[0]
        SHOW_DEBUG_FIGURES = False

    output_path = Path("output_images")
    if not output_path.exists():
        # create output directory
        output_path.mkdir(parents=True, exist_ok=True)

    output_filename = output_path / Path(input_filename.replace(".png", "_output.png"))
    if len(command_line_arguments) == 2:
        output_filename = Path(command_line_arguments[1])


    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(input_filename)
    print("readRGBImageToSeparatePixelArrays: %s seconds" % (time.time() - start_time))
    # setup the plots for intermediate results in a figure
    fig1, axs1 = pyplot.subplots(2, 2)
    axs1[0, 0].set_title('Input red channel of image')
    axs1[0, 0].imshow(px_array_r, cmap='gray')
    axs1[0, 1].set_title('Input green channel of image')
    axs1[0, 1].imshow(px_array_g, cmap='gray')
    axs1[1, 0].set_title('Input blue channel of image')
    axs1[1, 0].imshow(px_array_b, cmap='gray')


    # STUDENT IMPLEMENTATION here
    # first we have to convert the red, green and blue pixel arrays to a greyscale representation.
    start_time = time.time()
    px_array = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    print("computeRGBToGreyscale: %s seconds" % (time.time() - start_time))

    start_time = time.time()
    px_array = computeStandardDeviationImage5x5RepeatBorder(px_array, image_width, image_height)
    print("computeStandardDeviationImage5x5RepeatBorder: %s seconds" % (time.time() - start_time))

    start_time = time.time()
    px_array = scaleTo0And255AndQuantize(px_array, image_width, image_height)
    print("scaleTo0And255AndQuantize: %s seconds" % (time.time() - start_time))

    start_time = time.time()
    threshold = computeAdaptiveThreshold(px_array,image_width,image_height,50)
    px_array = computeThresholdGE(px_array, threshold, image_width, image_height)
    print("computeThresholdGE: %s seconds" % (time.time() - start_time))

    start_time = time.time()
    px_array = computeDilation8Nbh3x3FlatSE(px_array, image_width, image_height)
    #px_array = computeDilation8Nbh3x3FlatSE(px_array, image_width, image_height)
    #px_array = computeDilation8Nbh3x3FlatSE(px_array, image_width, image_height)
    px_array = computeErosion8Nbh3x3FlatSE(px_array, image_width, image_height)
    #px_array = computeErosion8Nbh3x3FlatSE(px_array, image_width, image_height)
    #px_array = computeErosion8Nbh3x3FlatSE(px_array, image_width, image_height)
    print("computeDilation8Nbh3x3FlatSE/computeErosion8Nbh3x3FlatSE: %s seconds" % (time.time() - start_time))

    start_time = time.time()
    #(px_array, cd) = computeConnectedComponentLabeling(px_array, image_width, image_height)
    #px_array = scaleTo0And255AndQuantize(px_array, image_width, image_height)
    (connect_array,cd) = computeConnectedComponentLabeling(px_array, image_width, image_height)
    # compute a dummy bounding box centered in the middle of the input image, and with as size of half of width and height
    center_x = image_width / 2.0
    center_y = image_height / 2.0
    #bbox_min_x = center_x - image_width / 4.0
    #bbox_max_x = center_x + image_width / 4.0
    #bbox_min_y = center_y - image_height / 4.0
    #bbox_max_y = center_y + image_height / 4.0
    (bbox_min_x,bbox_max_x,bbox_min_y,bbox_max_y)=setTheBoundry(connect_array,image_width,image_height,cd)
    print("computeConnectedComponentLabeling/setTheBoundry: %s seconds" % (time.time() - start_time))




    # Draw a bounding box as a rectangle into the input image
    axs1[1, 1].set_title('Final image of detection')
    axs1[1, 1].imshow(px_array, cmap='gray')
    rect = Rectangle((bbox_min_x, bbox_min_y), bbox_max_x - bbox_min_x, bbox_max_y - bbox_min_y, linewidth=1,
                     edgecolor='g', facecolor='none')
    axs1[1, 1].add_patch(rect)



    # write the output image into output_filename, using the matplotlib savefig method
    extent = axs1[1, 1].get_window_extent().transformed(fig1.dpi_scale_trans.inverted())
    pyplot.savefig(output_filename, bbox_inches=extent, dpi=600)

    if SHOW_DEBUG_FIGURES:
        # plot the current figure
        pyplot.show()
        print("Total_time: %s seconds" % (time.time() - total_time))

if __name__ == "__main__":
    main()