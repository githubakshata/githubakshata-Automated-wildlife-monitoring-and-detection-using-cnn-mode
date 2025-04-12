import sys
import os
from datetime import datetime

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

class InferenceController(QWidget):
    def __init__(self, parent):
        self.parent = parent
        
        self.list_view = self.parent.ui.infer_list_view

    @Slot(str)
    def add_inference(self, message: str):
        current_time = str(datetime.now())[:-7]
        self.list_view.addItem(f"{current_time} : {message}")
    
    def clear_inference(self):
        self.list_view.clear()