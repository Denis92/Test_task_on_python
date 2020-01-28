from fixPriceAPI import *


login = input("Введите логин: ")
password = input("Введите пароль: ")

user_data = UserData(login=login, password=password)
active_action = FindAction(login=login, password=password)
file_name = f"UserData_{login}.txt"
indent = len("Почтовый индекс:") + 5
with open(file=file_name, mode="w", encoding="utf-8") as f:
    f.write("<------------------Личные данные--------------->\n")
    f.write(f"{'Фамилия:':{indent}} {user_data.get_last_name()}\n")
    f.write(f"{'Имя:':{indent}} {user_data.get_name()}\n")
    f.write(f"{'Отчество:':{indent}} {user_data.get_second_name()}\n")
    f.write(f"{'Дата рождения:':{indent}} {user_data.get_bird_day()}\n")
    f.write(f"{'Пол:':{indent}} {user_data.get_gender()}\n")
    f.write(f"{'Город:':{indent}} {user_data.get_place()}\n")
    f.write(f"{'Почтовый индекс:':{indent}} {user_data.get_zip_code()}\n")
    f.write(f"{'Email:':{indent}} {user_data.get_email()}\n")
    f.write(f"{'Номер карты:':{indent}} {user_data.get_card_number()}\n\n")
    favorite_product = user_data.get_favorite_product()
    f.write("<------------------Избранное------------------>\n")
    for favorite_item in favorite_product:
        f.write(f"Товар: {favorite_item.get('product'):{50}}  Цена: {favorite_item.get('price')}P\n")
        f.write("-"*100)
        f.write("\n")

    f.write("\n<------------------Спосок действующих акций------------------>\n")
    active_action_list = active_action.get_action_product()
    for active_action_item in active_action_list:
        f.write(f"Описание акции: {active_action_item.get('description')}\n")
        f.write(f"\tСсылка на акцию: {active_action_item.get('link')}\n\n")

print(f"Вся информация записана в файл {file_name}")

