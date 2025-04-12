import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow

from ui import Ui_AppUI
from Controllers.MonitorController import MonitorController
from Controllers.DBController import DBController
from Controllers.SettingsController import SettingsController, ModelsController
from Controllers.UserController import UserController
from Controllers.InferenceController import InferenceController
from Controllers.AlertController import AlertController

class WildLifeApp(QMainWindow):
    def __init__(self):
        super(WildLifeApp, self).__init__()
        
        self.ui = Ui_AppUI()
        self.ui.setupUi(self)

        self.home_dir = os.path.dirname(os.path.abspath(__file__))

        self.init_controllers()
        self.init_ui()
        self.make_connections()        
    
    def init_ui(self):
        self.ui.MainStack.setCurrentIndex(2)

    def init_controllers(self):
        self.DBControl = DBController(parent=self)
        self.UserControl = UserController(parent= self)
        self.SettingsControl = SettingsController(parent=self)
        self.ModelsControl = ModelsController(parent=self)
        self.InferControl = InferenceController(parent=self)
        self.MonitorControl = MonitorController(parent=self)
        self.AlertControl = AlertController(parent=self)

        self.add_traps()
    
    def add_traps(self):
        self.MonitorControl.clean_up()
        traps = self.DBControl.fetch_cameras()
        for trap in traps.values():
            self.MonitorControl.add_trap(trap["Name"], trap["CameraPath"])

    def make_connections(self):
        self.ui.loginbtn.clicked.connect(self.login_btn_clicked)
        self.ui.Db_Logout_btn.clicked.connect(self.logout_btn_clicked)

        self.ui.Db_monitor_btn.clicked.connect(self.monitor_page)
        self.ui.Db_inference_btn.clicked.connect(self.inference_page)
        self.ui.Db_Alert_btn.clicked.connect(self.alert_page)
        self.ui.Db_analysis_btn.clicked.connect(self.analysis_page)
        self.ui.Db_help_btn.clicked.connect(self.help_page)
        self.ui.Db_aboutus_btn.clicked.connect(self.aboutus_page)
        self.ui.Db_management_btn.clicked.connect(self.management_page)
        self.ui.Db_models_btn.clicked.connect(self.models_page)
        self.ui.Db_settings_btn.clicked.connect(self.settings_page)
        self.ui.Db_analysis_btn.clicked.connect(self.analysis_page)
        self.ui.Db_help_btn.clicked.connect(self.help_page)
        
        self.ui.aboutus_back_btn.clicked.connect(self.dashboard_page)
        self.ui.InferencePageBack_btn.clicked.connect(self.dashboard_page)
        self.ui.alertpage_back_btn.clicked.connect(self.dashboard_page)
        self.ui.monitorPageBack_btn.clicked.connect(self.dashboard_page)
        self.ui.userManage_BackBtn.clicked.connect(self.dashboard_page)
        self.ui.aimodels_backBtn.clicked.connect(self.dashboard_page)
        self.ui.settingsPage_backBtn.clicked.connect(self.dashboard_page)
        self.ui.analysisPage_back_btn.clicked.connect(self.dashboard_page)
        self.ui.helpPage_back_btn.clicked.connect(self.dashboard_page)

        self.ui.CT1_btn.clicked.connect(lambda: self.MonitorControl.show_trap("Trap1"))
        self.ui.CT2_btn.clicked.connect(lambda: self.MonitorControl.show_trap("Trap2"))
        self.ui.CT3_btn.clicked.connect(lambda: self.MonitorControl.show_trap("Trap3"))

        '''
        ##########INDEX#########
        0 - dashboard
        1 - alert
        2 - login
        3 - aboutus
        4 - monitor
        5 - inference
        6 - User Management
        7 - AI Models
        8 - settings
        9 - help
        10 - analysis
        '''
    
    def login_btn_clicked(self):
        users = self.DBControl.fetch_users()

        if self.ui.userid_input.text() in users:
            user = users[self.ui.userid_input.text()]
            if self.ui.userid_input_2.text() == user["Password"]:
                self.current_user = self.ui.userid_input.text()
                self.set_user(user) 
                self.dashboard_page()
                self.clear_login()
                self.UserControl.init_session()
            else:
                self.ui.login_error_label.setText('Incorrect Password! Try Again')
        else:
            self.ui.login_error_label.setText('User Not Found!')
    
    def set_user(self, user):
        if self.current_user:
            full_name = user["FirstName"] + " " + user["LastName"]
            self.ui.username_label.setText(full_name)

    def clear_login(self):
            self.ui.userid_input.setText('')
            self.ui.userid_input_2.setText('')
            self.ui.login_error_label.setText('')

    def logout_btn_clicked(self):
        self.ui.MainStack.setCurrentIndex(2)

    def inference_page(self):
        self.ui.MainStack.setCurrentIndex(5)

    def alert_page(self):
        self.ui.DB_error_label.setText("")  
        user = self.DBControl.fetch_users()[self.current_user]
        if user["Designation"] in ["Sr. Scientist", "Superviser"]:
            self.ui.MainStack.setCurrentIndex(1)
            self.AlertControl.init_ui()
        else:
            self.ui.DB_error_label.setText("You Need to be Sr. Scientist/Supervisor to open Alert Panel!")      
    
    def analysis_page(self):
        self.ui.MainStack.setCurrentIndex(10)

    def help_page(self):
        self.ui.MainStack.setCurrentIndex(9)

    def monitor_page(self):
        self.ui.MainStack.setCurrentIndex(4)

    def aboutus_page(self):
        self.ui.MainStack.setCurrentIndex(3)

    def dashboard_page(self):
        self.ui.DB_error_label.setText("")
        self.ui.MainStack.setCurrentIndex(0)
    
    def models_page(self):
        self.ui.MainStack.setCurrentIndex(7)

    def management_page(self):
        self.ui.MainStack.setCurrentIndex(6)
    
    def settings_page(self):
        self.ui.MainStack.setCurrentIndex(8)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WildLifeApp()

    window.show()
    sys.exit(app.exec())
