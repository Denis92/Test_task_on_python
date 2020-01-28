from bs4 import BeautifulSoup
import requests
import re
import functools


def decor_except(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            return None
    return wrapper


class FixPrice:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def _get_session(self):
        session = requests.Session()

        response = session.post(url="https://fix-price.ru/ajax/auth_user.php",
                                data={
                                    "AUTH_FORM": "Y",
                                    "TYPE": "AUTH",
                                    "backurl": "/personal/",
                                    "login": self.login,
                                    "password": self.password
                                })
        if response.json().get("res"):
            print("Вход выполнен")
            return session
        else:
            print(F"Error: {response.json().get('mess')}")
            return exit(1)


class UserData(FixPrice):
    @decor_except
    def __init__(self, login, password):
        super().__init__(login, password)
        session = self._get_session()
        contents = session.get("https://fix-price.ru/personal/#profile").content.decode('utf-8')
        self.soup = BeautifulSoup(contents, 'html.parser')

    @decor_except
    def get_name(self):
        name = self.soup.find("input", {"name": "NAME"}).get('value')
        return name

    @decor_except
    def get_second_name(self):
        second_name = self.soup.find("input", {"name": "SECOND_NAME"}).get('value')
        return second_name

    @decor_except
    def get_last_name(self):
        last_name = self.soup.find("input", {"name": "LAST_NAME"}).get('value')
        return last_name

    @decor_except
    def get_email(self):
        email = self.soup.find("input", {"placeholder": "*EMAIL"}).get('value')
        return email

    @decor_except
    def get_bird_day(self):
        bird_day = self.soup.find("input", {"name": "PERSONAL_BIRTHDAY"}).get('value')
        return bird_day

    @decor_except
    def get_gender(self):
        gender = self.soup.findAll("input", {"name": "PERSONAL_GENDER"})
        gender_check = None
        for iter_gender in gender:
            if iter_gender.get("checked"):
                gender_check = "Женский" if iter_gender.get("value") == "F" else "Мужской"
        return gender_check

    @decor_except
    def get_place(self):
        place = self.soup.find("select", {"name": "PERSONAL_CITY"}).get("data-value")
        return place

    @decor_except
    def get_zip_code(self):
        zip_code = self.soup.find("input", {"name": "PERSONAL_ZIP"}).get("value")
        return zip_code

    @decor_except
    def get_card_number(self):
        card_number = self.soup.find("div", {"class": "personal-card__number"}).get_text()
        return card_number

    @decor_except
    def get_favorite_product(self):
        list_favorites = []
        favorites_item = self.soup.findAll("div", {"class": "main-list__card-item"})
        for favorites in favorites_item:
            find_name = favorites.find("a", {"class": "product-card__title"}).get_text()
            price = favorites.find("span", {"itemprop": "price"}).get_text()
            list_favorites.append({"product": re.sub(r"\s{2,}", " ", find_name),"price": price})

        return list_favorites


class FindAction(FixPrice):
    @decor_except
    def __init__(self, login, password):
        super().__init__(login, password)
        self.session = self._get_session()
        self.list_action = []

    @decor_except
    def __get_count_page(self):
        contents = self.session.get("https://fix-price.ru/actions/").content.decode('utf-8')
        soup = BeautifulSoup(contents, 'html.parser')
        page_count = soup.find_all("li", {"class": "paging__item"})[-1].get_text()
        return page_count

    @decor_except
    def __find_active_action(self, soup):
        action_active = soup.find_all("a", {"class": "action-block__item"})
        for action_active_item in action_active:
            if not "old-action" in action_active_item.get("class"):
                find_text_action = action_active_item.find("h4", {"class": "action-card__info"}).get_text()
                href = action_active_item.get("href")
                self.list_action.append({"description": re.sub(r"\s{2,}", " ", find_text_action),
                                         "link": f"https://fix-price.ru/{href}"})

    @decor_except
    def get_action_product(self):
        count_page = int(self.__get_count_page())
        for i in range(1, count_page + 1):
            contents = self.session.get(f"https://fix-price.ru/actions/?PAGEN_2={i}").content.decode('utf-8')
            soup = BeautifulSoup(contents, 'html.parser')
            self.__find_active_action(soup)
        return self.list_action


if __name__ == '__main__':
    pass

