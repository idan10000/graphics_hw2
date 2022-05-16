import random
import sys

import numpy as np

import Parser
import utils
from classes.Sphere import Sphere
from intersections import findFirstIntersection
from classes.Ray import Ray

backgroundColor = None
epsilon = np.array((0.1, 0.1, 0.1))


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


# ---------------------------------- Diffuse ----------------------------------

def calcLightIntensity(point, normal, light, entity, entities, shadow_rays):
    # randomVector = light.point - 1
    # right = np.cross(normal, randomVector)
    # right = right / np.linalg.norm(right)
    # up = np.cross(normal, right)
    #
    # right *= light.width / 2
    # up *= light.width / 2
    # top_right = light.point + up + right
    # bot_left = light.point - up - right
    #
    # x = np.meshgrid()

    ray = Ray(light.point, (point - light.point / np.linalg.norm(point - light.point)))
    t, int_entity, normal = findFirstIntersection(ray, entities)
    if entity == int_entity:
        return 1 - light.shadow

    return light.shadow
    # return 1


def getLightdiffuse(light_intensity, mat, N, L):
    mul = N @ L
    if mul < 0:
        mul = 0
    return mat.diffuse * light_intensity * mul


def getPixeldiffuse(point, entity, normal, lights, entities, shadow_rays):
    color = np.zeros(3)
    for light in lights:
        lightDirection = (light.point - point / np.linalg.norm(light.point - point))
        lightIntensity = calcLightIntensity(point, lightDirection, light, entity, entities, shadow_rays)
        color += getLightdiffuse(lightIntensity, entity.material, normal, lightDirection)
    return color


# ---------------------------------- Specular ----------------------------------

def getLightspec(light_intensity, mat, R, V):
    mul = R @ V
    if mul < 0:
        return np.zeros(3)
    return mat.spec * light_intensity * np.power(mul, mat.phong)


def getPixelSpecular(point, ray, material, normal, lights):
    color = np.zeros(3)
    for light in lights:
        lightDirection = (light.point - point / np.linalg.norm(light.point - point))
        R = lightDirection - 2 * (lightDirection @ normal) * normal
        R /= np.linalg.norm(R)
        color += getLightspec(light.spec, material, R, ray.v)
    return color


# ---------------------------------- Reflection ----------------------------------

def getLightReflect(point, entities, ray, shadow_rays, normal, lights, reflection_depth):
    reflection_depth -= 1
    R = ray.v - 2 * (ray.v @ normal) * normal  # + epsilon
    R /= np.linalg.norm(R)
    point += epsilon
    reflection_ray = Ray(point, R)
    # point += epsilon
    t, entity, intersection_normal = findFirstIntersection(reflection_ray, entities)
    # if type(entity) == Sphere:
    #     print("test")
    return entity.material.reflect * getColor(reflection_ray, t, entity, intersection_normal, lights, entities, shadow_rays, reflection_depth)


def getColor(ray, t, entity, normal, lights, entities, shadow_rays, reflection_depth):
    p = ray.p + t * ray.v
    if t is not np.inf:
        # if type(entity) == Sphere:
        #     print("test")
        diffuse = getPixeldiffuse(p, entity, normal, lights, entities, shadow_rays)
        specular = getPixelSpecular(p, ray, entity.material, normal, lights)
        if reflection_depth > 0:
            reflect = getLightReflect(p, entities, ray, shadow_rays, normal, lights, reflection_depth)
        else:
            reflect = np.zeros(3)
        # return diffuse + specular
        return diffuse + specular + reflect
    return backgroundColor


def rayTrace():
    inputPath, outputPath, width, height = sys.argv[1:]
    width = int(width)
    height = int(height)
    parsedParams = Parser.parseScene(inputPath)
    settings = parsedParams["settings"]
    entities = parsedParams["entities"]
    camera = parsedParams["camera"]

    global backgroundColor
    backgroundColor = settings.background_color

    p_0, vx, vy = initCameraVectors(camera, width, height)

    image = np.zeros((height, width, 3))
    for i in range(height):
        for j in range(width):
            ray = getPixelRay(i, j, p_0, vx, vy, camera.p)
            t, entity, normal = findFirstIntersection(ray, entities)
            image[i][j] = getColor(ray, t, entity, normal, parsedParams["lights"], entities, settings.sh_rays,
                                   settings.rec_max)
    return image


if __name__ == '__main__':
    image = rayTrace()
    print(image)
    image = np.rot90(image, 1)
    utils.save_image(image, "output")
