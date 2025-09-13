# backend/models/user_profile.py
"""
User Profile Model
------------------
Lightweight container for user-specific metadata that complements
the Second Brain memory system.
"""

from datetime import datetime
from typing import Optional, Dict, Any


class UserProfile:
    """
    Represents a user's core information and preferences.
    Extend this as needed (e.g., to store preferences, stats, etc.).
    """

    def __init__(
        self,
        user_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        preferences: Optional[Dict[str, Any]] = None,
    ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.preferences = preferences or {}
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    # ----- Basic Info -----
    def update_name(self, name: str):
        self.name = name
        self.updated_at = datetime.utcnow()

    def update_email(self, email: str):
        self.email = email
        self.updated_at = datetime.utcnow()

    # ----- Preferences -----
    def set_preference(self, key: str, value: Any):
        """
        Store a user preference, such as default answer style,
        favorite color, etc.
        """
        self.preferences[key] = value
        self.updated_at = datetime.utcnow()

    def get_preference(self, key: str, default=None):
        return self.preferences.get(key, default)

    # ----- Export -----
    def to_dict(self) -> Dict[str, Any]:
        """
        Return a serializable dictionary of user info,
        useful for APIs or saving to a DB.
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "preferences": self.preferences,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<UserProfile {self.user_id} name={self.name} email={self.email}>"
