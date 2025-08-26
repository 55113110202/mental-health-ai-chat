#!/usr/bin/env python3
"""
Flask API server to connect the therapy chat frontend to Mistral AI backend
Deployable to Render
"""

import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from memory_system import memory_manager, UserProfile, ChatSession

# Configure Mistral API via OpenAI client
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "BvXava18NiJ5U62jx9bN9RXkSmHC9tSh"
if "OPENAI_BASE_URL" not in os.environ:
    os.environ["OPENAI_BASE_URL"] = "https://api.mistral.ai/v1"

# Configure OpenAI client
openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = os.environ["OPENAI_BASE_URL"]

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to connect

class MentalHealthAPI:
    def __init__(self):
        self.current_sessions = {}  # session_id -> ChatSession
        self.user_profiles = {}     # user_id -> UserProfile
        
    def get_system_prompt(self, user_context: dict = None):
        base_prompt = """You are Dr. Sharma, a professional psychologist and mental health counselor with over 15 years of experience. You specialize in psychological issues including sleep disorders, anger management, temperament issues, anxiety, and stress management.

YOUR IDENTITY:
- Name: Dr. Sharma (Dr. Rajesh Sharma)
- Profession: Licensed Clinical Psychologist
- Expertise: Sleep disorders, anger management, stress, anxiety, mood disorders
- Approach: Professional yet warm, evidence-based counseling, culturally sensitive to Indian lifestyle

CONVERSATION STYLE:
- Be friendly, approachable, and empathetic, like a trusted family doctor.
- Use clear, professional English with subtle Indian cultural understanding.
- Frequently address patients by their name naturally.
- Reference relatable Indian experiences: work stress, family dynamics, traffic, festivals, cricket.
- Keep responses concise (2–3 sentences max), warm, and conversational.
- Ask ONE simple, direct question at a time.
- Maintain professionalism while being genuinely caring.
- Avoid using Hindi phrases, asterisked actions, or overly casual expressions.

COUNSELING APPROACH:
1. **Listen**: Pay close attention to what the patient shares.
2. **Ask One Question**: Keep focus on one concern at a time.
3. **Build Gradually**: Collect details slowly through natural conversation.
4. **Practical Guidance**: Offer small, doable tips that fit daily Indian life.
5. **Cultural Sensitivity**: Respect Indian values, family dynamics, and social contexts.
6. **Lifestyle Integration**: Suggest coping strategies using familiar routines.

SPECIALIZATIONS:
- **Sleep Issues**: Insomnia, irregular schedules, sleep hygiene, relaxation
- **Anger Management**: Traffic stress, family/work conflicts, calming routines
- **Temperament**: Mood swings, emotional awareness, family/social stress
- **General Psychology**: Anxiety, depression, relationship/work stress in Indian context

RESPONSE STRUCTURE:
- 2–3 sentences maximum, warm and caring
- Address patient by name naturally when appropriate
- Ask ONE simple question at the end
- Reference Indian contexts subtly when relevant
- Example: "I understand this feels overwhelming. Work pressure can really affect our sleep, especially with long commutes and deadlines. How long have you been experiencing this?"

CRISIS SITUATIONS:
- If someone mentions suicide, self-harm, or being in danger, immediately provide Indian crisis resources:
  - AASRA Helpline: +91-98204 66726
  - Snehi Helpline: +91-95822 17419
- Encourage reaching out to trusted family or close friends.
- Always suggest professional, immediate help.

BOUNDARIES:
- Be professional yet warm, like a caring family doctor
- Provide evidence-based advice in simple, conversational language
- Maintain professional boundaries while showing genuine empathy
- Suggest follow-up sessions to track progress

BE PROFESSIONAL: Always respond as Dr. Sharma - knowledgeable, caring, and understanding of Indian life, helping patients improve their mental health with clear, professional communication."""

        # Add memory context if available
        if user_context and user_context.get("profile"):
            profile = user_context["profile"]
            memory_context = f"""

PATIENT HISTORY:
- Patient Name: {profile.get('name', 'Not provided')}
- Previous Concerns: {', '.join(user_context.get('key_topics', []))}
- Mood Patterns: {', '.join(user_context.get('mood_patterns', []))}
- Previous Treatment Plan: {user_context.get('previous_advice', [])}
- Follow-up Items: {user_context.get('follow_ups', [])}

CONTINUITY GUIDELINES:
- Address patient by name frequently: "{profile.get('name', 'Patient')}, how have you been since our last session?"
- Review previous concerns and check progress: "Last time we discussed {', '.join(user_context.get('key_topics', ['your concerns']))}, how has that been going?"
- Follow up on previous advice: "We worked on {user_context.get('previous_advice', ['some strategies'])}, have you been able to practice those?"
- Build on treatment plan: "Based on our previous sessions, let's continue working on..."
- Track progress and adjust treatment plan accordingly"""

            return base_prompt + memory_context
        
        return base_prompt

    def get_or_create_user(self, user_identifier: str) -> tuple[str, UserProfile]:
        """Get or create user profile based on identifier (like name)"""
        user_id = memory_manager.generate_user_id(user_identifier)
        
        # Try to load existing profile
        profile = memory_manager.load_user_profile(user_id)
        
        if not profile:
            # Create new profile
            profile = UserProfile(
                user_id=user_id,
                name=user_identifier
            )
            memory_manager.save_user_profile(profile)
            print(f"👤 Created new user profile: {user_identifier} (ID: {user_id})")
        else:
            print(f"👤 Loaded existing user: {profile.name} (ID: {user_id})")
        
        return user_id, profile

    def extract_user_identifier(self, message: str) -> str:
        """Extract user identifier from message - simple name detection"""
        message_lower = message.lower()
        
        # Look for name patterns
        name_patterns = [
            "my name is ",
            "i'm ",
            "i am ",
            "call me ",
            "this is "
        ]
        
        for pattern in name_patterns:
            if pattern in message_lower:
                start_idx = message_lower.find(pattern) + len(pattern)
                # Get the next word(s) as name
                remaining = message[start_idx:].strip()
                name_parts = remaining.split()
                if name_parts:
                    # Take first word as name, clean it
                    name = name_parts[0].strip('.,!?').title()
                    if len(name) > 1 and name.isalpha():
                        return name
        
        return "User"  # Default identifier

    def get_response(self, user_message: str, session_id: str = None) -> tuple[str, str]:
        """Get AI response with memory context"""
        try:
            # Extract user identifier if this seems like an introduction
            user_identifier = self.extract_user_identifier(user_message)
            user_id, profile = self.get_or_create_user(user_identifier)
            
            # Get or create session
            if not session_id:
                session_id = memory_manager.create_session_id(user_id)
            
            if session_id not in self.current_sessions:
                # Try to load existing session or create new one
                existing_sessions = memory_manager.load_user_sessions(user_id, limit=1)
                if existing_sessions and existing_sessions[0].session_id == session_id:
                    self.current_sessions[session_id] = existing_sessions[0]
                else:
                    self.current_sessions[session_id] = ChatSession(
                        session_id=session_id,
                        user_id=user_id
                    )
            
            current_session = self.current_sessions[session_id]
            
            # Get user context for AI
            user_context = memory_manager.get_user_context(user_id)
            
            # Prepare messages for API call
            messages = [
                {"role": "system", "content": self.get_system_prompt(user_context)}
            ]
            
            # Add recent conversation history
            recent_messages = current_session.messages[-10:]  # Last 10 messages
            for msg in recent_messages:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            print(f"🧠 Sending to Mistral (User: {profile.name}): {user_message[:50]}...")
            
            # Call Mistral API
            response = openai.ChatCompletion.create(
                model="mistral-medium-latest",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Update session with new conversation
            memory_manager.update_session_data(current_session, user_message, ai_response)
            
            # Save session and profile
            memory_manager.save_session(current_session)
            memory_manager.save_user_profile(profile)
            
            print(f"✅ Mistral responded to {profile.name}: {ai_response[:50]}...")
            print(f"💾 Session saved: {session_id}")
            
            return ai_response, session_id
            
        except Exception as e:
            print(f"❌ Error calling Mistral API: {e}")
            error_response = "I apologize, but I'm experiencing technical difficulties right now. Please try again in a moment. If you're in crisis, please contact 988 immediately."
            return error_response, session_id or "error_session"

# Global API instance
mental_health_api = MentalHealthAPI()

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided", "status": "error"}), 400
        
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')  # Optional session ID from frontend
        
        if not user_message:
            return jsonify({"error": "Message is required", "status": "error"}), 400
        
        print(f"👤 Message: {user_message}")
        
        # Get AI response with memory
        ai_response, returned_session_id = mental_health_api.get_response(user_message, session_id)
        
        # Send response with session ID
        return jsonify({
            "response": ai_response,
            "session_id": returned_session_id,
            "status": "success"
        })
        
    except Exception as e:
        print(f"❌ Server error: {e}")
        return jsonify({"error": "Internal server error", "status": "error"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "service": "Mental Health API",
        "ai": "Mistral"
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Mental Health AI Chat API",
        "endpoints": {
            "chat": "/chat (POST)",
            "health": "/health (GET)"
        },
        "ai": "Mistral Medium"
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Mental Health API Server starting on port {port}")
    print(f"🔗 Endpoint: http://localhost:{port}/chat")
    print(f"🧠 Powered by Mistral AI (mistral-medium-latest)")
    print("💚 Ready to provide empathetic mental health support!")
    print("\n" + "="*60)
    
    app.run(host='0.0.0.0', port=port, debug=False)
