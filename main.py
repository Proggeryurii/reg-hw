import re
from pprint import pprint
import csv


# Reading the address book from a CSV file
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    data = list(rows)

# Processing the address book data
def format_phone(phone):
    return re.sub(r'(\+\d{3})(\d{3})(\d{3})(\d{2})(\d{2})', r'\1(\2)\3-\4-\5', phone) + (
        ' доб.' + re.sub(r'(\d{4})', r'\1', phone[-4:]) if len(phone) > 12 else ''
    )

result = []
for record in data[1:]:
    lastname, firstname, middlename, organization, position, phone, email = record
    fio = ' '.join([lastname, firstname, middlename.strip('.')]).strip()
    formatted_phone = format_phone(phone)
    result.append([fio, organization, position, formatted_phone, email])

# group by FIO
grouped = {}
for record in result:
    fio, organization, position, phone, email = record
    grouped.setdefault(fio, []).append(record)

# merge duplicates
merged = []
for fio, records in grouped.items():
    if len(records) > 1:
        organization = list({organization for _, organization, _, _, _ in records})[0] if set(organization for _, organization, _, _, _ in records) else ''
        position = list({position for _, _, position, _, _ in records})[0] if set(position for _, _, position, _, _ in records) else ''
        phones = [phone for _, _, _, phone, _ in records]
        email = list({email for _, _, _, _, email in records})[0] if set(email for _, _, _, _, email in records) else None
        merged.append([fio, organization, position, phones[0], email])
    else:
        merged.append(records[0])
# Writing the processed address book to a CSV file
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(merged)

pprint(merged)