import math
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
T_0 = 0
Y_0 = 1

# Final point
T_FINAL = 5

# Steps
DT = 0.5
DT_EXACT = 0.01


# Functions
def f(t, y):
    return math.sin(t)**2 * y

def euler_step(t_i, y_i, dt, f):
    return y_i + dt*f(t_i, y_i)

def rk4_step(t_i, y_i, dt, f):
    k1 = f(t_i, y_i)
    k2 = f(t_i + dt/2, y_i + k1*dt/2)
    k3 = f(t_i + dt/2, y_i + k2*dt/2)
    k4 = f(t_i + dt, y_i + k3*dt)
    return y_i + dt/6*(k1 + 2*k2 + 2*k3 + k4)

def exact_solution(t_0, y_0, t):
    exp_arg = 1/2 * ( (t-t_0) - (math.sin(t)*math.cos(t) - math.sin(t_0)*math.cos(t_0)) )
    return y_0*math.exp(exp_arg)


# Computing high resolution exact result
t = T_0

ys_exact_hr = []
ts_exact_hr = []

while t < T_FINAL:
    ys_exact_hr.append(exact_solution(T_0, Y_0, t))
    ts_exact_hr.append(t)
    t += DT_EXACT

# Computing exact results
t = T_0

ts_exact_p = [T_0]
ys_exact_p = [Y_0]

while t < T_FINAL:
    t += DT
    ts_exact_p.append(t)
    ys_exact_p.append(exact_solution(T_0, Y_0, t))


# Computing approximate results
ts = [T_0]
ys_rk4 = [Y_0]
ys_euler = [Y_0]

t = T_0
y_rk4 = Y_0
y_euler = Y_0

while t < T_FINAL:
    # Solving with Runge-Kutta
    y_rk4 = rk4_step(t, y_rk4, DT, f)

    # Solving with Euler
    y_euler = euler_step(t, y_euler, DT, f)

    # Increasing t
    t += DT

    # Appending results
    ts.append(t)
    ys_rk4.append(y_rk4)
    ys_euler.append(y_euler)

# Info table
data = {'Time': ts,
        'Exact Solution': ys_exact_p,
        'RK4 Solution': ys_rk4,
        'Euler Solution': ys_euler}

df = pd.DataFrame(data)

# Show the data frame individualy
# print(df)

# Create new window
window = tk.Tk()
window.title("DataFrame Viewer")

# Add a text area to display the DataFrame
txt_area = scrolledtext.ScrolledText(window, width=40, height=12)
txt_area.insert(tk.INSERT, df)
txt_area.pack(expand=True, fill=tk.BOTH)

# Plotting
fig, graphic = plt.subplots(figsize=(6, 4))
graphic.plot(ts, ys_rk4, color='red', marker='o', linewidth=0.0, label='RK4')
graphic.plot(ts, ys_euler, color='green', marker='o', linewidth=0.0, label='Euler')
graphic.plot(ts_exact_p, ys_exact_p, color='black', marker='x', linewidth=0.0, label='Exact')
graphic.plot(ts_exact_hr, ys_exact_hr, color='blue', label='Exact')
graphic.legend()

# Show the graphic individualy
# graphic.show()

# Add the figure to the window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Start the GUI event loop
window.mainloop()