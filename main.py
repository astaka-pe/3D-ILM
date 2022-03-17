import numpy as np
import open3d as o3d
from PIL import Image

import argparse

SIZE = 200

parser = argparse.ArgumentParser(description="3D initial logo maker")
parser.add_argument("--first", type=str, required=True)
parser.add_argument("--last", type=str, required=True)
FLAGS = parser.parse_args()

img1 = Image.open("images/{}.png".format(FLAGS.first.lower()))
img2 = Image.open("images/{}.png".format(FLAGS.last.lower()))
img1 = img1.convert(mode="1")
img2 = img2.convert(mode="1")
mask1 = np.array(img1).astype(np.int)
mask2 = np.array(img2).astype(np.int)
voxel1 = np.zeros([SIZE, SIZE, SIZE])
voxel2 = np.zeros([SIZE, SIZE, SIZE])

for i in range(SIZE):
    voxel1[:, :, i] = mask1
    voxel2[:, i, :] = mask2

final_voxel = voxel1 * voxel2
xs, ys, zs = np.where(final_voxel==1)
vs = np.array([xs, ys, zs]).T
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(vs)

mesh = o3d.geometry.TriangleMesh()
vertices = []
indices = []
for vi in range(len(vs)):
    x, y, z = vs[vi]
    vert = [
        [x-0.5, y-0.5, z-0.5],
        [x+0.5, y-0.5, z-0.5],
        [x-0.5, y+0.5, z-0.5],
        [x+0.5, y+0.5, z-0.5],
        [x-0.5, y-0.5, z+0.5],
        [x+0.5, y-0.5, z+0.5],
        [x-0.5, y+0.5, z+0.5],
        [x+0.5, y+0.5, z+0.5]
    ]
    i = vi*8
    indi = [
        [i+2, i+1, i],
        [i+1, i+2, i+3],
        [i+4, i+2, i],
        [i+2, i+4, i+6],
        [i+1, i+4, i],
        [i+4, i+1, i+5],
        [i+6, i+5, i+7],
        [i+5, i+6, i+4],
        [i+3, i+6, i+7],
        [i+6, i+3, i+2],
        [i+5, i+3, i+7],
        [i+3, i+5, i+1]
    ]
    vertices += vert
    indices += indi

vertices = np.array(vertices) - SIZE / 2.0
indices = np.array(indices)

mesh.vertices =  o3d.utility.Vector3dVector(vertices)
mesh.triangles =  o3d.utility.Vector3iVector(indices)
o3d.io.write_triangle_mesh("logo.obj", mesh, write_vertex_normals=False, write_vertex_colors=False, write_triangle_uvs=False)