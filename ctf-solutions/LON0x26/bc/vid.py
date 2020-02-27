import cv2
import os

cam = cv2.VideoCapture("video.avi")

values = []

def discrimator(frame):
    return frame[0][0][1] != 253

# Read each frame. Use discriminator on each frame to output a zero or one.
while True:
    ret, f = cam.read()
    if not ret:
        break
    values.append(
        discrimator(f)
    )

ones_and_zeroes = "".join(str(int(x)) for x in values)
byte_string = int(ones_and_zeroes, 2).to_bytes(len(ones_and_zeroes) // 8, byteorder='big')
os.write(1, byte_string)
