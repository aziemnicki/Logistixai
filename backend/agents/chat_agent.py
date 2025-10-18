"""
Chat Agent - Answers questions about reports using RAG with ChromaDB.
Fourth agent for interactive Q&A.
"""

from anthropic import Anthropic
from config import settings
from vector_db import vector_db
from typing import List, Dict, Any, Optional
import json


class ChatAgent:
    """Agent responsible for answering questions about reports using RAG."""

    def __init__(self):
        """Initialize Chat Agent with Claude client and vector DB."""
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL
        self.vector_db = vector_db

    async def answer_question(
        self,
        report_id: str,
        question: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Answer a question about a specific report using RAG.

        Args:
            report_id: Report to query
            question: User's question
            conversation_history: Previous messages for context

        Returns:
            Dictionary with answer and sources
        """
        print(f"💬 Chat Agent: Answering question about report {report_id}")

        try:
            # Step 1: Retrieve relevant context from ChromaDB
            report_context = self.vector_db.get_report_context(
                report_id=report_id,
                query=question,
                n_results=3
            )

            search_context = self.vector_db.get_search_results_context(
                report_id=report_id,
                query=question,
                n_results=5
            )

            print(f"   Retrieved {len(report_context)} report chunks, {len(search_context)} sources")

            # Step 2: Generate answer using Claude with context
            answer, sources = await self._generate_answer(
                question=question,
                report_context=report_context,
                search_context=search_context,
                conversation_history=conversation_history
            )

            return {
                "success": True,
                "answer": answer,
                "sources": sources
            }

        except Exception as e:
            print(f"❌ Chat Agent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "answer": "I apologize, but I encountered an error while processing your question.",
                "sources": []
            }

    async def _generate_answer(
        self,
        question: str,
        report_context: List[str],
        search_context: List[Dict[str, str]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> tuple[str, List[str]]:
        """Generate answer using RAG context."""

        # Build context section
        context_text = "# Report Context:\n"
        for i, ctx in enumerate(report_context, 1):
            context_text += f"\n## Context {i}:\n{ctx}\n"

        context_text += "\n# Original Sources:\n"
        sources_list = []
        for i, src in enumerate(search_context, 1):
            context_text += f"\n## Source {i}:\n"
            context_text += f"Title: {src.get('title', 'N/A')}\n"
            context_text += f"URL: {src.get('url', 'N/A')}\n"
            context_text += f"Content: {src.get('content', 'N/A')}\n"
            sources_list.append(src.get('url', ''))

        # Build conversation history
        history_text = ""
        if conversation_history:
            history_text = "\n# Previous Conversation:\n"
            for msg in conversation_history[-5:]:  # Last 5 messages
                role = msg.get("role", "user")
                content = msg.get("content", "")
                history_text += f"{role.upper()}: {content}\n"

        # Build prompt
        prompt = f"""You are a helpful assistant answering questions about a logistics compliance report.

{history_text}

{context_text}

# User Question:
{question}

# Instructions:
1. Answer the question based ONLY on the context provided above
2. Be specific and cite sources when possible
3. If the context doesn't contain enough information, say so
4. Use bullet points for clarity when appropriate
5. Be concise but thorough
6. Reference specific URLs from the sources when relevant

Provide your answer below:"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.content[0].text.strip()

        # Extract unique sources mentioned in answer or used in context
        unique_sources = list(set(filter(None, sources_list)))

        return answer, unique_sources

    async def generate_follow_up_questions(
        self,
        report_id: str,
        conversation_history: List[Dict[str, str]]
    ) -> List[str]:
        """
        Generate suggested follow-up questions based on conversation.

        Args:
            report_id: Report being discussed
            conversation_history: Conversation so far

        Returns:
            List of 3-5 suggested questions
        """
        try:
            # Get report summary for context
            report = self.vector_db.get_report_by_id(report_id)

            history_text = "\n".join([
                f"{msg['role'].upper()}: {msg['content']}"
                for msg in conversation_history[-5:]
            ])

            prompt = f"""Based on this conversation about a logistics compliance report, suggest 3-5 relevant follow-up questions the user might want to ask.

Conversation:
{history_text}

Report Summary:
{json.dumps(report.get('metadata', {}), indent=2) if report else 'N/A'}

Generate questions that:
1. Dive deeper into topics already discussed
2. Explore related compliance issues
3. Ask about specific actions or deadlines
4. Clarify risk levels or impacts

Return ONLY a JSON array of question strings:
["question 1", "question 2", "question 3"]"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text.strip()

            # Parse questions
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            questions = json.loads(content)
            return questions[:5] if isinstance(questions, list) else []

        except Exception as e:
            print(f"Warning: Could not generate follow-up questions: {e}")
            return [
                "What are the main risks identified in this report?",
                "Which routes are most affected by these changes?",
                "What actions should I take first?"
            ]
