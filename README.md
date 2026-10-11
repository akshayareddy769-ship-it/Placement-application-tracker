# Placement Application Tracker

A web application that helps students organize job applications
and track their interview progress.

## Features

- Add job applications
- Edit company, role, and application date
- Update application status
- Delete applications
- Search by company name
- Filter by status
- View application counts on a dashboard
- Save data using SQLite

## Technologies

Python, Flask, SQLite, HTML, and CSS.

## Run on Windows

Open a terminal inside the PlacementTracker folder.

Create a virtual environment:

```powershell
python -m venv .venv
```

Install Flask:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the application:

```powershell
.\.venv\Scripts\python.exe app.py
```

Open http://127.0.0.1:5000 in your browser.
Keep the terminal running while using the application.

The database is created automatically on the first run.

## Author

Akshaya C V