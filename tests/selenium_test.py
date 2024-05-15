# test_selenium.py
import pytest
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def flask_server():
    # 启动 Flask 服务器
    server = subprocess.Popen(["flask", "run", "--host=127.0.0.1", "--port=8080"])
    time.sleep(3)  # 等待服务器启动
    yield
    server.terminate()  # 结束 Flask 服务器
    server.wait()

@pytest.fixture(scope="class")
def setup(request):
    # 使用 ChromeOptions 指定 ChromeDriver 的路径
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("setup", "flask_server")
class TestCITS5505:
    def test_cITS5505(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8080/")
        driver.set_window_size(1562, 1296)

        login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
        driver.execute_script("arguments[0].scrollIntoView(true);", login_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", login_link)

        driver.find_element(By.ID, "username").send_keys("Admin")
        driver.find_element(By.ID, "password").send_keys("123123")
        driver.find_element(By.ID, "password").send_keys(Keys.ENTER)

        following_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Following")))
        driver.execute_script("arguments[0].scrollIntoView(true);", following_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", following_link)

        all_posts_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "All Posts")))
        driver.execute_script("arguments[0].scrollIntoView(true);", all_posts_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", all_posts_link)

        first_post_image = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".col:nth-child(1) .card-img-top")))
        driver.execute_script("arguments[0].scrollIntoView(true);", first_post_image)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", first_post_image)

        home_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Home")))
        driver.execute_script("arguments[0].scrollIntoView(true);", home_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", home_link)

        page_2_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "2")))
        driver.execute_script("arguments[0].scrollIntoView(true);", page_2_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", page_2_link)

        page_3_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "3")))
        driver.execute_script("arguments[0].scrollIntoView(true);", page_3_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", page_3_link)

        home_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Home")))
        driver.execute_script("arguments[0].scrollIntoView(true);", home_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", home_link)

        profile_img = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".profile-img")))
        driver.execute_script("arguments[0].scrollIntoView(true);", profile_img)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", profile_img)

        my_channel_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "My Channel")))
        driver.execute_script("arguments[0].scrollIntoView(true);", my_channel_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", my_channel_link)

        following_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Following")))
        driver.execute_script("arguments[0].scrollIntoView(true);", following_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", following_link)

        profile_img = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".profile-img")))
        driver.execute_script("arguments[0].scrollIntoView(true);", profile_img)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", profile_img)

        my_channel_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "My Channel")))
        driver.execute_script("arguments[0].scrollIntoView(true);", my_channel_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", my_channel_link)

        followers_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Followers")))
        driver.execute_script("arguments[0].scrollIntoView(true);", followers_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", followers_link)

        profile_img = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".profile-img")))
        driver.execute_script("arguments[0].scrollIntoView(true);", profile_img)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", profile_img)

        my_channel_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "My Channel")))
        driver.execute_script("arguments[0].scrollIntoView(true);", my_channel_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", my_channel_link)

        second_post_image = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".col:nth-child(2) .card-img-top")))
        driver.execute_script("arguments[0].scrollIntoView(true);", second_post_image)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", second_post_image)

        profile_img = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".profile-img")))
        driver.execute_script("arguments[0].scrollIntoView(true);", profile_img)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", profile_img)

        edit_profile_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Edit Profile")))
        driver.execute_script("arguments[0].scrollIntoView(true);", edit_profile_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", edit_profile_link)

        edit_profile_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Edit Profile")))
        driver.execute_script("arguments[0].scrollIntoView(true);", edit_profile_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", edit_profile_link)

        job_description = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "job_description")))
        driver.execute_script("arguments[0].scrollIntoView(true);", job_description)
        time.sleep(1)
        job_description.click()

        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submit")))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)
        submit_button.click()

        home_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Home")))
        driver.execute_script("arguments[0].scrollIntoView(true);", home_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", home_link)

        profile_img = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".profile-img")))
        driver.execute_script("arguments[0].scrollIntoView(true);", profile_img)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", profile_img)

        logout_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
        driver.execute_script("arguments[0].scrollIntoView(true);", logout_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", logout_link)
