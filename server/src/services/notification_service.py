# src/services/notification_service.py

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

class StudyNotificationType(Enum):
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    BREAK_TIME = "break_time"
    EXAM_ALERT = "exam_alert"
    REVIEW_REMINDER = "review_reminder"

class StudyNotificationService:
    def __init__(self):
        self.notification_templates = {
            StudyNotificationType.SESSION_START: {
                "title": "Time to Study {subject}",
                "message": "📚 Your {duration} minute study session is starting now. Topic: {topic}"
            },
            StudyNotificationType.BREAK_TIME: {
                "title": "Break Time!",
                "message": "⏰ Time for a {duration} minute break. You've earned it!"
            },
            StudyNotificationType.EXAM_ALERT: {
                "title": "{subject} Exam Coming Up!",
                "message": "📝 You have an exam in {days_left} days. Time to prepare!"
            },
            StudyNotificationType.REVIEW_REMINDER: {
                "title": "Review Time for {subject}",
                "message": "🔄 It's time to review {topic} to strengthen your understanding."
            }
        }

    async def create_study_notification(
        self,
        user_id: int,
        notification_type: StudyNotificationType,
        data: Dict,
        schedule_time: Optional[datetime] = None
    ):
        template = self.notification_templates[notification_type]
        
        return {
            "user_id": user_id,
            "type": notification_type.value,
            "title": template["title"].format(**data),
            "message": template["message"].format(**data),
            "schedule_time": schedule_time or datetime.now(),
            "created_at": datetime.now(),
            "read": False
        }

    async def schedule_study_session(
        self,
        user_id: int,
        subject: str,
        topic: str,
        start_time: datetime,
        duration: int,
        break_intervals: List[int] = [25]  # Default Pomodoro
    ):
        notifications = []

        # Start notification (5 minutes before)
        notifications.append(
            await self.create_study_notification(
                user_id,
                StudyNotificationType.SESSION_START,
                {
                    "subject": subject,
                    "topic": topic,
                    "duration": duration
                },
                start_time - timedelta(minutes=5)
            )
        )

        # Break notifications
        current_time = start_time
        for interval in break_intervals:
            current_time += timedelta(minutes=interval)
            notifications.append(
                await self.create_study_notification(
                    user_id,
                    StudyNotificationType.BREAK_TIME,
                    {"duration": 5},  # 5-minute break
                    current_time
                )
            )

        return notifications

    async def schedule_exam_reminder(
        self,
        user_id: int,
        subject: str,
        exam_date: datetime,
        reminder_days: List[int] = [7, 3, 1]  # Default reminder days
    ):
        notifications = []
        
        for days in reminder_days:
            reminder_date = exam_date - timedelta(days=days)
            notifications.append(
                await self.create_study_notification(
                    user_id,
                    StudyNotificationType.EXAM_ALERT,
                    {
                        "subject": subject,
                        "days_left": days
                    },
                    reminder_date
                )
            )

        return notifications

    async def schedule_review_reminder(
        self,
        user_id: int,
        subject: str,
        topic: str,
        initial_study_date: datetime,
        intervals: List[int] = [1, 3, 7, 14]  # Spaced repetition intervals
    ):
        notifications = []
        
        for days in intervals:
            review_date = initial_study_date + timedelta(days=days)
            notifications.append(
                await self.create_study_notification(
                    user_id,
                    StudyNotificationType.REVIEW_REMINDER,
                    {
                        "subject": subject,
                        "topic": topic
                    },
                    review_date
                )
            )

        return notifications
