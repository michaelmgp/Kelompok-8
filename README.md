# 🚀 Web3 Job Agent Platform

A comprehensive **Web3 job discovery platform** powered by **Fetch.ai uAgents**, **AI chatbot capabilities**, and **ICP smart contracts**, featuring a modern Next.js frontend with floating AI assistant.

## ✨ Features

- **🤖 AI-Powered Job Search** - Powered by Grok API for intelligent job matching
- **🔗 uAgents Integration** - ASI:1 compatible blockchain-based agent communication
- **🌐 Modern Frontend** - Next.js 14 with Tailwind CSS and floating AI chat
- **💬 Smart Chat Protocol** - Natural language job requests with session management
- **🔍 Intelligent Filtering** - Automatic job requirement parsing and extraction
- **📱 Agentverse Ready** - Discoverable on Fetch.ai ecosystem
- **⛓️ ICP Smart Contracts** - Motoko-based job and identity management
- **🔒 Security Focused** - Comprehensive security scanning and CVE management

## 🏗️ Project Architecture

> **📝 Note**: All test files have been organized into the `ai_chatbot/tests/` directory for better maintainability and structure.

```
Kelompok-8/
├── 📁 frontend/                    # 🌐 Next.js 14 Frontend Application
│   ├── 📁 src/
│   │   ├── 📁 app/                # Next.js App Router
│   │   │   ├── 📄 layout.tsx      # Root layout with floating AI
│   │   │   ├── 📄 page.tsx        # Homepage
│   │   │   ├── 📁 jobs/           # Job listings pages
│   │   │   ├── 📁 analytics/      # Career analytics
│   │   │   ├── 📁 docs/           # Documentation
│   │   │   └── 📁 demo/           # AI assistant demo
│   │   ├── 📁 components/         # React components
│   │   │   ├── 📁 ai/             # AI assistant components
│   │   │   │   ├── 📄 FloatingAIAssistant.tsx  # Floating chat widget
│   │   │   │   └── 📄 AIAssistant.tsx         # Legacy AI component
│   │   │   ├── 📁 layout/         # Layout components
│   │   │   │   ├── 📄 TopNavigation.tsx       # Main navigation
│   │   │   │   └── 📄 Sidebar.tsx             # Project sidebar
│   │   │   ├── 📁 ui/             # Base UI components
│   │   │   ├── 📁 jobs/           # Job-related components
│   │   │   ├── 📁 home/           # Homepage components
│   │   │   ├── 📁 dashboard/      # Dashboard components
│   │   │   └── 📁 analytics/      # Analytics components
│   │   └── 📁 lib/                # Utility libraries
│   │       └── 📄 api.ts          # API client for AI backend
│   ├── 📁 public/                 # Static assets
│   ├── 📁 scripts/                # Build and security scripts
│   ├── 📄 package.json            # Frontend dependencies
│   ├── 📄 next.config.js          # Next.js configuration
│   ├── 📄 tailwind.config.ts      # Tailwind CSS configuration
│   └── 📄 env.example             # Frontend environment template
│
├── 📁 ai_chatbot/                 # 🤖 AI Chatbot Service (Backend)
│   ├── 📁 chatbot/                # Core chatbot modules
│   │   ├── 📄 __init__.py         # Package initialization
│   │   ├── 📄 model.py            # LLM initialization and chains
│   │   ├── 📄 handlers.py         # Chat request handlers
│   │   ├── 📄 icp_integration.py  # ICP blockchain integration
│   │   └── 📄 user_management.py  # User profile management
│   ├── 📁 tests/                  # Comprehensive test suite
│   │   ├── 📁 unit/               # Unit tests (6 files)
│   │   │   ├── 📄 test_grok.py    # Grok API unit tests
│   │   │   ├── 📄 test_handlers.py # Handler unit tests
│   │   │   ├── 📄 test_logging.py  # Logging unit tests
│   │   │   ├── 📄 test_models.py   # Model unit tests
│   │   │   ├── 📄 test_prompts.py  # Prompt unit tests
│   │   │   └── 📄 test_specific_prompt.py # Specific prompt tests
│   │   ├── 📁 integration/        # Integration tests (4 files)
│   │   │   ├── 📄 test_chat_endpoints.py # Chat endpoint tests
│   │   │   ├── 📄 test_client.py   # Client integration tests
│   │   │   ├── 📄 test_icp_integration.py # ICP integration tests
│   │   │   └── 📄 test_api.py      # API endpoint tests
│   │   ├── 📁 performance/        # Performance tests
│   │   ├── 📁 utils/              # Test utilities
│   │   ├── 📄 quick_test.py       # Quick testing utility
│   │   ├── 📄 test_suite.py       # Comprehensive test suite
│   │   └── 📄 run_all_tests.py    # Test runner
│   ├── 📁 scripts/                # Security and utility scripts
│   │   └── 📄 security-check.sh   # Automated security scanning
│   ├── 📄 agent.py                # Fetch.ai uAgent (ASI:1 compatible)
│   ├── 📄 main.py                 # FastAPI server entry point
│   ├── 📄 requirements.txt        # Python dependencies
│   ├── 📄 env.example             # Environment variables template
│   ├── 📄 SETUP_GROK.md           # Grok API setup guide
│   ├── 📄 generate_agent_seed.py  # Agent seed generation script
│   ├── 📄 README.md               # Backend documentation
│   └── 📄 chatbot.log             # Application logs
│
├── 📁 icp_contracts/              # ⛓️ ICP Smart Contracts
│   ├── 📁 src/
│   │   ├── 📄 agent_contract.mo   # Agent management contract
│   │   ├── 📄 chat_contract.mo    # Chat protocol contract
│   │   ├── 📄 identity_contract.mo # User identity management
│   │   └── 📄 job_contract.mo     # Job management contract
│   ├── 📁 declarations/            # Contract interfaces
│   │   ├── 📁 identity_contract/  # Identity contract declarations
│   │   └── 📁 job_contract/       # Job contract declarations
│   ├── 📄 dfx.json                # DFX configuration
│   ├── 📄 CARA_PENGGUNAAN.md      # Usage instructions (ID)
│   └── 📄 USAGE.md                 # Usage instructions (EN)
│
├── 📄 README.md                    # This project overview
├── 📄 SECURITY.md                  # Security guidelines and tools
├── 📄 .gitignore                   # Git ignore patterns
└── 📄 .gitattributes              # Git attributes
```

## 🚀 Quick Start

### Recent Improvements ✨
- **🧹 Test Organization**: All test files moved to organized `tests/` directory
- **📁 Clean Structure**: Root directory cleaned of scattered test files
- **🔍 Better Testing**: Comprehensive test suite with unit, integration, and performance tests
- **📚 Documentation**: Updated project structure and testing guidelines

### Prerequisites

- **Node.js 18+** (for frontend)
- **Python 3.8+** (recommended: 3.12 for backend)
- **WSL/Ubuntu** (recommended for development)
- **Git**

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Kelompok-8
```

### 2. Set Up Frontend (Next.js)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp env.example .env.local
# Edit .env.local with your API configuration

# Start development server
npm run dev
```

**Frontend will be available at:** http://localhost:5000

### 3. Set Up AI Chatbot Service (Backend)

```bash
# Navigate to chatbot directory
cd ../ai_chatbot

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Backend Environment

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
HOST=0.0.0.0

# CORS Configuration
CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:5000,http://127.0.0.1:3000,http://127.0.0.1:5000

# uAgents Configuration
AGENT_NAME=job_chat_agent
AGENT_SEED=your_unique_agent_seed
MAILBOX_KEY=your_agentverse_mailbox_key
```

### 5. Get API Keys

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

### 6. Start the Services

#### **Start AI Chatbot Server:**
```bash
# Terminal 1: Start FastAPI server
python3 main.py
```

**Expected Output:**
```
🚀 Starting AI Chatbot Service...
🔧 Debug mode: True
🤖 Model type: grok
📡 Server will be available at: http://0.0.0.0:8081
📊 Health check: http://0.0.0.0:8081/health
💬 Chat endpoint: http://0.0.0.0:8081/chat
🌐 Final CORS origins: ['http://localhost:3000', 'http://localhost:5000', ...]
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

### **Test Organization**
The project includes a comprehensive test suite organized into logical categories:

- **Unit Tests** (`tests/unit/`): Individual component testing
- **Integration Tests** (`tests/integration/`): API and service integration testing
- **Performance Tests** (`tests/performance/`): Load and stress testing
- **Test Utilities** (`tests/utils/`): Helper functions and test data

### **Run All Tests**
```bash
cd ai_chatbot/tests
python run_all_tests.py
```

### **Test Frontend:**
1. Open http://localhost:5000
2. Look for the **blue AI assistant icon** in the bottom-right corner
3. Click it to open the floating chat window
4. Test the AI integration

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
# Test agent communication
cd tests/integration
python3 test_client.py
```

## 🌟 Frontend Features

### **Floating AI Assistant**
- **Always Accessible** - Available on every page
- **Expandable Chat** - Click to open, minimize when needed
- **Real-time Status** - Visual connection indicator
- **Quick Actions** - Pre-built job search queries
- **Responsive Design** - Works on all devices

### **Modern UI Components**
- **Next.js 14** with App Router
- **Tailwind CSS** for styling
- **TypeScript** for type safety
- **Radix UI** for accessible components
- **Lucide React** for icons

### **AI Integration**
- **Real-time Chat** with Grok API
- **Connection Monitoring** with status indicators
- **Error Handling** with user-friendly messages
- **Job Filter Parsing** with visual display

## 📚 API Reference

### **Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Server health check |
| `POST` | `/chat` | Process job search requests |
| `POST` | `/parse` | Extract job filters from text |
| `OPTIONS` | `/*` | CORS preflight handling |

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

### **Frontend Environment Variables**

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | AI backend URL | `http://localhost:8081` |
| `NEXT_PUBLIC_API_TIMEOUT` | API timeout (ms) | `10000` |
| `NEXT_PUBLIC_API_RETRIES` | API retry attempts | `3` |

### **Backend Environment Variables**

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_TYPE` | AI model provider | `grok` |
| `GROK_API_KEY` | Grok API key | Required |
| `PORT` | Server port | `8081` |
| `HOST` | Server host | `0.0.0.0` |
| `CORS_ALLOW_ORIGINS` | Allowed origins | Multiple localhost URLs |
| `AGENT_NAME` | uAgent name | `job_chat_agent` |
| `AGENT_SEED` | Unique agent seed | Required |
| `MAILBOX_KEY` | Agentverse mailbox key | Optional |

### **AI Models**

| Provider | Model | Features |
|----------|-------|----------|
| **Grok** | `llama3-8b-8192` | Fast, lightweight, cost-effective |
| **OpenAI** | `gpt-3.5-turbo` | High quality, cloud-based |

## 🔒 Security Features

### **Automated Security Scanning**
- **Frontend**: `npm audit`, `npm outdated`
- **Backend**: `pip-audit`, `safety`, `bandit`
- **Scripts**: Automated security checks in `scripts/` folders

### **Security Commands**
```bash
# Frontend security
npm run security:audit
npm run security:fix

# Backend security
cd ai_chatbot
./scripts/security-check.sh
```

## 🚀 Deployment

### **Frontend Deployment**

```bash
# Build for production
npm run build

# Start production server
npm start
```

### **Backend Deployment**

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
| **Frontend not connecting to backend** | Check CORS settings and API URL |
| **Port already in use** | Change `PORT` in `.env` or kill existing processes |
| **Grok API errors** | Verify `GROK_API_KEY` and account credits |
| **Agent not discoverable** | Check `MAILBOX_KEY` and agent registration |
| **Import errors** | Ensure virtual environment is activated |
| **CORS issues** | Verify `CORS_ALLOW_ORIGINS` includes frontend URL |

### **Debug Mode**

```bash
# Enable debug logging
export DEBUG=true
python3 main.py
```

### **Connection Status**

The floating AI assistant shows connection status:
- **🟢 Green**: Fully connected
- **🟠 Orange**: Backend running, agent not ready
- **🔴 Red**: Disconnected
- **🟡 Yellow**: Checking connection

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check individual module READMEs
- **Issues**: [GitHub Issues](link-to-issues)
- **Security**: See [SECURITY.md](SECURITY.md) for security guidelines

## 🙏 Acknowledgments

- **Fetch.ai** for uAgents framework and ASI:1 protocol
- **Grok** for AI API services
- **Agentverse** for agent discovery
- **Next.js** for modern frontend framework
- **Tailwind CSS** for utility-first styling

---

**Built with ❤️ by Kelompok-8**

*Ready to revolutionize job discovery with AI, blockchain technology, and modern web development!* 🚀
