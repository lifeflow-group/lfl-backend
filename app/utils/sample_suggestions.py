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
        "icon": "🏃‍♂️",
        "title": "Optimize your Morning Jog",
        "description": "Increase the intensity or duration of your jog gradually to challenge yourself and improve cardiovascular fitness.",
        "id": "78d2099b-d303-432a-9b07-1e738c9576db",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_001",
            "name": "Morning Jog",
            "user_id": "user_001",
            "category_id": "fitness",
            "start_date": "2025-02-28T14:52:00+00:00",
            "repeat_frequency": "DAILY",
            "reminder_enabled": True,
            "tracking_type": "COMPLETE",
            "quantity": None,
            "unit": None,
            "progress": None,
            "completed": False
        },
        "created_at": "2025-03-17T14:50:22.282073",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "📚",
        "title": "Reward Yourself for Reading",
        "description": "After completing your 'Read Books' sessions, treat yourself to a relaxing activity you enjoy.",
        "id": "73eb4155-05a3-4f5c-acf5-c743be6abc9d",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_002",
            "name": "Read Books",
            "user_id": "user_001",
            "category_id": "education",
            "start_date": "2025-02-17T22:14:00+00:00",
            "repeat_frequency": "WEEKLY",
            "reminder_enabled": True,
            "tracking_type": "PROGRESS",
            "quantity": 31,
            "unit": "sessions",
            "progress": 2,
            "completed": False
        },
        "created_at": "2025-03-17T14:50:22.282152",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "🧘‍♀️",
        "title": "Extend Meditation Sessions",
        "description": "Increase your meditation duration by 5-10 minutes each week for deeper practice.",
        "id": "5c16dadc-0588-41b5-886c-18db440dbebc",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_003",
            "name": "Meditation",
            "user_id": "user_001",
            "category_id": "spiritual",
            "start_date": "2025-02-14T06:04:00+00:00",
            "repeat_frequency": "DAILY",
            "reminder_enabled": True,
            "tracking_type": "COMPLETE",
            "quantity": None,
            "unit": None,
            "progress": None,
            "completed": True
        },
        "created_at": "2025-03-17T14:50:22.282202",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "🇪🇸",
        "title": "Set a Time for Learning Spanish",
        "description": "Practice at the same time daily and enable reminders to stay consistent.",
        "id": "93ba4e81-2d37-42e8-9935-0ca3468f09d3",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_004",
            "name": "Learn Spanish",
            "user_id": "user_001",
            "category_id": "education",
            "start_date": "2025-02-01T03:07:00+00:00",
            "repeat_frequency": "DAILY",
            "reminder_enabled": False,
            "tracking_type": "PROGRESS",
            "quantity": 25,
            "unit": "lessons",
            "progress": 7,
            "completed": False
        },
        "created_at": "2025-03-17T14:50:22.282241",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "💧",
        "title": "Drink More Water",
        "description": "Place water bottles in visible locations as reminders to stay hydrated.",
        "id": "bdf8583f-ff57-4ce7-a66d-5dabccc0a0de",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_309",
            "name": "Drink Water",
            "user_id": "user_001",
            "category_id": "health",
            "start_date": "2025-03-09T11:15:00+00:00",
            "repeat_frequency": "WEEKLY",
            "reminder_enabled": True,
            "tracking_type": "PROGRESS",
            "quantity": 14,
            "unit": "cups",
            "progress": 8,
            "completed": False
        },
        "created_at": "2025-03-17T14:50:22.282280",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "🏋️‍♂️",
        "title": "Increase Weightlifting Reps",
        "description": "Add an extra set to your weightlifting routine to build strength gradually.",
        "id": "a1",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_005",
            "name": "Weightlifting",
            "user_id": "user_001",
            "category_id": "fitness",
            "start_date": "2025-02-05T08:00:00+00:00",
            "repeat_frequency": "DAILY",
            "reminder_enabled": True,
            "tracking_type": "PROGRESS",
            "quantity": 3,
            "unit": "sets",
            "progress": 2,
            "completed": False
        },
        "created_at": "2025-03-17T14:51:22.282280",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "🚴‍♂️",
        "title": "Try a New Cycling Route",
        "description": "Explore different cycling routes to keep your routine exciting and challenging.",
        "id": "a2",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_006",
            "name": "Cycling",
            "user_id": "user_001",
            "category_id": "fitness",
            "start_date": "2025-01-25T07:00:00+00:00",
            "repeat_frequency": "WEEKLY",
            "reminder_enabled": False,
            "tracking_type": "COMPLETE",
            "quantity": None,
            "unit": None,
            "progress": None,
            "completed": False
        },
        "created_at": "2025-03-17T14:52:22.282280",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "🥗",
        "title": "Add Greens to Every Meal",
        "description": "Incorporate more leafy greens into each meal to improve your diet.",
        "id": "a3",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_007",
            "name": "Healthy Eating",
            "user_id": "user_001",
            "category_id": "health",
            "start_date": "2025-03-01T12:00:00+00:00",
            "repeat_frequency": "DAILY",
            "reminder_enabled": True,
            "tracking_type": "PROGRESS",
            "quantity": 3,
            "unit": "meals",
            "progress": 1,
            "completed": False
        },
        "created_at": "2025-03-17T14:53:22.282280",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "📓",
        "title": "Start a Gratitude Journal",
        "description": "Write down three things you are grateful for every night to boost positivity.",
        "id": "a4",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_008",
            "name": "Gratitude Journal",
            "user_id": "user_001",
            "category_id": "mental_health",
            "start_date": "2025-02-20T21:00:00+00:00",
            "repeat_frequency": "DAILY",
            "reminder_enabled": True,
            "tracking_type": "COMPLETE",
            "quantity": None,
            "unit": None,
            "progress": None,
            "completed": False
        },
        "created_at": "2025-03-17T14:54:22.282280",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "⏰",
        "title": "Establish a Sleep Schedule",
        "description": "Aim to go to bed and wake up at the same time daily to improve sleep quality.",
        "id": "a5",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_009",
            "name": "Sleep Early",
            "user_id": "user_001",
            "category_id": "health",
            "start_date": "2025-02-10T22:00:00+00:00",
            "repeat_frequency": "DAILY",
            "reminder_enabled": True,
            "tracking_type": "COMPLETE",
            "quantity": None,
            "unit": None,
            "progress": None,
            "completed": False
        },
        "created_at": "2025-03-17T14:55:22.282280",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "🧹",
        "title": "Declutter Your Workspace",
        "description": "Spend 10 minutes decluttering your workspace to improve focus and productivity.",
        "id": "a6",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_010",
            "name": "Clean Desk",
            "user_id": "user_001",
            "category_id": "productivity",
            "start_date": "2025-02-18T09:00:00+00:00",
            "repeat_frequency": "WEEKLY",
            "reminder_enabled": True,
            "tracking_type": "COMPLETE",
            "quantity": None,
            "unit": None,
            "progress": None,
            "completed": False
        },
        "created_at": "2025-03-17T14:56:22.282280",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "🎨",
        "title": "Schedule Creative Time",
        "description": "Block out time each week for creative activities like painting, writing, or music.",
        "id": "a7",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_011",
            "name": "Creative Hour",
            "user_id": "user_001",
            "category_id": "hobby",
            "start_date": "2025-03-01T17:00:00+00:00",
            "repeat_frequency": "WEEKLY",
            "reminder_enabled": True,
            "tracking_type": "PROGRESS",
            "quantity": 1,
            "unit": "hour",
            "progress": 0,
            "completed": False
        },
        "created_at": "2025-03-17T14:57:22.282280",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "📖",
        "title": "Daily Affirmations",
        "description": "Start your day with positive affirmations to boost confidence and mindset.",
        "id": "a8",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_012",
            "name": "Affirmations",
            "user_id": "user_001",
            "category_id": "mental_health",
            "start_date": "2025-02-05T06:00:00+00:00",
            "repeat_frequency": "DAILY",
            "reminder_enabled": True,
            "tracking_type": "COMPLETE",
            "quantity": None,
            "unit": None,
            "progress": None,
            "completed": False
        },
        "created_at": "2025-03-17T14:58:22.282280",
        "is_viewed": False,
        "is_implemented": False
    },
    {
        "icon": "🎧",
        "title": "Listen to Educational Podcasts",
        "description": "Dedicate 20 minutes to learning something new through podcasts.",
        "id": "a9",
        "user_id": "hoan",
        "habit_data": {
            "id": "habit_013",
            "name": "Podcast Learning",
            "user_id": "user_001",
            "category_id": "education",
            "start_date": "2025-02-28T08:00:00+00:00",
            "repeat_frequency": "DAILY",
            "reminder_enabled": False,
            "tracking_type": "PROGRESS",
            "quantity": 1,
            "unit": "episode",
            "progress": 0,
            "completed": False
        },
        "created_at": "2025-03-17T14:59:22.282280",
        "is_viewed": False,
        "is_implemented": False
    }
]



