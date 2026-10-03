from picamera2 import Picamera2
from pic_proccessing import StegerExtractor
from motor_control import StepperSerial
import time
import triangulation # Fixed typo in module name

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.set_controls({"AeEnable": False, "ExposureTime": 5000, "AnalogueGain": 1.0})

# ** hardware specifications **
baseline_mm = 255
laser_angle_deg = 35 
focal_length_x_px = 1739.13
focal_length_y_px = 1739.13
image_width_px = 1456
image_height_px = 1088
distance_to_center_mm = 350

# Convert to integer for clean loop logic
total_steps = int(360 / 1.8 * 8)
step_count = 0

#  ** inits of the classes **
steger = StegerExtractor(threshold=40)
# Removed 'self' and attached to module namespace
triangulation_engine = triangulation.TriangulationEngine(baseline_mm, laser_angle_deg, focal_length_x_px, focal_length_y_px, image_width_px, image_height_px)
stepper = StepperSerial("/dev/ttyESP", 115200, 2.0, 1.0)

point_cloud = []

def pipeline():
    global step_count
    
    picam2.start()

    # Standard loop condition
    while step_count < total_steps:
        frame = picam2.capture_array()
        pts = steger.process(frame)     

        for point in pts:  
            # Call method on the initialized class instance
            xyz_coordinate = triangulation_engine.calculate_3d_point(point[0], point[1])
            
            # Ensure the point is mathematically valid before passing it on
            if xyz_coordinate is not None:
                # Unpack the X, Y, Z tuple into separate arguments
                global_coords = triangulation.calculate_global_point(
                    xyz_coordinate[0], xyz_coordinate[1], distance_to_center_mm-xyz_coordinate[2], 
                    step_count, total_steps, 35, 10
                )
                point_cloud.append(global_coords)

        # Move stepper 5 times quickly
        for _ in range(5):
            stepper.step()
            
        # CRITICAL: Update the step count so the angle calculation knows we moved
        step_count += 5 
        print(f"progress: {(step_count/total_steps * 100):.1f}%")
        
    picam2.stop()

    filename = "my_first_scan.ply"

    with open(filename, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        # Unified the variable name to point_cloud
        f.write(f"element vertex {len(point_cloud)}\n") 
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("end_header\n")
        
        for (x, y, z) in point_cloud:
            f.write(f"{x:.4f} {y:.4f} {z:.4f}\n")

    print(f"Scan complete! Saved {len(point_cloud)} points to {filename}")

# Execute the main loop
pipeline()