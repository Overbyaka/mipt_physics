#%%
import sympy as sp
# Проверка наших уравнений
x = sp.Function('x')

t,k_1, k_2, m,d = sp.symbols('t, k_1, k_2, m, d')
eq = sp.Eq(-(k_1+k_2)*x(t), m*x(t).diff(t,t))

# решает уравнение относительно t
# с начальными условиями
sol = sp.dsolve(eq, ics={x(0): 10, sp.diff(x(t), t).subs(t,0): 5, })
sol_t = sp.lambdify(t, sol.rhs.subs({k_1: 10, k_2: 5, m:1, d:0.1}))

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

anim_f = -sol_t(ts)

def animate(frame):
    x = anim_f[frame]

    line_1.set_data(*spring((0, 1), (x, 1), 20, 0.5))
    line_2.set_data(*spring((0, -1), (x, -1), 25, 0.5))

    return line_1, line_2

fig = plt.figure()
ax = plt.axes(xlim=(-11, 11), ylim=(-2, 2))
ax.set_aspect("equal", "box")
line_1 = ax.plot([], [], lw=1)[0]
line_2 = ax.plot([], [], lw=1)[0]

anim = FuncAnimation(fig, animate,
                     frames=TOTAL_FRAMES, interval=int(FRAMETIME*1000), blit=True)

plt.show()

anim.save("2_springs.gif")
