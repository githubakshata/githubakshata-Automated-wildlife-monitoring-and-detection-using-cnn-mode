import sys
import os

from PySide6.QtWidgets import QComboBox

class UserController:
    def __init__(self, parent):
        self.parent = parent

        self.init_ui()
        self.make_connections()
        
    def init_session(self):
        current = self.parent.current_user
        users = self.parent.DBControl.fetch_users()
        if users[current]["Level"] == "Admin":
            self.is_current_user_admin = True
        else:
            self.is_current_user_admin = False
        
        if self.is_current_user_admin:
            self.parent.ui.addUserBtn.setVisible(True)
            self.parent.ui.deleteUsrBtn.setVisible(True)
        
        self.load_user(self.parent.current_user)
    
    def init_ui(self):
        self.parent.ui.changepswdWidget.setVisible(False)
        self.parent.ui.addUserBtn.setVisible(False)
        self.parent.ui.deleteUsrBtn.setVisible(False)
        self.parent.ui.profile_Btn.setVisible(False)
        self.parent.ui.profile_search_btn.setVisible(False)

        self.parent.ui.profile_gender_input.addItems(["Male", "Female"])
        self.parent.ui.profile_level_input.addItems(["Admin", "User"])
        self.parent.ui.profile_designation_input.addItems(["Administrator", "Superviser", "Researcher", "Sr. Scientist", "Jr. Scientist"])
        self.parent.ui.profile_DOB_input.setPlaceholderText("DD/MM/YYYY")
        
        self.set_edit_mode(False)
    
    def make_connections(self):
        self.parent.ui.updateProfileBtn.clicked.connect(self.update_profile_btn)
        self.parent.ui.addUserBtn.clicked.connect(self.add_user_btn)
        self.parent.ui.deleteUsrBtn.clicked.connect(self.delete_user_btn)
        self.parent.ui.ChangePswdBtn.clicked.connect(self.change_password_btn)
        self.parent.ui.profile_search_btn.clicked.connect(self.search_btn)
        self.parent.ui.profile_Btn.clicked.connect(self.profile_btn)
        self.parent.ui.chg_pswd_btn.clicked.connect(self.change_password)

    def search_btn(self):
        self.parent.ui.profile_error_label.setText("")

        if self.parent.ui.profile_usderid_input.text() == "":
            self.parent.ui.profile_error_label.setText("Please Enter UserID!")
            return
        
        user_id = self.parent.ui.profile_usderid_input.text()
        users = self.parent.DBControl.fetch_users()
        
        try:
            users[user_id]
        except KeyError:
            self.parent.ui.profile_error_label.setText("User Not Found")
            self.parent.ui.profile_Btn.setVisible(False)
            return
        
        self.load_user(user_id)

        self.parent.ui.profile_Btn.setVisible(True)

    def delete_user(self):
        user = self.parent.ui.profile_usderid_input.text()

        users = self.parent.DBControl.fetch_users()
        del users[user]

        self.parent.DBControl.save_settings("Users", users)

        print(f"Deleted User: {user}")
        self.parent.ui.profile_error_label.setText("User Delete Successfully!")

        self.clear_user()
        self.parent.ui.profile_search_btn.setVisible(False)
    
    def add_user(self):
        self.parent.ui.profile_error_label.setText("")

        new_user_id = self.parent.ui.profile_usderid_input.text()
        users = self.parent.DBControl.fetch_users()
        try:
            users[new_user_id]
            self.parent.ui.profile_error_label.setText(f"UserID {new_user_id} Already Exists! Try a Different One!")
            return
        except KeyError:
            pass

        if self.parent.ui.profile_firstname_input.text() == "":
            self.parent.ui.profile_error_label.setText("First Name is Empty!")
            return
        if self.parent.ui.profile_lastname_input.text() == "":
            self.parent.ui.profile_error_label.setText("Last Name is Empty!")
            return
        if self.parent.ui.profile_DOB_input.text() == "":
            self.parent.ui.profile_error_label.setText("Date of Birth is Empty!")
            return
        if self.parent.ui.profile_phone_input.text() == "":
            self.parent.ui.profile_error_label.setText("Phone Number is Empty!")
            return
        if self.parent.ui.profile_email_input.text() == "":
            self.parent.ui.profile_error_label.setText("EmailID is Empty!")
            return
        if self.parent.ui.profile_id_input.text() == "":
            self.parent.ui.profile_error_label.setText("Institute ID is Empty!")
            return
        if self.parent.ui.profile_gender_input.currentText() == "Choose":
            self.parent.ui.profile_error_label.setText("Please Choose Gender!")
            return
        if self.parent.ui.profile_level_input.currentText() == "Choose":
            self.parent.ui.profile_error_label.setText("Please Choose User Level!")
            return
        if self.parent.ui.profile_designation_input.currentText() == "Choose":
            self.parent.ui.profile_error_label.setText("Please Choose Designation!")
            return
        if self.parent.ui.change_new_pswd_input.text() == "":
            self.parent.ui.profile_error_label.setText("Please Enter New Password!")
            return
        if not self.parent.ui.change_new_pswd_input.text() == self.parent.ui.change_new_pswd_input2.text():
            self.parent.ui.profile_error_label.setText("Passwords Don't Match!")
            return
        
        users[new_user_id] = {} 
        users[new_user_id]["FirstName"] = self.parent.ui.profile_firstname_input.text()
        users[new_user_id]["LastName"] = self.parent.ui.profile_lastname_input.text()
        users[new_user_id]["DOB"] = self.parent.ui.profile_DOB_input.text()
        users[new_user_id]["PhoneNumber"] = self.parent.ui.profile_phone_input.text()
        users[new_user_id]["EmailID"] = self.parent.ui.profile_email_input.text()
        users[new_user_id]["InstituteID"] = self.parent.ui.profile_id_input.text()
        users[new_user_id]["Gender"] = self.parent.ui.profile_gender_input.currentText()
        users[new_user_id]["Level"] = self.parent.ui.profile_level_input.currentText()
        users[new_user_id]["Designation"] = self.parent.ui.profile_designation_input.currentText()
        users[new_user_id]["Password"] = self.parent.ui.change_new_pswd_input.text()

        self.parent.DBControl.save_settings("Users", users)
        self.parent.ui.profile_error_label.setText("User Added Successfully!")
        print(f'User Added: {new_user_id}')
        self.clear_password()
        self.parent.ui.changepswdWidget.setVisible(False)
        self.set_edit_mode(False)

    def update_user(self):
        self.parent.ui.profile_error_label.setText("")

        user_id = self.parent.current_user
        users = self.parent.DBControl.fetch_users()

        if self.parent.ui.profile_firstname_input.text() == "":
            self.parent.ui.profile_error_label.setText("First Name is Empty!")
            return
        if self.parent.ui.profile_lastname_input.text() == "":
            self.parent.ui.profile_error_label.setText("Last Name is Empty!")
            return
        if self.parent.ui.profile_DOB_input.text() == "":
            self.parent.ui.profile_error_label.setText("Date of Birth is Empty!")
            return
        if self.parent.ui.profile_phone_input.text() == "":
            self.parent.ui.profile_error_label.setText("Phone Number is Empty!")
            return
        if self.parent.ui.profile_email_input.text() == "":
            self.parent.ui.profile_error_label.setText("EmailID is Empty!")
            return
        if self.parent.ui.profile_id_input.text() == "":
            self.parent.ui.profile_error_label.setText("Institute ID is Empty!")
            return
        if self.parent.ui.profile_gender_input.currentText() == "Choose":
            self.parent.ui.profile_error_label.setText("Please Choose Gender!")
            return
        
        users[user_id]["FirstName"] = self.parent.ui.profile_firstname_input.text()
        users[user_id]["LastName"] = self.parent.ui.profile_lastname_input.text()
        users[user_id]["DOB"] = self.parent.ui.profile_DOB_input.text()
        users[user_id]["PhoneNumber"] = self.parent.ui.profile_phone_input.text()
        users[user_id]["EmailID"] = self.parent.ui.profile_email_input.text()
        users[user_id]["InstituteID"] = self.parent.ui.profile_id_input.text()
        users[user_id]["Gender"] = self.parent.ui.profile_gender_input.currentText()

        self.parent.DBControl.save_settings("Users", users)
        self.parent.ui.profile_error_label.setText("User Updated Successfully!")
        print(f'User Updated: {user_id}')
        self.set_edit_mode(False)

    def profile_btn(self):
        button_value = self.parent.ui.profile_Btn.text()
        if button_value == "Delete":
            self.delete_user()
        if button_value == "Add":
            self.add_user()
        if button_value == "Update":
            self.update_user()
            
    def change_password(self):
        self.parent.ui.changepswd_error_label.setText("")

        if self.parent.ui.change_cur_pswd_input.text() == "":
            self.parent.ui.changepswd_error_label.setText("Please Enter Current Password!")
            return
        
        if self.parent.ui.change_new_pswd_input.text() == "":
            self.parent.ui.changepswd_error_label.setText("Please Enter New Password!")
            return
        
        if self.parent.ui.change_new_pswd_input2.text() == "":
            self.parent.ui.changepswd_error_label.setText("Please Enter New Password Again!")
            return
        
        users = self.parent.DBControl.fetch_users()
        user = users[self.parent.current_user]

        if not self.parent.ui.change_cur_pswd_input.text() == user["Password"]:
            self.parent.ui.changepswd_error_label.setText("Incorrect Current Password!")
            return
        
        if self.parent.ui.change_cur_pswd_input.text() == self.parent.ui.change_new_pswd_input.text():
            self.parent.ui.changepswd_error_label.setText("Cannot Use Same Password!")
            return
        
        if not self.parent.ui.change_new_pswd_input.text() == self.parent.ui.change_new_pswd_input2.text():
            self.parent.ui.changepswd_error_label.setText("New Password not matching!")
            return
        
        new_password = self.parent.ui.change_new_pswd_input.text()

        users[self.parent.current_user]["Password"] = new_password

        self.parent.DBControl.save_settings("Users", users)

        self.parent.ui.changepswd_error_label.setText("Password Changed Successfully!")

        print(f"Password Change: {self.parent.current_user}")
    
    def change_password_btn(self):
        self.change_mode()
        self.parent.ui.profile_Btn.setVisible(False)
        self.parent.ui.changepswdWidget.setVisible(True)

        self.clear_password()

    def delete_user_btn(self):
        self.change_mode()
        self.clear_user()
        self.parent.ui.profile_Btn.setText("Delete")

        self.parent.ui.profile_search_btn.setVisible(True)

        self.set_edit_mode(False)
        self.parent.ui.profile_usderid_input.setEnabled(True)

    def add_user_btn(self):
        self.change_mode()
        self.clear_user()
        self.parent.ui.profile_Btn.setText("Add")
        self.parent.ui.profile_Btn.setVisible(True)
        self.parent.ui.changepswdWidget.setVisible(True)
        self.parent.ui.change_cur_pswd_input.setEnabled(False)

        self.set_edit_mode(True)

    def update_profile_btn(self):
        self.change_mode()
        self.clear_user()
        self.parent.ui.profile_Btn.setText("Update")
        self.parent.ui.profile_Btn.setVisible(True)
        
        self.set_edit_mode(True)
        self.load_user(self.parent.current_user)

        self.parent.ui.profile_usderid_input.setEnabled(False)
        if not self.is_current_user_admin:
            self.parent.ui.profile_level_input.setEnabled(False)
            self.parent.ui.profile_designation_input.setEnabled(False)
    
    def load_user(self, user_id):
        user = self.parent.DBControl.fetch_users()[user_id]
        
        self.parent.ui.profile_usderid_input.setText(user_id)
        self.parent.ui.profile_firstname_input.setText(user["FirstName"])
        self.parent.ui.profile_lastname_input.setText(user["LastName"])
        self.parent.ui.profile_DOB_input.setText(user["DOB"])
        self.parent.ui.profile_phone_input.setText(user["PhoneNumber"])
        self.parent.ui.profile_email_input.setText(user["EmailID"])
        self.parent.ui.profile_id_input.setText(user["InstituteID"])

        self.parent.ui.profile_gender_input.setCurrentText(user["Gender"])
        self.parent.ui.profile_level_input.setCurrentText(user["Level"])
        self.parent.ui.profile_designation_input.setCurrentText(user["Designation"])

    def change_mode(self):
        self.parent.ui.profile_Btn.setVisible(False)
        self.parent.ui.changepswdWidget.setVisible(False)
        self.parent.ui.profile_search_btn.setVisible(False)

    def clear_user(self):
        self.parent.ui.profile_error_label.setText("")
        self.parent.ui.profile_usderid_input.setText("")
        self.parent.ui.profile_firstname_input.setText("")
        self.parent.ui.profile_lastname_input.setText("")
        self.parent.ui.profile_DOB_input.setText("")
        self.parent.ui.profile_phone_input.setText("")
        self.parent.ui.profile_email_input.setText("")
        self.parent.ui.profile_id_input.setText("")

        self.parent.ui.profile_gender_input.setCurrentText("Choose")
        self.parent.ui.profile_level_input.setCurrentText("Choose")
        self.parent.ui.profile_designation_input.setCurrentText("Choose")

    def clear_password(self):
        self.parent.ui.changepswd_error_label.setText("")
        self.parent.ui.change_cur_pswd_input.setEnabled(True)
        self.parent.ui.change_cur_pswd_input.setText("")
        self.parent.ui.change_new_pswd_input.setText("")
        self.parent.ui.change_new_pswd_input2.setText("")

    def set_edit_mode(self, state):
        self.parent.ui.profile_usderid_input.setEnabled(state)
        self.parent.ui.profile_firstname_input.setEnabled(state)
        self.parent.ui.profile_lastname_input.setEnabled(state)
        self.parent.ui.profile_DOB_input.setEnabled(state)
        self.parent.ui.profile_phone_input.setEnabled(state)
        self.parent.ui.profile_email_input.setEnabled(state)
        self.parent.ui.profile_id_input.setEnabled(state)

        self.parent.ui.profile_gender_input.setEnabled(state)
        self.parent.ui.profile_level_input.setEnabled(state)
        self.parent.ui.profile_designation_input.setEnabled(state)