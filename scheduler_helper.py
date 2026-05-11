from datetime import datetime


def get_today_student(
    start_date,
    students,
    today=None
):

    if today is None:

        today = datetime.today()

    weekday = today.strftime("%A")

    # skip Sunday
    if weekday == "Sunday":
        return None

    if weekday not in students:
        return None

    day_students = students[weekday]

    if len(day_students) == 0:
        return None

    # weeks passed
    weeks_passed = (

        (today - start_date).days
        // 7
    )

    # rotating student
    index = (
        weeks_passed
        % len(day_students)
    )

    return day_students[index]