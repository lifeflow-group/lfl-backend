import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List
import json
import os
import uuid
import time
from datetime import datetime
import google.generativeai as genai
from google.generativeai import GenerativeModel
from dotenv import load_dotenv

from app.schemas.habit_analysis_input_schema import HabitAnalysisInput
from app.schemas.habit_schema import HabitResponse
from app.schemas.performance_metric_schema import PerformanceMetricResponse
from app.schemas.suggestion_schema import SuggestionResponse

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
genai.configure(api_key=GEMINI_API_KEY)

executor = ThreadPoolExecutor()


async def async_generate_content(prompt, model: GenerativeModel):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, model.generate_content, prompt)


async def get_ai_suggestions(
    habitAnalysisInput: HabitAnalysisInput,
    chunk_size: int = 300,  # Average: 1,000,000 / 15 per minute ≈ 66,666 tokens per request
) -> List[SuggestionResponse]:
    """
    Calls Gemini AI to generate suggestions based on habits and metrics.
    Splits the habits list into chunks to avoid exceeding token limits.
    Then consolidates the suggestions into top 3-5.
    """
    if not GEMINI_API_KEY:
        raise ValueError("Missing GEMINI_API_KEY in environment variables.")

    all_suggestions = []
    model = genai.GenerativeModel(GEMINI_MODEL)
    habits = habitAnalysisInput.habits

    # 1. Handle chunk splitting
    for i in range(0, len(habits), chunk_size):

        prompt = _create_suggestion_prompt(habitAnalysisInput, i, chunk_size)

        # Await for the asynchronous function
        response = await async_generate_content(prompt, model)

        chunk_suggestions = _parse_ai_response(response.text)
        all_suggestions.extend(chunk_suggestions)

        print(f"Processing habit chunks: {i} - {i + chunk_size}")
        time.sleep(2)

    # 2. Refine suggestions in chunks if the list is too big
    if len(all_suggestions) > 5:
        final_suggestions = []
        model1 = genai.GenerativeModel(GEMINI_MODEL)
        for i in range(0, len(all_suggestions), chunk_size):
            chunk_suggestions = all_suggestions[i : i + chunk_size]
            # Await for the asynchronous function
            prompt = _refine_suggestions_prompt(chunk_suggestions)
            response = await async_generate_content(prompt, model1)
            refined_chunk = _parse_ai_response(response.text)
            final_suggestions.extend(refined_chunk)
            print(f"Processing suggestion chunks: {i} - {i + chunk_size}")
            time.sleep(2)

    else:
        final_suggestions = all_suggestions

    return final_suggestions


def _create_suggestion_prompt(
    habitAnalysisInput: HabitAnalysisInput,
    i: int,
    chunk_size: int,
) -> str:
    chunk_habits = habitAnalysisInput.habits[i : i + chunk_size]

    # Convert datetime to string before serialization
    def convert_datetime(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")

    prompt = f"""
        You are an expert AI habit coach. Your task is to analyze the user's current habits and performance metrics, then generate personalized, actionable suggestions to help them improve their habits.

        ### Analysis Period:
        - Start Date: {habitAnalysisInput.start_date.strftime('%Y-%m-%d')}
        - End Date: {habitAnalysisInput.end_date.strftime('%Y-%m-%d')}

        ### Data:
        Here is the user's current habit data and performance metrics in JSON format:
        {json.dumps([habit.model_dump() for habit in chunk_habits], indent=2, default=convert_datetime)}

        Each item in the list has the following fields:
        - **id** (string): Unique identifier for the habit.
        - **name** (string): Name of the habit.
        - **category** (HabitCategory): The category this habit belongs to, providing context for its purpose and relevance.  
            Each category has the following fields:  
            + **id** (string): Unique identifier for the habit category.  
            + **name** (string): The display name of the category (e.g., "Health", "Work", "Fitness").  
            + **icon_path** (string, optional): Path to the icon representing the category.
            + **color_hex** (string, optional): The hexadecimal color code for the category (e.g., "#FF5733").
        - **tracking_type** (string): Whether the habit is tracked by `COMPLETE` (done/not done) or `PROGRESS` (measurable value like steps, minutes, etc.).
        
        - **target_value** (integer, optional): The goal value for `PROGRESS`-based habits (e.g., 8 glasses of water, 30 minutes of exercise).
        - **unit** (string, optional): The unit for `target_value` (e.g., "cups", "minutes").
        
        - **repeat_frequency** (string, optional): The recurrence rule for the habit (e.g., "DAILY", "WEEKLY", "MONTHLY").
        - **start_date** (ISO string): The date when the habit was first created.
        - **until_date** (ISO string, optional): The date when the habit tracking should end (if applicable).
        
        - **exceptions** (list[HabitExceptionBase], optional):  
        A list of exceptions affecting this habit. Exceptions can indicate skipped days, modified tracking values, or changes in reminders.  
        Each exception has the following fields:  
            + **habit_series_id** (string): Identifier linking this exception to a recurring habit series.  
            + **date** (ISO string): The specific date of the exception.  
            + **is_skipped** (boolean, default=False): Whether the habit was skipped on this date.  
            + **reminder_enabled** (boolean, default=False): Whether reminders were active on this date.  
            + **target_value** (integer, optional): Updated target value for progress-based habits on this date.  
            + **current_value** (integer, optional): The recorded value for progress-based habits on this date.  
            + **is_completed** (boolean, optional): Whether the habit was completed on this date.
        
        - **performance_metric: Performance Metrics:**
            + **completion_rate** (float, optional): Percentage of time the habit was completed (0.0 - 1.0).
            + **average_progress** (float, optional): Average value recorded for `PROGRESS`-based habits.
            + **total_progress** (float, optional): Total accumulated progress for `PROGRESS`-based habits.
            + **metric_description** (string, optional): A summary of the user's habit performance.
            + **metric_start_date** (ISO string, optional): The start date of the performance analysis period.
            + **metric_end_date** (ISO string, optional): The end date of the performance analysis period.


        ### Instructions:
        Based on the data above, generate **5 personalized suggestions**. Each suggestion should belong to **one** of the following categories:

        1. **Optimize Current Habits**
        - Help users adjust or improve existing habits (time, frequency, method...).
        - Provide specific, easy-to-implement solutions to maintain habits more effectively.

        2. **Motivation - Encouragement**
        - Provide encouragement based on achievements or progress.
        - Create small challenges or encourage users to reward themselves when completing goals.

        3. **Habit Expansion**
        - Suggest developing existing habits to a higher level or combining with related habits to increase effectiveness.

        4. **Smart Reminders**
        - Suggest additional reminders, notifications, or incorporating habits into personal schedules (habit stacking).
        - Suggest optimal time frames based on performance.

        5. **Personalization Based on Lifestyle / Interests**
        - Create suggestions that match the user's interests, schedule, and personal lifestyle.
        - Example: if the user enjoys music, suggest combining listening to music while performing the habit.

        ### Notes:
        - Ensure all suggestions are **personalized** based on user data.
        - Each suggestion must have a **clear benefit** and be **easy to understand**.

        ### Output format:
        Return suggestions in JSON format like this example:
        [
            {{
                "title": "Stay Hydrated Regularly", // Motivating and clear title
                "description": "Try setting reminders to drink water every 2 hours. You can place a water bottle on your desk as a visual cue.", // String: A concise action-oriented suggestion, followed by an explanation or two of why this action is useful or beneficial.
                "habitData": {{
                    "name": "Drink Water",                  // Name of the habit (string)
                    "category": {{                          // The category field *must* strictly be one of the following values, matching the user's habit or context: "health", "work", "personal_growth", "hobby", "fitness", "education", "finance", "social", "spiritual"
                        "id": "health",                         // ID of the category
                        "name": "Health",                      // Name of the category
                        "iconPath": "assets/icons/health.png", // Path to the category icon
                        "colorHex": "#FF5733"                  // Hexadecimal color code for the category
                    }},
                    "repeatFrequency": "daily"             // How often the habit repeats (daily, weekly, monthly)
                    "startDate": "2024-03-01T00:00:00Z",   // Start date in ISO 8601 format
                    "untilDate": "2024-06-01T00:00:00Z",   // End date, or null if it continues indefinitely
                    "reminderEnabled": true,               // Boolean: whether reminders are enabled
                    "trackingType": "complete",            // Tracking type (complete, progress)
                    "targetValue": 8,                      // target value (integer, if Tracking type is progress)
                    "unit": "cups",                         // Unit of measurement (string, if Tracking type is progress)
                }},
            }},
        ]
        """
    return prompt


def _parse_ai_response(response_text: str) -> List[SuggestionResponse]:
    try:
        json_start = response_text.find("[")
        json_end = response_text.rfind("]") + 1

        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            suggestions_data = json.loads(json_str)
        else:
            suggestions_data = json.loads(response_text)

        suggestions = []
        for item in suggestions_data:
            suggestion = SuggestionResponse(
                id=str(uuid.uuid4()),
                user_id="",  # Set later in the service
                icon=item.get("icon", "💡"),
                title=item.get("title", "Habit Suggestion"),
                description=item.get("description", ""),
                habit_data=item.get("habitData"),
                created_at=datetime.now(),
                is_viewed=False,
                is_implemented=False,
            )
            suggestions.append(suggestion)

        return suggestions

    except json.JSONDecodeError:
        return []


def _refine_suggestions_prompt(
    suggestions: List[SuggestionResponse], top_n: int = 5
) -> str:
    """
    Sends a final prompt to Gemini to consolidate and refine suggestions into top N.
    """
    # Convert SuggestionResponse objects to dict
    suggestions_dicts = [s.model_dump(by_alias=True) for s in suggestions]

    print(
        "Refining suggestions...",
        {json.dumps(suggestions_dicts, indent=2, default=str)},
    )

    prompt = f"""
        You are an expert AI habit coach. Below is a list of habit suggestions already generated.

        ### Suggestions List:
        {json.dumps(suggestions_dicts, indent=2, default=str)}

        ### Task:
        - From the provided list, select the **top {top_n} suggestions**.
        - Prioritize **diversity** (different categories) and **impactfulness**.
        - Make sure they are **actionable** and **clear**.

        ### VERY IMPORTANT:
        - DO NOT remove or nullify any fields.
        - KEEP every field in the original suggestion objects exactly as they are, including:
            - `habitData` (even if it contains nested objects)

        ### Output format:
        Return ONLY a **JSON array** of full suggestion objects, **without changing any field names**.  
        Keep the field `habitData` as it is, and do not replace it with anything else.
        For example:
        [
            {{
                "title": "Stay Hydrated Regularly", // Motivating and clear title
                "description": "Try setting reminders to drink water every 2 hours. You can place a water bottle on your desk as a visual cue.", // String: A concise action-oriented suggestion, followed by an explanation or two of why this action is useful or beneficial.
                "habitData": {{
                    "name": "Drink Water",                  // Name of the habit (string)
                    "category": {{                          // The category field *must* strictly be one of the following values, matching the user's habit or context: "health", "work", "personal_growth", "hobby", "fitness", "education", "finance", "social", "spiritual"
                        "id": "health",                         // ID of the category
                        "name": "Health",                      // Name of the category
                        "iconPath": "assets/icons/health.png", // Path to the category icon
                        "colorHex": "#FF5733"                  // Hexadecimal color code for the category
                    }},
                    "repeatFrequency": "daily"             // How often the habit repeats (daily, weekly, monthly)
                    "startDate": "2024-03-01T00:00:00Z",   // Start date in ISO 8601 format
                    "untilDate": "2024-06-01T00:00:00Z",   // End date, or null if it continues indefinitely
                    "reminderEnabled": true,               // Boolean: whether reminders are enabled
                    "trackingType": "complete",            // Tracking type (complete, progress)
                    "targetValue": 8,                      // target value (integer, if Tracking type is progress)
                    "unit": "cups",                         // Unit of measurement (string, if Tracking type is progress)
                }},
            }},
        ]
        """

    return prompt
