"""
Chat Service - Manages chat interactions with reports using RAG.
"""

from agents import ChatAgent
from config import settings
from typing import Dict, Any, List
import json
import os
from datetime import datetime
import uuid


class ChatService:
    """Service for managing chat conversations about reports."""

    def __init__(self):
        """Initialize chat service."""
        self.chat_agent = ChatAgent()
        os.makedirs(settings.CHAT_HISTORY_DIR, exist_ok=True)

    async def send_message(
        self,
        report_id: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Send a message and get AI response.

        Args:
            report_id: Report to chat about
            message: User's message

        Returns:
            Dictionary with response and metadata
        """
        # Load conversation history
        history = self.get_chat_history(report_id)

        # Get answer from chat agent
        result = await self.chat_agent.answer_question(
            report_id=report_id,
            question=message,
            conversation_history=history.get("messages", [])
        )

        if not result["success"]:
            return {
                "success": False,
                "error": result.get("error", "Unknown error")
            }

        # Create user message
        user_message = {
            "id": str(uuid.uuid4()),
            "report_id": report_id,
            "role": "user",
            "content": message,
            "created_at": datetime.utcnow().isoformat()
        }

        # Create assistant message
        assistant_message = {
            "id": str(uuid.uuid4()),
            "report_id": report_id,
            "role": "assistant",
            "content": result["answer"],
            "sources": result.get("sources", []),
            "created_at": datetime.utcnow().isoformat()
        }

        # Update history
        if not history:
            history = {"report_id": report_id, "messages": []}

        history["messages"].append(user_message)
        history["messages"].append(assistant_message)

        # Save history
        self._save_chat_history(report_id, history)

        return {
            "success": True,
            "message": assistant_message
        }

    def get_chat_history(self, report_id: str) -> Dict[str, Any]:
        """Get chat history for a report."""
        chat_path = os.path.join(
            settings.CHAT_HISTORY_DIR,
            f"{report_id}_chat.json"
        )

        if not os.path.exists(chat_path):
            return {"report_id": report_id, "messages": []}

        try:
            with open(chat_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading chat history for {report_id}: {e}")
            return {"report_id": report_id, "messages": []}

    def _save_chat_history(self, report_id: str, history: Dict[str, Any]) -> None:
        """Save chat history to JSON file."""
        chat_path = os.path.join(
            settings.CHAT_HISTORY_DIR,
            f"{report_id}_chat.json"
        )

        try:
            with open(chat_path, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving chat history for {report_id}: {e}")

    def clear_chat_history(self, report_id: str) -> bool:
        """Clear chat history for a report."""
        chat_path = os.path.join(
            settings.CHAT_HISTORY_DIR,
            f"{report_id}_chat.json"
        )

        try:
            if os.path.exists(chat_path):
                os.remove(chat_path)
            return True
        except Exception as e:
            print(f"Error clearing chat history for {report_id}: {e}")
            return False

    async def generate_suggested_questions(
        self,
        report_id: str
    ) -> List[str]:
        """Generate suggested follow-up questions."""
        history = self.get_chat_history(report_id)

        if not history.get("messages"):
            # Default questions for new chat
            return [
                "What are the main compliance risks in this report?",
                "Which of my routes are most affected?",
                "What actions should I prioritize?",
                "Are there any upcoming deadlines I need to know about?",
                "What changes affect hazardous cargo transport?"
            ]

        # Generate contextual questions
        try:
            questions = await self.chat_agent.generate_follow_up_questions(
                report_id=report_id,
                conversation_history=history.get("messages", [])
            )
            return questions
        except Exception as e:
            print(f"Error generating suggested questions: {e}")
            return [
                "Can you tell me more about this?",
                "What are the next steps?",
                "How does this affect my operations?"
            ]


# Global service instance
chat_service = ChatService()
