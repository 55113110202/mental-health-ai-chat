#!/usr/bin/env python3
"""
Simple startup script for Mental Health AI Chat
"""

import subprocess
import time
import webbrowser
import os

def start_servers():
    """Start both backend and frontend servers"""
    
    print("🚀 Starting Mental Health AI Chat...")
    print("=" * 50)
    
    # Start API server in background
    print("🧠 Starting Mistral AI backend...")
    api_process = subprocess.Popen(
        ["python", "api_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait a moment for API server to start
    time.sleep(2)
    
    # Start frontend server in background
    print("🌐 Starting frontend server...")
    frontend_process = subprocess.Popen(
        ["python", "-m", "http.server", "3000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for frontend to start
    time.sleep(2)
    
    # Open browser
    print("🔗 Opening browser...")
    webbrowser.open("http://localhost:3000/therapy_chat.html")
    
    print("\n✅ Mental Health AI Chat is now running!")
    print("📱 Frontend: http://localhost:3000/therapy_chat.html")
    print("🔧 Backend API: http://localhost:8000/chat")
    print("\n💡 Features:")
    print("  • Direct Mistral AI integration")
    print("  • Persistent memory across sessions")
    print("  • Natural, empathetic conversations")
    print("  • Crisis detection and safety protocols")
    
    print("\n🛑 Press Ctrl+C to stop all servers")
    
    try:
        # Keep both processes running
        api_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down servers...")
        api_process.terminate()
        frontend_process.terminate()
        print("✅ Servers stopped successfully")

if __name__ == "__main__":
    start_servers()
