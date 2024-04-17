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
X_0 = 0
Y_0 = 1

# Steps
H = 0.1
H_HR= 0.01

# Number of iterations
N = 5

# +-----------------------------+
# Functions
def f(x, y):
    return 6 * x ** 2 - 3 * x ** 2 * y

def euler_step(x_i, y_i, h, f):
    return y_i + h*f(x_i, y_i)

def rk4_step(x_i, y_i, h, f):
    k1 = f(x_i, y_i)
    k2 = f(x_i + h/2, y_i + k1*h/2)
    k3 = f(x_i + h/2, y_i + k2*h/2)
    k4 = f(x_i + h, y_i + k3*h)
    return y_i + h/6*(k1 + 2*k2 + 2*k3 + k4)

def exact_solution(x):
    return 2 - 1 / math.exp(x ** 3)

# +-----------------------------+
# Computing high resolution exact result
x = X_0

xs_exact_hr = [X_0]
ys_exact_hr = [Y_0]

while x < ((H * N) + X_0):
    x += H_HR
    xs_exact_hr.append(x)
    ys_exact_hr.append(exact_solution(x))

# +-----------------------------+
# Computing exact results
x = X_0

ys_exact_p = [Y_0]

for i in range(N):
    x += H
    ys_exact_p.append(exact_solution(x))

# +-----------------------------+
# Computing approximate results with Euler
x = X_0

ys_euler = [Y_0]
y_euler = Y_0

for i in range(N):
    y_euler = euler_step(x, y_euler, H, f)
    ys_euler.append(y_euler)
    x += H

# +-----------------------------+
# Computing approximate results with Runge-Kutta
x = X_0

ys_rk4 = [Y_0]
y_rk4 = Y_0

for i in range(N):
    y_rk4 = rk4_step(x, y_rk4, H, f)
    ys_rk4.append(y_rk4)
    x += H

# +-----------------------------+
# Computing errors
x = X_0

rk_abs_errs = []
rk_rel_errs = []
rk_rel_errs_p = []

euler_abs_errs = []
euler_rel_errs = []
euler_rel_errs_p = []

for i in range(N + 1):
    rk_abs_err = abs(ys_exact_p[i] - ys_rk4[i])
    rk_rel_err = rk_abs_err / ys_exact_p[i]
    rk_rel_err_p = rk_rel_err * 100
    
    euler_abs_err = abs(ys_exact_p[i] - ys_euler[i])
    euler_rel_err = euler_abs_err / ys_exact_p[i]
    euler_rel_err_p = euler_rel_err * 100
    
    rk_abs_errs.append(rk_abs_err)
    rk_rel_errs.append(rk_rel_err)
    rk_rel_errs_p.append(rk_rel_err_p)
    
    euler_abs_errs.append(euler_abs_err)
    euler_rel_errs.append(euler_rel_err)
    euler_rel_errs_p.append(euler_rel_err_p)
    
    x += H

# +-----------------------------+
# Computing x values
x = X_0

xs = [X_0]

for i in range(N):
    x += H
    xs.append(x)

# +-----------------------------+
# Rounding values
# xs = [round(value, 5) for value in xs]
# ys_exact_p = [round(value, 5) for value in ys_exact_p]
# ys_rk4 = [round(value, 5) for value in ys_rk4]
# rk_abs_errs = [round(value, 5) for value in rk_abs_errs]
# rk_rel_errs = [round(value, 5) for value in rk_rel_errs]
# rk_rel_errs_p = [round(value, 5) for value in rk_rel_errs_p]
# ys_euler = [round(value, 5) for value in ys_euler]
# euler_abs_errs = [round(value, 5) for value in euler_abs_errs]
# euler_rel_errs = [round(value, 5) for value in euler_rel_errs]
# euler_rel_errs_p = [round(value, 5) for value in euler_rel_errs_p]

# +-----------------------------+
# Info tables
data_rk = {'x': xs,
        'y(Exacta)': ys_exact_p,
        'y(RK4)': ys_rk4,
        'Err abs': rk_abs_errs,
        'Er rel': rk_rel_errs,
        'Err rel %': rk_rel_errs_p}

data_euler = {'x': xs,
        'y(Exacta)': ys_exact_p,
        'y(Euler)': ys_euler,
        'Err abs': euler_abs_errs,
        'Err rel': euler_rel_errs,
        'Err rel %': euler_rel_errs_p}

df_rk = pd.DataFrame(data_rk)
df_euler = pd.DataFrame(data_euler)

# Create new window
window = tk.Tk()
window.title("DataFrame Viewer")

# Add a text area to display the DataFrame
txt_area = scrolledtext.ScrolledText(window)
txt_area.insert(tk.INSERT, df_rk)
txt_area.insert(tk.END, '\n\n')
txt_area.insert(tk.INSERT, df_euler)
txt_area.pack(expand=True, fill=tk.BOTH)

# Plotting
plt.plot(xs, ys_rk4, color='red', marker='o', linewidth=0.0, label='RK4')
plt.plot(xs, ys_euler, color='green', marker='o', linewidth=0.0, label='Euler')
plt.plot(xs, ys_exact_p, color='blue', marker='x', linewidth=0.0, label='Exact')
plt.plot(xs_exact_hr, ys_exact_hr, color='black', label='Exact')
plt.legend()

# Show the graphic individualy
plt.show()

# Start the GUI event loop
window.mainloop()