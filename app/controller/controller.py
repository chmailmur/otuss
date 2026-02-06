import pandas as pd 
from app.view.view import View
from app.model.dictionary import PhoneBook



def main() -> None:
    """
    Точка входа контроллера телефонной книги.

    Управляет основным циклом приложения:
    - инициализирует модель (PhoneBook) и представление (View)
    - обрабатывает навигацию пользователя
    - вызывает соответствующие методы модели
    - передаёт результаты в представление

    Реализует роль Controller.
    """
    pb = PhoneBook()
    view = View()
    dict_functions = pb.functions
    print(dict_functions["show_contacts"]())

    while view.data.current_navigation is not None:

        if view.data.message is not None:
            view.message_view(view.data.message)

        if view.data.error_message is not None:
            view.error_view(view.data.error_message)

        result = view.main_navigation_view()

        if result.next_execute_function == "show_contacts":
            contacts = dict_functions["show_contacts"]()
            view.show_contacts_view(contacts)
            view.clean_object()

        if result.next_execute_function == "del_cocntact":
            result = view.del_cocntact_view()
            delete_contact = dict_functions[result.next_execute_function]
            deleting_result = delete_contact(result.data)

            if not deleting_result.empty:
                view.info_view(
                    f"Контакт с номером {result.data} был удален."
                )
            else:
                view.info_view(
                    f"Контакт с номером {result.data} не был удален. "
                    f"Попробуйте ввести другой номер."
                )

            view.clean_object()

        if result.next_execute_function == "change_contact":
            result.current_navigation = result.next_execute_function

            view.show_contacts_view(dict_functions["show_contacts"]())

            search_dict = view.choose_contact_view().copy()
            search_contact = dict_functions["search_contact"](search_dict)
            view.show_contacts_view(search_contact)

            if view.data.message is not None:
                view.message_view(view.data.message)
                view.clean_object()
                continue

            view.change_contact_view()
            change_dict = view.data.data

            updated_contacts = dict_functions["change_contact"](
                search_dict,
                change_dict
            )
            view.show_contacts_view(updated_contacts)
            view.clean_object()

        if result.next_execute_function == "search_contact":
            result.current_navigation = result.next_execute_function
            view.search_contact_view()

            search_dict = view.data.data
            if search_dict is None:
                continue

            search_contact = dict_functions["search_contact"]
            result_search_contact = search_contact(search_dict)

            view.show_contacts_view(result_search_contact)
            view.clean_object()

        if result.next_execute_function == "create_contact":
            result = view.create_contact_view()
            create_contact = dict_functions[result.next_execute_function]

            create_contact(result.data)
            view.show_contacts_view(dict_functions["show_contacts"]())
            view.clean_object()

        if result.next_execute_function == "_exit":
            result.current_navigation = None