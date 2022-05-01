from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-0.85, (134/255, 142/255, 150/255))
scene.set_background_color((206/255, 212/255, 218/255))
scene.set_directional_light((1, 10, -1), 0.5, (1, 0.8, 0.6))


@ti.func
def create_block(pos, size, color, color_noise,model):
    for I in ti.grouped(
            ti.ndrange( (pos[0], pos[0] + size[0]), 
                        (pos[1], pos[1] + size[1]),
                        (pos[2], pos[2] + size[2]))):
        scene.set_voxel(I, model, color + color_noise * ti.random())

@ti.func
def bigcube(pos, color,model):
    for i in range(80):
        scopex = ti.random()*6+20
        scopey = ti.random()*6+20
        scopez = ti.random()*6+20
        if ti.random() < 0.03:
            scene.set_voxel(pos+ivec3(scopex,scopey,scopez),2,color)
        else:
            create_block(pos+ivec3(scopex,scopey,scopez),ivec3(1,1,1),color,vec3(0.01),1)
            
@ti.func
def cloud(pos,size):
    for i in range(size):
        scopex = ti.random()*i+5
        scopey = ti.random()*i+5
        scopez = ti.random()*i+5
        bigcube(pos+ivec3(scopex,scopey,scopez),vec3(110, 155, 197)/255,2)


#todo
#把草出现的位置做成迷宫
@ti.func
def grass():
    #-60, -39, -60 to 60,-39,60
    for i, j in ti.ndrange((-60,60),(-60, 60)):
        height = ti.random() * 5+7
        if ti.random() < 0.1:
            create_block(ivec3(i, -40, j), ivec3(1, height, 1), vec3(151, 117, 250)/255, vec3(0.3),1)
        if ti.random() <0.03:
            scene.set_voxel(ivec3(i, height-50, j), 2, vec3(148, 216, 45)/255)
        if ti.random() <0.0013:
            cloud(ivec3(i, height-15, j),15)

@ti.kernel
def initialize_voxels():
    for i in range(4):
        create_block(ivec3(-60, -(i + 1)**2 - 40, -60),
                     ivec3(120, 2 * i + 1, 120),
                     vec3(0.5 - i * 0.1) * vec3(1.0, 0.8, 0.6),
                     vec3(0.02 * (3 - i)), 
                    1)

    create_block(ivec3(-60, -40, -60), ivec3(120, 1, 120), vec3(238, 121, 89)/255,vec3(0.01),1)

    grass()

    create_block(ivec3(0, -39, 20),ivec3(3,35,3),vec3(95, 67, 33)/255, vec3(0.1),1)
    for i in range(50):
        scopex = -ti.random()*20+10
        scopey = -ti.random()*20+10
        scopez = -ti.random()*20+10
        bigcube(ivec3(-20,-25,0)+ivec3(scopex,scopey,scopez),vec3(119, 150, 73)/255,1)

    create_block(ivec3(-20, -39, -30),ivec3(3,35,3),vec3(95, 67, 33)/255, vec3(0.1),1)
    for i in range(50):
        scopex = -ti.random()*20+10
        scopey = -ti.random()*20+10
        scopez = -ti.random()*20+10
        bigcube(ivec3(-40,-20,-50)+ivec3(scopex,scopey,scopez),vec3(1.0, 0.3, 0.9),1)


initialize_voxels()

scene.finish()