import sys

import numpy as np

import Parser
import utils
from intersections import findFirstIntersection
from classes.Ray import Ray


def initCameraVectors(camera, imageWidth, imageHeight):
    towards = (camera.look_at - camera.p)
    b = np.cross(camera.u, towards)

    towards = towards / np.linalg.norm(towards)
    b = b / np.linalg.norm(b)

    fixed_up = np.cross(towards, b)

    g_x = camera.sc_width / 2
    g_y = g_x * ((imageHeight - 1) / (imageWidth - 1))

    vx = ((2 * g_x) / (imageWidth - 1)) * b
    vy = ((2 * g_y) / (imageHeight - 1)) * fixed_up
    p_0 = towards * camera.sc_dist - g_x * b - g_y * fixed_up

    return p_0, vx, vy


def getPixelRay(i, j, p_0, vx, vy, cameraOrigin):
    p_ij = p_0 + vx * (i - 1) + vy * (j - 1)
    ray = p_ij / np.linalg.norm(p_ij)

    return Ray(cameraOrigin, ray)


def getColor(ray, t, entity):
    if t is not np.inf:
        return np.array(entity.material.diffuse)
    return np.array((255, 255, 255))


def rayTrace():
    inputPath, outputPath, width, height = sys.argv[1:]
    width = int(width)
    height = int(height)
    parsedParams = Parser.parseScene(inputPath)
    p_0, vx, vy = initCameraVectors(parsedParams["camera"], width, height)

    image = np.zeros((height, width, 3))
    for i in range(height):
        for j in range(width):
            ray = getPixelRay(i, j, p_0, vx, vy, parsedParams["camera"].p)
            t, entity = findFirstIntersection(ray, parsedParams["entities"])
            image[i][j] = getColor(ray, t, entity)
    return image


if __name__ == '__main__':
    image = rayTrace()
    print(image)
    utils.save_image(image, "output")
