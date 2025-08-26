#!/usr/bin/env python3
"""
Memory system for persistent chat sessions and user information
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class UserProfile:
    """User profile with persistent information"""
    user_id: str
    name: str = ""
    age: Optional[int] = None
    concerns: List[str] = None
    preferences: Dict[str, Any] = None
    emergency_contact: str = ""
    created_at: str = ""
    last_active: str = ""
    
    def __post_init__(self):
        if self.concerns is None:
            self.concerns = []
        if self.preferences is None:
            self.preferences = {}
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.last_active = datetime.now().isoformat()

@dataclass
class ChatSession:
    """Individual chat session data"""
    session_id: str
    user_id: str
    messages: List[Dict[str, str]] = None
    topics_discussed: List[str] = None
    mood_indicators: List[str] = None
    advice_given: List[str] = None
    follow_ups_needed: List[str] = None
    risk_level: str = "low"
    session_summary: str = ""
    started_at: str = ""
    ended_at: str = ""
    
    def __post_init__(self):
        if self.messages is None:
            self.messages = []
        if self.topics_discussed is None:
            self.topics_discussed = []
        if self.mood_indicators is None:
            self.mood_indicators = []
        if self.advice_given is None:
            self.advice_given = []
        if self.follow_ups_needed is None:
            self.follow_ups_needed = []
        if not self.started_at:
            self.started_at = datetime.now().isoformat()

class MemoryManager:
    """Manages persistent user memory and chat sessions"""
    
    def __init__(self, data_dir: str = "user_data"):
        self.data_dir = data_dir
        self.profiles_dir = os.path.join(data_dir, "profiles")
        self.sessions_dir = os.path.join(data_dir, "sessions")
        
        # Create directories if they don't exist
        os.makedirs(self.profiles_dir, exist_ok=True)
        os.makedirs(self.sessions_dir, exist_ok=True)
        
        print(f"📁 Memory system initialized: {data_dir}")
    
    def generate_user_id(self, identifier: str) -> str:
        """Generate a consistent user ID from an identifier (like name)"""
        return hashlib.md5(identifier.lower().encode()).hexdigest()[:12]
    
    def create_session_id(self, user_id: str) -> str:
        """Generate a new session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{user_id}_{timestamp}"
    
    def load_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Load user profile from disk"""
        profile_path = os.path.join(self.profiles_dir, f"{user_id}.json")
        
        if os.path.exists(profile_path):
            try:
                with open(profile_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return UserProfile(**data)
            except Exception as e:
                print(f"❌ Error loading profile {user_id}: {e}")
                return None
        return None
    
    def save_user_profile(self, profile: UserProfile) -> bool:
        """Save user profile to disk"""
        profile_path = os.path.join(self.profiles_dir, f"{profile.user_id}.json")
        
        try:
            profile.last_active = datetime.now().isoformat()
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(profile), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving profile {profile.user_id}: {e}")
            return False
    
    def load_user_sessions(self, user_id: str, limit: int = 5) -> List[ChatSession]:
        """Load recent sessions for a user"""
        sessions = []
        user_sessions_dir = os.path.join(self.sessions_dir, user_id)
        
        if not os.path.exists(user_sessions_dir):
            return sessions
        
        try:
            # Get session files sorted by modification time (newest first)
            session_files = []
            for filename in os.listdir(user_sessions_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(user_sessions_dir, filename)
                    mtime = os.path.getmtime(filepath)
                    session_files.append((mtime, filepath))
            
            session_files.sort(reverse=True)  # Newest first
            
            # Load the most recent sessions
            for _, filepath in session_files[:limit]:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sessions.append(ChatSession(**data))
                    
        except Exception as e:
            print(f"❌ Error loading sessions for {user_id}: {e}")
        
        return sessions
    
    def save_session(self, session: ChatSession) -> bool:
        """Save chat session to disk"""
        user_sessions_dir = os.path.join(self.sessions_dir, session.user_id)
        os.makedirs(user_sessions_dir, exist_ok=True)
        
        session_path = os.path.join(user_sessions_dir, f"{session.session_id}.json")
        
        try:
            with open(session_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(session), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving session {session.session_id}: {e}")
            return False
    
    def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user context for AI"""
        context = {
            "profile": None,
            "recent_sessions": [],
            "key_topics": [],
            "ongoing_concerns": [],
            "previous_advice": [],
            "follow_ups": [],
            "mood_patterns": []
        }
        
        # Load profile
        profile = self.load_user_profile(user_id)
        if profile:
            context["profile"] = asdict(profile)
        
        # Load recent sessions
        sessions = self.load_user_sessions(user_id, limit=3)
        context["recent_sessions"] = [asdict(session) for session in sessions]
        
        # Extract patterns from sessions
        if sessions:
            all_topics = []
            all_advice = []
            all_follow_ups = []
            all_moods = []
            
            for session in sessions:
                all_topics.extend(session.topics_discussed)
                all_advice.extend(session.advice_given)
                all_follow_ups.extend(session.follow_ups_needed)
                all_moods.extend(session.mood_indicators)
            
            # Get unique items with frequency
            context["key_topics"] = list(set(all_topics))[:5]
            context["previous_advice"] = list(set(all_advice))[:3]
            context["follow_ups"] = list(set(all_follow_ups))[:3]
            context["mood_patterns"] = list(set(all_moods))[:5]
        
        return context
    
    def update_session_data(self, session: ChatSession, user_message: str, ai_response: str):
        """Update session with new message and extract insights"""
        # Add messages
        session.messages.append({"role": "user", "content": user_message, "timestamp": datetime.now().isoformat()})
        session.messages.append({"role": "assistant", "content": ai_response, "timestamp": datetime.now().isoformat()})
        
        # Extract topics and insights
        self._extract_session_insights(session, user_message, ai_response)
    
    def _extract_session_insights(self, session: ChatSession, user_message: str, ai_response: str):
        """Extract topics, mood, and advice from conversation"""
        user_lower = user_message.lower()
        
        # Extract topics
        topic_keywords = {
            "sleep": ["sleep", "insomnia", "tired", "sleepy", "awake", "rest"],
            "anxiety": ["anxious", "anxiety", "worried", "panic", "stress"],
            "depression": ["sad", "depressed", "hopeless", "down", "empty"],
            "work": ["work", "job", "boss", "colleague", "office", "career"],
            "relationships": ["friend", "family", "partner", "relationship", "social"],
            "health": ["health", "medication", "doctor", "physical", "body"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                if topic not in session.topics_discussed:
                    session.topics_discussed.append(topic)
        
        # Extract mood indicators
        mood_keywords = {
            "positive": ["good", "happy", "better", "great", "fine", "okay"],
            "negative": ["bad", "terrible", "awful", "horrible", "worse"],
            "anxious": ["anxious", "worried", "nervous", "stressed"],
            "sad": ["sad", "down", "depressed", "hopeless", "empty"],
            "tired": ["tired", "exhausted", "sleepy", "fatigue"]
        }
        
        for mood, keywords in mood_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                if mood not in session.mood_indicators:
                    session.mood_indicators.append(mood)
        
        # Extract advice given (simple heuristic)
        ai_lower = ai_response.lower()
        advice_patterns = [
            "try", "consider", "might help", "suggestion", "recommend", 
            "could", "maybe", "perhaps", "what if", "how about"
        ]
        
        if any(pattern in ai_lower for pattern in advice_patterns):
            # Simple extraction - in a real system, this would be more sophisticated
            advice_snippet = ai_response[:100] + "..." if len(ai_response) > 100 else ai_response
            if advice_snippet not in session.advice_given:
                session.advice_given.append(advice_snippet)
        
        # Check for follow-ups needed
        if any(word in user_lower for word in ["follow up", "next time", "again", "continue"]):
            session.follow_ups_needed.append("User expressed interest in continuing conversation")

# Global memory manager instance
memory_manager = MemoryManager()
