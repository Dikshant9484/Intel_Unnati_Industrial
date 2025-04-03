import cv2
import numpy as np
import random
import time

# Define object properties
COLORS = {'red': (0, 0, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0)}
SHAPES = ['circle', 'square', 'triangle']
PICK_POSITION = (300, 150)
PLACE_POSITIONS = {'red': (100, 300), 'green': (300, 300), 'blue': (500, 300)}

# Generate stacked objects
def generate_objects(num_objects=5):
    objects = []
    stack_x, stack_y = 300, 100
    for i in range(num_objects):
        color = random.choice(list(COLORS.keys()))
        shape = random.choice(SHAPES)
        size = random.randint(20, 50)
        objects.append({'color': color, 'shape': shape, 'size': size, 'position': (stack_x, stack_y - i * 30)})
    return objects

# Draw different shapes
def draw_shape(img, shape, position, size, color):
    if shape == 'circle':
        cv2.circle(img, position, size, color, -1)
    elif shape == 'square':
        top_left = (position[0] - size, position[1] - size)
        bottom_right = (position[0] + size, position[1] + size)
        cv2.rectangle(img, top_left, bottom_right, color, -1)
    elif shape == 'triangle':
        pts = np.array([[position[0], position[1] - size],
                        [position[0] - size, position[1] + size],
                        [position[0] + size, position[1] + size]], np.int32)
        cv2.fillPoly(img, [pts], color)

# Draw a warehouse-like background
def draw_warehouse_background(img):
    img[:] = (210, 210, 210)  # Light grey background
    cv2.rectangle(img, (50, 50), (550, 350), (180, 180, 180), -1)  # Warehouse floor
    cv2.rectangle(img, (100, 50), (500, 80), (120, 120, 120), -1)  # Shelf top
    cv2.rectangle(img, (100, 80), (120, 250), (100, 100, 100), -1)  # Left shelf
    cv2.rectangle(img, (480, 80), (500, 250), (100, 100, 100), -1)  # Right shelf
    cv2.putText(img, "Warehouse Sorting System", (140, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)

# Draw a realistic robotic arm with joints
def draw_robotic_arm(img, shoulder, elbow, wrist, gripper):
    # Draw arm segments
    cv2.line(img, shoulder, elbow, (50, 50, 50), 8)
    cv2.line(img, elbow, wrist, (50, 50, 50), 6)

    # Draw joints
    cv2.circle(img, shoulder, 10, (0, 0, 0), -1)
    cv2.circle(img, elbow, 8, (0, 0, 0), -1)
    cv2.circle(img, wrist, 6, (0, 0, 0), -1)

    # Draw gripper
    cv2.rectangle(img, (gripper[0] - 10, gripper[1] - 5), (gripper[0] + 10, gripper[1] + 5), (0, 0, 0), -1)

# Simulate robotic arm picking and placing
def robotic_arm_simulation(objects):
    for obj in objects:
        print(f"Picking Object -> Color: {obj['color'].capitalize()}, Shape: {obj['shape'].capitalize()}, Size: {obj['size']}")

        # Create warehouse background
        img = np.zeros((400, 600, 3), dtype=np.uint8)
        draw_warehouse_background(img)

        color_bgr = COLORS[obj['color']]
        place_position = PLACE_POSITIONS[obj['color']]
        
        # Draw stacked objects
        for stacked_obj in objects:
            draw_shape(img, stacked_obj['shape'], stacked_obj['position'], stacked_obj['size'], COLORS[stacked_obj['color']])

        # Draw bins
        cv2.rectangle(img, (50, 280), (150, 350), (0, 0, 0), 2)
        cv2.rectangle(img, (250, 280), (350, 350), (0, 0, 0), 2)
        cv2.rectangle(img, (450, 280), (550, 350), (0, 0, 0), 2)
        cv2.putText(img, "Red Bin", (60, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        cv2.putText(img, "Green Bin", (260, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        cv2.putText(img, "Blue Bin", (460, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # Move robotic arm step by step
        shoulder = (300, 50)
        elbow = (300, 100)
        wrist = (obj['position'][0], 150)
        gripper = obj['position']

        for step in range(150, 250, 10):
            frame = img.copy()
            wrist = (wrist[0], step)
            gripper = (gripper[0], step)
            draw_robotic_arm(frame, shoulder, elbow, wrist, gripper)
            draw_shape(frame, obj['shape'], gripper, obj['size'], color_bgr)
            cv2.imshow("Robotic Arm Simulation", frame)
            cv2.waitKey(100)

        # Move to placement bin
        for step_x in range(gripper[0], place_position[0], 10 if place_position[0] > gripper[0] else -10):
            frame = img.copy()
            wrist = (step_x, 250)
            gripper = (step_x, 250)
            draw_robotic_arm(frame, shoulder, elbow, wrist, gripper)
            draw_shape(frame, obj['shape'], gripper, obj['size'], color_bgr)
            cv2.imshow("Robotic Arm Simulation", frame)
            cv2.waitKey(100)

        # Final placement
        frame = img.copy()
        draw_robotic_arm(frame, shoulder, elbow, wrist, place_position)
        draw_shape(frame, obj['shape'], place_position, obj['size'] - 5, color_bgr)  # Shrink object slightly
        cv2.imshow("Robotic Arm Simulation", frame)
        cv2.waitKey(500)

        print(f"Placed in {obj['color'].capitalize()} Bin ✅")
        print("Objects are being sorted...")
        time.sleep(0.5)

    cv2.destroyAllWindows()

# Generate and simulate
objects = generate_objects(5)
robotic_arm_simulation(objects)
