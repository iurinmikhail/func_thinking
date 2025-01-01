from typing import TypedDict, NamedTuple, TypeAlias, Any


MAIL_LIST = []


class Email(NamedTuple):
    value: str


class Elements(TypedDict):
    email: Email


class Form(NamedTuple):
    elements: Elements


class Event(NamedTuple):
    target: Form


def add(array: list, elem: Any) -> list:
    new_arr = array.copy()
    new_arr.append(elem)
    return new_arr


def add_contact(mail_list: list[Email], email: Email) -> list[Email]:

    return add(mail_list, email)


def submit_form_handler(event: Event) -> None:
    global MAIL_LIST
    form = event.target
    email = form.elements["email"].value
    MAIL_LIST = add_contact(MAIL_LIST, email)


if __name__ == "__main__":
    email = Email(value="123@mail.com")
    event = Event(target=Form(elements=Elements(email=email)))
    submit_form_handler(event=event)
    assert MAIL_LIST == [email.value]
