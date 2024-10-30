import cv2
import json
import os
import numpy as np
from ImageSelector import ImageViewer

class Submain:
    def __init__(self, image_path):
        self.file_path = image_path
        self.image = cv2.imread(image_path)
        self.rectangles = []
        self.top_left = (0, 0)
        self.bottom_right = (0, 0)
        self.drawing = False
        self.rectangle_finished = False

    def resize_image(self, image, width, height):
        resized = cv2.resize(image, (width, height))
        return resized

    def draw_all_rectangles(self, image, rectangles):
        output_image = image.copy()
        for rectangle in rectangles:
            cv2.rectangle(output_image, rectangle[0], rectangle[1], (255, 0, 0), 2)
        return output_image

    def draw_rectangle(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.top_left = (x, y)
            self.rectangle_finished = False

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.bottom_right = (x, y)
                output_image = self.image_with_rectangles.copy()
                cv2.rectangle(output_image, self.top_left, self.bottom_right, (255, 0, 0), 2)
                cv2.imshow('Draw Rectangle', output_image)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.bottom_right = (x, y)
            self.rectangle_finished = True
            self.rectangles.append((self.top_left, self.bottom_right))
            self.image_with_rectangles[:] = self.draw_all_rectangles(self.resized_image, self.rectangles)

    def save_coordinates(self, coordinates):
        with open('xray_coordinates.json', 'w') as file:
            json.dump(coordinates, file)
   
    def load_coordinates(self):
        if os.path.exists('xray_coordinates.json'):
            with open('xray_coordinates.json', 'r') as file:
                return json.load(file)
        else:
            return []
    
    def run_submain(self):
        # Load the original image
        original_image = cv2.imread(self.file_path)
        # Resize the original image to 640x480 (or any desired width and height)
        self.resized_image = self.resize_image(original_image, 640, 480)
        # Set the resized image as the output image with rectangles
        self.image_with_rectangles = self.resized_image.copy()

        cv2.namedWindow('Draw Rectangle')
        cv2.setMouseCallback('Draw Rectangle', self.draw_rectangle)
        cv2.imshow('Draw Rectangle', self.image_with_rectangles)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        for i, rectangle in enumerate(self.rectangles):
            print(f"Rectangle {i + 1} Coordinates: {rectangle}")

        if self.rectangles:
            mask = np.zeros_like(self.image_with_rectangles[:, :, 0])
            for rectangle in self.rectangles:
                roi = self.image_with_rectangles[rectangle[0][1]:rectangle[1][1], rectangle[0][0]:rectangle[1][0]]
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray_roi, threshold1=120, threshold2=190)
                mask[rectangle[0][1]:rectangle[1][1], rectangle[0][0]:rectangle[1][0]] = edges

        coordinates = []
        for y in range(mask.shape[0]):
            for x in range(mask.shape[1]):
                if mask[y, x] != 0:
                    coordinates.append((x, y))

        self.save_coordinates(coordinates)


if __name__ == "__main__":
    def handle_image_selected(file_path):
        submain = Submain(file_path)
        submain.run_submain()

    image_viewer = ImageViewer()
    image_viewer.image_selected.connect(handle_image_selected)
    image_viewer.show()

