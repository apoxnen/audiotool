from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6 import QtGui
from time import time
import pyaudio
import sys
import os
import wave

class RecordingThread(QThread):
    stopped = False
    sig_started = pyqtSignal()
    sig_stopped = pyqtSignal()

    def __init__(self, target_file):
        self.target_file = target_file
        super().__init__()

    def run(self) -> None:
        # Record in chunks of 1024 samples
        chunk = 1024 
        
        # 16 bits per sample
        sample_format = pyaudio.paInt16 
        chanels = 2
        
        # Record at 44400 samples per second
        smpl_rt = 44400 

        timeout = 60000 # value in ms
        
        # Create an interface to PortAudio
        pa = pyaudio.PyAudio() 
        dev_index = 3

        print("Setting index for audio mixer")

        for i in range(pa.get_device_count()):
            dev = pa.get_device_info_by_index(i)
            if (dev['name'] == 'Stereo Mix (Realtek HD Audio Stereo input)' and dev['hostApi'] == 0):
                dev_index = dev['index']
                print('dev_index', dev_index)

        stream = pa.open(format=sample_format, channels=chanels,
                        rate=smpl_rt, input=True,
                        input_device_index = dev_index,
                        frames_per_buffer=chunk)
        
        print('Recording...')
        
        # Initialize array that be used for storing frames
        frames = [] 
        start_time = time()
        current_time = time()

        self.stopped = False
        self.sig_started.emit()

        while not self.stopped:
            data = stream.read(1024)
            frames.append(data)
            current_time = time()

        stream.stop_stream()
        stream.close()

        self.sig_stopped.emit()

        pa.terminate()
        wf = wave.open(self.target_file, 'wb')
        wf.setnchannels(chanels)
        wf.setsampwidth(pa.get_sample_size(sample_format))
        wf.setframerate(smpl_rt)
        wf.writeframes(b''.join(frames))
        wf.close()

    @pyqtSlot()
    def stop(self):
        self.stopped = True



class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("AudioTool by apoxnen")

        # Create recording thread and attach slots to its signals
        self.recording_thread = RecordingThread(target_file='test_recording.wav')
        self.recording_thread.sig_started.connect(self.recording_started)
        self.recording_thread.sig_stopped.connect(self.recording_stopped)

        # Create demucs thread and attach slots to its signals
        self.demucs_thread = RecordingThread(target_file='test_recording.wav')
        self.demucs_thread.sig_started.connect(self.demucs_started)
        self.demucs_thread.sig_stopped.connect(self.demucs_stopped)
        
        icon_path = os.path.abspath("icon.png")
        self.setWindowIcon(QtGui.QIcon(icon_path))
 
        layout = QVBoxLayout()

        self.label = QLabel("Ready")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.adjustSize()
        layout.addWidget(self.label)
 
        self.record_button = QPushButton('▶ Record')
        self.record_button.clicked.connect(self.recording_thread.start)
        layout.addWidget(self.record_button)
 
        self.stop_button = QPushButton("▪Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.recording_thread.stop)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    @pyqtSlot()
    def recording_started(self):
        """This slot is called when recording starts"""
        self.label.setText('◉ Recording...')
        self.stop_button.setDisabled(False)
        self.record_button.setDisabled(True)

    @pyqtSlot()
    def recording_stopped(self):
        """This slot is called when recording stops"""
        self.label.setText('Done!')
        self.record_button.setDisabled(False)
        self.stop_button.setDisabled(True)
    
    @pyqtSlot()
    def demucs_started(self):
        """This slot is called when demucs starts"""
        self.label.setText('Running demucs...')
        self.stop_button.setDisabled(True)
        self.record_button.setDisabled(True)

    @pyqtSlot()
    def demucs_stopped(self):
        """This slot is called when demucs is cancelled"""
        self.label.setText('Canceled!')
        self.record_button.setDisabled(False)
        self.stop_button.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()