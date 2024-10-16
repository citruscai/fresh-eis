import math

# Function to calculate the distance in 2D
def calculate_distance_2d(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Function to calculate the azimuth angle in the xy-plane
def calculate_azimuth(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle = math.atan2(delta_y, delta_x)  # Calculate the angle in radians
    return math.degrees(angle)  # Convert to degrees

# Function to calculate the angle of elevation between you and the target
def calculate_elevation(delta_z, distance_xy):
    return math.degrees(math.atan2(delta_z, distance_xy))

# Function to calculate the Z-coordinate of the target
def calculate_z_target(moving_object, target_2d, delta_z):
    x3, y3, z3 = moving_object
    x_target, y_target = target_2d
    z_target = z3 + delta_z
    return z_target

# Function to handle tracking logic
def track_target(moving_object, target_2d, delta_z):
    x3, y3, z3 = moving_object
    x_target, y_target = target_2d

    # Calculate the 2D distance between the moving object and the target
    distance_xy = calculate_distance_2d(x3, y3, x_target, y_target)

    # Calculate the azimuth angle
    azimuth_angle = calculate_azimuth(x3, y3, x_target, y_target)

    # Calculate the elevation angle
    z_target = calculate_z_target(moving_object, target_2d, delta_z)
    elevation_angle = calculate_elevation(z_target - z3, distance_xy)

    # If distance is greater than 5 meters, return only the azimuth angle
    if distance_xy > 5:
        return {"status": "azimuth", "azimuth": azimuth_angle}

    # If distance is less than or equal to 5 meters, return both angles and exact position
    else:
        return {
            "status": "position_and_angles",
            "azimuth": azimuth_angle,
            "elevation": elevation_angle,
            "x_target": x_target,
            "y_target": y_target,
            "z_target": z_target
        }

# Function to read positions from a file and process them
def process_positions_from_file(file_path):
    """
    Process each line from the input file and compute the azimuth and elevation angles.
    
    :param file_path: Path to the file containing position data
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split and parse the line into float values (coordinates)
                values = list(map(float, line.strip().split(',')))

                # Moving object coordinates (x, y, z)
                moving_object = (values[0], values[1], values[2])

                # Target 2D coordinates (x_target, y_target)
                target_2d = (values[3], values[4])

                # Delta Z (difference in Z between the target and the moving object)
                delta_z = values[5]

                # Call the tracking function with the parsed values
                result = track_target(moving_object, target_2d, delta_z)

                # Output the result to standard output
                if result["status"] == "azimuth":
                    print(f"The azimuth angle to turn to the target is: {result['azimuth']} degrees")
                else:
                    print(f"The azimuth angle to turn to the target is: {result['azimuth']} degrees")
                    print(f"The elevation angle to the target is: {result['elevation']} degrees")
                    print(f"Exact position of the target: X = {result['x_target']}, Y = {result['y_target']}, Z = {result['z_target']}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

# Main entry point
if __name__ == "__main__":
    # File path containing positions (update with the actual file path)
    file_path = "positions.txt"  # Example file name

    # Call the function to process positions from the file
    process_positions_from_file(file_path)
