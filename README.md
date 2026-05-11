# Ex-Valuation - Memory Value Calculator

A beautiful, philosophical web application that evaluates the "soul value" of your memories using AI.

## Features

- 📸 Upload photos to evaluate their emotional value
- 💔 Adjustable heartbreak level (1-10)
- 🔮 AI-generated philosophical comfort messages
- 🔥 Interactive "burn memory" feature with stunning animations
- ✨ Beautiful flowing particle background
- 🌍 Fully English interface

## Setup

### 1. Install Dependencies

```bash
pip install flask requests python-dotenv
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
BAIDU_API_KEY=your_baidu_api_key
BAIDU_SECRET_KEY=your_baidu_secret_key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

### 3. Run the Application

```bash
python app.py
```

Visit `http://localhost:1000` in your browser.

## Deployment

### Replit (Recommended - Easiest)

1. Visit [replit.com](https://replit.com)
2. Create a new Python Repl
3. Upload all project files
4. Add environment variables in Secrets
5. Click Run!

Your app will get a public URL automatically.

### Railway

1. Visit [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will auto-detect Python/Flask
4. Add environment variables
5. Deploy!

### Render

1. Visit [render.com](https://render.com)
2. Create a new "Web Service"
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Add environment variables
7. Deploy!

## API Keys Required

- **Baidu AI**: [Console](https://console.bce.baidu.com/) - Image recognition
- **DeepSeek**: [Platform](https://platform.deepseek.com/) - AI chat generation

## Tech Stack

- Flask (Backend)
- HTML5/CSS3/JavaScript (Frontend)
- Baidu AI (Image Analysis)
- DeepSeek (AI Content Generation)
- Canvas API (Animations)

## License

MIT License

## Note

This project is completely free and open source. No premium features, no ads, no tracking.
