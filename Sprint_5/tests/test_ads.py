import pytest
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from locators import (
    MainPageLocators, AuthFormLocators, AdFormLocators,
    ProfilePageLocators, ModalLocators
)


class TestAds: # Тесты создания объявлений
    
    # Тест создания объявления неавторизованным пользователем
    def test_create_ad_unauthorized(self, driver, wait):
    
        # Нажать кнопку «Разместить объявление»
        wait.until(EC.element_to_be_clickable(MainPageLocators.POST_AD_BUTTON)).click()
        
        # Проверить: отображается модальное окно с заголовком
        modal_message = wait.until(EC.visibility_of_element_located(ModalLocators.MODAL_AUTH_MESSAGE))
        assert modal_message.text == "Чтобы разместить объявление, авторизуйтесь", \
            f"Ожидалось 'Чтобы разместить объявление, авторизуйтесь', получено '{modal_message.text}'"
        
        # Закрыть модальное окно
        close_button = wait.until(EC.element_to_be_clickable(ModalLocators.CLOSE_BUTTON))
        close_button.click()
    
    # Тест создания объявления авторизованным пользователем
    def test_create_ad_authorized(self, driver, wait, registered_user_only):
        # 1. Авторизоваться
        email = registered_user_only["email"]
        password = registered_user_only["password"]
        
        wait.until(EC.element_to_be_clickable(MainPageLocators.LOGIN_REG_BUTTON)).click()
        wait.until(EC.visibility_of_element_located(AuthFormLocators.EMAIL_INPUT)).send_keys(email)
        driver.find_element(*AuthFormLocators.PASSWORD_INPUT).send_keys(password)
        driver.find_element(*AuthFormLocators.LOGIN_BUTTON).click()
        
        # Ждем успешной авторизации
        wait.until(EC.visibility_of_element_located(MainPageLocators.POST_AD_BUTTON))
        time.sleep(1)
        
        # 2. Нажать кнопку «Разместить объявление»
        post_ad_button = wait.until(EC.element_to_be_clickable(MainPageLocators.POST_AD_BUTTON))
        post_ad_button.click()
        
        # Ждем загрузки формы
        time.sleep(2)
        
        # 3. Заполнить поле «Название»
        unique_ad_title = f"Тестовое объявление {email.split('@')[0]}"
        title_input = wait.until(EC.visibility_of_element_located(AdFormLocators.TITLE_INPUT))
        title_input.send_keys(unique_ad_title)
        
        # 4. Выбрать RadioButton «Состояние товара» (Новый)
        condition_new = wait.until(EC.element_to_be_clickable(AdFormLocators.CONDITION_NEW))
        driver.execute_script("arguments[0].scrollIntoView(true);", condition_new)
        time.sleep(0.5)
        condition_new.click()
        
        # 5. Город оставляем по умолчанию (Москва) — ничего не делаем
        
        # 6. Заполнить поле «Описание товара» через JavaScript
        ad_description = "Описание тестового товара"
        
        description_input = wait.until(EC.presence_of_element_located(AdFormLocators.DESCRIPTION_INPUT))
        driver.execute_script("arguments[0].scrollIntoView(true);", description_input)
        time.sleep(0.5)
        driver.execute_script("arguments[0].value = arguments[1];", description_input, ad_description)
        
        # 7. Заполнить поле «Стоимость»
        ad_price = "1000"
        price_input = wait.until(EC.visibility_of_element_located(AdFormLocators.PRICE_INPUT))
        driver.execute_script("arguments[0].scrollIntoView(true);", price_input)
        time.sleep(0.5)
        price_input.send_keys(ad_price)
        
        # 8. Нажать кнопку «Опубликовать»
        publish_button = wait.until(EC.element_to_be_clickable(AdFormLocators.PUBLISH_BUTTON))
        driver.execute_script("arguments[0].scrollIntoView(true);", publish_button)
        time.sleep(0.5)
        publish_button.click()
        
        # Небольшая пауза для обработки
        time.sleep(2)
        
        # 9. Перейти в профиль пользователя
        user_avatar = wait.until(EC.element_to_be_clickable(MainPageLocators.USER_AVATAR))
        user_avatar.click()
        
        # 10. Прокрутить страницу вниз, чтобы блок «Мои объявления» стал видимым
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)
        
        # 11. Проверить: отображается блок «Мои объявления» (используем ProfilePageLocators)
        my_ads_block = wait.until(EC.visibility_of_element_located(ProfilePageLocators.MY_ADS_BLOCK))
        assert my_ads_block.is_displayed(), "Блок «Мои объявления» не отображается"
        
        # 12. Находим все заголовки объявлений (используем ProfilePageLocators)
        ad_titles = driver.find_elements(*ProfilePageLocators.AD_TITLE)
        titles_text = [title.text for title in ad_titles]
        
        # 13. Проверяем, что созданное объявление есть в списке
        assert unique_ad_title in titles_text, \
            f"Объявление '{unique_ad_title}' не найдено в списке. Найденные объявления: {titles_text}"
        
        