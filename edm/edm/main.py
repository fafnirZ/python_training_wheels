import math
import numpy as np



def edm(x,y):
    """Euclidean Distance Matrix.

    d**2 = sum(x**2) - 2 sum(dot(x,y)) + sum(y**2)
            = sum(x**2) - 2 dot(x,(y**T)) + sum(y**2)
    
    Refs:
        https://medium.com/@aishahsofea/for-loops-vs-matrix-multiplication-ee67868f937
        https://medium.com/swlh/euclidean-distance-matrix-4c3e1378d87f
    """
    x_sq = np.sum(np.square(x), axis=1)
    y_sq = np.sum(np.square(x), axis=1)
    dot_product = 2 * np.dot(x, y.T)
    dists = np.sqrt(x_sq[:,np.newaxis] - dot_product + y_sq)
    return dists


def point_distance(points: np.array):
    """Given a single list of 2D points, find distance between each other."""
    assert points.shape[1] == 2
    return edm(points, points)

def point_distance_manual(points: np.array):
    assert points.shape[1] == 2
    res = []
    for point in points:
        x_1, y_1 = point
        res_layer = []
        for point in points:
            x_2, y_2 = point
            distance = math.sqrt(
                (x_1 - x_2)**2 + (y_1 - y_2)**2
            )
            res_layer.append(distance)
        res.append(res_layer)

    return np.array(res)





# if __name__ == "__main__":
#     case_1 = np.array([
#         [1,2],
#         [2,10],
#         [5,20],
#     ])

#     res_manual = point_distance_manual(case_1)
#     res_edm = point_distance(case_1)
#     assert (res_edm==res_manual).all()
