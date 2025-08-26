# 🤖 AI Chatbot Service

A powerful AI-powered job search chatbot service built with FastAPI and LangChain, supporting **Grok API** (lightweight) and **OpenAI** models, with full uAgents integration for blockchain communication.

## ✨ Features

- **🤖 AI-Powered Job Search** - Powered by Grok API for intelligent job matching
- **🔗 uAgents Integration** - Blockchain-based agent communication
- **🌐 RESTful API** - Clean endpoints for frontend integration
- **💬 Smart Chat Protocol** - Natural language job requests
- **🔍 Intelligent Filtering** - Automatic job requirement parsing
- **📱 Agentverse Ready** - Discoverable on Fetch.ai ecosystem

## 🏗️ Architecture

```
ai_chatbot/
├── chatbot/                    # Core chatbot modules
│   ├── __init__.py            # Package initialization
│   ├── model.py               # LLM initialization & conversation chains
│   ├── handlers.py            # Chat request handling & user management
│   └── fetch_agent_client.py  # FetchAI integration stub
├── main.py                    # FastAPI entry point
├── agent.py                   # uAgents implementation
├── test_client.py             # Chat protocol test client
├── generate_agent_seed.py     # Agent seed generator
├── requirements.txt           # Python dependencies
├── env.example                # Environment variables template
├── SETUP_GROK.md              # Grok setup guide
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (recommended: 3.12)
- **WSL/Ubuntu** (recommended for development)
- **Git**

### 1. Set Up Environment

   ```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
   pip install -r requirements.txt
   ```

### 2. Configure Environment

   ```bash
# Copy environment template
cp env.example .env

# Edit .env with your API keys
nano .env
```

**Required Environment Variables:**
```env
# AI Configuration
MODEL_TYPE=grok
GROK_API_KEY=your_grok_api_key_here

# Server Configuration
PORT=8081

# uAgents Configuration
AGENT_NAME=job_chat_agent
AGENT_SEED=your_unique_agent_seed
MAILBOX_KEY=your_agentverse_mailbox_key
```

### 3. Get API Keys

#### **Grok API Key:**
1. Visit [Grok Console](https://console.groq.com/)
2. Sign up and get your API key
3. Add to `.env` file

#### **Agent Seed:**
   ```bash
# Generate unique agent seed
python3 generate_agent_seed.py
# Copy the output to your .env file
```

#### **Mailbox Key:**
1. Visit [Agentverse](https://agentverse.ai/)
2. Create account and get mailbox key
3. Add to `.env` file

### 4. Start the Services

#### **Start AI Chatbot Server:**
   ```bash
# Terminal 1: Start FastAPI server
python3 main.py
```

**Expected Output:**
```
🚀 Starting AI Chatbot Service...
📡 Server will be available at: http://0.0.0.0:8081
🤖 Model type: grok
📊 Health check: http://0.0.0.0:8081/health
💬 Chat endpoint: http://0.0.0.0:8081/chat
```

#### **Start uAgents Service:**
```bash
# Terminal 2: Start uAgents
python3 agent.py
```

**Expected Output:**
```
INFO: Agent address: agent1...
INFO: Mailbox enabled; your agent is discoverable on Agentverse.
```

## 🧪 Testing

### **Test API Endpoints:**

```bash
# Health check
curl http://localhost:8081/health

# Chat with AI
curl -X POST "http://localhost:8081/chat" \
     -H "Content-Type: application/json" \
     -d '{"user_prompt": "I need a Python developer"}'

# Parse job filters
curl -X POST "http://localhost:8081/parse" \
     -H "Content-Type: application/json" \
     -d '{"user_prompt": "Remote React developer, $50-100/hour"}'
```

### **Test uAgents:**
```bash
# Edit test_client.py and add your agent's address
python3 test_client.py
```

## 📚 API Reference

### **Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Server health check |
| `POST` | `/chat` | Process job search requests |
| `POST` | `/parse` | Extract job filters from text |

### **Chat Request Format**
```json
{
  "user_prompt": "I need a Python developer for web development",
  "top_k": 5
}
```

### **Response Format**
```json
{
  "message": "I'll help you find a Python developer...",
  "filters": {
    "skills": ["python", "web development"],
    "keywords": ["python", "web"],
    "budget_min": null,
    "budget_max": null,
    "rate_type": null,
    "remote": null,
    "duration_days_max": null,
    "top_k": 5
  },
  "should_fetch_jobs": true
}
```

## 🔧 Configuration

### **Environment Variables**

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_TYPE` | AI model provider | `grok` |
| `GROK_API_KEY` | Grok API key | Required |
| `PORT` | Server port | `8081` |
| `AGENT_NAME` | uAgent name | `job_chat_agent` |
| `AGENT_SEED` | Unique agent seed | Required |
| `MAILBOX_KEY` | Agentverse mailbox key | Optional |

### **AI Models**

| Provider | Model | Features |
|----------|-------|----------|
| **Grok** | `llama3-8b-8192` | Fast, lightweight, cost-effective |
| **OpenAI** | `gpt-3.5-turbo` | High quality, cloud-based |

## 🚀 Deployment

### **Production Setup**

1. **Set Production Environment:**
   ```bash
   export DEBUG=false
   export HOST=0.0.0.0
   export PORT=8081
   ```

2. **Use Process Manager:**
   ```bash
   # Install PM2
   npm install -g pm2
   
   # Start services
   pm2 start "python3 main.py" --name "job-chatbot"
   pm2 start "python3 agent.py" --name "job-agent"
   ```

3. **Set Up Reverse Proxy:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8081;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 🐛 Troubleshooting

### **Common Issues**

| Issue | Solution |
|-------|----------|
| **Port already in use** | Change `PORT` in `.env` or kill existing processes |
| **Grok API errors** | Verify `GROK_API_KEY` and account credits |
| **Agent not discoverable** | Check `MAILBOX_KEY` and agent registration |
| **Import errors** | Ensure virtual environment is activated |
| **Duplicate responses** | Check agent.py for message deduplication |

### **Debug Mode**

```bash
# Enable debug logging
export DEBUG=true
python3 main.py
```

## 🔗 Integration

### **Frontend Integration**

Your frontend can communicate with the chatbot using:

```javascript
// Chat endpoint
const response = await fetch('http://localhost:8081/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_prompt: "I need a React developer"
  })
});

const result = await response.json();
console.log(result.message);        // AI response
console.log(result.filters);        // Parsed job filters
```

### **uAgents Integration**

The service is fully compatible with the uAgents ecosystem:

- **Agentverse Discovery** - Your agent is discoverable
- **Chat Protocol** - ASI:1 compatible messaging
- **Blockchain Communication** - Fetch.ai integration ready

## 📖 Additional Documentation

- **[SETUP_GROK.md](SETUP_GROK.md)** - Detailed Grok setup guide
- **[requirements.txt](requirements.txt)** - Python dependencies
- **[env.example](env.example)** - Environment configuration template

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open Pull Request**

## 📄 License

This project is licensed under the MIT License.

---

**Ready to revolutionize job discovery with AI and blockchain technology!** 🚀
