import numpy as np
from classes.Cube import Cube
from classes.Plane import Plane
from classes.Sphere import Sphere


def intersectSphere(ray, sphere):
    L = sphere.center - ray.p
    t_ca = L @ ray.v

    if t_ca < 0:
        return np.inf

    d_squared = L @ L - (t_ca ** 2)
    if d_squared > sphere.radius ** 2:
        return np.inf

    t_hc = np.sqrt(sphere.radius ** 2 - d_squared)
    t = t_ca - t_hc
    p = ray.p + t * ray.v
    N = (p - sphere.center) / np.linalg.norm(p - sphere.center)
    return t, N


def intersectPlane(ray, plane):
    # TODO: might need to add plane offset instead of subtract
    t = -1 * (ray.p @ plane.normal - plane.offset) / (ray.v @ plane.normal)
    return t, plane.normal


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
            if t < min_t:
                minEntity = entity
                min_t = t
                minNormal = N
    return min_t, minEntity, minNormal
