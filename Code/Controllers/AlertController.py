import sys
import os
import time

from datetime import datetime
from PySide6.QtCore import QCoreApplication
class AlertController:
    def __init__(self, parent):
        self.parent = parent
        self.init_ui()
        self.make_connections()

    def send_alert(self, title: str, message: str, target: str):
        """
        Object to implement your own transmission API/Protocol
        """
        pass

    def init_ui(self):
        self.parent.ui.alert_error_label.setText("")
        self.parent.ui.alert_title_input.setText("")
        self.parent.ui.alert_details_input.setText("")
        self.parent.ui.alert_team_input.setCurrentText("Choose")
        self.parent.ui.alert_error_label.setStyleSheet("color: white")

    def make_connections(self):
        self.parent.ui.alert_send_btn.clicked.connect(self.send_btn)
    
    def send_btn(self):
        self.parent.ui.alert_error_label.setText("")
        self.parent.ui.alert_error_label.setStyleSheet("color: white")

        if self.parent.ui.alert_team_input.currentText() == "Choose":
            self.parent.ui.alert_error_label.setText("Please Choose Team!")
            return
        team = self.parent.ui.alert_team_input.currentText()

        if self.parent.ui.alert_title_input.text() == "":
            self.parent.ui.alert_error_label.setText("Please Enter Title!")
            return
        title = self.parent.ui.alert_title_input.text()

        if self.parent.ui.alert_details_input.toPlainText() == "":
            self.parent.ui.alert_error_label.setText("Please Enter Details!")
            return
        details = self.parent.ui.alert_details_input.toPlainText()

        current_time = datetime.now()

        self.send_alert(title, details, team)

        self.parent.ui.alert_error_label.setText(f"Alert Send Successfully at {current_time}")
        QCoreApplication.processEvents()
        time.sleep(3)
        self.parent.ui.alert_error_label.setStyleSheet("color: green")
        self.parent.ui.alert_error_label.setText("Alert Received By The Team Successfully!")
        