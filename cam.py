import cv2
import os
import time
from submain import Submain
from datetime import datetime

class Cam:
    @staticmethod
    def execute_cam(coordinates):
        def draw_coordinates(frame, coordinates, shift_x):
            frame_copy = frame.copy()  
            for coord in coordinates:
                x, y = coord
                x += shift_x
                cv2.circle(frame_copy, (x, y), 1, (0, 0, 255), 1)  
            return frame_copy

        cap = cv2.VideoCapture(0)  
        current_date = datetime.now().strftime("%Y-%m-%d")

        directory = os.path.join('captured_images', current_date)
        if not os.path.exists(directory):
            os.makedirs(directory)
        image_count = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            height, width = frame.shape[:2]
            shift_x = 10

            frame_with_visualization = draw_coordinates(frame, coordinates, shift_x)

            cv2.imshow('Camera Feed with Visualization', frame_with_visualization)

            key = cv2.waitKey(1)
            if key == ord(' ') or cv2.waitKey(1) == 32:
                image_count += 1
                current_time = time.strftime("%H-%M-%S")
                image_name = f'{image_count}_{current_time}.jpg'
                image_path = os.path.join(directory, image_name)
                cv2.imwrite(image_path, frame)
                print(f"Image captured and saved as {image_name} in {directory}")
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    submain = Submain()
    coordinates = submain.load_coordinates()  # Load coordinates from Submain
    Cam.execute_cam(coordinates)