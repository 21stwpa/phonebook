from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


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
        return f"{main_number} доб.{ext_match.group(2)}"
    return main_number

header = contacts_list[0]
data = contacts_list[1:]
processed_data = []

for row in data:
    lastname, firstname, surname, organization, position, phone, email = row
    if lastname and ' ' in lastname:
        parts = lastname.split()
        lastname = parts[0]
        rest = " ".join(parts[1:])
        firstname = (rest + " " + firstname).strip() if firstname else rest

    if firstname and ' ' in firstname:
        parts = firstname.split()
        firstname = parts[0]
        if len(parts) >= 2 and not surname:
            surname = parts[1]
    
    if not lastname and firstname:
        lastname = firstname
        firstname = ""
    
    if surname and ' ' in surname and not firstname:
        parts = surname.split()
        firstname = parts[0]
        surname = parts[1] if len(parts) >= 2 else ""
    
    if phone:
        phone = normalize_phone(phone)
    
    processed_data.append([lastname, firstname, surname, organization, position, phone, email])

def merge_duplicates(data_list):
    merged = {}
    for row in data_list:
        lastname, firstname, surname, organization, position, phone, email = row
        key = (lastname.lower().strip(), firstname.lower().strip())
        
        if key not in merged:
            merged[key] = list(row)
        else:
            existing = merged[key]
            if not existing[2] and surname:
                existing[2] = surname
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

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list_final)

pprint(contacts_list_final)
