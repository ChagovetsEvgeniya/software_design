def add_order():
    print("Виберіть тип комп'ютера: 1 - Настільний, 2 - Ноутбук")
    comp_type = input("Ваш вибір: ")
    if comp_type not in ['1', '2']:
        print("Невірний вибір")
        return
    print("Введіть комплектуючі...")
    components = input("Комплектуючі: ")
    if not components:
        print("A2: Не всі комплектуючі вибрані. Прецедент завершується.")
        return
    print("Замовлення створене. Номер: 123. Друк рахунку...")
def change_order():
    order_id = input("Введіть номер замовлення для зміни: ")
    if order_id != "123":
        print("A3: Невірний номер. Прецедент завершується.")
        return
    print("Поточна інформація замовлення показана.")
    input("Введіть нову інформацію: ")
    print("Зміни збережено.")
def delete_order():
    order_id = input("Введіть номер замовлення для видалення: ")
    if order_id != "123":
        print("A3: Невірний номер. Прецедент завершується.")
        return
    confirm = input("Видалити замовлення? (так/ні): ")
    if confirm.lower() == "так":
        print("Замовлення видалено.")
    else:
        print("A4: Видалення відкладено. Дані збережено.")
def view_order():
    order_id = input("Введіть номер замовлення для перегляду: ")
    if order_id != "123":
        print("A3: Невірний номер. Прецедент завершується.")
        return
    print("Показ інформації про замовлення...")
def main():
    print("Вхід у систему...")
    login = input("Логін: ")
    password = input("Пароль: ")
    if login != "admin" or password != "1234":
        print("A1: Невірні логін або пароль. Прецедент завершується.")
        return
    while True:
        print("\nМеню:")
        print("1. Додати замовлення")
        print("2. Змінити замовлення")
        print("3. Видалити замовлення")
        print("4. Переглянути замовлення")
        print("5. Вийти")
        choice = input("Ваш вибір: ")
        if choice == '1':
            add_order()
        elif choice == '2':
            change_order()
        elif choice == '3':
            delete_order()
        elif choice == '4':
            view_order()
        elif choice == '5':
            print("Вихід із системи.")
            break
        else:
            print("Невірний вибір.")
if __name__ == "__main__":
    main()