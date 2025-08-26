# Mental Health AI Chat - Direct Mistral

A clean, fast mental health therapy chat interface powered directly by Mistral AI with persistent memory.

## ✨ Features

- 🧠 **Direct Mistral AI** - Fast, empathetic responses
- 💾 **Persistent Memory** - Remembers conversations across sessions
- 👤 **User Profiles** - Automatic name detection and user management
- 🗂️ **Session Management** - Continue where you left off
- 💬 **Natural Conversation** - Like chatting with a caring friend
- 🛡️ **Crisis Detection** - Built-in safety protocols
- 📱 **Modern UI** - Clean, responsive chat interface

## 🚀 Quick Start

### Option 1: One-Click Start (Recommended)
```bash
python start.py
```
This automatically starts both servers and opens your browser!

### Option 2: Manual Start
```bash
# Terminal 1: Start the Backend
python api_server.py

# Terminal 2: Start the Frontend
python -m http.server 3000

# Open in Browser
http://localhost:3000/therapy_chat.html
```

## 🌐 Deploy to Render (Free)

**Ready to deploy online?** See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions!

Quick deploy:
1. Push to GitHub
2. Connect to [Render.com](https://render.com) 
3. Deploy frontend to [Netlify](https://netlify.com)
4. Update API endpoint in `therapy_chat.html`

**Files ready for deployment:**
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration  
- ✅ Flask API server - Production ready
- ✅ Static frontend - Deploy anywhere

## 📁 Project Structure

```
├── api_server.py           # Backend API server (Flask + Mistral)
├── memory_system.py        # User profiles & session persistence  
├── therapy_chat.html       # Frontend chat interface
├── requirements.txt        # Python dependencies (Render ready)
├── render.yaml            # Render deployment configuration
├── DEPLOYMENT.md          # Complete deployment guide
├── start.py               # One-click startup script
├── user_data/             # Stored user conversations
│   ├── profiles/          # User profiles
│   └── sessions/          # Chat sessions
└── README.md              # This file
```

## 🔧 Configuration

### API Key
Update your Mistral API key in `api_server.py`:
```python
os.environ["OPENAI_API_KEY"] = "your-mistral-api-key-here"
```

### System Prompt
Customize AI behavior in `api_server.py` → `get_system_prompt()` method

## 💡 Usage

1. **Introduce Yourself**: "My name is John"
2. **Start Chatting**: Share your thoughts and feelings
3. **Return Later**: Your conversations are automatically saved
4. **New Session**: Click "🔄 New Session" to start fresh

## 🎯 Memory Features

- **Automatic Name Detection**: Recognizes when you introduce yourself
- **Topic Tracking**: Remembers what you've discussed (sleep, work, anxiety, etc.)
- **Mood Patterns**: Tracks emotional indicators over time
- **Advice History**: Won't repeat the same suggestions
- **Session Continuity**: Pick up exactly where you left off

## 🛡️ Safety & Privacy

- **Local Storage**: All data stored locally in `user_data/`
- **Crisis Detection**: Automatic safety protocols for emergencies
- **No Diagnosis**: AI provides support, not medical diagnosis
- **Professional Boundaries**: Encourages professional help when needed

## 📞 Emergency Resources

- **US**: 988 (Suicide & Crisis Lifeline)
- **Crisis Text**: Text HOME to 741741
- **Emergency**: 911

## 🎨 Customization

### Change AI Personality
Edit the system prompt in `api_server.py` to modify how the AI responds.

### UI Styling
Modify colors, fonts, and layout in `therapy_chat.html` CSS section.

### Memory Behavior
Adjust what information is stored in `memory_system.py`.

---

## 🎊 **Ultra-Clean Setup**

This is a **production-ready, minimal** mental health AI chat system:
- ✅ **Only 5 core files** - No bloat, no complexity
- ✅ **Direct Mistral integration** - Fast, efficient responses  
- ✅ **Zero dependencies** - Just Python standard library + OpenAI client
- ✅ **Instant deployment** - Copy anywhere and run
- ✅ **Easy customization** - Simple, readable code

**Built for mental health support with privacy and empathy in mind.** 💚