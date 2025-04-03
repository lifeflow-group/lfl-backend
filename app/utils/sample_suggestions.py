import copy
from datetime import datetime
import random
from uuid import uuid4


def get_sample_suggestions(user_id: str, limit: int = 5):
    # Validate user_id
    if not user_id:
        raise ValueError("user_id is required")

    # Randomize and limit the sample suggestions
    sample_pool = random.sample(SAMPLE_SUGGESTIONS, min(limit, len(SAMPLE_SUGGESTIONS)))

    result = []
    for suggestion in sample_pool:
        # Create a deep copy to avoid mutating the original SAMPLE_SUGGESTIONS
        s = copy.deepcopy(suggestion)

        # Update the user_id in both suggestion and habit_data
        s["user_id"] = user_id
        if "habit_data" in s and s["habit_data"]:
            s["habit_data"]["user_id"] = user_id

        # Optional: regenerate id and created_at if necessary
        s["id"] = str(uuid4())
        s["created_at"] = datetime.now().isoformat()

        result.append(s)

    return result


SAMPLE_SUGGESTIONS = [
    {
        "title": "Stay Hydrated Regularly",
        "description": "Try setting reminders to drink water every 2 hours. You can place a water bottle on your desk as a visual cue.",
        "habitData": {
            "name": "Drink Water",
            "category": {
                "id": "health",
                "label": "Health",
                "iconPath": "assets/icons/health.png",
            },
            "repeatFrequency": "DAILY",
            "startDate": "2024-03-01T00:00:00Z",
            "untilDate": "2024-06-01T00:00:00Z",
            "reminderEnabled": True,
            "trackingType": "COMPLETE",
            "targetValue": 8,
            "unit": "cups",
        },
    },
    {
        "title": "Morning Jog for a Fresh Start",
        "description": "Start your day with a 15-minute jog to boost your energy and improve cardiovascular health.",
        "habitData": {
            "name": "Morning Jog",
            "category": {
                "id": "fitness",
                "label": "Fitness",
                "iconPath": "assets/icons/fitness.png",
            },
            "repeatFrequency": "DAILY",
            "startDate": "2024-03-01T06:30:00Z",
            "untilDate": None,
            "reminderEnabled": True,
            "trackingType": "COMPLETE",
            "targetValue": None,
            "unit": None,
        },
    },
    {
        "title": "Read a Book Before Bed",
        "description": "Wind down your day by reading 10 pages of a book before going to sleep. It helps reduce stress and improve sleep quality.",
        "habitData": {
            "name": "Read Before Bed",
            "category": {
                "id": "education",
                "label": "Education",
                "iconPath": "assets/icons/education.png",
            },
            "repeatFrequency": "DAILY",
            "startDate": "2024-03-01T22:00:00Z",
            "untilDate": None,
            "reminderEnabled": True,
            "trackingType": "PROGRESS",
            "targetValue": 10,
            "unit": "pages",
        },
    },
    {
        "title": "Practice Meditation Daily",
        "description": "Spend 10 minutes each morning practicing mindfulness meditation to reduce stress and increase focus.",
        "habitData": {
            "name": "Meditation",
            "category": {
                "id": "spiritual",
                "label": "Spiritual",
                "iconPath": "assets/icons/spiritual.png",
            },
            "repeatFrequency": "DAILY",
            "startDate": "2024-03-01T07:00:00Z",
            "untilDate": None,
            "reminderEnabled": True,
            "trackingType": "COMPLETE",
            "targetValue": None,
            "unit": None,
        },
    },
    {
        "title": "Save Money Monthly",
        "description": "Set aside a small portion of your income each month to build financial security and achieve your savings goals.",
        "habitData": {
            "name": "Save Money",
            "category": {
                "id": "finance",
                "label": "Finance",
                "iconPath": "assets/icons/finance.png",
            },
            "repeatFrequency": "MONTHLY",
            "startDate": "2024-03-01T00:00:00Z",
            "untilDate": None,
            "reminderEnabled": True,
            "trackingType": "PROGRESS",
            "targetValue": 500,
            "unit": "USD",
        },
    },
    {
        "title": "Call a Friend Weekly",
        "description": "Stay connected with loved ones by scheduling a weekly call with a close friend or family member.",
        "habitData": {
            "name": "Call a Friend",
            "category": {
                "id": "social",
                "label": "Social",
                "iconPath": "assets/icons/social.png",
            },
            "repeatFrequency": "WEEKLY",
            "startDate": "2024-03-01T18:00:00Z",
            "untilDate": None,
            "reminderEnabled": True,
            "trackingType": "COMPLETE",
            "targetValue": None,
            "unit": None,
        },
    },
    {
        "title": "Write in a Journal",
        "description": "Reflect on your thoughts and emotions by writing a journal entry each night before bed.",
        "habitData": {
            "name": "Journal Writing",
            "category": {
                "id": "personal_growth",
                "label": "Personal Growth",
                "iconPath": "assets/icons/personal_growth.png",
            },
            "repeatFrequency": "DAILY",
            "startDate": "2024-03-01T21:30:00Z",
            "untilDate": None,
            "reminderEnabled": True,
            "trackingType": "COMPLETE",
            "targetValue": None,
            "unit": None,
        },
    },
    {
        "title": "Learn a New Language",
        "description": "Dedicate 30 minutes a day to learning a new language through an app or online course.",
        "habitData": {
            "name": "Language Learning",
            "category": {
                "id": "education",
                "label": "Education",
                "iconPath": "assets/icons/education.png",
            },
            "repeatFrequency": "DAILY",
            "startDate": "2024-03-01T19:00:00Z",
            "untilDate": None,
            "reminderEnabled": True,
            "trackingType": "PROGRESS",
            "targetValue": 30,
            "unit": "minutes",
        },
    },
    {
        "title": "Meal Prep for the Week",
        "description": "Prepare your meals in advance every Sunday to save time and maintain a healthy diet.",
        "habitData": {
            "name": "Meal Prep",
            "category": {
                "id": "health",
                "label": "Health",
                "iconPath": "assets/icons/health.png",
            },
            "repeatFrequency": "WEEKLY",
            "startDate": "2024-03-03T10:00:00Z",
            "untilDate": None,
            "reminderEnabled": True,
            "trackingType": "COMPLETE",
            "targetValue": None,
            "unit": None,
        },
    },
]
