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


def calcEdges(cube):
    Edges = []

    xRightSide = cube.center + np.array(((cube.length / 2), 0, 0))
    xLeftSide = cube.center - np.array(((cube.length / 2), 0, 0))
    xAlignedSides = np.array((xRightSide, xLeftSide))

    for side in xAlignedSides:
        first = side + np.array((0, cube.length / 2, cube.length / 2))
        second = side + np.array((0, -(cube.length / 2), cube.length / 2))
        third = side + np.array((0, -(cube.length / 2), -(cube.length / 2)))
        fourth = side + np.array((0, cube.length / 2, -(cube.length / 2)))
        Edges.append(np.array((first, second, third, fourth)))

    xRightEdges = Edges[0]
    xLeftEdges = Edges[1]

    Edges.append(np.array((xRightEdges[0], xRightEdges[1], xLeftEdges[0], xLeftEdges[1])))  # frontSide
    Edges.append(np.array((xRightEdges[2], xRightEdges[3], xLeftEdges[2], xLeftEdges[3])))  # backSide
    Edges.append(np.array((xRightEdges[0], xRightEdges[3], xLeftEdges[0], xLeftEdges[3])))  # upSide
    Edges.append(np.array((xRightEdges[1], xRightEdges[2], xLeftEdges[1], xLeftEdges[2])))  # downSide

    return Edges


def getNearestAndFurthestCorners(point, side):
    distances = []
    for corner in side:
        distances.append(np.linalg.norm(point - corner))
    return side[np.argmin(distances)], side[np.argmax(distances)]


def intersectCube(ray, cube):
    t = np.inf
    N = None
    side_dist = cube.length / 2

    if not ray.v.all():
        print("zero")

    tmin = ((cube.center[0] - side_dist) - ray.p[0]) / ray.v[0]
    tmax = ((cube.center[0] + side_dist) - ray.p[0]) / ray.v[0]

    if (tmin > tmax):
        tmin, tmax = tmax, tmin

    tymin = ((cube.center[1] - side_dist) - ray.p[1]) / ray.v[1]
    tymax = ((cube.center[1] + side_dist) - ray.p[1]) / ray.v[1]

    if (tymin > tymax):
        tymin, tymax = tymax, tymin

    if ((tmin > tymax) or (tymin > tmax)):
        return np.inf, None

    if (tymin > tmin):
        tmin = tymin

    if (tymax < tmax):
        tmax = tymax

    tzmin = ((cube.center[2] - side_dist) - ray.p[2]) / ray.v[2]
    tzmax = ((cube.center[2] + side_dist) - ray.p[2]) / ray.v[2]

    if (tzmin > tzmax):
        tzmin, tzmax = tzmax, tzmin

    if ((tmin > tzmax) or (tzmin > tmax)):
        return np.inf, None

    if (tzmin > tmin):
        tmin = tzmin

    if (tzmax < tmax):
        tmax = tzmax

    if tmin >= 0:
        t = tmin
    elif tmax >= 0:
        t = tmax
    else:
        return np.inf, None

    hitPoint = ray.p + t * ray.v
    if side_dist + epsilon >= abs(hitPoint[0] - cube.center[0]) >= side_dist - epsilon:
        N = np.sign(hitPoint[0] - cube.center[0]) * np.array([1, 0, 0])
    elif side_dist + epsilon >= abs(hitPoint[1] - cube.center[1]) >= side_dist - epsilon:
        N = np.sign(hitPoint[1] - cube.center[1]) * np.array([0, 1, 0])
    elif side_dist + epsilon >= abs(hitPoint[2] - cube.center[2]) >= side_dist - epsilon:
        N = np.sign(hitPoint[2] - cube.center[2]) * np.array([0, 0, 1])
    else:
        print("error")
        return np.inf, None

    return t, N


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
