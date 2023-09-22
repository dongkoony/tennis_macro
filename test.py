from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QCalendarWidget, QCheckBox, QLabel
from PyQt5.QtCore import QDate, QSettings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


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
        desired_location = self.location_input.text()
        selected_date = self.date_label.text().replace('-', '')

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

        # 로그인 버튼 클릭
        login_page_button = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/div[1]/a')
        login_page_button.click()

        # 아이디, 패스워드 기입 및 로그인
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="userid"]'))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="userpwd"]'))).send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="addUserForm"]/div[1]/button').click()

        # 원하는 지역 검색
        search_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search2"]/fieldset/div[2]/input')))
        search_field.send_keys(desired_location)
        driver.find_element(By.XPATH, '//*[@id="search2"]/fieldset/button[1]').click()

        # 화면 중간까지 스크롤 내리기
        window_height = driver.execute_script("return window.innerHeight")
        scroll_amount = window_height / 2
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")

        # 테스트 테니스장 클릭
        tennis_court_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]/div[3]/ul/li[1]/a')))
        tennis_court_link.click()

        # 화면 중간까지 스크롤 내리기
        window_height = driver.execute_script("return window.innerHeight")
        scroll_amount = window_height / 3
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")

        # 팝업창 처리
        action = ActionChains(driver)
        action.move_by_offset(10, 10).click().perform()

        # 날짜 선택
        date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body[@class='ko']/div[@id='wrapper']/div[@id='sub_contents']/div[@class='container']/div[@id='contents']/form[@id='aform']/div[@class='dt_top_box']/div[@class='left_box']/div[@class='cal_wrap']/div[@id='calendar']/table[@class='tbl_cal']/tbody/tr[3]/td[@id='calendar_20231017']/a[@id='cal_20231017']/span[@class='date']")))
        date_element.click()

        # 예약하기 버튼 클릭
        reserve_button_xpath = "/html/body[@class='ko']/div[@id='wrapper']/div[@id='sub_contents']/div[@class='container']/div[@id='contents']/form[@id='aform']/div[@class='dt_top_box']/div[@class='con_box']/div[@class='dt_con_each']/div[@class='common_btn_box']/a[@class='common_btn blue']"
        reserve_button_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, reserve_button_xpath)))
        reserve_button_element.click()

        # 예약 시간대 스크롤
        element = driver.find_element(By.XPATH, "/html/body[@class='ko']/div[@id='wrapper']/div[@id='sub_contents']/div[@class='container']/div[@id='contents']/div[@class='booking_wrap']/form[@id='aform']/div[@class='book_box']/div[@class='left_box']/div[@class='book_each'][1]/div[@class='cal_wrap']/div[@id='calendar_tm_area']/div[@class='con_box']")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight / 3;", element)

        # 예약 시간대 클릭
        reservation_time_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body[@class='ko']/div[@id='wrapper']/div[@id='sub_contents']/div[@class='container']/div[@id='contents']/div[@class='booking_wrap']/form[@id='aform']/div[@class='book_box']/div[@class='left_box']/div[@class='book_each'][1]/div[@class='cal_wrap']/div[@id='calendar_tm_area']/div[@class='con_box']/ul[@id='useUnit']/li[@id='unit6']/a[@class='rsv_unit_seq_row']"))
        )
        reservation_time_element.click()

        # 이용 인원 증가 버튼 클릭
        team_count_increase_xpath = "/html/body[@class='ko']/div[@id='wrapper']/div[@id='sub_contents']/div[@class='container']/div[@id='contents']/div[@class='booking_wrap']/form[@id='aform']/div[@class='book_box']/div[@class='left_box']/div[@id='user_cnt_area']/div[@class='fee_each']/div[1]/div[@class='right_txt']/div[@class='form_sel']/div[@class='book_user']/button[@class='user_plus']"
        team_count_increase_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body[@class='ko']/div[@id='wrapper']/div[@id='sub_contents']/div[@class='container']/div[@id='contents']/div[@class='booking_wrap']/form[@id='aform']/div[@class='book_box']/div[@class='left_box']/div[@id='user_cnt_area']/div[@class='fee_each']/div[1]/div[@class='right_txt']/div[@class='form_sel']/div[@class='book_user']/button[@class='user_plus']")))
        team_count_increase_button.click()

        # 인적 사항
        element_to_click = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body[@class='ko']/div[@id='wrapper']/div[@id='sub_contents']/div[@class='container']/div[@id='contents']/div[@class='booking_wrap']/form[@id='aform']/div[@class='book_box']/div[@class='left_box']/div[@class='book_each'][4]/h5[@class='book_tit2']/span[@class='chk_each']/label/span[@class='vchkbox']")))
        element_to_click.click()

        # 전체 동의
        element_to_click = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body[@class='ko']/div[@id='wrapper']/div[@id='sub_contents']/div[@class='container']/div[@id='contents']/div[@class='booking_wrap']/form[@id='aform']/div[@class='book_box']/div[@class='left_box']/div[@class='book_each'][5]/div[@class='total_agree']/span[@class='chk_each']/label/span[@class='vchkbox']")))
        element_to_click.click()
        
        # 마지막 예약하기 버튼 클릭
        reservation_button_xpath = "/html/body[@class='ko']/div[@id='wrapper']/div[@id='sub_contents']/div[@class='container']/div[@id='contents']/div[@class='booking_wrap']/form[@id='aform']/div[@class='book_box']/div[@class='right_box']/div[@class='info_wrap']/div[@class='common_btn_box']/button[@class='common_btn blue']"
        reservation_button_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, reservation_button_xpath)))
        reservation_button_element.click()


if __name__ == "__main__":
    app = QApplication([])
    ex = App()
    app.exec_()
