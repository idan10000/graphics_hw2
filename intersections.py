import numpy as np
from classes.Cube import Cube
from classes.Plane import Plane
from classes.Sphere import Sphere

epsilon = 1e-9

def intersectSphere(ray, sphere):
    L = sphere.center - ray.p
    t_ca = np.dot(L, ray.v)
    t = 0
    if t_ca < epsilon:
        return np.inf, np.inf

    d_squared = np.dot(L, L) - (t_ca ** 2)
    if d_squared > sphere.radius ** 2:
        return np.inf, np.inf

    t_hc = np.sqrt(sphere.radius ** 2 - d_squared)
    t = t_ca - t_hc

    p = ray.p + t * ray.v
    N = (p - sphere.center) / np.linalg.norm(p - sphere.center)
    return t, N


def intersectPlane(ray, plane):
    t = -1 * (np.dot(ray.p, plane.normal) - plane.offset) / np.dot(ray.v, plane.normal)
    return t, plane.normal / np.linalg.norm(plane.normal)


def intersectCube(ray, cube):
    pass


def intersect(ray, entity):
    if type(entity) is Sphere:
        return intersectSphere(ray, entity)
    elif type(entity) is Plane:
        return intersectPlane(ray, entity)
    else:
        return intersectCube(ray, entity)


def findFirstIntersection(ray, scene):
    min_t = np.inf
    minEntity = None
    minNormal = None
    for entity in scene:
        t, N = intersect(ray, entity)
        if type(t) is not np.complex128:
            if min_t > t > 0:
                minEntity = entity
                min_t = t
                minNormal = N
    return min_t, minEntity, minNormal


def findAllIntersections(ray, scene):
    intersectedObjects = []
    for entity in scene:
        t, N = intersect(ray, entity)
        if type(t) is not np.complex128:
            if t != np.inf and t > 0:
                intersectedObjects.append((t, entity, N))
    intersectedObjects.sort(key=lambda tup: tup[0])
    return intersectedObjects
