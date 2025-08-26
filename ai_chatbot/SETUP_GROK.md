# 🚀 Grok Integration Setup Guide

This guide will help you set up Grok API as a lightweight alternative to heavy local models for your AI chatbot.

## Why Grok Instead of Local Models?

| Feature | Local Models (Ollama) | Grok API |
|---------|----------------------|----------|
| **Setup Time** | 5-10 minutes | ⚡ 2 minutes |
| **Memory Usage** | 2-8 GB RAM | 🟢 Minimal |
| **Model Download** | 2-40 GB | 🟢 None |
| **Response Speed** | Medium | 🟢 Very Fast |
| **Cost** | Free | 🟢 Very Low |
| **Maintenance** | High | 🟢 None |

## 🎯 Quick Setup (5 minutes)

### Step 1: Get Grok API Key
1. Visit [Grok Console](https://console.groq.com/)
2. Sign up for a free account
3. Copy your API key from the dashboard

### Step 2: Install Dependencies
```bash
cd ai_chatbot
pip install -r requirements.txt
```

### Step 3: Configure Environment
1. Copy `env.example` to `.env`
2. Edit `.env` and add your Grok API key:
```env
MODEL_TYPE=grok
GROK_API_KEY=your_actual_api_key_here
GROK_MODEL=llama3-8b-8192
```

### Step 4: Test Integration
```bash
python test_grok.py
```

### Step 5: Start the Service
```bash
python main.py
```

## 🔧 Troubleshooting

### "GROK_API_KEY not found"
- Make sure you created a `.env` file
- Check that `GROK_API_KEY=your_key` is in the file
- Verify there are no spaces around the `=` sign

### "Module not found" errors
- Run the dependency installation script
- Make sure you're in the `ai_chatbot` directory
- Check that Python is installed and in PATH

### "Invalid API key" error
- Verify your API key from [Grok Console](https://console.groq.com/)
- Make sure your account has credits
- Check if the key is copied correctly

## 📊 Available Grok Models

| Model | Size | Context | Speed | Quality |
|-------|------|---------|-------|---------|
| `llama3-8b-8192` | 8B | 8K | ⚡ Fast | 🟡 Good |
| `llama3-70b-8192` | 70B | 8K | 🟡 Medium | 🟢 High |
| `mixtral-8x7b-32768` | 8B | 32K | 🟡 Medium | 🟢 High |

**Recommendation**: Start with `llama3-8b-8192` for best speed/quality balance.

## 💰 Cost Information

Grok API pricing is very affordable:
- **Free tier**: Generous free credits
- **Paid tier**: ~$0.05 per 1M tokens
- **Typical chat**: ~$0.001 per conversation

## 🚀 Next Steps

After successful setup:

1. **Test the API endpoints**:
   ```bash
   curl -X POST "http://localhost:8081/chat" \
        -H "Content-Type: application/json" \
        -d '{"user_prompt": "Find me a Python developer job"}'
   ```

2. **Integrate with your frontend**:
   - Update API calls to use the new endpoints
   - Handle the new response format

3. **Customize the prompts**:
   - Edit `chatbot/handlers.py` to modify behavior
   - Adjust temperature and other parameters in `model.py`

## 🔄 Switching to OpenAI

If you ever want to use OpenAI instead:
1. Set `MODEL_TYPE=openai` in `.env`
2. Add your `OPENAI_API_KEY`

## 📞 Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Run `python test_grok.py` to diagnose issues
- Verify your `.env` file configuration

---

**🎉 Congratulations!** You now have a lightweight, fast AI chatbot powered by Grok API instead of heavy local models.
