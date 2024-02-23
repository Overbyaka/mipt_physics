#%%
import math

import sympy as sp
# Проверка наших уравнений
x = sp.Function('x')
y = sp.Function('y')
# l - длина от одной стены, до другой, h - высота между пружинами
t,k_1, k_2, m, d, l, h = sp.symbols('t, k_1, k_2, m, d, l, h')
eqx = sp.Eq(-k_1*x(t) + k_2*(l-x(t)), m*x(t).diff(t,t))
eqy = sp.Eq(-k_1*y(t) + k_2*(h-y(t)), m*y(t).diff(t,t))

# решает уравнение относительно t
# с начальными условиями
solx = sp.dsolve(eqx, ics={x(0): 10, sp.diff(x(t), t).subs(t,0): 7.5, })
soly = sp.dsolve(eqy, ics={y(0): 1, sp.diff(y(t), t).subs(t,0): 1, })
sol_tx = sp.lambdify(t, solx.rhs.subs({k_1: 3, k_2: 3, m:1, d:0.1, l: 20}))
sol_ty= sp.lambdify(t, soly.rhs.subs({k_1: 3, k_2: 3, m:1, d:0.1, h: 2}))

#%%
sol_ty

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

anim_fx = sol_tx(ts)
anim_fy = sol_ty(ts)

def animate(frame):
    x = anim_fx[frame]
    y = anim_fy[frame]
    l = 20
    h = 2;

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
