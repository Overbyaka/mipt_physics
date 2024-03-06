#%%
import math

import sympy as sp
# Начальные условия
x = 0
y = 1
vx = 0
vy = 0
s_1 = 1
s_2 = 3
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
vx_values = []
vy_values = []

def dx(vx):
    dx = vx
    return dx
def dy(vy):
    dy = vy
    return dy
def dvx(x, y, vx):
    dvx = (-d*vx -k_1 * abs(s_1 + x) * (1 - 1 / math.sqrt((1 + x / s_1) ** 2 + (y / s_1) ** 2)) + k_2 * abs(s_2 - x) * (
                1 - 1 / math.sqrt((1 - x / s_2) ** 2 + (y / s_2) ** 2))) / m
    return dvx
def dvy(x, y, vy):
    dvy = (-d * vy + k_1 * abs(y) * (1 - 1 / math.sqrt((1 + x / s_1) ** 2 + (y / s_1) ** 2)) + k_2 * abs(y) * (
                1 - 1 / math.sqrt((1 - x / s_2) ** 2 + (y / s_2) ** 2)) - g)/m
    return dvy

#RT4
#F = ...
#ma = ...
#dV/dT = .../m
while t < t_max:
    dx1 = dx(vx)
    dy1 = dy(vy)
    dvx1 = dvx(x, y, vx)
    dvy1 = dvy(x, y, vy)

    dx2 = dx(vx + dvx1*h/2)
    dy2 = dy(vy + dvy1*h/2)
    dvx2 = dvx(x + dx1 * h / 2, y + dy1 * h / 2, vx + dvx1 * h / 2)
    dvy2 = dvy(x + dx1 * h / 2, y + dy1 * h / 2, vy + dvy1 * h / 2)

    dx3= dx(vx + dvx2*h/2)
    dy3 = dy(vy + dvy2*h/2)
    dvx3 = dvx(x + dx2 * h / 2, y + dy2 * h / 2, vx + dvx2 * h / 2)
    dvy3 = dvy(x + dx2 * h / 2, y + dy2 * h / 2, vy + dvy2 * h / 2)

    dx4= dx(vx + dvx3*h)
    dy4 = dy(vy + dvy3*h)
    dvx4 = dvx(x + dx3 * h, y + dy3 * h, vx + dvx3 * h)
    dvy4 = dvy(x + dx3 * h, y + dy3 * h, vy + dvy3 * h)

    #сохраняем значения
    time.append(t)
    x_values.append(x)
    y_values.append(y)
    vx_values.append(vx)
    vy_values.append(vy)

    #обновляем значения
    x = x + (dx1 + 2 * dx2 + 2 * dx3 + dx4) * h / 6.0
    y = y + (dy1 + 2 * dy2 + 2 * dy3 + dy4) * h / 6.0
    vx = vx + (dvx1 + 2 * dvx2 + 2 * dvx3 + dvx4) * h / 6.0
    vy = vy + (dvy1 + 2 * dvy2 + 2 * dvy3 + dvy4) * h / 6.0

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

def animate(frame):

    line_1.set_data(*spring((-2, 0), (x_values[frame], y_values[frame]), 10, 0.5))
    line_2.set_data(*spring((2, 0), (x_values[frame], y_values[frame]), 15, 0.5))

    return line_1, line_2

fig = plt.figure()
ax = plt.axes(xlim=(-2, 2), ylim=(-5, 2))
ax.set_aspect("equal", "box")
line_1 = ax.plot([], [], lw=1)[0]
line_2 = ax.plot([], [], lw=1)[0]

anim = FuncAnimation(fig, animate,
                     frames=TOTAL_FRAMES, interval=int(FRAMETIME*1000), blit=True)

plt.show()

anim.save("2_springs_2D.gif")
