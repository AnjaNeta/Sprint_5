import pytest
import time
from selenium.webdriver.support import expected_conditions as EC
from locators import MainPageLocators


class TestLogout: # Тесты выхода пользователя
    
    def test_successful_logout(self, driver, wait, registered_user):
        # Тест успешного выхода пользователя"""
        # Нажать кнопку «Выйти»
        logout_button = wait.until(EC.element_to_be_clickable(MainPageLocators.LOGOUT_BUTTON))
        logout_button.click()
        
        # Ждем небольшой паузы
        time.sleep(1)
        
        # Обновляем страницу, чтобы применить изменения
        driver.refresh()
        time.sleep(1)
        
        # Проверить: появилась кнопка «Вход и регистрация»
        login_reg_button = wait.until(EC.visibility_of_element_located(
            MainPageLocators.LOGIN_REG_BUTTON
        ))
        assert login_reg_button.is_displayed(), "Кнопка «Вход и регистрация» не отображается"
        
        # Проверить: аватар пользователя исчез
        user_avatars = driver.find_elements(*MainPageLocators.USER_AVATAR)
        assert len(user_avatars) == 0, \
            f"Аватар пользователя все еще отображается. Найдено: {len(user_avatars)}"
        
        # Проверить: имя пользователя исчезло
        user_names = driver.find_elements(*MainPageLocators.USER_NAME)
        assert len(user_names) == 0, \
            f"Имя пользователя все еще отображается. Найдено: {len(user_names)}"
        
        # Проверить: кнопка «Разместить объявление» остается на странице
        post_ad_button = driver.find_element(*MainPageLocators.POST_AD_BUTTON)
        assert post_ad_button.is_displayed(), "Кнопка «Разместить объявление» не отображается"

        