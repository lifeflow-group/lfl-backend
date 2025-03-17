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
    habits: List[HabitResponse],
    metrics: List[PerformanceMetricResponse],
    chunk_size: int = 300 # Average: 1,000,000 / 15 per minute ≈ 66,666 tokens per request 
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

    # 1. Handle chunk splitting
    for i in range(0, len(habits), chunk_size):
        chunk_habits = habits[i:i + chunk_size]
        chunk_metrics = [m for m in metrics if m.habit_id in [h.id for h in chunk_habits]]
        
        prompt = _create_suggestion_prompt(chunk_habits, chunk_metrics)
        
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
            chunk_suggestions = all_suggestions[i:i + chunk_size]
            # Await for the asynchronous function
            prompt = _refine_suggestions_prompt(chunk_suggestions)
            response = await async_generate_content(prompt, model1)
            refined_chunk= _parse_ai_response(response.text)
            final_suggestions.extend(refined_chunk)
            print(f"Processing suggestion chunks: {i} - {i + chunk_size}")
            time.sleep(2)

    else:
        final_suggestions = all_suggestions

    return final_suggestions
    # return all_suggestions


def _create_suggestion_prompt(habits: List[HabitResponse], metrics: List[PerformanceMetricResponse]) -> str:
    habits_with_metrics = []
    for habit in habits:
        metric = next((m for m in metrics if m.habit_id == habit.id), None)
        if metric:
            habits_with_metrics.append({
                "id": habit.id,
                "name": habit.name,
                "category": habit.category.label if habit.category else "",
                "repeat_frequency": habit.repeat_frequency.value if habit.repeat_frequency else None,
                "reminder_enabled": habit.reminder_enabled,
                "tracking_type": habit.tracking_type.value if habit.tracking_type else None,
                "quantity": habit.quantity,
                "unit": habit.unit,
                "progress": habit.progress,
                "completed": habit.completed,
                "start_date": habit.start_date.isoformat() if habit.start_date else None,

                # Performance metrics
                "completion_rate": metric.completion_rate,
                "average_progress": metric.average_progress,
                "total_progress": metric.total_progress,
                "metric_description": metric.description,
                "metric_start_date": metric.start_date.isoformat() if metric.start_date else None,
                "metric_end_date": metric.end_date.isoformat() if metric.end_date else None,
            })

    prompt = f"""
        You are an expert AI habit coach. Your task is to analyze the user's current habits and performance metrics, then generate personalized, actionable suggestions to help them improve their habits.

        ### Data:
        Here is the user's current habit data and performance metrics in JSON format:
        {json.dumps(habits_with_metrics, indent=2)}

        Each item in the list has the following fields:
        - id (string): Unique identifier for the habit.
        - name (string): Name of the habit.
        - category (string): The category this habit belongs to (e.g., Health, Work).
        - repeat_frequency (string): How often the habit repeats (daily, weekly, monthly).
        - reminder_enabled (boolean): Whether the habit has reminders enabled.
        - tracking_type (string): Whether the habit is tracked by completion (complete/incomplete) or progress (amount-based).
        - quantity (integer): The target quantity for progress-based habits (e.g., 8 glasses of water).
        - unit (string): The unit for the quantity (e.g., cups, minutes).
        - progress (integer): Current progress made toward completing the habit.
        - completed (boolean): Whether the habit was completed today.
        - start_date (ISO string): When the habit was started.
          // Performance metrics:
        - completion_rate (float): How often the habit is completed (0.0 - 1.0).
        - average_progress (float): Average progress made over time.
        - total_progress (float): Total amount of progress made.
        - metric_description (string): Optional description or summary of the user's performance.
        - metric_start_date (ISO string): The start date of the period being measured.
        - metric_end_date (ISO string): The end date of the period being measured.

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
                "icon": "💧",   // Emoji representing the suggestion (related to the habit)
                "title": "Stay Hydrated Regularly", // Motivating and clear title
                "description": "Try setting reminders to drink water every 2 hours. You can place a water bottle on your desk as a visual cue.", // String: A concise action-oriented suggestion, followed by an explanation or two of why this action is useful or beneficial.
                "habit_data": {{
                    "id": "habit_001",                      // Unique habit ID (string)
                    "name": "Drink Water",                  // Name of the habit (string)
                    "user_id": "user_001",                  // The user associated with the habit (string)
                    "category_id": "health",                // The category_id field *must* strictly be one of the following values, matching the user's habit or context: "health", "work", "personal_growth", "hobby", "fitness", "education", "finance", "social", "spiritual"
                    "start_date": "2024-03-01T00:00:00Z",   // Start date in ISO 8601 format
                    "repeat_frequency": "DAILY",            // Repeat frequency (DAILY, WEEKLY, MONTHLY)
                    "reminder_enabled": true,               // Boolean: whether reminders are enabled
                    "tracking_type": "COMPLETE",            // Tracking type (COMPLETE, PROGRESS)
                    "quantity": 8,                          // Quantity target (integer, if Tracking type is PROGRESS)
                    "unit": "cups",                         // Unit of measurement (string, if if Tracking type is PROGRESS)
                    "progress": 0,                          // Current progress (integer, if Tracking type is PROGRESS)
                    "completed": false                      // Boolean: whether the habit was completed today (if Tracking type is COMPLETE)
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
                habit_data=item.get("habit_data"),
                created_at=datetime.now(),
                is_viewed=False,
                is_implemented=False
            )
            suggestions.append(suggestion)

        return suggestions

    except json.JSONDecodeError:
        return []

def _refine_suggestions_prompt(suggestions: List[SuggestionResponse], top_n: int = 5) -> str:
    """
    Sends a final prompt to Gemini to consolidate and refine suggestions into top N.
    """
    # Convert SuggestionResponse objects to dict
    suggestions_dicts = [s.model_dump() for s in suggestions]
    
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
            - `habit_data` (even if it contains nested objects)
            - `created_at`
            - `is_viewed`
            - `is_implemented`

        ### Output format:
        Return ONLY a **JSON array** of full suggestion objects, **without changing any field names**.  
        Keep the field `habit_data` as it is, and do not replace it with anything else.
        For example:
        [
            {{
                "icon": "💧",   // Emoji representing the suggestion (related to the habit)
                "title": "Stay Hydrated Regularly", // Motivating and clear title
                "description": "Try setting reminders to drink water every 2 hours. You can place a water bottle on your desk as a visual cue.", // String: A concise action-oriented suggestion, followed by an explanation or two of why this action is useful or beneficial.
                "habit_data": {{
                    "id": "habit_001",                      // Unique habit ID (string)
                    "name": "Drink Water",                  // Name of the habit (string)
                    "user_id": "user_001",                  // The user associated with the habit (string)
                    "category_id": "health",                // The category_id field *must* strictly be one of the following values, matching the user's habit or context: "health", "work", "personal_growth", "hobby", "fitness", "education", "finance", "social", "spiritual"
                    "start_date": "2024-03-01T00:00:00Z",   // Start date in ISO 8601 format
                    "repeat_frequency": "DAILY",            // Repeat frequency (DAILY, WEEKLY, MONTHLY)
                    "reminder_enabled": true,               // Boolean: whether reminders are enabled
                    "tracking_type": "COMPLETE",            // Tracking type (COMPLETE, PROGRESS)
                    "quantity": 8,                          // Quantity target (integer, if Tracking type is PROGRESS)
                    "unit": "cups",                         // Unit of measurement (string, if if Tracking type is PROGRESS)
                    "progress": 0,                          // Current progress (integer, if Tracking type is PROGRESS)
                    "completed": false                      // Boolean: whether the habit was completed today (if Tracking type is COMPLETE)
                }},
            }},
        ]
        """

    return prompt
