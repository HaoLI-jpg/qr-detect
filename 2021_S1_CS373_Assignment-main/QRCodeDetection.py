import math

from matplotlib import pyplot
from matplotlib.patches import Rectangle

import imageIO.png

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

def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array


def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)

    for i in range(image_height):
        for n in range(image_width):
            greyscale_pixel_array[i][n] = round(
                pixel_array_r[i][n] * 0.299 + pixel_array_g[i][n] * 0.587 + pixel_array_b[i][n] * 0.114)

    return greyscale_pixel_array

def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):

    # new pixel_array
    new = createInitializedGreyscalePixelArray(image_width, image_height)
    # get minimum and maximum values
    min, max = computeMinAndMaxValues(pixel_array, image_width, image_height)

    if max == min:
        return new

    # iterate over pixel_array
    for i in range(len(pixel_array)):
        for j in range(len(pixel_array[0])):
            new[i][j] = round((pixel_array[i][j]-min)/(max-min)*255)
    return new

def computeMinAndMaxValues(pixel_array, image_width, image_height):
    minimum = pixel_array[0][0]
    maximum = minimum
    # iterate over each pixel row
    for row in pixel_array:
        if min(row) < minimum:
            minimum = min(row)
        if max(row) > maximum:
            maximum = max(row)
    return (minimum, maximum)

def computeVerticalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    result = 0
    new_array = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(image_height):
        for x in range(image_width):
            new_array[y][x] = 0
    for y in range(1,image_height - 1):
        for x in range(1,image_width - 1):
            result += -pixel_array[y - 1][x - 1] - 2 * pixel_array[y][x - 1] - pixel_array[y + 1][x - 1] +\
                      pixel_array[y - 1][x + 1] + 2*pixel_array[y][x + 1] + pixel_array[y + 1][x + 1]
            new_array[y][x] += result/8
            result = 0
    return new_array

def computeHorizontalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    result = 0.0
    new_array = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(image_height):
        for x in range(image_width):
            new_array[y][x] = 0.0
    for y in range(1,image_height - 1):
        for x in range(1,image_width - 1):
            result += pixel_array[y - 1][x - 1] + 2* pixel_array[y - 1][x] + pixel_array[y - 1][x + 1] - pixel_array[y + 1][x - 1] - 2*pixel_array[y + 1][x] - pixel_array[y + 1][x + 1]
            new_array[y][x] += result/8
            result = 0
    return new_array

def gradient(h,v, image_width, image_height):
    new = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(image_height):
        for x in range(image_width):
            new[y][x] = math.sqrt(h[y][x] ** 2 + v[y][x] ** 2)
    return new
# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def computeBoxAveraging3x3(pixel_array, image_width, image_height):
    result = 0.0
    new_array = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(image_height):
        for x in range(image_width):
            new_array[y][x] = 0.0
    for y in range(1,image_height - 1):
        for x in range(1,image_width - 1):
            result = pixel_array[y - 1][x - 1] + pixel_array[y][x - 1] + pixel_array[y + 1][x - 1] + pixel_array[y - 1][x + 1]+\
                        pixel_array[y][x + 1]+ pixel_array[y + 1][x + 1] + pixel_array[y + 1][x] + pixel_array[y][x]+ pixel_array[y - 1][x]
            new_array[y][x] += result/9
            result = 0
    return new_array

def computeThresholdGE(pixel_array, threshold_value, image_width, image_height):
    new = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(image_height):
        for x in range(image_width):
            if pixel_array[y][x] < threshold_value :
                new[y][x] = 0
            else:
                new[y][x] = 255
    return new


def computeErosion8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    result = 0
    max = 0
    new = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(image_height):
        for x in range(image_width):
            if pixel_array[y][x] > max:
                max = pixel_array[y][x]
    for y in range(image_height):
        for x in range(image_width):
            if y == 0 or y == image_height - 1:
                new[y][x] = 0
            elif x == 0 or x == image_width - 1:
                new[y][x] = 0
            else:
                result += pixel_array[y - 1][x - 1] + pixel_array[y - 1][x] + pixel_array[y - 1][x + 1] + \
                          pixel_array[y][x - 1] + pixel_array[y][x] + pixel_array[y][x + 1] + \
                          pixel_array[y + 1][x - 1] + pixel_array[y + 1][x] + pixel_array[y + 1][x + 1]
                if result == 9 * max:
                    new[y][x] = 1

            result = 0
    return new

def computeDilation8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    new = createInitializedGreyscalePixelArray(image_width, image_height)
    for y in range(image_height):
        for x in range(image_width):
            if pixel_array[y][x] != 0:

                if x == 0:
                    if y == 0:
                        new[y][x] = 1
                        new[y][x + 1] = 1
                        new[y + 1][x] = 1
                        new[y + 1][x + 1] = 1
                    elif y == image_height - 1:
                        new[y][x] = 1
                        new[y][x + 1] = 1
                        new[y - 1][x] = 1
                        new[y - 1][x + 1] = 1
                    else:
                        new[y - 1][x] = 1
                        new[y][x] = 1
                        new[y + 1][x] = 1
                        new[y - 1][x + 1] = 1
                        new[y][x + 1] = 1
                        new[y + 1][x + 1] = 1
                elif x == image_width - 1:
                    if y == 0:
                        new[y][x] = 1
                        new[y + 1][x] = 1
                        new[y][x - 1] = 1
                        new[y + 1][x - 1] = 1
                    elif y == image_height - 1:
                        new[y][x] = 1
                        new[y - 1][x] = 1
                        new[y][x - 1] = 1
                        new[y - 1][x - 1] = 1
                    else:
                        new[y - 1][x] = 1
                        new[y][x] = 1
                        new[y + 1][x] = 1
                        new[y - 1][x - 1] = 1
                        new[y][x - 1] = 1
                        new[y + 1][x - 1] = 1
                else:
                    if y == 0:
                        new[y][x - 1] = 1
                        new[y][x] = 1
                        new[y][x + 1] = 1
                        new[y + 1][x - 1] = 1
                        new[y + 1][x] = 1
                        new[y + 1][x + 1] = 1
                    elif y == image_height - 1:
                        new[y][x - 1] = 1
                        new[y][x] = 1
                        new[y][x + 1] = 1
                        new[y - 1][x - 1] = 1
                        new[y - 1][x] = 1
                        new[y - 1][x + 1] = 1
                    else:
                        new[y][x - 1] = 1
                        new[y][x] = 1
                        new[y][x + 1] = 1
                        new[y - 1][x - 1] = 1
                        new[y - 1][x] = 1
                        new[y - 1][x + 1] = 1
                        new[y + 1][x - 1] = 1
                        new[y + 1][x] = 1
                        new[y + 1][x + 1] = 1
    return new


def computeConnectedComponentLabeling(pixel_array, image_width, image_height):
    new = createInitializedGreyscalePixelArray(image_width, image_height)
    visit = createInitializedGreyscalePixelArray(image_width, image_height)
    label = 1
    for y in range(image_height):
        for x in range(image_width):
            if pixel_array[y][x] != 0 and visit[y][x] == 0:
                q = Queue()
                q.enqueue([y, x])

                while not q.isEmpty():
                    out = q.dequeue()
                    current_y = out[0]
                    current_x = out[1]
                    visit[current_y][current_x] = 1
                    new[current_y][current_x] = label
                    if pixel_array[current_y - 1][current_x] and visit[current_y - 1][current_x] == 0:
                        q.enqueue([current_y - 1, current_x])
                        visit[current_y - 1][current_x] = 1
                    if pixel_array[current_y + 1][current_x] and visit[current_y + 1][current_x] == 0:
                        q.enqueue([current_y + 1, current_x])
                        visit[current_y - 1][current_x] = 1
                    if pixel_array[current_y][current_x + 1] and visit[current_y][current_x + 1] == 0:
                        q.enqueue([current_y, current_x + 1])
                        visit[current_y][current_x + 1] = 1
                    if pixel_array[current_y][current_x - 1] and visit[current_y][current_x - 1] == 0:
                        q.enqueue([current_y, current_x - 1])
                        visit[current_y][current_x - 1] = 1
                label += 1

    nr = {}
    for l in range(1, label):
        nr[l] = 0
    for y in range(image_height):
        for x in range(image_width):
            for l in range(1, label):
                if new[y][x] == l:
                    nr[l] = nr[l] + 1

    return (new, nr)


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

# This method packs together three individual pixel arrays for r, g and b values into a single array that is fit for
# use in matplotlib's imshow method
def prepareRGBImageForImshowFromIndividualArrays(r,g,b,w,h):
    rgbImage = []
    for y in range(h):
        row = []
        for x in range(w):
            triple = []
            triple.append(r[y][x])
            triple.append(g[y][x])
            triple.append(b[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage
    

# This method takes a greyscale pixel array and writes it into a png file
def writeGreyscalePixelArraytoPNG(output_filename, pixel_array, image_width, image_height):
    # now write the pixel array as a greyscale png
    file = open(output_filename, 'wb')  # binary mode is important
    writer = imageIO.png.Writer(image_width, image_height, greyscale=True)
    writer.write(file, pixel_array)
    file.close()



def main():
    filename = "./images/covid19QRCode/poster1small.png"
    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)
    # get access to the current pyplot figure
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    # paint the rectangle over the current plot
    grey = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    grey = scaleTo0And255AndQuantize(grey, image_width, image_height)
    greyV = computeVerticalEdgesSobelAbsolute(grey, image_width, image_height)
    greyH = computeHorizontalEdgesSobelAbsolute(grey, image_width, image_height)
    grad = gradient(greyH, greyV, image_width, image_height)
    mean = computeBoxAveraging3x3(grad, image_width, image_height)
    mean = computeBoxAveraging3x3(mean, image_width, image_height)
    mean = computeBoxAveraging3x3(mean, image_width, image_height)
    mean = computeBoxAveraging3x3(mean, image_width, image_height)
    mean = computeBoxAveraging3x3(mean, image_width, image_height)
    mean = computeBoxAveraging3x3(mean, image_width, image_height)
    smooth = scaleTo0And255AndQuantize(mean, image_width, image_height)
    threshold = computeThresholdGE(smooth, 70, image_width, image_height)
    dilation = computeDilation8Nbh3x3FlatSE(threshold, image_width, image_height)
    dilation = computeDilation8Nbh3x3FlatSE(dilation, image_width, image_height)
    erosion = computeErosion8Nbh3x3FlatSE(dilation, image_width, image_height)
    erosion = computeErosion8Nbh3x3FlatSE(erosion, image_width, image_height)
    (img, s) = computeConnectedComponentLabeling(erosion, image_width, image_height)
    maxv = 0
    key = 0
    for sz in s.keys():
        print("{}: {}".format(sz, s[sz]))
        if s[sz] > maxv:
            maxv = s[sz]
            key = sz
    print(maxv)
    print(key)
    pyplot.imshow(img, cmap='gray')
    pyplot.show()
    for y in range(image_height):
        for x in range(image_width):
            if img[y][x] != key:
                img[y][x] = 0
    pyplot.imshow(img, cmap='gray')
    pyplot.show()
    min_coordinate = (0,0)
    max_coordinate = (0,0)

    for y in range(image_height):
        for x in range(image_width):
            if img[y][x]:
                min_coordinate = (x,y)
                break
        if min_coordinate != (0,0):
            break
    for y in range(image_height):
        for x in range(image_width):
            if img[y][x]:
                max_coordinate = (x,y)
    width = max_coordinate[0] - min_coordinate[0]
    length = max_coordinate[1] - min_coordinate[1]
    print(min_coordinate)
    print(max_coordinate)
    print(image_width)
    print(image_height)
    pyplot.imshow(prepareRGBImageForImshowFromIndividualArrays(px_array_r, px_array_g, px_array_b, image_width, image_height))
    axes = pyplot.gca()
    rect = Rectangle(min_coordinate, width, length, linewidth=3, edgecolor='g', facecolor='none')
    axes.add_patch(rect)
    pyplot.show()
if __name__ == "__main__":
    main()