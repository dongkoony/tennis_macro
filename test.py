from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QCalendarWidget, QCheckBox, QLabel
from PyQt5.QtCore import QDate, QSettings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Test_Macro'
        self.settings = QSettings('MyCompany', 'MyApp')
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        layout = QVBoxLayout()

        layout.addWidget(QLabel('아이디'))
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('아이디 입력')
        self.username_input.setText(self.settings.value("username", ""))
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel('비밀번호'))
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('비밀번호 입력')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText(self.settings.value("password", ""))
        layout.addWidget(self.password_input)

        layout.addWidget(QLabel('원하는 지역'))
        self.location_input = QLineEdit(self)
        self.location_input.setPlaceholderText('지역 이름 입력')
        layout.addWidget(self.location_input)

        self.remember_credentials_checkbox = QCheckBox('아이디/비밀번호 저장', self)
        self.remember_credentials_checkbox.setChecked(self.settings.value("rememberCredentials", False, type=bool))
        layout.addWidget(self.remember_credentials_checkbox)

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.showDate)
        layout.addWidget(self.calendar)

        self.date_label = QLineEdit(self)
        self.date_label.setPlaceholderText('선택된 날짜')
        layout.addWidget(self.date_label)

        button = QPushButton('예약 시작', self)
        button.clicked.connect(self.run_automation)
        layout.addWidget(button)

        self.setLayout(layout)
        self.show()

    def showDate(self, date):
        self.date_label.setText(date.toString())

    def run_automation(self):
        username = self.username_input.text()
        password = self.password_input.text()
        desired_location = self.location_input.text()  # 원하는 지역 정보를 가져옵니다.

        if self.remember_credentials_checkbox.isChecked():
            self.settings.setValue("username", username)
            self.settings.setValue("password", password)
            self.settings.setValue("rememberCredentials", True)
        else:
            self.settings.remove("username")
            self.settings.remove("password")
            self.settings.setValue("rememberCredentials", False)

        driver = webdriver.Chrome(executable_path='C:/path/to/chromedriver.exe')
        driver.maximize_window()
        driver.get("https://yeyak.seoul.go.kr/web/search/selectPageListDetailSearchImg.do?code=T100&dCode=T108")
        
        try:
            # 로그인 버튼 클릭
            login_page_button = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/div[1]/a')
            login_page_button.click()

            # 아이디, 패스워드 기입 및 로그인
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="userid"]'))).send_keys(username)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="userpwd"]'))).send_keys(password)
            driver.find_element(By.XPATH, '//*[@id="addUserForm"]/div[1]/button').click()

            # 원하는 지역 검색
            search_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search2"]/fieldset/div[2]/input')))
            search_field.send_keys(desired_location)  # 지역 정보를 기입합니다.
            driver.find_element(By.XPATH, '//*[@id="search2"]/fieldset/button[1]').click()

            print(f"Automating with {username}, {password}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
