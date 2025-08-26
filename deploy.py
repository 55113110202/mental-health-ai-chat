#!/usr/bin/env python3
"""
Deployment helper script for Mental Health AI Chat
Checks deployment readiness and provides instructions
"""

import os
import sys

def check_file_exists(filename, description):
    """Check if a file exists and print status"""
    if os.path.exists(filename):
        print(f"✅ {filename} - {description}")
        return True
    else:
        print(f"❌ {filename} - {description} (MISSING)")
        return False

def main():
    print("🚀 Mental Health AI Chat - Deployment Check")
    print("=" * 50)
    
    # Check required files
    required_files = [
        ("api_server.py", "Flask API server"),
        ("memory_system.py", "Memory management system"),
        ("requirements.txt", "Python dependencies"),
        ("render.yaml", "Render deployment config"),
        ("therapy_chat.html", "Frontend interface"),
        ("DEPLOYMENT.md", "Deployment guide")
    ]
    
    all_files_present = True
    for filename, description in required_files:
        if not check_file_exists(filename, description):
            all_files_present = False
    
    print("\n" + "=" * 50)
    
    if all_files_present:
        print("🎉 All files are ready for deployment!")
        print("\n📋 Next Steps:")
        print("1. Push your code to GitHub")
        print("2. Go to https://render.com and sign up")
        print("3. Create a new Web Service")
        print("4. Connect your GitHub repository")
        print("5. Configure:")
        print("   - Name: therapy-chat-api")
        print("   - Environment: Python 3")
        print("   - Build Command: pip install -r requirements.txt")
        print("   - Start Command: python api_server.py")
        print("   - Plan: Free")
        print("6. Add environment variable:")
        print("   - Key: MISTRAL_API_KEY")
        print("   - Value: BvXava18NiJ5U62jx9bN9RXkSmHC9tSh")
        print("7. Deploy frontend to Netlify/Vercel")
        print("8. Update API endpoint in therapy_chat.html")
        print("\n📖 See DEPLOYMENT.md for detailed instructions")
    else:
        print("❌ Some files are missing. Please ensure all required files are present.")
        sys.exit(1)

if __name__ == "__main__":
    main()
