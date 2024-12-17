# Trajectory_visualization
## Required libraries
- Python 3.x
- NumPy
- Pandas
- Matplotlib
- Open3D
- Evo
```bash command to install the required libraries
pip install numpy pandas matplotlib open3d evo
```
## Usage
The script can be executed with several command line arguments to specify input files and plotting preferences.
## Command Line Arguments
- trajectory_files: Paths to one or more camera trajectory files. Multiple files should be separated by spaces.
- '''bash --point_clouds''' : (Optional) Paths to point cloud files corresponding to the trajectory files.
- --distance: (Optional) Distance in meters to calculate left and right points, default is 1.0 meter.
- --plot: (Optional) Flag to plot both the furthest left and right points along with the trajectory.
- --left: (Optional) Flag to plot only the furthest left points.
- --right: (Optional) Flag to plot only the furthest right points.
