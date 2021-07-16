def computeConnectedComponentLabeling(pixel_array, image_width, image_height):
    new = createInitializedGreyscalePixelArray(image_width, image_height)
    label = 1
    for y in range(image_height):
        for x in range(image_width):
            if pixel_array[y][x] != 0 and new[y][x] == 0:
                q = Queue()
                q.enqueue([y, x])
                while !q.isEmpty():
                    out = q.dequeue()
                    current_y = out[0]
                    current_x = out[1]
                    new[current_y][current_x] = label
                    if pixel_array[current_y - 1][current_x] != 0 and new[y][x] == 0:
                        q.enqueue([current_y - 1, current_x])

                    if pixel_array[current_y + 1][current_x] != 0 and new[y][x] == 0:
                        q.enqueue([current_y + 1, current_x])

                    if pixel_array[current_y][current_x + 1] != 0 and new[y][x] == 0:
                        q.enqueue([current_y, current_x + 1])

                    if pixel_array[current_y][current_x - 1] != 0 and new[y][x] == 0:
                        q.enqueue([current_y, current_x - 1])
                label += 1
    thisdict = {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1964
    }
    return (new, thisdict)
