from parser import load_students

from scheduler_helper import (
    get_today_student
)

from image_manager import (
    get_morning_image
)

from mail_sender import send_mail


start_date, students = (
    load_students()
)


student = get_today_student(
    start_date,
    students
)

if student is None:

    print(
        "[INFO] No student today"
    )

else:

    image = get_morning_image(
        student["email"]
    )

    print(
        f"[MORNING] {student['name']}"
    )

    body = f"""
Chào {student['name']} 😄

Đừng quên rằng hôm nay bạn có lịch trực nhật Lab lúc 17:30 nhé!

Chú ý:
- Mail này được gửi tự động để nhắc bạn về lịch trực nhật =))
- Nếu vì lí do bận bạn có thể đổi với người khác.
- Nếu bạn quên trực nhật thì sẽ phải nộp quỹ Lab 20.000 VNĐ.

Chúc bạn một ngày vui vẻ 👀
"""

    send_mail(

        student["email"],

        "[ Nhắc trực nhật Lab ]",

        body,

        image
    )

    print(
        "[SUCCESS] Morning mail sent"
    )