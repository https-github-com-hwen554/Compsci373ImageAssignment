Given is a greyscale input image in the form of a pixel array (a list of pixel rows, with each row represented again as a list). Every pixel contains an integer value between 0 and nr_bins-1! For a 3 bit input image, nr_bins is 8.

Write a Python3 function 'computeLookupTableHistEq(pixel_array, image_width, image_height, nr_bins)' which computes the lookup table for histogram equalization of the input image according to the strategy we discussed in the lecture.

Return solely the lookup table as a list datastructure, with the length of the lookup table being equal to the number of bins. The datatype of the lookup table is floating point. You don't have to do any rounding of the result values.



Note: You can assume that a method computeCumulativeHistogram(pixel_array, image_width, image_height, nr_bins) is available for your use, which you can call from within your code (see below).


def computeCumulativeHistogram(pixel_array, image_width, image_height, nr_bins = 256):

    # compute histogram
    histogram = [0.0 for q in range(nr_bins)]
    
    for y in range(image_height):
        for x in range(image_width):
            histogram[pixel_array[y][x]] += 1.0


    # compute cumulative histogram
    cumulative_histogram = [0.0 for q in range(nr_bins)]

    running_sum = 0.0
    for q in range(nr_bins):
        running_sum += histogram[q]
        cumulative_histogram[q] = running_sum

    return cumulative_histogram

For example:

Test	Result
image_width = 6
image_height = 5
pixel_array = [ [6, 3, 2, 6, 4, 7], 
                [5, 3, 2, 7, 0, 6], 
                [6, 2, 7, 7, 1, 7], 
                [7, 6, 6, 2, 7, 3], 
                [2, 2, 2, 5, 1, 2] ]
nr_bins = 8
lookup_table= computeLookupTableHistEq(pixel_array, image_width, image_height, nr_bins)
for q in range(len(lookup_table)):
   print("{}: {}".format(q, round(lookup_table[q], 2)))
0: 0.0
1: 0.48
2: 2.41
3: 3.14
4: 3.38
5: 3.86
6: 5.31
7: 7.0
image_width = 6
image_height = 5
pixel_array = [ [3, 7, 2, 3, 2, 3], 
                [0, 4, 3, 1, 4, 4], 
                [3, 1, 2, 2, 2, 2], 
                [1, 3, 3, 1, 2, 2], 
                [4, 4, 3, 2, 0, 0] ]
nr_bins = 8
lookup_table= computeLookupTableHistEq(pixel_array, image_width, image_height, nr_bins)
for q in range(len(lookup_table)):
   print("{}: {}".format(q, round(lookup_table[q], 2)))
0: 0.0
1: 1.04
2: 3.37
3: 5.44
4: 6.74
5: 6.74
6: 6.74
7: 7.0


**Answer**：
```
image_width = 6
image_height = 6
pixel_array = [ [64, 102, 102, 102, 76, 76],
                [115, 153, 205, 128, 115, 128],
                [102, 153, 205, 179, 153, 128],
                [115, 128, 153, 179, 102, 115],
                [76, 102, 128, 115, 102, 128],
                [89, 102, 76, 89, 76, 76]]
nr_bins = 256
lookup_table= computeLookupTableHistEq(pixel_array, image_width, image_height, nr_bins)
last = 0.0
for i in range(len(lookup_table)):
   if lookup_table[i] > last:
      print(i, round(lookup_table[i],2))
      last = lookup_table[i]
out_array = createInitializedGreyscalePixelArray(image_width, image_height)
for y in range(image_height):
   for x in range(image_width):
      out_array[y][x] = int(round(lookup_table[ pixel_array[y][x] ]))
for i in range(len(out_array)):
   print(out_array[i])
```