from langchain.memory import ChatMessageHistory


class SessionMemory:
    def __init__(self):
        self.sessions = {}

    def get_memory(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatMessageHistory(session_id=session_id)
        return self.sessions[session_id]
