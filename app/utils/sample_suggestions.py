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

        # Update the user_id in both suggestion and habit
        s["user_id"] = user_id
        if "habit" in s and s["habit"]:
            s["habit"]["user_id"] = user_id

        # Optional: regenerate id and created_at if necessary
        s["id"] = str(uuid4())
        s["created_at"] = datetime.now().isoformat()

        result.append(s)

    return result


SAMPLE_SUGGESTIONS = [
    {
        "title": "Stay Hydrated Regularly",
        "description": "Try setting reminders to drink water every 2 hours. You can place a water bottle on your desk as a visual cue.",
        "habit": {
            "id": "habit_water_" + str(uuid4())[:8],
            "name": "Drink Water",
            "userId": "",
            "category": {
                "id": "health",
                "name": "Health",
                "iconPath": "assets/icons/health.png",
                "colorHex": "#FF5733",
            },
            "date": "2024-03-01T00:00:00Z",
            "series": {
                "id": "series_" + str(uuid4())[:8],
                "userId": "",
                "habitId": "habit_water_" + str(uuid4())[:8],
                "startDate": "2024-03-01T00:00:00Z",
                "untilDate": "2024-06-01T00:00:00Z",
                "repeatFrequency": "daily",
            },
            "reminderEnabled": True,
            "trackingType": "complete",
            "targetValue": 8,
            "currentValue": 0,
            "unit": "cups",
            "isCompleted": False,
        },
    },
    {
        "title": "Morning Jog for a Fresh Start",
        "description": "Start your day with a 15-minute jog to boost your energy and improve cardiovascular health.",
        "habit": {
            "id": "habit_jog_" + str(uuid4())[:8],
            "name": "Morning Jog",
            "userId": "",
            "category": {
                "id": "fitness",
                "name": "Fitness",
                "iconPath": "assets/icons/fitness.png",
                "colorHex": "#2ECC71",
            },
            "date": "2024-03-01T06:30:00Z",
            "series": {
                "id": "series_" + str(uuid4())[:8],
                "userId": "",
                "habitId": "habit_jog_" + str(uuid4())[:8],
                "startDate": "2024-03-01T06:30:00Z",
                "untilDate": None,
                "repeatFrequency": "daily",
            },
            "reminderEnabled": True,
            "trackingType": "complete",
            "targetValue": None,
            "currentValue": None,
            "unit": None,
            "isCompleted": False,
        },
    },
    {
        "title": "Read a Book Before Bed",
        "description": "Wind down your day by reading 10 pages of a book before going to sleep. It helps reduce stress and improve sleep quality.",
        "habit": {
            "id": "habit_read_" + str(uuid4())[:8],
            "name": "Read Before Bed",
            "userId": "",
            "category": {
                "id": "education",
                "name": "Education",
                "iconPath": "assets/icons/education.png",
                "colorHex": "#E67E22",
            },
            "date": "2024-03-01T22:00:00Z",
            "series": {
                "id": "series_" + str(uuid4())[:8],
                "userId": "",
                "habitId": "habit_read_" + str(uuid4())[:8],
                "startDate": "2024-03-01T22:00:00Z",
                "untilDate": None,
                "repeatFrequency": "daily",
            },
            "reminderEnabled": True,
            "trackingType": "progress",
            "targetValue": 10,
            "currentValue": 0,
            "unit": "pages",
            "isCompleted": False,
        },
    },
    {
        "title": "Practice Meditation Daily",
        "description": "Spend 10 minutes each morning practicing mindfulness meditation to reduce stress and increase focus.",
        "habit": {
            "id": "habit_meditation_" + str(uuid4())[:8],
            "name": "Meditation",
            "userId": "",
            "category": {
                "id": "spiritual",
                "name": "Spiritual",
                "iconPath": "assets/icons/spiritual.png",
                "colorHex": "#8E44AD",
            },
            "date": "2024-03-01T07:00:00Z",
            "series": {
                "id": "series_" + str(uuid4())[:8],
                "userId": "",
                "habitId": "habit_meditation_" + str(uuid4())[:8],
                "startDate": "2024-03-01T07:00:00Z",
                "untilDate": None,
                "repeatFrequency": "daily",
            },
            "reminderEnabled": True,
            "trackingType": "complete",
            "targetValue": None,
            "currentValue": None,
            "unit": None,
            "isCompleted": False,
        },
    },
    {
        "title": "Save Money Monthly",
        "description": "Set aside a small portion of your income each month to build financial security and achieve your savings goals.",
        "habit": {
            "id": "habit_save_" + str(uuid4())[:8],
            "name": "Save Money",
            "userId": "",
            "category": {
                "id": "finance",
                "name": "Finance",
                "iconPath": "assets/icons/finance.png",
                "colorHex": "#27AE60",
            },
            "date": "2024-03-01T00:00:00Z",
            "series": {
                "id": "series_" + str(uuid4())[:8],
                "userId": "",
                "habitId": "habit_save_" + str(uuid4())[:8],
                "startDate": "2024-03-01T00:00:00Z",
                "untilDate": None,
                "repeatFrequency": "monthly",
            },
            "reminderEnabled": True,
            "trackingType": "progress",
            "targetValue": 500,
            "currentValue": 0,
            "unit": "USD",
            "isCompleted": False,
        },
    },
    {
        "title": "Call a Friend Weekly",
        "description": "Stay connected with loved ones by scheduling a weekly call with a close friend or family member.",
        "habit": {
            "id": "habit_call_" + str(uuid4())[:8],
            "name": "Call a Friend",
            "userId": "",
            "category": {
                "id": "social",
                "name": "Social",
                "iconPath": "assets/icons/social.png",
                "colorHex": "#E74C3C",
            },
            "date": "2024-03-01T18:00:00Z",
            "series": {
                "id": "series_" + str(uuid4())[:8],
                "userId": "",
                "habitId": "habit_call_" + str(uuid4())[:8],
                "startDate": "2024-03-01T18:00:00Z",
                "untilDate": None,
                "repeatFrequency": "weekly",
            },
            "reminderEnabled": True,
            "trackingType": "complete",
            "targetValue": None,
            "currentValue": None,
            "unit": None,
            "isCompleted": False,
        },
    },
    {
        "title": "Write in a Journal",
        "description": "Reflect on your thoughts and emotions by writing a journal entry each night before bed.",
        "habit": {
            "id": "habit_journal_" + str(uuid4())[:8],
            "name": "Journal Writing",
            "userId": "",
            "category": {
                "id": "personal_growth",
                "name": "Personal Growth",
                "iconPath": "assets/icons/personal_growth.png",
                "colorHex": "#9B59B6",
            },
            "date": "2024-03-01T21:30:00Z",
            "series": {
                "id": "series_" + str(uuid4())[:8],
                "userId": "",
                "habitId": "habit_journal_" + str(uuid4())[:8],
                "startDate": "2024-03-01T21:30:00Z",
                "untilDate": None,
                "repeatFrequency": "daily",
            },
            "reminderEnabled": True,
            "trackingType": "complete",
            "targetValue": None,
            "currentValue": None,
            "unit": None,
            "isCompleted": False,
        },
    },
    {
        "title": "Learn a New Language",
        "description": "Dedicate 30 minutes a day to learning a new language through an app or online course.",
        "habit": {
            "id": "habit_language_" + str(uuid4())[:8],
            "name": "Language Learning",
            "userId": "",
            "category": {
                "id": "education",
                "name": "Education",
                "iconPath": "assets/icons/education.png",
                "colorHex": "#E67E22",
            },
            "date": "2024-03-01T19:00:00Z",
            "series": {
                "id": "series_" + str(uuid4())[:8],
                "userId": "",
                "habitId": "habit_language_" + str(uuid4())[:8],
                "startDate": "2024-03-01T19:00:00Z",
                "untilDate": None,
                "repeatFrequency": "daily",
            },
            "reminderEnabled": True,
            "trackingType": "progress",
            "targetValue": 30,
            "currentValue": 0,
            "unit": "minutes",
            "isCompleted": False,
        },
    },
    {
        "title": "Meal Prep for the Week",
        "description": "Prepare your meals in advance every Sunday to save time and maintain a healthy diet.",
        "habit": {
            "id": "habit_meal_" + str(uuid4())[:8],
            "name": "Meal Prep",
            "userId": "",
            "category": {
                "id": "health",
                "name": "Health",
                "iconPath": "assets/icons/health.png",
                "colorHex": "#FF5733",
            },
            "date": "2024-03-03T10:00:00Z",
            "series": {
                "id": "series_" + str(uuid4())[:8],
                "userId": "",
                "habitId": "habit_meal_" + str(uuid4())[:8],
                "startDate": "2024-03-03T10:00:00Z",
                "untilDate": None,
                "repeatFrequency": "weekly",
            },
            "reminderEnabled": True,
            "trackingType": "complete",
            "targetValue": None,
            "currentValue": None,
            "unit": None,
            "isCompleted": False,
        },
    },
]
