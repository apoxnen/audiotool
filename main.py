from PyQt6.QtWidgets import (
      QApplication, QVBoxLayout, QWidget, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6 import QtGui
import sys
import os

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("AudioTool by apoxnen")
        
        icon_path = os.path.abspath("icon.png")
        self.setWindowIcon(QtGui.QIcon(icon_path))
 
        layout = QVBoxLayout()
        self.setLayout(layout)
 
        self.label = QLabel("Vamos")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.adjustSize()
        layout.addWidget(self.label)
 
        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.record)
        layout.addWidget(self.record_button)
 
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_recording)
        layout.addWidget(self.stop_button)
 
    def record(self):
        self.record_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.stop_button
        self.label.setText("Recording...")
     
    def stop_recording(self):
        self.stop_button.setEnabled(False)
        self.record_button.setEnabled(True)
        self.label.setText("Done!")
         
 
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())


#SP_MediaPlay