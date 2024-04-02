# +-----------------------------+
# Imports
import math
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# +-----------------------------+
# Constants
X_0 = 1
Y_0 = 1

# Final point
X_FINAL = 5

# Steps
H = 0.5
H_HR= 0.01

# +-----------------------------+
# Functions
def f(x, y):
    return math.sin(x)**2 * y

def euler_step(x_i, y_i, h, f):
    return y_i + h*f(x_i, y_i)

def rk4_step(x_i, y_i, h, f):
    k1 = f(x_i, y_i)
    k2 = f(x_i + h/2, y_i + k1*h/2)
    k3 = f(x_i + h/2, y_i + k2*h/2)
    k4 = f(x_i + h, y_i + k3*h)
    return y_i + h/6*(k1 + 2*k2 + 2*k3 + k4)

def exact_solution(x_0, y_0, x):
    exp_arg = 1/2 * ( (x-x_0) - (math.sin(x)*math.cos(x) - math.sin(x_0)*math.cos(x_0)) )
    return y_0*math.exp(exp_arg)

# +-----------------------------+
# Computing high resolution exact result
x = X_0

xs_exact_hr = [X_0]
ys_exact_hr = [Y_0]

while x < X_FINAL:
    x += H_HR
    xs_exact_hr.append(x)
    ys_exact_hr.append(exact_solution(X_0, Y_0, x))

# +-----------------------------+
# Computing exact results
x = X_0

ys_exact_p = [Y_0]

while x < X_FINAL:
    x += H
    ys_exact_p.append(exact_solution(X_0, Y_0, x))

# +-----------------------------+
# Computing approximate results with Euler
x = X_0

ys_euler = [Y_0]
y_euler = Y_0

while x < X_FINAL:
    y_euler = euler_step(x, y_euler, H, f)
    ys_euler.append(y_euler)
    x += H

# +-----------------------------+
# Computing approximate results with Runge-Kutta
x = X_0

ys_rk4 = [Y_0]
y_rk4 = Y_0

while x < X_FINAL:
    y_rk4 = rk4_step(x, y_rk4, H, f)
    ys_rk4.append(y_rk4)
    x += H

# +-----------------------------+
# Computing errors
x = X_0



# +-----------------------------+
# Computing x values
x = X_0

xs = [X_0]

while x < X_FINAL:
    x += H
    xs.append(x)

# +-----------------------------+
# Info table
data = {'x': xs,
        'y(Exact)': ys_exact_p,
        'y(RK4)': ys_rk4,
        'y(Euler)': ys_euler}

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
graphic.plot(xs, ys_rk4, color='red', marker='o', linewidth=0.0, label='RK4')
graphic.plot(xs, ys_euler, color='green', marker='o', linewidth=0.0, label='Euler')
graphic.plot(xs, ys_exact_p, color='black', marker='x', linewidth=0.0, label='Exact')
graphic.plot(xs_exact_hr, ys_exact_hr, color='blue', label='Exact')
graphic.legend()

# Show the graphic individualy
# graphic.show()

# Add the figure to the window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Start the GUI event loop
window.mainloop()