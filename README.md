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
- ` --point_clouds` : (Optional) Paths to point cloud files corresponding to the trajectory files.
- `--distance` : (Optional) Distance in meters to calculate left and right points, default is 1.0 meter.
- `--plot` : (Optional) Flag to plot both the furthest left and right points along with the trajectory.
- `--left` : (Optional) Flag to plot only the furthest left points.
- `--right` : (Optional) Flag to plot only the furthest right points.

  ## Examples
  There are some example trajectories and point cloud data files in the source folder.
  ## Plotting multiple trajectories in 2D
  `python3 trajectory_visualization2D.py svin_Trajectory01.txt svin_Tajectory02.txt`
![Screenshot from 2024-12-16 22-08-57](https://github.com/user-attachments/assets/95ad9ac1-fd3f-41cd-8400-ba9e0a81f528)
