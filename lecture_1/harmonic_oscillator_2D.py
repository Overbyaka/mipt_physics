#%%
import math

import sympy as sp
# Проверка наших уравнений
xy = sp.Function('xy')

# l - длина от одной стены, до другой, h - высота между пружинами
t,k_1, k_2, m, d, l, h = sp.symbols('t, k_1, k_2, m, d, l, h')
eq = sp.Eq(-k_1*xy(t) + k_2*(sp.sqrt(h*h + l*l)-xy(t)), m*xy(t).diff(t,t))

# решает уравнение относительно t
# с начальными условиями
sol = sp.dsolve(eq, ics={xy(0): math.sqrt(2*2+20*20)/2, sp.diff(xy(t), t).subs(t,0): 5, })
sol_t = sp.lambdify(t, sol.rhs.subs({k_1: 3, k_2: 3, m:1, d:0.1, l: 20, h: 2}))

#%%
sol_t

#%%
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from spring import spring

ANIM_TIME = 5 # seconds
FPS = 45
FRAMETIME = 1 / FPS # in seconds
TOTAL_FRAMES = ANIM_TIME * FPS

ts = np.linspace(0, ANIM_TIME, FPS * ANIM_TIME)

anim_f = sol_t(ts)

def animate(frame):
    l = 20
    h = 2
    cos = math.sqrt(1/(1+(h*h)/(l*l)))
    sin = math.sqrt(1/(1+(l*l)/(h*h)))
    #1+tg^2=1/cos^2
    #1+ctg^2=1/sin^2
    x = anim_f[frame]*cos
    y = anim_f[frame]*sin

    line_1.set_data(*spring((0, 0), (x, y), 25, 0.5))
    line_2.set_data(*spring((l, h), (x, y), 25, 0.5))

    return line_1, line_2

fig = plt.figure()
ax = plt.axes(xlim=(0, 20), ylim=(-2, 4))
ax.set_aspect("equal", "box")
line_1 = ax.plot([], [], lw=1)[0]
line_2 = ax.plot([], [], lw=1)[0]

anim = FuncAnimation(fig, animate,
                     frames=TOTAL_FRAMES, interval=int(FRAMETIME*1000), blit=True)

plt.show()

anim.save("2_springs_2D.gif")
