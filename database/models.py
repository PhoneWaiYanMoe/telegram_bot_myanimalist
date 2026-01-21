from datetime import datetime

class UserSession:
    """Store user session data in memory (use Redis in production)"""
    sessions = {}
    
    @classmethod
    def get(cls, user_id):
        if user_id not in cls.sessions:
            cls.sessions[user_id] = {
                'cart': [],
                'current_item': {},
                'stage': 'start',
                'user_info': {}
            }
        return cls.sessions[user_id]
    
    @classmethod
    def update(cls, user_id, data):
        session = cls.get(user_id)
        session.update(data)
        cls.sessions[user_id] = session
    
    @classmethod
    def clear(cls, user_id):
        if user_id in cls.sessions:
            del cls.sessions[user_id]
