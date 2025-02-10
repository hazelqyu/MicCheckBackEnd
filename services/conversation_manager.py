# services/conversation_manager.py
import threading


class ConversationManager:
    def __init__(self):
        self._conversation_histories = {}
        self._lock = threading.Lock()

    def get_conversation_history(self, conversation_id: str) -> list:
        """Retrieve conversation history for a given session."""
        with self._lock:
            return self._conversation_histories.get(conversation_id, [])

    def update_conversation_history(self, conversation_id: str, message: dict):
        """Append a message (dictionary with 'role' and 'content') to the history."""
        with self._lock:
            if conversation_id not in self._conversation_histories:
                self._conversation_histories[conversation_id] = []
            self._conversation_histories[conversation_id].append(message)

    def reset_conversation(self, conversation_id: str):
        """Reset the conversation history for a given session."""
        with self._lock:
            self._conversation_histories[conversation_id] = []


# Create a singleton instance.
conversation_manager = ConversationManager()
