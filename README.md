# RawAccel Alternative

A Python-based application providing a graphical user interface for creating custom mouse acceleration curves for Hyprland, similar in concept to RawAccel.

## Features

* **Interactive Curve Editing:** Create custom acceleration curves by dragging points on a graph.
* **Preset Curves:** Choose from several built-in acceleration presets (Linear, Natural, Power, etc.).
* **Custom Curve Input:** Define your own curve by entering comma-separated y-values.
* **Subdivision Control:** Adjust the number of subdivisions for the curve.
* **Output Display:** Displays the curve parameters in a format similar to libinput's custom acceleration profile.

## Prerequisites

* Python 3.6 or later
* Required Python packages: `tkinter`, `matplotlib`, `numpy`
* On Arch:
  ```bash
  yay -S --needed python-matplotlib python-numpy tk
  ```

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/arnaav11/custom_accel_hyprland.git
    cd custom_accel_hyprland
    ```
2.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
    On Arch:
    ```bash
    yay -S --needed python-matplotlib python-numpy tk
    ```

## How to Use

1.  Run the application:
    ```bash
    python main.py
    ```
2.  Use the GUI to create or select an acceleration curve.
    * Drag the points on the graph to modify the curve.
    * Select a preset from the dropdown menu.
    * Enter comma-separated values in the "Enter Custom Curve" dialog.
    * Adjust the number of subdivisions using the entry box and "Update" button.
3.  The "Output" text box will display the curve parameters.
4.  Click "Apply" to apply the changes.
5.  In the "Output" box, there should be a line that you can copy and paste into you hyprland.conf under input
6.  Done!

## Screenshot
![image](https://github.com/user-attachments/assets/fa648b44-1ea0-407d-bf01-d4066ec66d1c)


