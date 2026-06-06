# AutoMail

Automated email reminder system for lab cleaning duty (trực nhật) at HUST. Every morning, a GitHub Actions workflow determines whose turn it is to clean the lab and sends them a reminder email via Office365.

## How it works

1. `students.txt` defines a weekly schedule — one list of members per weekday — and a start date.
2. The scheduler calculates how many weeks have passed since the start date and picks the current member by rotating through the weekday list.
3. A reminder email (in Vietnamese, with a random image) is sent to that member's HUST email address.
4. The workflow runs automatically every day at **08:00 AM Vietnam time** (01:00 UTC) via GitHub Actions.

## Setup

### 1. Configure the schedule

Edit `students.txt`:

```
Start time : 11 May 2026
Monday :
    Nguyen Van A - 20230001
    Tran Thi B - 20230002

Tuesday :
    Le Van C - 20230003
```

- **Start time** — the Monday of the first week of the schedule.
- Each weekday block lists members in rotation order, one per line, as `Full Name - StudentID`.
- Student IDs follow the HUST format (e.g., `20230001`); emails are auto-generated as `givenname.initials<id>@sis.hust.edu.vn`.

### 2. Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|--------|-------------|
| `EMAIL` | Office365 sender address |
| `PASSWORD` | Office365 account password or app password |

### 3. (Optional) Add images

Place `.jpg` images in the `images/` folder named `image1.jpg` through `image6.jpg`. One is picked randomly for each email.

## Running manually

```bash
pip install -r requirements.txt

# Set credentials
export EMAIL="your@email.com"
export PASSWORD="yourpassword"

python morning_job.py
```

On Windows (PowerShell):

```powershell
$env:EMAIL = "your@email.com"
$env:PASSWORD = "yourpassword"
python morning_job.py
```

## Project structure

```
AutoMail/
├── students.txt          # Weekly schedule and start date
├── morning_job.py        # Entry point — orchestrates the daily job
├── parser.py             # Parses students.txt, generates HUST email addresses
├── scheduler_helper.py   # Rotating-schedule logic (weeks since start date)
├── mail_sender.py        # Sends HTML email via Office365 SMTP
├── image_manager.py      # Picks a random image from images/
├── images/               # Image assets attached to emails
└── .github/workflows/
    └── morning_mail.yml  # GitHub Actions cron job (daily at 01:00 UTC)
```

## Email format

The reminder email is sent in Vietnamese and includes:
- A personalised greeting with the member's name
- The cleaning time (17:30)
- Notes about swapping duties and the 20,000 VND penalty for no-shows
- A random image from the `images/` folder
