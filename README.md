# RawAccel Alternative

A Python-based application providing a graphical user interface for creating custom mouse acceleration curves, similar in concept to RawAccel.

## Features

* **Interactive Curve Editing:** Create custom acceleration curves by dragging points on a graph.
* **Preset Curves:** Choose from several built-in acceleration presets (Linear, Natural, Power, etc.).
* **Custom Curve Input:** Define your own curve by entering comma-separated y-values.
* **Subdivision Control:** Adjust the number of subdivisions for the curve.
* **Output Display:** Displays the curve parameters in a format similar to libinput's custom acceleration profile.
* **Cross-Platform:** Uses Tkinter for the GUI and should run on Windows, macOS, and Linux.

## Prerequisites

* Python 3.6 or later
* Required Python packages: `tkinter`, `matplotlib`, `numpy`

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  Run the application:
    ```bash
    python your_script_name.py  # Replace with the actual name of your main Python file
    ```
2.  Use the GUI to create or select an acceleration curve.
    * Drag the points on the graph to modify the curve.
    * Select a preset from the dropdown menu.
    * Enter comma-separated values in the "Enter Custom Curve" dialog.
    * Adjust the number of subdivisions using the entry box and "Update" button.
3.  The "Output" text box will display the curve parameters.
4.  Click "Apply" to (placeholder) apply the changes.  (Note: The "Apply" button functionality is a placeholder and needs to be implemented.)

##  Custom Curve Input Format
To enter a custom curve, click on "Enter Custom Curve" and enter the y-values of the curve points, separated by commas. For example:
