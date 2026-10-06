import math

class Triangulation:
    def __init__(self, baseline_mm, laser_angle_deg, focal_length_x_px, focal_length_y_px, image_width_px, image_height_px):
        self.b = baseline_mm
        self.theta = math.radians(laser_angle_deg)
        self.fx = focal_length_x_px
        self.fy = focal_length_y_px
        self.cx = image_width_px / 2.0
        self.cy = image_height_px / 2.0

    def calculate_3d_point(self, steger_x, steger_y):
        disparity = steger_x - self.cx
        denominator = (disparity / self.fx) + math.tan(self.theta)
        
        if denominator == 0:
            return None 
            
        z_depth = self.b / denominator
        real_x = (steger_x - self.cx) * (z_depth / self.fx)
        real_y = (steger_y - self.cy) * (z_depth / self.fy)
        
        return (real_x, real_y, z_depth)


# UN-INDENTED: This is now a standalone function in the module
def calculate_global_point(x, y, z, current_step, steps_per_rev, x_rot, z_rot):
    """
    Spins a static 3D point around the turntable's axis into a global point cloud coordinate.
    """
    alpha = (2.0 * math.pi * current_step) / steps_per_rev
    
    x_shifted = x - x_rot
    z_shifted = z - z_rot
    
    x_global = x_shifted * math.cos(alpha) + z_shifted * math.sin(alpha)
    y_global = y 
    z_global = -x_shifted * math.sin(alpha) + z_shifted * math.cos(alpha)

    return (x_global, y_global, z_global)