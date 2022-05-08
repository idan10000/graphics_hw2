import sys

import numpy as np

import Parser
import utils
from intersections import findFirstIntersection
from classes.Ray import Ray

backgroundColor = None


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


def getLightdiffuse(light_intensity, mat, N, L):
    return mat.diffuse * light_intensity * (N @ L)


def getLightspec(light_intensity, mat, R, V):
    return mat.spec * light_intensity * ((R @ V) ** mat.phong)


def getPixeldiffuse(point, light_intensity, material, normal, lights):
    color = np.zeros(3)
    for light in lights:
        lightDirection = (point - light.point / np.linalg.norm(point - light.point))
        color += getLightdiffuse(light_intensity, material, normal, lightDirection)
    return color

def getPixelSpecular(point, light_intensity, material, normal, lights):
    color = np.zeros(3)
    for light in lights:
        lightDirection = (point - light.point / np.linalg.norm(point - light.point))
        color += getLightdiffuse(light_intensity, material, normal, lightDirection)
    return color


def getColor(ray, t, entity, normal, lights):
    p = ray.p + t * ray.v
    if t is not np.inf:
        diffuse = getPixeldiffuse(p, calcLightIntensity(), entity.material, normal, lights)
        specular = getp
    return backgroundColor


def rayTrace():
    inputPath, outputPath, width, height = sys.argv[1:]
    width = int(width)
    height = int(height)
    parsedParams = Parser.parseScene(inputPath)
    global backgroundColor
    backgroundColor = parsedParams["settings"].background_color
    p_0, vx, vy = initCameraVectors(parsedParams["camera"], width, height)

    image = np.zeros((height, width, 3))
    for i in range(height):
        for j in range(width):
            ray = getPixelRay(i, j, p_0, vx, vy, parsedParams["camera"].p)
            t, entity, normal = findFirstIntersection(ray, parsedParams["entities"])
            image[i][j] = getColor(ray, t, entity, normal, parsedParams["lights"])
    return image


if __name__ == '__main__':
    image = rayTrace()
    print(image)
    utils.save_image(image, "output")
