import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os

home = os.path.expanduser("~")
global_points = []
global_output = ""

class InteractiveLineChart:
    def __init__(self, root):
        self.root = root
        self.root.title("RawAccel Alternative")

        # Use GTK theme if available (cross-platform)
        try:
            ttk.Style().theme_use('clam')  # Good cross-platform theme
        except tk.TclError:
            print("Clam theme not available. Using default.")

        self.num_subdivisions = 10
        self.num_points = self.num_subdivisions + 1
        self.x_values = np.linspace(0, 1, self.num_points)
        self.points = list(np.linspace(0, 1, self.num_points))
        self.max_graph_value = 2  # Track the maximum y-value for the graph
        self.custom_points = None
        self.offset_points = self.points[:]
        self.offset = 0  # Initialize the offset attribute here
        self.is_custom = False # added to track custom state

        global global_points
        global_points = self.points[:]

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.line, = self.ax.plot(self.x_values, self.points, marker='o', linestyle='-', markersize=8)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, self.max_graph_value)
        self.ax.set_xticks(np.linspace(0, 1, self.num_points))
        self.ax.set_yticks(np.linspace(0, self.max_graph_value, self.num_points))
        self.ax.grid(True, linestyle='--', alpha=0.7)
        # self.ax.set_aspect('equal') # Remove this line
        self.fig.patch.set_facecolor('#f0f0f0')

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=10)

        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)

        self.dragging_point = None

        # Main frame for controls
        controls_frame = ttk.Frame(root, padding=10)
        controls_frame.pack(side=tk.TOP, fill=tk.X)

        # Preset dropdown
        self.preset_label = ttk.Label(controls_frame, text="Presets:")
        self.preset_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.presets = ["Custom","Linear", "Natural", "Power", "Ease In Out", "Ease In", "Ease Out", "Sine",
                        "Expo", "Log", "Sqrt", "Cubic", "Quintic", "Circular In", "Circular Out",
                        "Circular In Out", "Ease In Sine", "Ease Out Sine", "Ease In Out Sine",
                        "Ease In Quad", "Ease Out Quad", "Ease In Out Quad",
                        "Overshoot", "Overshoot Extreme", "Parabola", "Inverse Sqrt", "Scaled Linear", "Scaled Natural", "Scaled Power"] # changed the order
        self.preset_var = tk.StringVar()
        self.preset_var.set(self.presets[0])
        self.preset_dropdown = ttk.Combobox(controls_frame, textvariable=self.preset_var, values=self.presets, state="readonly")
        self.preset_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        self.preset_dropdown.bind("<<ComboboxSelected>>", self.apply_preset)

        # Subdivision textbox
        self.subdivision_label = ttk.Label(controls_frame, text="Subdivisions:")
        self.subdivision_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.subdivision_sv = tk.StringVar()
        self.subdivision_sv.set("")
        self.subdivision_entry = ttk.Entry(controls_frame, width=10, textvariable=self.subdivision_sv)
        
        self.subdivision_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.update_button = ttk.Button(controls_frame, text="Update Graph", command=self.update_graph)
        self.update_button.grid(row=1, column=2, padx=5, pady=5, sticky='w')

        # Max Speed Input
        self.max_speed_label = ttk.Label(controls_frame, text="DPI:")
        self.max_speed_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.max_speed_sv = tk.StringVar()
        # self.max_speed_sv.set("")
        # self.subdivision_entry = ttk.Entry(controls_frame, width=10, textvariable=self.max_speed_sv)
        self.max_speed_entry = ttk.Entry(controls_frame, width=10, textvariable=self.max_speed_sv)
        self.max_speed_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Offset Input
        self.offset_label = ttk.Label(controls_frame, text="Offset:")
        self.offset_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.offset_sv = tk.StringVar()
        # self.offset_sv.set("")
        self.offset_entry = ttk.Entry(controls_frame, width=10, textvariable=self.offset_sv)
        
        self.offset_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Reset and Apply buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky='we')
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_curve)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        self.apply_button = ttk.Button(button_frame, text="Apply", command=self.apply_changes)
        self.apply_button.pack(side=tk.LEFT, padx=5)
        self.disable_button = ttk.Button(button_frame, text="Disable", command=disable_config)
        self.disable_button.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = ttk.Label(root, text="Ready", anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Output Text
        self.output_label = ttk.Label(root, text="Output:")
        self.output_label.pack(padx=10, pady=(0, 0), anchor=tk.W)
        self.output_text = tk.Text(root, height=4, width=40, font=('Consolas', 10),
                                  background='#e0e0e0', foreground='#101010',
                                  insertbackground='#101010')
        self.output_text.pack(padx=10, pady=(0, 10), fill=tk.X)

        controls_frame.columnconfigure(1, weight=1)

        self.subdivision_entry.insert(0, "10")
        self.offset_entry.insert(0, "0")  # Default offset value
        self.max_speed_entry.insert(0, "800")  # Default value

        self.subdivision_sv.trace_add("write", self.offset_callback)
        self.max_speed_sv.trace_add("write", self.offset_callback)
        self.offset_sv.trace_add("write", self.offset_callback)

        # self.apply_preset()
        # self.apply_changes()

    def offset_callback(self, *args):
        if( (self.subdivision_entry.get() and int(self.subdivision_entry.get())) and (self.offset_entry.get()) and (self.max_speed_entry.get() and int(self.max_speed_entry.get()))):
            # self.apply_changes()
            pass
        else:
            print(self.max_speed_entry.get())

    def apply_changes(self):
        """Updates the global points and displays output."""
        global global_points
        # global_points = self.points[:]  # Do not update here. Do it in update_graph
        self.output_text.delete(1.0, tk.END)

        try:
            self.max_input_speed = float(self.max_speed_entry.get())  # Use max_speed_entry
            if self.max_input_speed <= 0:
                raise ValueError("Max input speed must be greater than 0.")
            # self.offset = float(self.offset_entry.get())  # Get offset value

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            self.status_label.config(text="Error: Invalid Input", foreground='red')
            return

        if self.num_subdivisions > 0:
            step = self.max_input_speed / self.num_points  # step
            # x_values = np.linspace(0, max_input_speed, self.num_points) # x values
            # y_values = [min(y + self.offset, 1) for y in self.points]
        else:
            step = 0
            # x_values = [0]
            # y_values = [min(y + self.offset, 1) for y in self.points]

        self.update_graph()  # Update the graph after applying changes
        output_string = "accel_profile = custom "
        output_string += f"{step:.3f} "
        output_string += " ".join(f"{y*self.max_input_speed:.3f}" for y in self.offset_points)
        self.output_text.insert(tk.END, output_string)
        change_conf(output_string)
        self.status_label.config(text="Changes Applied", foreground='green')

    def reset_curve(self):
        """Resets the curve."""
        self.points = list(np.linspace(0, self.max_graph_value, self.num_points))
        self.offset_points = self.points[:]
        self.offset = 0  # Reset offset
        self.offset_entry.delete(0, tk.END)
        self.offset_entry.insert(0, "0")
        global global_points
        global_points = self.points[:]
        self.line.set_ydata(self.points)
        self.canvas.draw()
        self.preset_var.set("Linear")
        self.status_label.config(text="Curve Reset", foreground='blue')
        self.is_custom = False

    def apply_preset(self, event=None):
        """Applies preset curves."""
        preset = self.preset_var.get()
        x = np.linspace(0, 1, self.num_points)

        self.is_custom = False
        if preset == "Linear":
            y = x
        elif preset == "Natural":
            y = x**2
        elif preset == "Power":
            y = x**3
        elif preset == "Ease In Out":
            y = (np.sin((x * np.pi) - np.pi / 2) + 1) / 2
        elif preset == "Ease In":
            y = 1 - np.cos((x * np.pi) / 2)
        elif preset == "Ease Out":
            y = np.sin((x * np.pi) / 2)
        elif preset == "Sine":
            y = np.sin(x * np.pi)
        elif preset == "Expo":
            y = (2**(x))-1
        elif preset == "Log":
            y = (np.log10(1 + 9 * x))
        elif preset == "Sqrt":
            y = np.sqrt(x)
        elif preset == "Cubic":
            y = x**3
        elif preset == "Quintic":
            y = x**5
        elif preset == "Circular In":
            y = 1 - np.sqrt(1 - x**2)
        elif preset == "Circular Out":
            y = np.sqrt(1 - (x - 1)**2)
        elif preset == "Circular In Out":
            y = [(1 - np.sqrt(1 - (2 * val - 1)**2)) / 2 if val < 0.5 else (np.sqrt(1 - (2 * val - 1)**2) + 1) / 2 for val in x]
        elif preset == "Ease In Sine":
            y = 1 - np.cos(x * np.pi / 2)
        elif preset == "Ease Out Sine":
            y = np.sin(x * np.pi / 2)
        elif preset == "Ease In Out Sine":
            y = -(np.cos(np.pi * x) - 1) / 2
        elif preset == "Ease In Quad":
            y = x**2
        elif preset == "Ease Out Quad":
            y = 1 - (1 - x) ** 2
        elif preset == "Ease In Out Quad":
            y = [2 * val**2 if val < 0.5 else 1 - (2 * (1 - val))**2 / 2 for val in x]
        elif preset == "Overshoot":
            amplitude = 1.5
            y = (amplitude + 1) * x**3 - amplitude * x**2
        elif preset == "Overshoot Extreme":
            amplitude = 1.7
            y = (amplitude + 1) * x**5 - amplitude * x**4
        elif preset == "Parabola":
            y = 4*x**2
        elif preset == "Inverse Sqrt":
            y = 1/np.sqrt(x) if x > 0 else 0
        elif preset == "Scaled Linear":
            y = x * self.max_graph_value
        elif preset == "Scaled Natural":
            y = x**2 * self.max_graph_value
        elif preset == "Scaled Power":
            y = x**3 * self.max_graph_value
        elif preset == "Custom":
            if self.custom_points:
                self.points = self.custom_points[:]
            else:
                self.custom_points = self.points[:]
            self.is_custom =  True
            # return

        # Apply the limit and offset
        if not self.is_custom:
            self.points = [max(0, val) for val in y]  # Ensure no negative values
            y_values = [val for val in self.points] # scale the points.  val is already scaled.
            self.offset_points = list(y_values)
        # self.is_custom = False # when preset is selected, it is not custom anymore

        global global_points
        global_points = self.points[:]
        self.update_graph(update_points=True)
        self.status_label.config(text=f"Preset Applied: {preset}", foreground='green')
        self.update_output_text()

    def update_graph(self, update_points=True):
        """Updates subdivisions and redraws the graph."""
        try:
            self.offset = float(self.offset_entry.get())  # Get the offset
            value = int(self.subdivision_entry.get())
            if 1 <= value <= 100:
                self.num_subdivisions = value
                self.num_points = self.num_subdivisions + 1
                self.x_values = np.linspace(0, 1, self.num_points)
                if update_points:
                    old_x_values = np.linspace(0, 1, len(self.points))
                    self.points = np.interp(self.x_values, old_x_values, self.points).tolist()
                    self.points = [max(0, val) for val in self.points] # Ensure no negative values
                    self.offset_points = [max(0, point + self.offset) for point in self.points] # Ensure no negatives
                    self.offset_points[0] = 0


                global global_points
                global_points = self.points[:]

                self.ax.clear()
                y_values = [min(point, self.max_graph_value) for point in self.points]
                self.line, = self.ax.plot(self.x_values, self.offset_points, marker='o', linestyle='-', markersize=8)
                self.ax.set_xlim(0, 1)
                self.ax.set_ylim(0, self.max_graph_value)
                self.ax.set_xticks(np.linspace(0, 1, self.num_points))
                self.ax.set_yticks(np.linspace(0, self.max_graph_value, self.num_points))
                self.ax.grid(True, linestyle='--', alpha=0.7)
                # self.ax.set_aspect('equal')  # Remove this line
                self.fig.patch.set_facecolor('#f0f0f0')

                self.canvas.draw()
                # self.apply_preset()
                self.status_label.config(text=f"Graph Updated", foreground='green')
                # self.update_output_text()
            else:
                messagebox.showerror("Error", "Subdivisions must be between 1 and 100.")
                self.status_label.config(text="Error: Invalid Subdivision Value", foreground='red')
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input. Please enter an integer. {e}")
            self.status_label.config(text="Error: Invalid Input", foreground='red')

    def on_press(self, event):
        """Handles mouse press."""
        if event.inaxes:
            for i, (x, y) in enumerate(zip(self.x_values, self.points)):
                if abs(x - event.xdata) < 1 / (2 * self.num_subdivisions):
                    self.dragging_point = i
                    # Switch to custom preset when a point is dragged
                    if not self.is_custom: # only switch if it was not custom before
                         self.preset_var.set("Custom")
                         self.is_custom = True
                    break

    def on_motion(self, event):
        """Handles mouse motion."""
        if self.dragging_point is not None and event.inaxes:
            snapped_y = event.ydata
            snapped_y = max(0, min(self.max_graph_value, snapped_y))
            self.points[self.dragging_point] = max(0, snapped_y - self.offset) # Ensure no negatives
            self.custom_points = self.points[:] # Store the points
            self.custom_points[self.dragging_point] =  max(0, snapped_y - self.offset)

            global global_points
            global_points = self.points[:]

            y_values = [max(0, point + self.offset) for point in self.points] # Ensure no negatives
            self.line.set_ydata(y_values)
            self.canvas.draw()

    def on_release(self, event):
        """Handles mouse release."""
        if self.dragging_point:
            self.dragging_point = None
            self.status_label.config(text="Curve Modified", foreground='blue')
            # self.apply_changes()

    def update_output_text(self):
        """Updates the output text box with the current curve data."""
        self.output_text.delete(1.0, tk.END)
        self.max_input_speed = float(self.max_speed_entry.get())
        if self.num_subdivisions > 0:
            step = self.max_input_speed
            # x_values = np.linspace(0, max_input_speed, self.num_points)
            y_values = [point for point in self.offset_points]
        else:
            step = 0
            # x_values = [0]
            y_values = [point for point in self.offset_points]

        output_string = "accel_profile = custom "
        output_string += f"{0.25/step:.3f} "
        output_string += " ".join(f"{y:.3f}" for y in y_values)
        self.output_text.insert(tk.END, output_string)

def change_conf(output_string):
    file = open(f"{home}/.config/hypr/hyprland.conf", "r+")
    s = file.readlines()

    for i in range(-1, -5, -1):
        print(s[i])
        if "input:accel_profile" in s[i]:
            s[i] = f"input:{output_string}"
            file.seek(0)
            file.truncate()
            file.writelines(s)
            return
    s.append(f"input:{output_string}")

    file.seek(0)
    file.truncate()
    file.writelines(s)

def disable_config(*args):
    file = open(f"{home}/.config/hypr/hyprland.conf", "r+")
    s = file.readlines()

    for i in range(-1, -5, -1):
        print(s[i])
        if "input:accel_profile" in s[i]:
            s[i] = f"#{s[i]}"
            file.seek(0)
            file.truncate()
            file.writelines(s)
            return

    file.seek(0)
    file.truncate()
    file.writelines(s)

if __name__ == "__main__":
    print(f"{home}/.config/hypr/hyprland.conf")
    root = tk.Tk()
    app = InteractiveLineChart(root)
    root.mainloop()
    print("[ ", end="")
    print(*global_points, sep=", ", end=" ]")
