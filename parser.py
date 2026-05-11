import unicodedata
import re

from datetime import datetime


def remove_accents(text):

    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )


def generate_hust_email(full_name, student_id):

    full_name = remove_accents(full_name)

    words = full_name.strip().split()

    last_name = words[-1]

    initials = ''.join(
        word[0]
        for word in words[:-1]
    )

    short_id = student_id[2:]

    return (
        f"{last_name}.{initials}"
        f"{short_id}@sis.hust.edu.vn"
    )


def load_students():

    students = {}

    current_day = None

    start_date = None

    with open(
        "students.txt",
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            # start date
            if line.startswith(
                "Start time"
            ):

                date_text = (
                    line.split(":")[1]
                    .strip()
                )

                # remove st/nd/rd/th
                date_text = re.sub(
                    r"(st|nd|rd|th)",
                    "",
                    date_text
                )

                # add current year
                if len(
                    date_text.split()
                ) == 2:

                    current_year = (
                        datetime.today().year
                    )

                    date_text += (
                        f" {current_year}"
                    )

                start_date = (
                    datetime.strptime(
                        date_text,
                        "%d %B %Y"
                    )
                )

            elif ":" in line:

                current_day = (
                    line.replace(":", "")
                    .strip()
                )

                students[current_day] = []

            else:

                name, sid = line.split("-")

                name = name.strip()
                sid = sid.strip()

                students[current_day].append({

                    "name": name,

                    "email":
                    generate_hust_email(
                        name,
                        sid
                    )
                })

    return start_date, students