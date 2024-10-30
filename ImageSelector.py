import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt

class ImageViewer(QMainWindow):
    image_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 420, 360)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel(self)
        self.label.setFixedSize(400, 300)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        self.open_button = QPushButton("Open Image", self)
        self.open_button.clicked.connect(self.open_image)
        layout.addWidget(self.open_button, alignment=Qt.AlignCenter)

        self.file_dialog = QFileDialog(self, "Open Image", "", "Image files (*.jpg *.jpeg *.png *.bmp)")
        self.file_dialog.setFileMode(QFileDialog.ExistingFile)
        self.file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        self.file_dialog.setOption(QFileDialog.DontUseNativeDialog)
        self.file_dialog.fileSelected.connect(self.image_selected.emit)
        self.file_dialog.setWindowFlags(Qt.Sheet)
        self.file_dialog.setFixedSize(800, 600)

    def open_image(self):
        self.file_dialog.show()

    def print_image_path(self, file_path):
        pixmap = QPixmap(file_path)
        image = image.scaled(640, 480, aspectRatioMode=True)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)       
        print("Image selected:", file_path)
        return file_path
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    window.image_selected.connect(window.print_image_path)
    sys.exit(app.exec_())
