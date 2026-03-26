import pytest
from selenium.webdriver.support import expected_conditions as EC
from locators import MainPageLocators, AuthFormLocators


class TestLogin: #Тесты авторизации пользователя
    
    # Тест успешного входа пользователя
    def test_successful_login(self, driver, wait, registered_user_only):
        
        # Используем данные пользователя (фикстура уже вышла из аккаунта)
        email = registered_user_only["email"]
        password = registered_user_only["password"]
        
        # Нажать кнопку «Вход и регистрация»
        wait.until(EC.element_to_be_clickable(MainPageLocators.LOGIN_REG_BUTTON)).click()
        
        # Заполнить поля формы авторизации
        wait.until(EC.visibility_of_element_located(AuthFormLocators.EMAIL_INPUT)).send_keys(email)
        driver.find_element(*AuthFormLocators.PASSWORD_INPUT).send_keys(password)
        
        # Нажать кнопку «Войти»
        driver.find_element(*AuthFormLocators.LOGIN_BUTTON).click()
        
        # Проверить: произошёл переход на главную страницу
        post_ad_button = wait.until(EC.visibility_of_element_located(
            MainPageLocators.POST_AD_BUTTON
        ))
        assert post_ad_button.is_displayed(), "Кнопка «Разместить объявление» не отображается"
        
        # Проверить: отображается аватар пользователя
        user_avatar = wait.until(EC.visibility_of_element_located(
            MainPageLocators.USER_AVATAR
        ))
        assert user_avatar.is_displayed(), "Аватар пользователя не отображается"
        
        # Проверить: отображается имя пользователя
        user_name = wait.until(EC.visibility_of_element_located(
            MainPageLocators.USER_NAME
        ))
        assert user_name.is_displayed(), "Имя пользователя не отображается"
        assert user_name.text == "User.", f"Ожидалось 'User.', получено '{user_name.text}'"



