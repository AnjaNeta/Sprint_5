from selenium.webdriver.common.by import By


class MainPageLocators:
    """Локаторы главной страницы"""
    
    LOGIN_REG_BUTTON = (By.XPATH, "//button[text()='Вход и регистрация']")
    POST_AD_BUTTON = (By.XPATH, "//button[text()='Разместить объявление']")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выйти']")
    USER_AVATAR = (By.CLASS_NAME, "circleSmall")
    USER_NAME = (By.CSS_SELECTOR, "h3.profileText.name")


class AuthFormLocators:
    """Локаторы формы авторизации/регистрации"""
    
    NO_ACCOUNT_BUTTON = (By.XPATH, "//button[text()='Нет аккаунта']")
    EMAIL_INPUT = (By.XPATH, "//input[@placeholder='Введите Email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Пароль']")
    CONFIRM_PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Повторите пароль']")
    CREATE_ACCOUNT_BUTTON = (By.XPATH, "//button[text()='Создать аккаунт']")
    EXIST_ACCOUNT = (By.XPATH, "//button[text()='Уже есть аккаунт']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    
    # Локаторы для проверки ошибок
    EMAIL_FIELD_ERROR = (By.CSS_SELECTOR, "#email.error")
    PASSWORD_FIELD_ERROR = (By.CSS_SELECTOR, "#password.error")
    CONFIRM_PASSWORD_FIELD_ERROR = (By.CSS_SELECTOR, "#confirm-password.error")
    ERROR_MESSAGE = (By.XPATH, "//span[text()='Ошибка']")


class AdFormLocators:
    """Локаторы формы создания объявления"""
    
    TITLE_INPUT = (By.NAME, "name")
    DESCRIPTION_INPUT = (By.NAME, "description")
    PRICE_INPUT = (By.XPATH, "//input[@name='price' and @placeholder='Стоимость']")
    CATEGORY_INPUT = (By.NAME, "category")
    CONDITION_NEW = (By.XPATH, "//label[text()='Новый']")
    CONDITION_USED = (By.XPATH, "//label[text()='Б/У']")
    PUBLISH_BUTTON = (By.XPATH, "//button[text()='Опубликовать']")


class ProfilePageLocators:
    """Локаторы страницы профиля"""
    
    MY_ADS_BLOCK = (By.XPATH, "//h1[text()='Мои объявления']")
    AD_CARD = (By.CSS_SELECTOR, ".card")
    AD_TITLE = (By.CSS_SELECTOR, ".card .about h2")
    AD_CITY = (By.CSS_SELECTOR, ".card .about h3")
    AD_PRICE = (By.CSS_SELECTOR, ".card .price h2")


class ModalLocators:
    """Локаторы модальных окон"""
    
    MODAL_CONTAINER = (By.CSS_SELECTOR, ".popUp_shell__LuyqR")
    MODAL_AUTH_MESSAGE = (By.XPATH, "//h1[text()='Чтобы разместить объявление, авторизуйтесь']")
    CLOSE_BUTTON = (By.CSS_SELECTOR, ".popUp_XBtn__uEWoB")

    