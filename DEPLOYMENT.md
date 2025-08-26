# 🚀 Deploy to Render - Mental Health AI Chat

## Quick Deploy Steps

### 1. **Prepare Your Repository**
- Push your code to GitHub
- Make sure you have these files:
  - `api_server.py` (Flask server)
  - `memory_system.py` (Memory management)
  - `requirements.txt` (Dependencies)
  - `render.yaml` (Optional config)

### 2. **Deploy to Render**

#### Step 1: Sign Up
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Connect your repository

#### Step 2: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name:** `therapy-chat-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python api_server.py`
   - **Plan:** Free

#### Step 3: Add Environment Variables
In Render dashboard → Environment:
- **Key:** `MISTRAL_API_KEY`
- **Value:** `BvXava18NiJ5U62jx9bN9RXkSmHC9tSh`

#### Step 4: Deploy
Click **"Create Web Service"** and wait for deployment.

### 3. **Deploy Frontend**

#### Option A: Netlify (Recommended)
1. Go to [netlify.com](https://netlify.com)
2. Drag & drop your `therapy_chat.html` file
3. Get your URL (e.g., `https://your-app.netlify.app`)

#### Option B: Vercel
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repo
3. Deploy automatically

### 4. **Update Frontend URL**
In `therapy_chat.html`, change:
```javascript
const API_ENDPOINT = 'https://your-app-name.onrender.com/chat';
```

## File Structure for Deployment

```
your-repo/
├── api_server.py          # Flask API server
├── memory_system.py       # Memory management
├── requirements.txt       # Python dependencies
├── render.yaml           # Render configuration
├── therapy_chat.html     # Frontend (deploy separately)
└── user_data/            # Local data (not needed on Render)
```

## Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `MISTRAL_API_KEY` | `BvXava18NiJ5U62jx9bN9RXkSmHC9tSh` | Your Mistral API key |
| `PORT` | `8000` | Port (auto-set by Render) |

## API Endpoints

- **POST** `/chat` - Send message, get AI response
- **GET** `/health` - Health check
- **GET** `/` - API info

## Free Tier Limitations

- ⏰ **Sleep after 15 minutes** of inactivity
- 💾 **512 MB RAM** (sufficient for this app)
- 🔄 **Auto-sleep/wake** (first request after sleep takes ~30 seconds)
- 💰 **Completely free** - no credit card required

## Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check `requirements.txt` has all dependencies
   - Ensure Python version compatibility

2. **API Not Responding**
   - Check environment variables are set
   - Verify Mistral API key is valid

3. **CORS Errors**
   - Frontend can't connect to API
   - Ensure CORS is enabled in Flask app

4. **Memory Not Working**
   - Render doesn't persist local files
   - Consider using a database for production

## Production Considerations

For a production app, consider:
- **Database:** PostgreSQL for user data persistence
- **Authentication:** User login system
- **HTTPS:** Automatic with Render
- **Monitoring:** Render provides basic logs
- **Backups:** Database backups for user data

## Support

- **Render Docs:** [docs.render.com](https://docs.render.com)
- **Flask Docs:** [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Mistral API:** [docs.mistral.ai](https://docs.mistral.ai)
