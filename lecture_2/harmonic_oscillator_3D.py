#%%
import math

import sympy as sp
# Начальные условия
x = 0.5
y = 1.5
z = 1
vx = 0
vy = 0
vz = 0
s_1 = 0.5
s_2 = 1.5
k_1 = 9
k_2 = 7
m = 5
g = 9.8
d = 0.2

# Временной интервал
t = 0
h = 0.05
t_max = 400

# Значения

time = []
x_values = []
y_values = []
z_values = []

def dx(vx):
    dx = vx
    return dx
def dy(vy):
    dy = vy
    return dy
def dz(vz):
    dz = vz
    return dz
def dvx(x, y, z, vx):
    dvx = (-d * vx -k_1 * (s_1 + x) * (1 - s_1 / math.sqrt((s_1+x) ** 2 + y ** 2 + z**2)) +
           k_2 * (s_2 - x) * (1 - s_2 / math.sqrt((s_2 - x) ** 2 + y ** 2 + z ** 2))) / m
    return dvx
def dvy(x, y, z, vy):
    dvy = (-d * vy - k_1 * y * (1 - s_1 / math.sqrt((s_1 + x) ** 2 + y ** 2 + z ** 2)) +
           k_2 * y * (1 - s_2 / math.sqrt((s_2 - x) ** 2 + y ** 2 + z ** 2))) / m
    return dvy
def dvz(x, y, z, vz):
    dvz = (-d * vz + k_1 * z * (1 - s_1 / math.sqrt((s_1 + x) ** 2 + y ** 2 + z ** 2)) +
           k_2 * z * (1 - s_2 / math.sqrt((s_2 - x) ** 2 + y ** 2 + z ** 2)) - g) / m
    return dvz

#RT4
#F = ...
#ma = ...
#dV/dT = .../m
while t < t_max:
    dx1 = dx(vx)
    dy1 = dy(vy)
    dz1 = dz(vz)
    dvx1 = dvx(x, y, z, vx)
    dvy1 = dvy(x, y, z, vy)
    dvz1 = dvy(x, y, z, vz)

    dx2 = dx(vx + dvx1*h/2)
    dy2 = dy(vy + dvy1*h/2)
    dz2 = dz(vz + dvz1*h/2)
    dvx2 = dvx(x + dx1 * h / 2, y + dy1 * h / 2, z + dz1 * h / 2, vx + dvx1 * h / 2)
    dvy2 = dvy(x + dx1 * h / 2, y + dy1 * h / 2, z + dz1 * h / 2, vy + dvy1 * h / 2)
    dvz2 = dvy(x + dx1 * h / 2, y + dy1 * h / 2, z + dz1 * h / 2, vz + dvz1 * h / 2)

    dx3 = dx(vx + dvx2*h/2)
    dy3 = dy(vy + dvy2*h/2)
    dz3 = dz(vz + dvz2*h/2)
    dvx3 = dvx(x + dx2 * h / 2, y + dy2 * h / 2, z + dz2 * h / 2, vx + dvx2 * h / 2)
    dvy3 = dvy(x + dx2 * h / 2, y + dy2 * h / 2, z + dz2 * h / 2, vy + dvy2 * h / 2)
    dvz3 = dvy(x + dx2 * h / 2, y + dy2 * h / 2, z + dz2 * h / 2, vz + dvz2 * h / 2)

    dx4 = dx(vx + dvx3*h)
    dy4 = dy(vy + dvy3*h)
    dz4 = dz(vy + dvz3*h)
    dvx4 = dvx(x + dx3 * h, y + dy3 * h, z + dz3 * h, vx + dvx3 * h)
    dvy4 = dvy(x + dx3 * h, y + dy3 * h, z + dz3 * h, vy + dvy3 * h)
    dvz4 = dvy(x + dx3 * h, y + dy3 * h, z + dz3 * h, vz + dvz3 * h)

    #сохраняем значения
    time.append(t)
    x_values.append(x)
    y_values.append(y)
    z_values.append(z)

    #обновляем значения
    x = x + (dx1 + 2 * dx2 + 2 * dx3 + dx4) * h / 6.0
    y = y + (dy1 + 2 * dy2 + 2 * dy3 + dy4) * h / 6.0
    z = z + (dz1 + 2 * dz2 + 2 * dz3 + dz4) * h / 6.0
    vx = vx + (dvx1 + 2 * dvx2 + 2 * dvx3 + dvx4) * h / 6.0
    vy = vy + (dvy1 + 2 * dvy2 + 2 * dvy3 + dvy4) * h / 6.0
    vz = vz + (dvz1 + 2 * dvz2 + 2 * dvz3 + dvz4) * h / 6.0

    #обновляем время
    t += h

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from spring import spring

ANIM_TIME = 15 # seconds
FPS = 45
FRAMETIME = 1 / FPS # in seconds
TOTAL_FRAMES = ANIM_TIME * FPS

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.set(xlim3d=(-2, 2), xlabel='X')
ax.set(ylim3d=(-4, 4), ylabel='Y')
ax.set(zlim3d=(-5, 4), zlabel='Z')

line_1, = ax.plot([], [], [], color = "red", lw=1)
line_2, = ax.plot([], [], [], color = "blue", lw=1)

def init():
    line_1.set_data([], [])
    line_1.set_3d_properties([])
    line_2.set_data([], [])
    line_2.set_3d_properties([])
    return line_1, line_2
def animate(frame):

    line_1.set_data([-2, x_values[frame]], [0, y_values[frame]])
    line_1.set_3d_properties([0, z_values[frame]])
    line_2.set_data([2, x_values[frame]], [0, y_values[frame]])
    line_2.set_3d_properties([0, z_values[frame]])

    return line_1, line_2

anim = FuncAnimation(fig, animate, init_func=init,
                     frames=TOTAL_FRAMES, interval=int(FRAMETIME*1000), blit=True)

plt.show()

anim.save("2_springs_3D.gif")
