import sys
import os

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog

class SettingsController:
    def __init__(self, parent: QObject):
        self.parent = parent
        
        self.make_connections()
        self.init_settings()
        
    def init_settings(self):
        cameras = self.parent.DBControl.fetch_cameras()
        appsettings = self.parent.DBControl.fetch_engine_data()
        settings = self.parent.DBControl.fetch_settings()

        self.parent.ui.trap1_path_label.setText(cameras["Trap1"]["CameraPath"])
        self.parent.ui.trap2_path_label.setText(cameras["Trap2"]["CameraPath"])
        self.parent.ui.trap3_path_label.setText(cameras["Trap3"]["CameraPath"])

        self.parent.ui.target_speces_name.setText(appsettings["Target Species"])
        self.parent.ui.rules_path_label.setText(settings["rules"]["path"])


    def make_connections(self):
        self.parent.ui.trap1_path_btn.clicked.connect(lambda: self.select_trap("Trap1"))
        self.parent.ui.trap2_path_btn.clicked.connect(lambda: self.select_trap("Trap2"))
        self.parent.ui.trap3_path_btn.clicked.connect(lambda: self.select_trap("Trap3"))

        self.parent.ui.rules_path_btn.clicked.connect(self.select_rules_path)
        self.parent.ui.settings_save_btn.clicked.connect(self.save_settings)

    def select_trap(self, trap_name: str):
        path, _ = QFileDialog.getOpenFileName(self.parent,"Open Camera", "", "Video Files (*.mp4 *.3gp)")
        print(path)
        if trap_name == 'Trap1':
            self.parent.ui.trap1_path_label.setText(path)
        elif trap_name == 'Trap2':
            self.parent.ui.trap2_path_label.setText(path)
        else:
            self.parent.ui.trap3_path_label.setText(path)

    def select_rules_path(self):
        path, _ = QFileDialog.getOpenFileName(self.parent,"Select Rules File", "", "Video Files (*.txt *.rules)")

        self.parent.ui.rules_path_label.setText(path)
    
    def save_settings(self):
        cameras = self.parent.DBControl.fetch_cameras()
        cameras["Trap1"]["CameraPath"] = self.parent.ui.trap1_path_label.text()
        cameras["Trap2"]["CameraPath"] = self.parent.ui.trap2_path_label.text()
        cameras["Trap3"]["CameraPath"] = self.parent.ui.trap3_path_label.text()

        appengine = self.parent.DBControl.fetch_engine_data()
        appengine["Target Species"] = self.parent.ui.target_speces_name.text()

        settings = self.parent.DBControl.fetch_settings()
        settings["rules"]["path"] = self.parent.ui.rules_path_label.text()

        self.parent.DBControl.save_settings("Cameras", cameras)
        self.parent.DBControl.save_settings("Settings", settings)
        self.parent.DBControl.save_settings("AppEngine", appengine)

        self.parent.add_traps()
        
        print("Settings Saved!")


class ModelsController:
    def __init__(self, parent: QObject):
        self.parent = parent
        
        self.make_connections()
        self.init_settings()
        
    def init_settings(self):
        models = self.parent.DBControl.fetch_models()

        self.parent.ui.detector_model_label.setText(models["AnimalDetector"]["model"])
        self.parent.ui.detector_proto_label.setText(models["AnimalDetector"]["proto"])
        self.parent.ui.class_model_label.setText(models["AnimalClassifier"]["model"])
        self.parent.ui.class_proto_label.setText(models["AnimalClassifier"]["proto"])
        self.parent.ui.relation_label.setText(models["RelationshipDetector"])
        self.parent.ui.diesese_label.setText(models["DieseaseDetector"])
        self.parent.ui.behaviour_label.setText(models["BehaviourDetector"])

    def make_connections(self):
        self.parent.ui.detector_model_btn.clicked.connect(lambda: self.select_model("detector_model"))
        self.parent.ui.detector_proto_btn.clicked.connect(lambda: self.select_model("detector_proto"))

        self.parent.ui.classifier_model_btn.clicked.connect(lambda: self.select_model("classifier_model"))
        self.parent.ui.classifier_proto_btn.clicked.connect(lambda: self.select_model("classifier_proto"))

        self.parent.ui.relationship_btn.clicked.connect(lambda: self.select_model("relationship_model"))
        self.parent.ui.disease_btn.clicked.connect(lambda: self.select_model("disease_model"))
        self.parent.ui.behaviour_btn.clicked.connect(lambda: self.select_model("behaviour_model"))
        self.parent.ui.models_save_btn.clicked.connect(self.save_model_settings)

    def select_model(self, model):
        path, _ = QFileDialog.getOpenFileName(self.parent,"Open Model", "", "Model Files (*.model *.pkf *.caffemodel *.txt)")

        if model == "detector_model":   
            self.parent.ui.detector_model_label.setText(path)
        elif model == "detector_proto":   
            self.parent.ui.detector_proto_label.setText(path)
        elif model == "classifier_model":   
            self.parent.ui.class_model_label.setText(path)
        elif model == "classifier_proto":   
            self.parent.ui.class_proto_label.setText(path)
        elif model == "relationship_model":   
            self.parent.ui.relation_label.setText(path)
        elif model == "disease_model":   
            self.parent.ui.diesese_label.setText(path)
        elif model == "behaviour_model":   
            self.parent.ui.behaviour_label.setText(path)
        else:
            pass
    
    def save_model_settings(self):
        models = self.parent.DBControl.fetch_models()

        models["AnimalDetector"]["model"] = self.parent.ui.detector_model_label.text()
        models["AnimalDetector"]["proto"] = self.parent.ui.detector_proto_label.text()
        models["AnimalClassifier"]["model"] = self.parent.ui.class_model_label.text()
        models["AnimalClassifier"]["proto"] = self.parent.ui.class_proto_label.text()
        models["RelationshipDetector"] = self.parent.ui.relation_label.text()
        models["DieseaseDetector"] = self.parent.ui.diesese_label.text()
        models["BehaviourDetector"] = self.parent.ui.behaviour_label.text()

        self.parent.DBControl.save_settings("Models", models)
        print("Model Settings Saved!")





