from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
from collections import defaultdict

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ
def parse_name(full_string):

    if not full_string or full_string.strip() == "":
        return "", "", ""

    parts = full_string.split()

    first_three = parts[:3]
    fio = " ".join(first_three)
    normalized = fio.split()

    while len(normalized) < 3:
        normalized.append("")

    lastname = normalized[0]
    firstname = normalized[1]
    surname = normalized[2]
    return lastname, firstname, surname


def normalize_phone(phone):

    if not phone or phone.strip() == "":
        return ""

    phone = phone.strip()

    main_pattern = r'(\+7|8)?[\s\-\(\)]*(\d{3})[\s\-\(\)]*(\d{3})[\s\-\(\)]*(\d{2})[\s\-\(\)]*(\d{2})'
    ext_pattern = r'(доб\.?\s*|ext\.?\s*|д\.\s*)(\d+)'

    main_match = re.search(main_pattern, phone)
    if not main_match:
        return phone


    main_number = f"+7({main_match.group(2)}){main_match.group(3)}-{main_match.group(4)}-{main_match.group(5)}"
    ext_match = re.search(ext_pattern, phone, re.IGNORECASE)
    if ext_match:
        ext_number = ext_match.group(2)
        return f"{main_number} доб.{ext_number}"

    return main_number


header = contacts_list[0]
data = contacts_list[1:]

processed_data = []

for row in data:
    # Создаем список из 7 полей
    lastname, firstname, surname, organization, position, phone, email = row

    # Проверяем, есть ли пробелы в полях ФИО
    if lastname and ' ' in lastname:
        last, first, middle = parse_name(lastname)
        lastname = last if last else lastname
        firstname = first if first else firstname
        surname = middle if middle else surname

    if firstname and ' ' in firstname:
        last, first, middle = parse_name(firstname)
        lastname = last if last else lastname
        firstname = first
        surname = middle if middle else surname

    if surname and ' ' in surname:
        last, first, middle = parse_name(surname)
        lastname = last if last else lastname
        firstname = first if first else firstname
        surname = middle

    # Если lastname пустое, а firstname заполнено
    if not lastname and firstname:
        parts = firstname.split()
        if len(parts) >= 1:
            lastname = parts[0]
        if len(parts) >= 2:
            firstname = parts[1]
        if len(parts) >= 3:
            surname = parts[2]

    # 2. Нормализация телефона (пункт 2)
    if phone:
        phone = normalize_phone(phone)

    processed_data.append([lastname, firstname, surname, organization, position, phone, email])



def merge_duplicates(data_list):
    merged = {}

    for row in data_list:
        lastname, firstname, surname, organization, position, phone, email = row

        key = (lastname.lower(), firstname.lower(), surname.lower())

        if key not in merged:
            merged[key] = row.copy() if isinstance(row, list) else list(row)
        else:
            existing = merged[key]
            if not existing[3] and organization:
                existing[3] = organization
            if not existing[4] and position:
                existing[4] = position
            if not existing[5] and phone:
                existing[5] = phone
            if not existing[6] and email:
                existing[6] = email

    return list(merged.values())

final_data = merge_duplicates(processed_data)

contacts_list_final = [header] + final_data
# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_list_final)

  pprint(contacts_list_final)