import cv2 as cv
from os import listdir
from os.path import isfile, join

colorThreshold = 50
antiBlueThreshold = 50
deltaThreshold = 10
rustPixelThreshold = 100
def detectRust(filename):
    img = cv.imread(filename)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if img[x][y][2] > img[x][y][0] + colorThreshold and img[x][y][2] > img[x][y][1] + colorThreshold:
                img[x][y] = (255, 255, 255)
            else:
                img[x][y] = (0, 0, 0)
    cv.imwrite(filename[:-4] + "redmask.jpg", img)

    img = cv.imread(filename)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if img[x][y][0] < antiBlueThreshold and img[x][y][2] > img[x][y][1] + deltaThreshold:
                img[x][y] = (255, 255, 255)
            else:
                img[x][y] = (0, 0, 0)
    cv.imwrite(filename[:-4] + "brownmask.jpg", img)

def detectRustOverlay(filename):
    img = cv.imread(filename)
    img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if img[x][y][2] > img[x][y][0] + colorThreshold and img[x][y][2] > img[x][y][1] + colorThreshold:
                img[x][y][0] = 0
                img[x][y][1] = 0
                img[x][y][2] = 255
            else:
                img[x][y][3] = 0
    cv.imwrite(filename[:-4] + "redmask.jpg", img)

    img = cv.imread(filename)
    img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if img[x][y][0] < antiBlueThreshold and img[x][y][2] > img[x][y][1] + deltaThreshold:
                img[x][y][0] = 0
                img[x][y][1] = 0
                img[x][y][2] = 255
            else:
                img[x][y][3] = 0
    cv.imwrite(filename[:-4] + "brownmask.jpg", img)

def hasRust(filename):
    sum = 0
    img = cv.imread(filename)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if img[x][y][0] < antiBlueThreshold and img[x][y][2] > img[x][y][1] + deltaThreshold:
                sum += 1
    return sum >= rustPixelThreshold