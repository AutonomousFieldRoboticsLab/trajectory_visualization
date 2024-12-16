# Copyright Tsbih Salman
import math
import numpy as np
import pandas as pd
import open3d as o3d
import matplotlib.pyplot as plt
from evo.core.trajectory import PoseTrajectory3D
from mpl_toolkits.mplot3d import Axes3D
import argparse

# Read the camera trajectory data
def read_traj(file_path: str) -> PoseTrajectory3D:
    with open(file_path, newline="") as file:
        lines = [line.strip().split() for line in file if not line.startswith("#")]
    
    data = np.array([[float(value) for value in line] for line in lines]).astype(float)
    data = data[:, :8] 
    
    df = pd.DataFrame(data, columns=["timestamp", "x", "y", "z", "qw", "qx", "qy", "qz"])
    df.sort_values(by=["timestamp"], inplace=True)
    
    sorted_data = df.to_numpy()
    
    time_stamps = sorted_data[:, 0]  # n x 1
    coordinates = sorted_data[:, 1:4]  
    quaternion = sorted_data[:, 4:] 
    quaternion = np.roll(quaternion, 1, axis=1) 
    
    if not hasattr(file_path, "read"): 
        print(f"Loaded {len(time_stamps)} timestamps and poses from: {file_path}")
    
    return PoseTrajectory3D(coordinates, quaternion, time_stamps)

# Read a point cloud file
def read_point_cloud(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    points = np.asarray(pcd.points)
    return pd.DataFrame(points, columns=['x', 'y', 'z'])

def calculate_heading(point_a, point_b):
    x_A, y_A, z_A = point_a
    x_B, y_B, z_B = point_b

    # Calculate the direction vector D
    D = (x_B - x_A, y_B - y_A, z_B - z_A)
    
    # Calculate the magnitude of the direction vector
    magnitude_D = math.sqrt(D[0]**2 + D[1]**2 + D[2]**2)

    # Normalize the direction vector
    D_normalized = (D[0] / magnitude_D, D[1] / magnitude_D, D[2] / magnitude_D)

    # Calculate the azimuth angle (horizontal direction)
    azimuth = math.atan2(D[1], D[0])  # in radians

    # Calculate the elevation angle (vertical direction)
    elevation = math.asin(D[2] / magnitude_D)  

    azimuth_deg = math.degrees(azimuth)
    elevation_deg = math.degrees(elevation)

    return {
        "direction_vector": D,
        "normalized_direction_vector": D_normalized,
        "azimuth_radians": azimuth,
        "elevation_radians": elevation,
        "azimuth_degrees": azimuth_deg,
        "elevation_degrees": elevation_deg
    }

def calculate_camera_trajectory_headings(traj: PoseTrajectory3D):
    headings = []
    positions = traj.positions_xyz

    for i in range(len(positions) - 1):
        point_a = positions[i]
        point_b = positions[i + 1]
        heading = calculate_heading(point_a, point_b)
        headings.append(heading)

    return headings

def find_left_right_points(traj_points, headings, distance):
    left_points = []
    right_points = []

    for i in range(len(traj_points) - 1): # loop through the points and skip the last one 
        x, y, z = traj_points[i]
        heading = headings[i]

        azimuth = heading['azimuth_radians'] # horizontal direction

        # Calculate left and right points
        left_x = x - distance * math.sin(azimuth)
        left_y = y + distance * math.cos(azimuth)
        right_x = x + distance * math.sin(azimuth)
        right_y = y - distance * math.cos(azimuth)

        left_point = [left_x, left_y, z]
        right_point = [right_x, right_y, z]

        if i > 0: # check for the first point
            previous_left_point = left_points[-1]
            previous_right_point = right_points[-1]
            left_distance = np.linalg.norm(np.array(left_point) - np.array(previous_left_point))
            right_distance = np.linalg.norm(np.array(right_point) - np.array(previous_right_point))

            if left_distance >= 1 and right_distance >= 1: # check if distance between points is greater than or equal to 1 meter 
                left_points.append(left_point)
                right_points.append(right_point)
        else:
            left_points.append(left_point)
            right_points.append(right_point)

    return np.array(left_points), np.array(right_points)

def calculate_distances(points):
    distances = []
    for i in range(len(points) - 1):
        point_a = points[i]
        point_b = points[i + 1]
        distance = np.linalg.norm(point_b - point_a)
        distances.append(distance)
    return distances

def calculate_trajectory_length(traj: PoseTrajectory3D) -> float:
    positions = traj.positions_xyz  # Extract the trajectory points
    total_length = 0.0

    # Sum the distances between consecutive points
    for i in range(len(positions) - 1):
        point_a = positions[i]
        point_b = positions[i + 1]
        total_length += np.linalg.norm(point_b - point_a)

    return total_length
     
# Write to a file
def write_points_to_file(file_path, traj: PoseTrajectory3D, left_points: np.ndarray, right_points: np.ndarray):
    with open(file_path, 'w') as file:
        file.write("Camera Trajectory Points:\n")
        for point in traj.positions_xyz:
            file.write(f"{point[0]} {point[1]} {point[2]}\n")
        
        file.write("\nLeft Points:\n")
        for point in left_points:
            file.write(f"{point[0]} {point[1]} {point[2]}\n")
        
        file.write("\nRight Points:\n")
        for point in right_points:
            file.write(f"{point[0]} {point[1]} {point[2]}\n")

def write_distances_to_file(file_path, left_distances, right_distances):
    with open(file_path, 'w') as file:
        file.write("Distances between consecutive furthest left points:\n")
        for dist in left_distances:
            file.write(f"{dist}\n")
        
        file.write("\nDistances between consecutive furthest right points:\n")
        for dist in right_distances:
            file.write(f"{dist}\n")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Process one or more camera trajectory files with optional point cloud data."
    )
    parser.add_argument(
        "trajectory_files",
        type=str,
        nargs='+',  # Allows multiple file paths
        help="Paths to one or more camera trajectory files (e.g., trajectory1.txt trajectory2.txt)."
    )
    parser.add_argument(
        "--point_clouds",
        type=str,
        nargs='+',  # Accepts multiple file paths
        help="Paths to one or more point cloud files corresponding to the trajectory files (optional)."
    )
    parser.add_argument(
        "--distance",
        type=float,
        default=1.0,
        help="Distance in meters to calculate left and right points (default: 1.0)."
    )
    parser.add_argument(
        "--plot",
        action="store_true",  
        help="Flag to plot both the furthest left and right points along with the trajectory."
    )
    parser.add_argument(
        "--left",
        action="store_true",  
        help="Plot only the furthest left points along with the trajectory."
    )
    parser.add_argument(
        "--right",
        action="store_true",  
        help="Plot only the furthest right points along with the trajectory."
    )

    args = parser.parse_args()

    # Initialize the 3D plot
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')  # Add a 3D subplot

    # Process each trajectory file
    for idx, trajectory_file_path in enumerate(args.trajectory_files):
        print(f"Processing trajectory file: {trajectory_file_path}")
        trajectory = read_traj(trajectory_file_path)  # Load the trajectory

        # Calculate the total length of the trajectory
        trajectory_length = calculate_trajectory_length(trajectory)
        print(f"Total camera trajectory length for {trajectory_file_path}: {trajectory_length:.2f} meters")

        # Calculate headings for the trajectory
        headings = calculate_camera_trajectory_headings(trajectory)

        # Calculate left and right points
        left_points, right_points = find_left_right_points(trajectory.positions_xyz, headings, args.distance)

        # Get color for this trajectory
        color = plt.colormaps["viridis"](idx / len(args.trajectory_files))

        # Plot based on the flags
        ax.plot(trajectory.positions_xyz[:, 0], trajectory.positions_xyz[:, 1], trajectory.positions_xyz[:, 2], label=f'Trajectory {idx + 1}', color=color)

        if args.left:
            ax.scatter(left_points[:, 0], left_points[:, 1], left_points[:, 2], label=f'Left Points {idx + 1}', color='red', s=10)
        if args.right:
            ax.scatter(right_points[:, 0], right_points[:, 1], right_points[:, 2], label=f'Right Points {idx + 1}', color='green', s=10)
        if args.plot:
            ax.scatter(left_points[:, 0], left_points[:, 1], left_points[:, 2], label=f'Left Points {idx + 1}', color='red', s=10)
            ax.scatter(right_points[:, 0], right_points[:, 1], right_points[:, 2], label=f'Right Points {idx + 1}', color='green', s=10)

    # Finalize the plot
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.title('3D Trajectories with Furthest Left and Right Points')
    plt.show()

if __name__ == "__main__":
    main()



