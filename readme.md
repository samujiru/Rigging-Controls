Rigging Controller Tool for Maya

Description
The Rigging Controller Tool is a Python-based utility for Autodesk Maya designed to streamline the rigging process. This tool allows users to quickly generate a variety of NURBS curve shapes to serve as animation controllers.

You can specify naming conventions and a toggle for Offset Groups. This ensures that controllers are brought into the scene with frozen transformations, adhering to professional rigging standards by keeping the controller's channels at zero while the group handles the world-space positioning.

How to operate
Once all the files are in the script tab in Maya, paste the following lines into the script editor tab:
import controller_ui
import importlib
importlib.reload(controller_ui)
controller_ui.show_ui()

File Structure
The project is structured to ensure modularity and ease of maintenance:

main.py: The execution script. It handles the sys.path configuration to ensure all modules are discoverable and contains the self-test logic for viewport verification.

core_utils.py: The library module containing all mathematical point data and builder functions for the NURBS shapes.

README.md: Project documentation, including function descriptions and usage instructions.

Core Builder Functions
The following functions are implemented in core_utils.py. Every function includes descriptive parameters, default values, and returns the name of the created object.

1. create_circle
Description: Generates a standard 2D NURBS circle.

2. create_cube
Description: Creates a 3D wireframe box using a single continuous NURBS curve.

3. create_sphere
Description: Generates a wireframe sphere consisting of three intersecting NURBS circles (XY, YZ, and ZX planes).

2. create_pyramid
Description: Creates a 3D wireframe pyramid using a single continuous NURBS curve.

5. create_gear
Description: Generates a custom NURBS shape with "teeth" to represent mechanical or rotational controls.

Technical Specifications
Module Docstrings: Every .py file includes a header describing the file's purpose and author information.

Dependency Management: main.py utilizes a sys.path block to dynamically source the core_utils module regardless of the local file path.

Self-Testing: The tool includes an if __name__ == "__main__": block in the main script. Running the script directly will:

Open a new Maya file.

Iterate through all 5 controller types.

Build them in the viewport to verify geometry and grouping logic.
