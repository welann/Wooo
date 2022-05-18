from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-0.85, (134/255, 142/255, 150/255))
scene.set_background_color((206/255, 212/255, 218/255))
scene.set_directional_light((1, 10, -1), 0.5, vec3(169, 190, 123)/255)


@ti.func
def drawaline(begin,end,color):             
    for i,j,k in ti.ndrange((begin[0],end[0]+1),
                        (begin[1],end[1]+1),
                        (begin[2],end[2]+1)):
        scene.set_voxel(ivec3(i,j,k),2, color)   
        


# @ti.func
# def create_block(pos, size, color, color_noise,model):
#     for I in ti.grouped(
#             ti.ndrange( (pos[0], pos[0] + size[0]), 
#                         (pos[1], pos[1] + size[1]),
#                         (pos[2], pos[2] + size[2]))):
#         # scene.set_voxel(I, 1, color + color_noise * ti.random())




@ti.kernel
def initialize_voxels():
    drawaline(ivec3(0,0,0),ivec3(0,10,10),vec3(238, 121, 89)/255);
    # for i,j,k in ti.ndrange((0,10),(0,1),(0,1)):
    #     scene.set_voxel(ivec3(i,j,k), 1, vec3(238, 121, 89)/255)

initialize_voxels()

scene.finish()
