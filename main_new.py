import sys
from PyQt5.QtWidgets import QApplication
from ImageSelector import ImageViewer
from submain import Submain
from cam import Cam

if __name__ == "__main__":
    # Create the PyQt application
    app = QApplication(sys.argv)

    # Create the ImageViewer instance
    image_viewer = ImageViewer()

    # Define a function to handle the selected image file path
    def handle_image_selected(file_path):
        # Create an instance of Submain with the selected image path
        submain = Submain(file_path)
        
        # Run the Submain to process the image and obtain coordinates
        submain.run_submain()

        # Load the coordinates from Submain
        coordinates = submain.load_coordinates()

        # Execute the Cam with the loaded coordinates
        Cam.execute_cam(coordinates)

        # Close the application after processing
        app.quit()

    # Connect the image_selected signal to the handle_image_selected slot
    image_viewer.image_selected.connect(handle_image_selected)

    # Show the ImageViewer application and enter the event loop
    image_viewer.show()

    # Execute the application event loop
    sys.exit(app.exec_())
