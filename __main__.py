import sys
import pathlib
import os
import cv2
import numpy

def err(msg: str):
    print(msg)
    exit(1)

def assert_err(cond: any, msg: str):
    if cond == None or cond == False:
        err(msg)

def flipped(x: int) -> int:
    return -x - 1

def convert(video: cv2.VideoCapture):
    '''
    Converts a VideoCapture to a dictionary containing
    a texture for each face.
    '''
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frames = []

    while True:
        ok, image = video.read()
        if not ok:
            break
        else:
            frames.append(image)

    frame_count = len(frames) - 1 # -2 to skim the random blank frame

    def front():
        '''
        Takes the first frame and leaves it unchanged.

        X = Height
        Y = Width
        '''
        return frames[0]
    
    def back():
        '''
        Takes the last frame (which for whatever reason is one
        less than the array length) and flips it horizontally.

        X = Height (Pixels)
        Y = Width (Pixels)
        '''
        texture = numpy.zeros((height, width, 3), numpy.uint8)
        frame = frames[frame_count - 1] 

        for x in range(0, height):
            for y in range(0, width):
                texture[x, flipped(y)] = frame[x, y]

        return texture

    def top():
        '''
        Scans the first row of pixels through time and flips it
        vertically.

        X = Width (Pixels)
        Y = Time (Frames, First Frame @ Bottom)
        '''
        texture = numpy.zeros((frame_count, width, 3), numpy.uint8)
        for frame_no in range(0, frame_count):
            frame = frames[frame_no]
            for i in range(0, width):
                texture[flipped(frame_no), i] = frame[0, i]
        return texture;

    def bottom():
        '''
        Scans the bottom row of pixels through time and flips it
        horizontally and vertically.

        X = Width (Pixels)
        Y = Time (Frames, First Frame @ Top)
        '''
        texture = numpy.zeros((frame_count, width, 3), numpy.uint8)
        for frame_no in range(0, frame_count):
            frame = frames[frame_no]
            for i in range(0, width):
                texture[flipped(frame_no), flipped(i)] = frame[height - 1, i]
        return texture;

    def right():
        '''
        Scans the left-most column of pixels through time and
        flips it horizontally.

        X = Time (Frames, First Frame @ Right)
        Y = Height (Pixels)
        '''
        texture = numpy.zeros((height, frame_count, 3), numpy.uint8)
        for frame_no in range(0, frame_count):
            frame = frames[frame_no]
            for i in range(0, height):
                texture[i, flipped(frame_no)] = frame[i, 0]
        return texture;

    def left():
        '''
        Scans the right-most column of pixels through time and
        leaves it unchanged.

        X = Time (Frames, First Frame @ Left)
        Y = Height (Pixels)
        '''
        texture = numpy.zeros((height, frame_count, 3), numpy.uint8)
        for frame_no in range(0, frame_count):
            frame = frames[frame_no]
            for i in range(0, height):
                texture[i, frame_no] = frame[i, width - 1]
        return texture;

    return {
        "front": front(),
        "back": back(),
        "top": top(),
        "bottom": bottom(),
        "right": right(),
        "left": left(),
    }   

def main():
    assert_err(len(sys.argv) == 3, "specify input file and output directory")
    
    input = sys.argv[1]
    output_dir = sys.argv[2]

    assert_err(os.path.isfile(input), f"file '{input}' not found")
    assert_err(os.path.isdir(output_dir), f"directory '{output_dir}' not found")

    textures = convert(cv2.VideoCapture(input))
    for side, texture in textures.items():
        
        textures[side] = cv2.imwrite(output_dir + "/" + side + ".png", texture)

if __name__ == "__main__":
    main()