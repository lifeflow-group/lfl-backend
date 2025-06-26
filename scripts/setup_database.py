import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Add root directory to sys.path to enable imports from app
sys.path.append(str(Path(__file__).parent.parent))

from app.models.user import User
from app.models.category import Category
from app.models.habit import Habit, TrackingType, RepeatFrequency
from app.models.habit_series import HabitSeries
from app.models.suggestion import Suggestion
from app.models.habit_plan import HabitPlan, HabitPlanSuggestion
from app.database import SessionLocal, engine, Base

# Create all tables if they don't exist
Base.metadata.create_all(bind=engine)


def create_test_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(User).first() is not None:
            print("Database already has data. Skipping initialization.")
            return

        print("Starting sample data initialization...")

        # Create sample user
        test_user = User(id="user_1", name="Test User")
        db.add(test_user)
        db.flush()

        # Create categories
        categories = [
            Category(
                id="health",
                name="Health",
                color_hex="#FF5733",  # Reddish orange
                icon_path="assets/icons/health.png",
            ),
            Category(
                id="work",
                name="Work",
                color_hex="#3498DB",  # Blue
                icon_path="assets/icons/work.png",
            ),
            Category(
                id="personal_growth",
                name="Personal Growth",
                color_hex="#9B59B6",  # Purple
                icon_path="assets/icons/personal_growth.png",
            ),
            Category(
                id="hobby",
                name="Hobby",
                color_hex="#F1C40F",  # Yellow
                icon_path="assets/icons/hobby.png",
            ),
            Category(
                id="fitness",
                name="Fitness",
                color_hex="#2ECC71",  # Green
                icon_path="assets/icons/fitness.png",
            ),
            Category(
                id="education",
                name="Education",
                color_hex="#E67E22",  # Orange
                icon_path="assets/icons/education.png",
            ),
            Category(
                id="finance",
                name="Finance",
                color_hex="#27AE60",  # Dark Green
                icon_path="assets/icons/finance.png",
            ),
            Category(
                id="social",
                name="Social",
                color_hex="#E74C3C",  # Red
                icon_path="assets/icons/social.png",
            ),
            Category(
                id="spiritual",
                name="Spiritual",
                color_hex="#8E44AD",  # Dark Purple
                icon_path="assets/icons/spiritual.png",
            ),
            Category(
                id="mindfulness",
                name="Mindfulness",
                color_hex="#1ABC9C",  # Turquoise
                icon_path="assets/icons/mindfulness.png",
            ),
            Category(
                id="sleep",
                name="Sleep",
                color_hex="#34495E",  # Dark Blue
                icon_path="assets/icons/sleep.png",
            ),
            Category(
                id="productivity",
                name="Productivity",
                color_hex="#16A085",  # Green Sea
                icon_path="assets/icons/productivity.png",
            ),
        ]

        for cat in categories:
            db.add(cat)

        db.flush()
        print(f"Created {len(categories)} categories.")

        # Create sample habits
        habits = []

        # Health habits
        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440001",  # Cập nhật theo định dạng yêu cầu
                name="Morning Hydration",
                user_id=test_user.id,
                category_id=categories[0].id,  # Health
                tracking_type=TrackingType.PROGRESS,
                target_value=8,
                unit="glass",
                current_value=0,
                is_completed=False,
                reminder_enabled=True,
            )
        )

        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440002",
                name="Morning Stretch",
                user_id=test_user.id,
                category_id=categories[0].id,  # Health
                tracking_type=TrackingType.COMPLETE,
                reminder_enabled=True,
            )
        )

        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440003",
                name="Nutritious Breakfast",
                user_id=test_user.id,
                category_id=categories[0].id,  # Health
                tracking_type=TrackingType.COMPLETE,
                reminder_enabled=True,
            )
        )

        # Mindfulness habits
        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440004",
                name="Deep Breathing",
                user_id=test_user.id,
                category_id=categories[2].id,  # Mindfulness
                tracking_type=TrackingType.PROGRESS,
                target_value=5,
                unit="minutes",
                current_value=0,
                is_completed=False,
                reminder_enabled=True,
            )
        )

        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440005",
                name="Meditation",
                user_id=test_user.id,
                category_id=categories[2].id,  # Mindfulness
                tracking_type=TrackingType.PROGRESS,
                target_value=10,
                unit="minutes",
                current_value=0,
                is_completed=False,
                reminder_enabled=True,
            )
        )

        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440006",
                name="Gratitude Practice",
                user_id=test_user.id,
                category_id=categories[2].id,  # Mindfulness
                tracking_type=TrackingType.COMPLETE,
                reminder_enabled=True,
            )
        )

        # Productivity habits
        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440007",
                name="Focus Session",
                user_id=test_user.id,
                category_id=categories[1].id,  # Productivity
                tracking_type=TrackingType.PROGRESS,
                target_value=25,
                unit="minutes",
                current_value=0,
                is_completed=False,
                reminder_enabled=True,
            )
        )

        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440008",
                name="Day Planning",
                user_id=test_user.id,
                category_id=categories[1].id,  # Productivity
                tracking_type=TrackingType.COMPLETE,
                reminder_enabled=True,
            )
        )

        # Sleep habits
        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440009",
                name="No screens before bed",
                user_id=test_user.id,
                category_id=categories[3].id,  # Sleep
                tracking_type=TrackingType.COMPLETE,
                reminder_enabled=True,
            )
        )

        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440010",
                name="Consistent sleep time",
                user_id=test_user.id,
                category_id=categories[3].id,  # Sleep
                tracking_type=TrackingType.COMPLETE,
                reminder_enabled=True,
            )
        )

        # Growth habits
        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440011",
                name="Daily Reading",
                user_id=test_user.id,
                category_id=categories[4].id,  # Personal Growth
                tracking_type=TrackingType.PROGRESS,
                target_value=20,
                unit="minutes",
                current_value=0,
                is_completed=False,
                reminder_enabled=True,
            )
        )

        habits.append(
            Habit(
                id="habit-550e8400-e29b-41d4-a716-446655440012",
                name="Learning Session",
                user_id=test_user.id,
                category_id=categories[4].id,  # Personal Growth
                tracking_type=TrackingType.PROGRESS,
                target_value=30,
                unit="minutes",
                current_value=0,
                is_completed=False,
                reminder_enabled=True,
            )
        )

        for habit in habits:
            db.add(habit)

        db.flush()
        print(f"Created {len(habits)} sample habits.")

        # Create HabitSeries for each habit
        habit_series_list = []

        # Health habits series (Daily)
        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440001",  # Cập nhật theo định dạng yêu cầu
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440001",  # Liên kết với habit tương ứng
                start_date=datetime.now(timezone.utc),
                until_date=datetime.now(timezone.utc) + timedelta(days=90),  # 3 months
                repeat_frequency=RepeatFrequency.DAILY,
            )
        )

        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440002",
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440002",
                start_date=datetime.now(timezone.utc),
                repeat_frequency=RepeatFrequency.DAILY,
            )
        )

        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440003",
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440003",
                start_date=datetime.now(timezone.utc),
                repeat_frequency=RepeatFrequency.DAILY,
            )
        )

        # Mindfulness habits series (mix of daily and weekly)
        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440004",
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440004",
                start_date=datetime.now(timezone.utc),
                repeat_frequency=RepeatFrequency.DAILY,
            )
        )

        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440005",
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440005",
                start_date=datetime.now(timezone.utc),
                repeat_frequency=RepeatFrequency.DAILY,
            )
        )

        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440006",
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440006",
                start_date=datetime.now(timezone.utc),
                repeat_frequency=RepeatFrequency.WEEKLY,
            )
        )

        # Productivity habits series
        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440007",
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440007",
                start_date=datetime.now(timezone.utc),
                repeat_frequency=RepeatFrequency.DAILY,
            )
        )

        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440008",
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440008",
                start_date=datetime.now(timezone.utc),
                repeat_frequency=RepeatFrequency.DAILY,
            )
        )

        # Sleep habits series
        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440009",
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440009",
                start_date=datetime.now(timezone.utc),
                repeat_frequency=RepeatFrequency.DAILY,
            )
        )

        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440010",
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440010",
                start_date=datetime.now(timezone.utc),
                repeat_frequency=RepeatFrequency.DAILY,
            )
        )

        # Growth habits series
        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440011",
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440011",
                start_date=datetime.now(timezone.utc),
                repeat_frequency=RepeatFrequency.DAILY,
            )
        )

        habit_series_list.append(
            HabitSeries(
                id="series-550e8400-e29b-41d4-a716-446655440012",
                user_id=test_user.id,
                habit_id="habit-550e8400-e29b-41d4-a716-446655440012",
                start_date=datetime.now(timezone.utc),
                repeat_frequency=RepeatFrequency.WEEKLY,
            )
        )

        # Add all series to db
        for series in habit_series_list:
            db.add(series)

        db.flush()
        print(f"Created {len(habit_series_list)} habit series.")

        # Update habits with corresponding habit_series_id
        for series in habit_series_list:
            # Find the corresponding habit and update its habit_series_id
            habit = db.query(Habit).filter(Habit.id == series.habit_id).first()
            if habit:
                habit.habit_series_id = series.id

        db.flush()
        print("Updated habits with their series IDs.")

        # Create suggestions
        suggestions = []

        # Health suggestions
        suggestions.append(
            Suggestion(
                id="sugg_water",
                title="Morning Hydration",
                description="Drink a glass of water right after waking up to rehydrate your body after sleep. "
                "Overnight, your body becomes dehydrated. Drinking water first thing in the morning "
                "rehydrates your body, kickstarts your metabolism, and helps flush out toxins.",
                user_id=test_user.id,
                habit_id=habits[0].id,
                created_at=datetime.now(),
            )
        )

        suggestions.append(
            Suggestion(
                id="sugg_stretch",
                title="Morning Stretch",
                description="Morning stretching improves blood circulation, increases flexibility, and helps your "
                "muscles prepare for the day. It also reduces stiffness from sleep and can improve your "
                "posture throughout the day.",
                user_id=test_user.id,
                habit_id=habits[1].id,
                created_at=datetime.now(),
            )
        )

        suggestions.append(
            Suggestion(
                id="sugg_breakfast",
                title="Nutritious Breakfast",
                description="A healthy breakfast provides energy for the day, stabilizes blood sugar levels, and "
                "helps prevent overeating later. Including protein and fiber keeps you fuller longer and "
                "supports sustained energy release.",
                user_id=test_user.id,
                habit_id=habits[2].id,
                created_at=datetime.now(),
            )
        )

        # Mindfulness suggestions
        suggestions.append(
            Suggestion(
                id="sugg_breathing",
                title="Deep Breathing",
                description="Deep, controlled breathing activates your parasympathetic nervous system, which controls "
                "your relaxation response. This simple practice can quickly reduce stress hormones and promote "
                "a sense of calm.",
                user_id=test_user.id,
                habit_id=habits[3].id,
                created_at=datetime.now(),
            )
        )

        suggestions.append(
            Suggestion(
                id="sugg_meditation",
                title="Meditation",
                description="Regular meditation strengthens the prefrontal cortex and reduces activity in the amygdala, "
                "physically changing how your brain processes stress and emotions over time. Even short "
                "sessions provide meaningful benefits.",
                user_id=test_user.id,
                habit_id=habits[4].id,
                created_at=datetime.now(),
            )
        )

        suggestions.append(
            Suggestion(
                id="sugg_gratitude",
                title="Gratitude Practice",
                description="Gratitude practices activate your brain's reward pathways and increase serotonin production. "
                "Regular gratitude journaling has been shown to significantly improve happiness, reduce depression, "
                "and enhance overall life satisfaction.",
                user_id=test_user.id,
                habit_id=habits[5].id,
                created_at=datetime.now(),
            )
        )

        # Productivity suggestions
        suggestions.append(
            Suggestion(
                id="sugg_focus",
                title="Focus Session",
                description="Using time-blocking techniques like the Pomodoro method helps maximize concentration by "
                "working in defined intervals. This approach prevents burnout while maintaining high "
                "productivity during focused periods.",
                user_id=test_user.id,
                habit_id=habits[6].id,
                created_at=datetime.now(),
            )
        )

        suggestions.append(
            Suggestion(
                id="sugg_planning",
                title="Day Planning",
                description="Planning your day the evening before reduces decision fatigue and creates a clear roadmap "
                "for immediate action. This practice also helps your brain relax by transferring tasks from "
                "mental storage to an external system.",
                user_id=test_user.id,
                habit_id=habits[7].id,
                created_at=datetime.now(),
            )
        )

        # Sleep suggestions
        suggestions.append(
            Suggestion(
                id="sugg_no_screen",
                title="No screens before bed",
                description="Blue light from screens suppresses melatonin, the hormone responsible for sleep. Establishing "
                "a screen-free period before bed helps your body naturally prepare for sleep and improves sleep quality.",
                user_id=test_user.id,
                habit_id=habits[8].id,
                created_at=datetime.now(),
            )
        )

        suggestions.append(
            Suggestion(
                id="sugg_sleep_time",
                title="Consistent bedtime",
                description="A regular sleep schedule strengthens your circadian rhythm – your body's internal clock. "
                "This helps you fall asleep faster and wake up more refreshed by aligning your sleep with "
                "your natural biological cycles.",
                user_id=test_user.id,
                habit_id=habits[9].id,
                created_at=datetime.now(),
            )
        )

        # Growth suggestions
        suggestions.append(
            Suggestion(
                id="sugg_reading",
                title="Daily Reading",
                description="Regular reading strengthens neural connections, improves vocabulary, and exposes you to "
                "new ideas. This habit compounds over time, with as little as 20 minutes daily leading to "
                "significant knowledge acquisition over months.",
                user_id=test_user.id,
                habit_id=habits[10].id,
                created_at=datetime.now(),
            )
        )

        suggestions.append(
            Suggestion(
                id="sugg_learning",
                title="Learning Session",
                description="Deliberate practice of new skills creates and strengthens neural pathways. This type of "
                "focused learning activates multiple brain regions and contributes to cognitive reserve, "
                "protecting brain function as you age.",
                user_id=test_user.id,
                habit_id=habits[11].id,
                created_at=datetime.now(),
            )
        )

        for suggestion in suggestions:
            db.add(suggestion)

        db.flush()
        print(f"Created {len(suggestions)} suggestions.")

        # Create 10 HabitPlans
        habit_plans = [
            # 1. Morning Routine
            HabitPlan(
                id="plan_morning_routine",
                title="Morning Health Routine",
                description="""## Introduction

A structured morning routine can set you up for success throughout the day. This plan combines hydration, movement, and nutrition to give your body what it needs first thing in the morning.

## Benefits

- **Improved Energy Levels**: Start your day with practices that energize your body
- **Better Metabolism**: Kickstart your metabolism for improved digestion throughout the day
- **Mental Clarity**: Set a positive tone for your day with mindful morning practices

## Scientific Background

Studies show that consistent morning habits can improve energy levels, metabolism, and overall wellbeing. Research published in the Journal of Physiology found that morning exercise can help regulate circadian rhythms and improve sleep quality.
""",
                category_id="health",
                image_path="static/images/plans/morning_routine.png",
            ),
            # 2. Stress Management
            HabitPlan(
                id="plan_stress_management",
                title="Stress Management",
                description="""## Introduction

Chronic stress can negatively impact both physical and mental health. This plan introduces evidence-based habits for managing stress through mindfulness, physical activity, and healthy boundaries.

## Key Benefits

- **Reduced Anxiety**: Learn techniques to calm your nervous system
- **Improved Focus**: Clear mental fog caused by chronic stress
- **Better Sleep**: Address stress-related sleep disturbances
- **Healthier Relationships**: Manage stress to improve interactions with others

## How It Works

By incorporating these habits into your routine, you can build resilience and improve your body's response to stressors. Each habit targets different aspects of stress management for a comprehensive approach.
""",
                category_id="health",
                image_path="static/images/plans/stress_management.png",
            ),
            # 3. Better Sleep
            HabitPlan(
                id="plan_better_sleep",
                title="Better Sleep",
                description="""## Introduction

Quality sleep is essential for physical health, cognitive function, and emotional wellbeing. This plan focuses on habits that promote better sleep hygiene and establish a consistent sleep schedule.

## Benefits of Better Sleep

- **Improved Memory and Cognition**: Sleep helps consolidate memories and enhances learning
- **Stronger Immune Function**: Quality sleep supports your body's defense systems
- **Mood Regulation**: Sleep plays a critical role in emotional processing and stability
- **Weight Management**: Sleep affects hormones that regulate hunger and metabolism

## The Science

Research from the National Sleep Foundation indicates that consistent sleep habits can dramatically improve sleep quality. These practices help align your body's circadian rhythm and create optimal conditions for restorative sleep.
""",
                category_id="sleep",
                image_path="static/images/plans/better_sleep.png",
            ),
            # 4. Deep Work
            HabitPlan(
                id="plan_deep_work",
                title="Deep Work Mastery",
                description="""## Introduction

Deep work is the ability to focus without distraction on cognitively demanding tasks. This plan helps you develop habits that enhance concentration, reduce distractions, and create optimal conditions for high-quality work.

## Key Benefits

- **Increased Output Quality**: Produce better work through focused attention
- **Faster Completion**: Accomplish tasks more efficiently with fewer distractions
- **Greater Satisfaction**: Experience the fulfillment of deep engagement with your work
- **Skill Development**: Accelerate learning and mastery through deliberate practice

## Applied Techniques

Based on Cal Newport's research on knowledge work productivity, these habits establish boundaries that protect your cognitive resources and create systems for consistent deep work sessions.
""",
                category_id="productivity",
                image_path="static/images/plans/deep_work.png",
            ),
            # 5. Time Management
            HabitPlan(
                id="plan_time_management",
                title="Effective Time Management",
                description="""## Introduction

Good time management allows you to accomplish more in less time, reduce stress, and improve work-life balance. This plan introduces practices that help you prioritize tasks, minimize distractions, and make the most of your available time.

## Benefits

- **Reduced Overwhelm**: Clear systems for organizing priorities and tasks
- **Increased Productivity**: Focus on high-impact activities first
- **Better Work-Life Balance**: Create boundaries between work and personal time
- **Lower Stress Levels**: Eliminate the anxiety of disorganization

## Implementation Strategy

These habits build on time management research from productivity experts like David Allen (Getting Things Done) and Francesco Cirillo (The Pomodoro Technique), adapted for practical daily use.
""",
                category_id="productivity",
                image_path="static/images/plans/time_management.png",
            ),
            # 6. Daily Mindfulness
            HabitPlan(
                id="plan_mindfulness",
                title="Daily Mindfulness",
                description="""## Introduction

Mindfulness is the practice of bringing one's attention to the present moment. This plan introduces habits that help you cultivate mindfulness throughout your day, reducing anxiety, improving focus, and enhancing your enjoyment of life's experiences.

## Benefits of Mindfulness

- **Stress Reduction**: Decrease physiological markers of stress
- **Improved Attention**: Strengthen your ability to focus and avoid distraction
- **Emotional Regulation**: Develop greater awareness and control of emotional responses
- **Enhanced Relationships**: Improve the quality of interactions through present-moment awareness

## Scientific Foundation

Regular mindfulness practice has been linked to reduced stress, better emotional regulation, and improved relationships. Research from institutions like Harvard and UCLA has documented structural brain changes resulting from consistent mindfulness practice.
""",
                category_id="mindfulness",
                image_path="static/images/plans/mindfulness.png",
            ),
            # 7. Continuous Learning
            HabitPlan(
                id="plan_continuous_learning",
                title="Continuous Learning",
                description="""## Introduction

Continuous learning keeps your mind sharp and opens doors to new opportunities. This plan helps you establish habits for regular learning, whether through reading, courses, or practical application.

## Benefits of Lifelong Learning

- **Career Advancement**: Stay relevant in a rapidly changing work environment
- **Cognitive Health**: Build cognitive reserve that protects brain function as you age
- **Personal Fulfillment**: Experience the satisfaction of ongoing growth and discovery
- **Adaptability**: Develop the ability to thrive amid change and uncertainty

## Implementation Approach

By committing to ongoing education, you can stay relevant in your field, discover new interests, and maintain cognitive health. This plan balances structured learning with exploratory discovery for a sustainable practice.
""",
                category_id="personal_growth",
                image_path="static/images/plans/learning.png",
            ),
            # 8. Physical Wellness
            HabitPlan(
                id="plan_physical_wellness",
                title="Physical Wellness",
                description="""## Introduction

Regular physical activity is essential for overall health and wellbeing. This plan introduces simple, sustainable exercise habits that can be incorporated into your daily routine regardless of your fitness level.

## Benefits of Physical Activity

- **Improved Cardiovascular Health**: Strengthen your heart and improve circulation
- **Better Mood**: Exercise releases endorphins that boost your mental state
- **Increased Energy**: Regular movement enhances mitochondrial function
- **Weight Management**: Physical activity helps maintain a healthy body composition

## Getting Started

The key to sustainable exercise is finding activities you enjoy and starting with achievable goals. This plan helps you build a foundation of regular movement that can be expanded over time as your fitness improves.
""",
                category_id="fitness",
                image_path="static/images/plans/physical_wellness.png",
            ),
            # 9. Digital Wellbeing
            HabitPlan(
                id="plan_digital_wellbeing",
                title="Digital Wellbeing",
                description="""## Introduction

In our connected world, developing a healthy relationship with technology is crucial for mental health. This plan helps you establish boundaries with digital devices to reduce stress and reclaim your attention.

## Benefits of Digital Balance

- **Improved Focus**: Reduce the constant interruptions that fragment attention
- **Better Sleep**: Limit blue light exposure that disrupts circadian rhythms
- **Reduced Anxiety**: Minimize social media comparison and information overload
- **More Present**: Engage more fully in real-world experiences and relationships

## Implementation Strategy

Rather than attempting a complete digital detox, this plan focuses on creating intentional boundaries around technology use while maintaining its benefits in your life.
""",
                category_id="mindfulness",
                image_path="static/images/plans/digital_wellbeing.png",
            ),
            # 10. Emotional Intelligence
            HabitPlan(
                id="plan_emotional_intelligence",
                title="Emotional Intelligence",
                description="""## Introduction

Emotional intelligence (EQ) is the ability to recognize, understand and manage emotions in yourself and others. This plan introduces practices that strengthen emotional awareness and regulation.

## Benefits of Emotional Intelligence

- **Better Relationships**: Improve communication and connection with others
- **Reduced Conflict**: Handle disagreements with more skill and less stress
- **Improved Decision Making**: Make choices that align with your long-term values
- **Greater Resilience**: Bounce back more quickly from setbacks and challenges

## The Science

Research suggests emotional intelligence may be more important than IQ for success in many areas of life. These habits help develop the neural pathways involved in emotional processing and regulation.
""",
                category_id="personal_growth",
                image_path="static/images/plans/emotional_intelligence.png",
            ),
        ]

        for plan in habit_plans:
            db.add(plan)

        db.flush()
        print(f"Created {len(habit_plans)} habit plans.")

        # Create links between HabitPlans and Suggestions
        plan_suggestions = [
            # Morning Routine
            HabitPlanSuggestion(
                habit_plan_id="plan_morning_routine", suggestion_id="sugg_water"
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_morning_routine", suggestion_id="sugg_stretch"
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_morning_routine", suggestion_id="sugg_breakfast"
            ),
            # Stress Management
            HabitPlanSuggestion(
                habit_plan_id="plan_stress_management", suggestion_id="sugg_breathing"
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_stress_management", suggestion_id="sugg_meditation"
            ),
            # Better Sleep
            HabitPlanSuggestion(
                habit_plan_id="plan_better_sleep", suggestion_id="sugg_no_screen"
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_better_sleep", suggestion_id="sugg_sleep_time"
            ),
            # Deep Work
            HabitPlanSuggestion(
                habit_plan_id="plan_deep_work", suggestion_id="sugg_focus"
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_deep_work", suggestion_id="sugg_planning"
            ),
            # Time Management
            HabitPlanSuggestion(
                habit_plan_id="plan_time_management", suggestion_id="sugg_planning"
            ),
            # Daily Mindfulness
            HabitPlanSuggestion(
                habit_plan_id="plan_mindfulness", suggestion_id="sugg_meditation"
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_mindfulness", suggestion_id="sugg_breathing"
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_mindfulness", suggestion_id="sugg_gratitude"
            ),
            # Continuous Learning
            HabitPlanSuggestion(
                habit_plan_id="plan_continuous_learning", suggestion_id="sugg_reading"
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_continuous_learning", suggestion_id="sugg_learning"
            ),
            # Digital Wellbeing
            HabitPlanSuggestion(
                habit_plan_id="plan_digital_wellbeing", suggestion_id="sugg_no_screen"
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_digital_wellbeing", suggestion_id="sugg_meditation"
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_digital_wellbeing", suggestion_id="sugg_reading"
            ),
            # Physical Wellness
            HabitPlanSuggestion(
                habit_plan_id="plan_physical_wellness", suggestion_id="sugg_stretch"
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_physical_wellness", suggestion_id="sugg_water"
            ),
            # Emotional Intelligence
            HabitPlanSuggestion(
                habit_plan_id="plan_emotional_intelligence",
                suggestion_id="sugg_gratitude",
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_emotional_intelligence",
                suggestion_id="sugg_meditation",
            ),
            HabitPlanSuggestion(
                habit_plan_id="plan_emotional_intelligence",
                suggestion_id="sugg_breathing",
            ),
        ]

        for ps in plan_suggestions:
            db.add(ps)

        db.commit()
        print(f"Created {len(plan_suggestions)} links between plans and suggestions.")
        print("Sample data initialization completed!")

    except Exception as e:
        db.rollback()
        print(f"Error initializing data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting database initialization script...")
    create_test_data()
