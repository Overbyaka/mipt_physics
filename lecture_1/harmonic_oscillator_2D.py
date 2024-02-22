#%%
import math

import sympy as sp
# Проверка наших уравнений
x = sp.Function('x')
# l - длина от одной стены, до другой
t,k_1, k_2, m, d, l = sp.symbols('t, k_1, k_2, m, d, l')
eq = sp.Eq(-k_1*x(t) + k_2*(l-x(t)), m*x(t).diff(t,t))

# решает уравнение относительно t
# с начальными условиями
sol = sp.dsolve(eq, ics={x(0): 10, sp.diff(x(t), t).subs(t,0): 5, })
sol_t = sp.lambdify(t, sol.rhs.subs({k_1: 3, k_2: 3, m:1, d:0.1, l: 20}))

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
    x = anim_f[frame]
    l = 20
    h = 2;

    #y координату находим с помощью теоремы Пифагора
    line_1.set_data(*spring((0, 0), (x, x*h/l), 25, 0.5))
    line_2.set_data(*spring((l, h), (x, x*h/l), 25, 0.5))

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
