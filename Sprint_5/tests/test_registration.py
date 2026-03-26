import pytest
import time
from selenium.webdriver.support import expected_conditions as EC
from locators import MainPageLocators, AuthFormLocators, ModalLocators


class TestRegistration: # Тесты регистрации пользователя
    
    def test_successful_registration(self, driver, wait, generate_unique_email):
    # Тест успешной регистрации пользователя
    # Нажать кнопку «Вход и регистрация»
        wait.until(EC.element_to_be_clickable(MainPageLocators.LOGIN_REG_BUTTON)).click()
    
    # Нажать кнопку «Нет аккаунта»
        wait.until(EC.element_to_be_clickable(AuthFormLocators.NO_ACCOUNT_BUTTON)).click()
    
    # Заполнить поля формы регистрации
        email = generate_unique_email
        password = "TestPassword123"
    
        wait.until(EC.visibility_of_element_located(AuthFormLocators.EMAIL_INPUT)).send_keys(email)
        driver.find_element(*AuthFormLocators.PASSWORD_INPUT).send_keys(password)
        driver.find_element(*AuthFormLocators.CONFIRM_PASSWORD_INPUT).send_keys(password)
    
    # Нажать кнопку «Создать аккаунт»
        driver.find_element(*AuthFormLocators.CREATE_ACCOUNT_BUTTON).click()
    
    # Проверяем, что после регистрации появилась кнопка «Разместить объявление»
        post_ad_button = wait.until(EC.visibility_of_element_located(MainPageLocators.POST_AD_BUTTON))
        assert post_ad_button.is_displayed(), "Кнопка «Разместить объявление» не отображается"
    
    # Проверяем, что отображается аватар пользователя
        user_avatar = wait.until(EC.visibility_of_element_located(MainPageLocators.USER_AVATAR))
        assert user_avatar.is_displayed(), "Аватар пользователя не отображается"
    
    # Проверяем, что отображается имя пользователя "User."
        user_name = wait.until(EC.visibility_of_element_located(MainPageLocators.USER_NAME))
        assert user_name.is_displayed(), "Имя пользователя не отображается"
        assert user_name.text == "User.", f"Ожидалось 'User.', получено '{user_name.text}'"
    
    def test_registration_invalid_email(self, driver, wait):
        # Тест регистрации с email не по маске
        wait.until(EC.element_to_be_clickable(MainPageLocators.LOGIN_REG_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(AuthFormLocators.NO_ACCOUNT_BUTTON)).click()
        
        wait.until(EC.visibility_of_element_located(AuthFormLocators.EMAIL_INPUT)).send_keys("invalid-email")
        driver.find_element(*AuthFormLocators.CREATE_ACCOUNT_BUTTON).click()
        
        error_message = wait.until(EC.visibility_of_element_located(AuthFormLocators.ERROR_MESSAGE))
        assert error_message.text == "Ошибка", f"Ожидалось 'Ошибка', получено '{error_message.text}'"
        
        close_button = wait.until(EC.element_to_be_clickable(ModalLocators.CLOSE_BUTTON))
        close_button.click()
        wait.until(EC.invisibility_of_element_located(ModalLocators.MODAL_CONTAINER))
    
    def test_registration_existing_user(self, driver, wait, registered_user_only):
        # Тест регистрации уже существующего пользователя
        # Полностью перезагружаем страницу после предыдущего теста
        driver.get("https://qa-desk.stand.praktikum-services.ru/")
        time.sleep(2)
        
        # Явно ждем появления кнопки
        login_button = wait.until(EC.presence_of_element_located(MainPageLocators.LOGIN_REG_BUTTON))
        wait.until(EC.visibility_of(login_button))
        wait.until(EC.element_to_be_clickable(MainPageLocators.LOGIN_REG_BUTTON)).click()
        
        # Ждем появления кнопки «Нет аккаунта»
        wait.until(EC.visibility_of_element_located(AuthFormLocators.NO_ACCOUNT_BUTTON))
        wait.until(EC.element_to_be_clickable(AuthFormLocators.NO_ACCOUNT_BUTTON)).click()
        
        # Используем данные из фикстуры
        email = registered_user_only["email"]
        password = registered_user_only["password"]
        
        # Заполнить поля
        email_field = wait.until(EC.visibility_of_element_located(AuthFormLocators.EMAIL_INPUT))
        email_field.send_keys(email)
        driver.find_element(*AuthFormLocators.PASSWORD_INPUT).send_keys(password)
        driver.find_element(*AuthFormLocators.CONFIRM_PASSWORD_INPUT).send_keys(password)
        
        # Нажать кнопку «Создать аккаунт»
        driver.find_element(*AuthFormLocators.CREATE_ACCOUNT_BUTTON).click()
        
        # Проверить ошибку
        error_message = wait.until(EC.visibility_of_element_located(AuthFormLocators.ERROR_MESSAGE))
        assert error_message.text == "Ошибка"

        