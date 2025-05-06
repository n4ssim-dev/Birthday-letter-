import os
from dotenv import load_dotenv
import smtplib

import pandas
import random
from datetime import datetime

load_dotenv()

my_email = os.getenv('my_email')
password = os.getenv('password')

now = datetime.now()
today_date = (now.month, now.day)

data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

if today_date in birthdays_dict:
    # Sélectionne celui qui fête son anniversaire
    birthday_person = birthdays_dict[today_date]
    # Choisi un template de lettre aléatoire
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"

    # lis la lettre choisis
    with open(file_path) as letter_file:
        contents = letter_file.read()
        # Customize la lettre et y intègre le nom de la personne
        contents = contents.replace("[NAME]", birthday_person["name"])

    # Envoie le mail
    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Joyeux Anniversaire !!\n\n{contents}"
        )