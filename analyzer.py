import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.widgets import TextBox
import tkinter as tk

def update_dashboard(function_string):
    try:
        ax.clear()
        x = sp.Symbol('x')
        eq = sp.simplify(function_string)
        
        # --- Mathematical Analysis Engine ---
        dif = sp.diff(eq, x)
        second_dif = sp.diff(dif, x)
        
        # Filter only real number
        roots = [r for r in sp.solve(eq, x) if r.is_real]
        critic = [c for c in sp.solve(dif, x) if c.is_real]
        inflection = [i for i in sp.solve(second_dif, x) if i.is_real]
        
        # Asymptotes
        vert_asym = [a for a in sp.singularities(eq, x) if a.is_real]
        lim_right = sp.limit(eq, x, sp.oo)
        lim_left = sp.limit(eq, x, -sp.oo)
        num, den = sp.fraction(eq)
        
        # --- Drawing Dara ---
        x_vals = np.linspace(-10, 10, 1000)
        f_num = sp.lambdify(x, eq, "numpy")
        y_vals = f_num(x_vals)
        y_vals[np.abs(y_vals) > 50] = np.nan

        # --- Visualization ---
        ax.plot(x_vals, y_vals, label='Function', color='#00e5ff', lw=2.5, zorder=3)

        # Asymptote Drawing
        for va in vert_asym:
            ax.axvline(x=float(va), color='red', linestyle='--', alpha=0.6)
        if lim_right.is_real:
            ax.axhline(y=float(lim_right), color='red', linestyle=':', alpha=0.5)
        if den != 1 and sp.degree(num, x) == sp.degree(den, x) + 1:
            oblique = sp.series(eq, x, sp.oo, 1).removeO()
            f_obl = sp.lambdify(x, oblique, "numpy")
            ax.plot(x_vals, f_obl(x_vals), color='orange', linestyle='-.', alpha=0.7)

        # Point Signs
        for r in roots:
            ax.scatter(float(r), 0, color='yellow', marker='*', s=150, zorder=5)
        for c in critic:
            ax.scatter(float(c), float(eq.subs(x, c)), color='green', s=80, zorder=5)
        for i in inflection:
            ax.scatter(float(i), float(eq.subs(x, i)), color='magenta', marker='x', s=100)

        # Information Board
        info_text = f"Roots: {len(roots)}\n"
        info_text += f"Critic Points: {len(critic)}\n"
        info_text += f"Inflection Points: {len(inflection)}"
        
        ax.text(0.02, 0.95, info_text, transform=ax.transAxes, verticalalignment='top', 
                color='cyan', fontsize=10, weight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a1a', alpha=0.8, edgecolor='cyan'))

        #  Aesthetic ve Lejand
        ax.axhline(0, color='white', lw=0.8)
        ax.axvline(0, color='white', lw=0.8)
        ax.grid(True, linestyle=':', alpha=0.2)
        ax.set_ylim(-20, 20)
        ax.set_xlim(-10, 10)
        
        # Spesific Lejand Symbols
        handles, labels = ax.get_legend_handles_labels()
        extra_handles = [
            Line2D([0], [0], marker='*', color='w', markerfacecolor='yellow', markersize=12, linestyle='None', label='Root'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8, linestyle='None', label='Critical Point'),
            Line2D([0], [0], marker='x', color='magenta', markerfacecolor='magenta', markersize=8, linestyle='None', label='Inflection')
        ]
        ax.legend(handles=handles + extra_handles, loc='upper right', facecolor='#1a1a1a', edgecolor='gray')
        
        plt.draw()
    except Exception as e:
        print(f"Error: {e}")

# --- GUI SETUP ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 8), facecolor='#121212')
plt.subplots_adjust(bottom=0.2)
def on_key(event):
    # Ctrl + V 
    if event.key == 'control' or event.key == 'v': 
        try:
            # Get the text from the system clipboard.
            root = tk.Tk()
            root.withdraw() # Prevent open new windows
            clipboard_text = root.clipboard_get()
            root.destroy()
            
            # Update Textbox Contents
            existing_text = text_box.text
            text_box.set_val(existing_text + clipboard_text)
        except:
            pass
axbox = plt.axes([0.2, 0.05, 0.6, 0.075], facecolor='#1a1a1a')
text_box = TextBox(axbox, 'Function: ', initial="(x**3 + 2*x**2) / (x**2 - 1)", color='#1a1a1a',hovercolor= '#1a1a1a')
text_box.label.set_color('white')
text_box.text_disp.set_color('cyan')
text_box.cursor.set_color('white')
text_box.on_submit(update_dashboard)
fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()