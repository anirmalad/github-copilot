"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

import email

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice team plays and compete in intramural basketball games",
        "schedule": "Mondays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "nina@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swim training and lap practice for all skill levels",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["luke@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and creative design projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "sophie@mergington.edu"]
    },
    "Drama Club": {
        "description": "Rehearse scenes and prepare performances for school productions",
        "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["oliver@mergington.edu", "mia@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Compete in science and engineering challenges and experiments",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["sam@mergington.edu", "anna@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice public speaking, research, and competitive debate",
        "schedule": "Mondays and Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 14,
        "participants": ["charlie@mergington.edu", "nora@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    # Check if student is already signed up   
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
