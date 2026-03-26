import pytest
import uuid
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import MainPageLocators, AuthFormLocators


@pytest.fixture(autouse=True)
def clean_state(driver):
    # Автоматически очищает состояние перед каждым тестом(при запуске тестов подряд)
    driver.delete_all_cookies()  # Удаляем cookies (выход из аккаунта)
    driver.refresh()  # Обновляем страницу
    # Небольшая пауза для полной загрузки после обновления
    driver.implicitly_wait(1)
    yield


@pytest.fixture
def driver():
    # Фикстура для создания и закрытия драйвера
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://qa-desk.stand.praktikum-services.ru/")
    driver.maximize_window()
    
    yield driver
    
    driver.quit()


@pytest.fixture
def wait(driver):
    # Фикстура для явного ожидания
    return WebDriverWait(driver, 10)


@pytest.fixture
def generate_unique_email():
    # Генерация уникального email для тестов регистрации
    unique_id = uuid.uuid4().hex[:8]
    return f"test_{unique_id}@example.com"


@pytest.fixture
def registered_user(driver, wait, generate_unique_email):
    # Фикстура для создания зарегистрированного и авторизованного пользователя
    # Открываем форму регистрации
    wait.until(EC.element_to_be_clickable(MainPageLocators.LOGIN_REG_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(AuthFormLocators.NO_ACCOUNT_BUTTON)).click()
    
    # Регистрация
    email = generate_unique_email
    password = "TestPassword123"
    
    wait.until(EC.visibility_of_element_located(AuthFormLocators.EMAIL_INPUT)).send_keys(email)
    driver.find_element(*AuthFormLocators.PASSWORD_INPUT).send_keys(password)
    driver.find_element(*AuthFormLocators.CONFIRM_PASSWORD_INPUT).send_keys(password)
    driver.find_element(*AuthFormLocators.CREATE_ACCOUNT_BUTTON).click()
    
    # Ждем появления кнопки «Разместить объявление»
    wait.until(EC.visibility_of_element_located(MainPageLocators.POST_AD_BUTTON))
    
    return {"email": email, "password": password}


@pytest.fixture
def registered_user_only(driver, wait, generate_unique_email):
    # Фикстура для создания зарегистрированного пользователя (без авторизации)
    # Открываем форму регистрации
    wait.until(EC.element_to_be_clickable(MainPageLocators.LOGIN_REG_BUTTON)).click()
    wait.until(EC.element_to_be_clickable(AuthFormLocators.NO_ACCOUNT_BUTTON)).click()
    
    # Регистрация
    email = generate_unique_email
    password = "TestPassword123"
    
    wait.until(EC.visibility_of_element_located(AuthFormLocators.EMAIL_INPUT)).send_keys(email)
    driver.find_element(*AuthFormLocators.PASSWORD_INPUT).send_keys(password)
    driver.find_element(*AuthFormLocators.CONFIRM_PASSWORD_INPUT).send_keys(password)
    driver.find_element(*AuthFormLocators.CREATE_ACCOUNT_BUTTON).click()
    
    # Ждем, что регистрация прошла успешно (появилась кнопка "Разместить объявление")
    wait.until(EC.visibility_of_element_located(MainPageLocators.POST_AD_BUTTON))
    
    # ВЫХОДИМ ИЗ АККАУНТА
    wait.until(EC.element_to_be_clickable(MainPageLocators.LOGOUT_BUTTON)).click()
    
    # Ждем, что вышли (появилась кнопка "Вход и регистрация")
    wait.until(EC.visibility_of_element_located(MainPageLocators.LOGIN_REG_BUTTON))
    
    return {"email": email, "password": password}






