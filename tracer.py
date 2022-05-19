import random
import sys

import numpy as np

import Parser
import utils
from classes.Plane import Plane
from classes.Sphere import Sphere
from intersections import findAllIntersections, findFirstIntersection
from classes.Ray import Ray

backgroundColor = np.array((1, 1, 1))
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
    p_ij = p_0 + vy * i + vx * j
    ray = p_ij / np.linalg.norm(p_ij)

    return Ray(cameraOrigin, ray)


# ---------------------------------- Diffuse ----------------------------------

def calcLightIntensity(point, normal, light, entity, entities, shadow_rays):
    randomVector = np.array([0, 0, 1]) / np.linalg.norm(np.array([0, 0, 1]))
    right = np.cross(normal, randomVector)
    right /= np.linalg.norm(right)
    up = np.cross(normal, right)
    up /= np.linalg.norm(up)

    bot_left = light.point + (up + right) * light.width / -2
    up *= light.width / shadow_rays
    right *= light.width / shadow_rays

    lightHits = 0
    for i in range(1, shadow_rays + 1):
        for j in range(1, shadow_rays + 1):
            randUp, randRight = np.random.uniform(0, 1, 2)
            lightPoint = bot_left + (i -1 + randUp) * up + (j - 1 + randRight) * right
            ray = Ray(lightPoint, ((point - lightPoint) / np.linalg.norm(point - lightPoint)))
            t, int_entity, normal = findFirstIntersection(ray, entities)
            if entity == int_entity:
                lightHits += 1
    return (1 - light.shadow) + light.shadow * (lightHits / (shadow_rays ** 2))


def getLightdiffuse(light_intensity, mat, N, L):
    mul = np.dot(N, L)
    if mul < 0:
        mul = 0
    return mat.diffuse * light_intensity * mul


def getPixeldiffuse(point, entity, normal, lights, lightIntensities):
    color = np.zeros(3)
    for i in range(len(lightIntensities)):
        lightDirection = ((lights[i].point - point) / np.linalg.norm(lights[i].point - point))
        # print(lightIntensity)
        color += getLightdiffuse(lightIntensities[i], entity.material, normal, lightDirection) * lights[i].color
    return color


# ---------------------------------- Specular ----------------------------------

def getLightspec(light_intensity, mat, R, V):
    mul = R @ V
    if mul < 0:
        return np.zeros(3)
    return mat.spec * light_intensity * np.power(mul, mat.phong)


def getPixelSpecular(point, ray, material, normal, lightIntensities, lights):
    color = np.zeros(3)
    for i in range(len(lightIntensities)):
        lightDirection = ((lights[i].point - point) / np.linalg.norm(lights[i].point - point))
        R = lightDirection - 2 * np.dot(lightDirection, normal) * normal
        R /= np.linalg.norm(R)
        color += getLightspec(lights[i].spec, material, R, ray.v) * lights[i].color * lightIntensities[i]
    return color


# ---------------------------------- Reflection ----------------------------------

def getLightReflect(point, entities, entity, ray, shadow_rays, normal, lights, reflection_depth):
    reflection_depth -= 1
    R = ray.v - 2 * (np.dot(ray.v, normal)) * normal  # + epsilon
    R /= np.linalg.norm(R)
    reflection_ray = Ray(point, R)

    if type(entity) == Plane:
        print("s")

    intersections = findAllIntersections(reflection_ray, entities)
    if len(intersections) == 0:
        return backgroundColor * entity.material.reflect
    t, reflectedEntity, intersection_normal = intersections[0]
    if reflectedEntity == entity:
        intersections = intersections[1:]
        if len(intersections) == 0:
            return backgroundColor * entity.material.reflect
        t, reflectedEntity, intersection_normal = intersections[0]
    # if type(entity) == Sphere:
    #     print("test")
    return entity.material.reflect * getColor(reflection_ray, t, reflectedEntity, intersection_normal, lights,
                                                       entities, shadow_rays, reflection_depth, intersections[1:])


def getColor(ray, t, entity, normal, lights, entities, shadow_rays, reflection_depth, intersections):
    p = ray.p + t * ray.v
    if t is not np.inf:
        transparencyColor = np.zeros(3)
        diffuse = np.zeros(3)
        specular = np.zeros(3)
        reflect = np.zeros(3)
        mat = entity.material
        lightIntensities = []

        if mat.diffuse.any() or mat.spec.any():
            for light in lights:
                lightDirection = ((light.point - p) / np.linalg.norm(light.point - p))
                lightIntensities.append(calcLightIntensity(p, lightDirection, light, entity, entities, shadow_rays))

        if mat.diffuse.any():
            diffuse = getPixeldiffuse(p, entity, normal, lights, lightIntensities)

        if mat.spec.any():
            specular = getPixelSpecular(p, ray, mat, normal, lightIntensities, lights)

        if reflection_depth > 0 and mat.reflect.any():
            reflect = getLightReflect(p, entities, entity, ray, shadow_rays, normal, lights, reflection_depth)

        if mat.trans != 0:
            transparencyColor = getBackground(entities, ray, shadow_rays, lights, reflection_depth, intersections)

        return (diffuse + specular) * (1 - mat.trans) + transparencyColor * mat.trans + reflect
        # return diffuse
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
            intersections = findAllIntersections(ray, entities)
            if len(intersections) == 0:
                image[i][j] = backgroundColor
            else:
                t, entity, normal = intersections[0]
                image[i][j] = getColor(ray, t, entity, normal, parsedParams["lights"], entities, int(settings.sh_rays),
                                       settings.rec_max, intersections[1:])
    return image


if __name__ == '__main__':
    image = rayTrace()
    print(image)
    image = np.rot90(image, 2)
    utils.save_image(image, "output")
