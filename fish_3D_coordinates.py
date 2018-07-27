import numpy as np
import cv2

#start - change when moving to a different tank setting
tank_Height = 10
tank_width = 28
tank_length = 48

#pixel coordinates matching world coordinates
cam_up_coordinates = np.array([[1118, 545], [303, 558], [1015, 111], [294, 135]], dtype=np.float32).reshape((4,1,2))
cam_side_coordinates = np.array([[242, 472], [887, 469], [119, 526], [984, 523]], dtype=np.float32).reshape((4,1,2))
#end - change when moving to a different tank setting
world_coordinates = np.array([[0, 0, 0], [tank_length, 0, 0], [0, tank_width, 0], [tank_length, tank_width, 0]], dtype=np.float32).reshape((4,1,3))

matrix_side_cam = np.load('side_cam/cam_mat.npy')
dist_side_cam = np.load('side_cam/dist.npy').reshape((5, 1))
matrix_up_cam = np.load('up_cam/cam_mat.npy')
dist_up_cam = np.load('up_cam/dist.npy').reshape((5, 1))

plane_normal_up_cam = np.array([0,0,1])
plane_normal_side_cam = np.array([0,1,0])

plane_up_cam_points = np.array([[0,0,0],[tank_length,0,0],[0,tank_width,0],[tank_length,tank_width,0]])
plane_side_cam_points = np.array([[0,tank_width,0],[tank_length,tank_width,0],[0,tank_width,tank_Height],[tank_length,tank_width,tank_Height]])

airRefraction = 1.0
waterRefraction = 1.33

def calculateParamsAndCamPosition(cam_matrix, cam_dist, cam_coordinates , world_coordinates):
    ret, rvec, tvec = cv2.solvePnP(world_coordinates , cam_coordinates , cam_matrix, cam_dist, flags=cv2.SOLVEPNP_P3P)
    rotation_matrix = cv2.Rodrigues(rvec)[0]
    cam_position = -np.dot(rotation_matrix.T, tvec).T
    return rotation_matrix, cam_position

#calculate R^-1K^-1[u v 1]^T
#ray that comes from camera center to pixel point in picture
def calcRay(cam_matrix, cam_dist, cam_point, rotation_matrix):
    #calculate R^-1
    inverse_rotation_matrix = np.linalg.inv(rotation_matrix)
    #calculate K^-1[u v 1]^T
    cordinate = np.array([[cam_point]])
    lensDistortion = cv2.undistortPoints(cordinate, cam_matrix, cam_dist)
    lensDistortion = lensDistortion[0][0]  # Unwrap point from array of array
    lensDistortion = np.array([lensDistortion[0], lensDistortion[1], 1.0])

    ray = np.dot(inverse_rotation_matrix, lensDistortion)
    normalized_ray = ray / np.linalg.norm(ray)
    return normalized_ray

#finds refraction point
def planeRayIntersection(ray, plane_point, ray_point, plane_normal):
    #r_0 = point on the ray
    #p_0 = point on the plane
    #n = normal to plane
    lambda_top = np.dot((plane_point - ray_point), plane_normal)
    lambda_bottom = np.dot(ray, plane_normal)
    lambda_val = float(lambda_top)/lambda_bottom
    intersection = (lambda_val * ray) + ray_point
    return intersection.flatten()

#calculate rays after refraction
#first refraction - air
#second refraction - water
#ray - ray before refraction point
#normal to plane of refraction
def calculateRefractedRays(first_refraction, second_refraction, ray, plane_normal):
    refraction = float(first_refraction)/second_refraction
    cos_o1 = np.dot(-plane_normal, ray)
    cos_o2 = np.sqrt(1.0-((refraction**2)*(1.0-((cos_o1)**2))))
    refracted_ray = (refraction*ray) + ((refraction*cos_o1-cos_o2)*plane_normal)
    return refracted_ray

#cam1_ray - first camera direction vector of the refracted ray
#cam2_ray - second camera direction vector of the refracted ray
#cam1_refractio_point (point of intersection with plane) - first camera point of refraction
#cam2_ref_point - second camera point of refraction
#find ray intersection
def triangulateRays(cam1_ray, cam2_ray, cam1_ref_point, cam2_ref_point):
    #calculate m1, m2 according to formulas 6.10,6.11 in the article
    rays_mul = np.dot(cam1_ray, cam2_ray)
    ray1_mul = np.dot(cam1_ray, cam1_ray)
    ray2_mul = np.dot(cam2_ray, cam2_ray)
    points_dist = cam2_ref_point - cam1_ref_point
    ray1_mul_points_dist = np.dot(cam1_ray, points_dist)
    ray2_mul_points_dist = np.dot(cam2_ray, points_dist)
    normalizer = (ray1_mul*ray2_mul) - (rays_mul**2)
    top_m1 = (-rays_mul*ray2_mul_points_dist) + (ray1_mul_points_dist*ray2_mul)
    top_m2 = (rays_mul*ray1_mul_points_dist) - (ray2_mul_points_dist*ray1_mul)

    m1 = cam1_ref_point + (cam1_ray * (float(top_m1) / normalizer))
    m2 = cam2_ref_point + (cam2_ray * (float(top_m2) / normalizer))

    #find intersection point according to formula 6.12
    p = (m1+m2)/2
    return p

def calculate3DCoordinates(side_cam_point, up_cam_point):
    rotation_matrix1, cam_position1 = calculateParamsAndCamPosition(matrix_side_cam, dist_side_cam, cam_side_coordinates, world_coordinates)
    ray_cam1 = calcRay(matrix_side_cam, dist_side_cam, side_cam_point, rotation_matrix1)
    plane_ray_intersection1 = planeRayIntersection(ray_cam1, plane_side_cam_points[0], cam_position1.flatten(), plane_normal_side_cam)
    refracted_ray_cam1 = calculateRefractedRays(airRefraction, waterRefraction, ray_cam1, plane_normal_side_cam)

    rotation_matrix2, cam_position2 = calculateParamsAndCamPosition(matrix_up_cam, dist_up_cam, cam_up_coordinates, world_coordinates)
    ray_cam2 = calcRay(matrix_up_cam, dist_up_cam, up_cam_point, rotation_matrix2)
    plane_ray_intersection2 = planeRayIntersection(ray_cam2, plane_up_cam_points[0], cam_position2.flatten(), plane_normal_up_cam)
    refracted_ray_cam2 = calculateRefractedRays(airRefraction, waterRefraction, ray_cam2, plane_normal_up_cam)

    intersection = triangulateRays(refracted_ray_cam1, refracted_ray_cam2, plane_ray_intersection1, plane_ray_intersection2)
    return intersection

#float coordinates  in pixels for each camera
sideCoordinates  = np.array( [642. , 592.] )
upCoordinates = np.array([581. , 345.])
point = calculate3DCoordinates(sideCoordinates, upCoordinates)
print point
