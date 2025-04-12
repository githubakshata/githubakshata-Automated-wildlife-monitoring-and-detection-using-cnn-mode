import sys
import os

import cv2

from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtCore import Slot, Signal

from AIEngine.animal_detector import AnimalDetector

class Trap:
    def __init__(self, name, camera_path):
        self.name = name
        self.path = camera_path

class MonitorController(QWidget):
    #inference_signal = Signal(str)
    def __init__(self, parent):
        self.parent = parent
        
        self._traps = []

        self.detector = AnimalDetector()
        #self.inference_signal.connect(parent.InferControl.add_inference)

    @Slot(str)
    def browse_camera(self, name=str):
        return QFileDialog.getOpenFileName(self.parent, "Open Camera", self.parent.home_dir, "Video Files (*.mp4 *.mkv *.3gp)")

    def add_trap(self, name, camera_path):
        trap = Trap(name, camera_path)
        self._traps.append(trap)

    @Slot(str)
    def show_trap(self, trap_name: str):
        try:
            _trap = None
            for trap in self._traps:
                if trap.name == trap_name:
                    _trap = trap
                    break
            
            if _trap is None:
                print('Trap Not Found!')
                return
            
            data = self.detector.detect( _trap.name, _trap.path)
            for animal in data:
                self.parent.InferControl.add_inference(f'Animal Detected from {trap_name}. Possible Classification: {animal}')
        except Exception as E:
            print(f'Error While Running Detector: {E}')

    def clean_up(self):
        self._traps = []