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
  ## 1) Plotting multiple trajectories in 2D
  `python3 trajectory_visualization2D.py svin_Trajectory01.txt svin_Tajectory02.txt`

  command used to plot the following:
```bash python3 trajectory_visualization2D.py svin_2024_11_12_23_13_40CatacombsCenter.txt svin_2024_11_13_02_38_05CatacombsLeft.txt svin_2024_11_13_21_18_52CatacombsRight.txt```

  <img src="https://github.com/user-attachments/assets/3c5e31f5-2a96-4e70-a292-c7cc1f64f054" width="400" height="300">

  ## 2) Plotting trajectories in 3D
  `python3 trajectory_visualization3D.py  svin_Trajectory01.txt`
  
  <img src="https://github.com/user-attachments/assets/8c425b68-4abd-4b3d-b142-6c2d04d8bde5" width="400" height="300">

  ## 3) Plotting trajectories with furthest left and right points
  `python3 trajectory_visualization2D.py  svin_Trajectory01.txt --point_cloud Challenge2OGpointcloud1.ply --plot`
  
   <img src="https://github.com/user-attachments/assets/cc81ef5d-cd88-467f-ae35-dc3a8795df25" width="400" height="300">








  
