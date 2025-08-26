# 🚀 Web3 Job Agent Platform

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)

A comprehensive **Web3 job discovery platform** powered by **Fetch.ai uAgents**, **AI chatbot capabilities**, and **ICP smart contracts**, featuring a modern Next.js frontend with floating AI assistant.

## 📋 Project Summary & Overview

### **Problem Statement**
Traditional job platforms lack intelligent matching, are centralized, and don't leverage blockchain technology for trust and transparency. Job seekers struggle to find relevant opportunities, while employers face challenges in reaching qualified candidates efficiently.

### **Solution**
We've built a decentralized job discovery platform that combines:
- **AI-powered job matching** using Grok API for intelligent candidate-opportunity pairing
- **Fetch.ai uAgents** for decentralized, autonomous job search and matching
- **ICP smart contracts** for secure job posting and identity management
- **Modern web interface** with floating AI assistant for seamless user experience

### **Uniqueness**
This project introduces a novel Web3 use case by combining Fetch.ai's autonomous agents with ICP's smart contracts to create a decentralized job marketplace. The AI-powered matching system learns from user interactions and improves over time, while the blockchain infrastructure ensures transparency and trust.

### **Revenue Model**
- **Freemium Model**: Basic job search free, premium features for advanced filtering
- **Employer Subscriptions**: Monthly/yearly plans for enhanced job posting features
- **AI Matching Premium**: Advanced AI-powered candidate matching for enterprise clients
- **Agent Marketplace**: Revenue sharing from successful job placements via uAgents

### **Full-Stack Development**
The application is fully functional end-to-end with:
- ✅ **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- ✅ **Backend**: FastAPI server with AI integration
- ✅ **Blockchain**: ICP smart contracts in Motoko
- ✅ **Agents**: Fetch.ai uAgents with ASI:1 compatibility
- ✅ **Database**: Job storage and user management
- ✅ **AI Integration**: Grok API for intelligent job matching

## 🏗️ Project Architecture

### **System Overview**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   AI Backend    │    │   ICP Network   │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Smart       │
│                 │    │                 │    │    Contracts)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User          │    │   Fetch.ai      │    │   Job Data      │
│   Interface     │    │   uAgents       │    │   Storage       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Component Architecture**
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
│   │   └── 📄 handlers.py         # Chat request handlers
│   ├── 📁 scripts/                # Security and utility scripts
│   │   └── 📄 security-check.sh   # Automated security scanning
│   ├── 📄 agent.py                # Fetch.ai uAgent (ASI:1 compatible)
│   ├── 📄 main.py                 # FastAPI server entry point
│   ├── 📄 requirements.txt        # Python dependencies
│   ├── 📄 env.example             # Environment variables template
│   ├── 📄 SETUP_GROK.md           # Grok API setup guide
│   ├── 📄 generate_agent_seed.py  # Agent seed generation script
│   ├── 📄 test_client.py          # uAgent testing client
│   └── 📄 test_grok.py            # Grok API testing script
│
├── 📁 explorer_agent/             # 🔍 Job Scraping & Discovery
│   ├── 📁 scrapers/               # Job platform scrapers
│   │   ├── 📄 linkedin_scraper.py # LinkedIn job scraper
│   │   ├── 📄 indeed_scraper.py   # Indeed job scraper
│   │   ├── 📄 upwork_scraper.py   # Upwork job scraper
│   │   └── 📄 base_scraper.py     # Base scraper class
│   ├── 📁 api/                    # REST API endpoints
│   ├── 📁 core/                   # Core agent logic
│   └── 📁 models/                 # Data models
│
├── 📁 icp_contracts/              # ⛓️ ICP Smart Contracts
│   ├── 📁 src/
│   │   ├── 📄 job_contract.mo     # Motoko job management contract
│   │   ├── 📄 identity_contract.mo # User identity management
│   │   └── 📄 chat_contract.mo    # Chat session management
│   └── 📄 dfx.json                # DFX configuration
│
├── 📄 README.md                    # This project overview
├── 📄 SECURITY.md                  # Security guidelines and tools
├── 📄 .gitignore                   # Git ignore patterns
└── 📄 .gitattributes              # Git attributes
```

## 🚀 Quick Start

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

## 🚀 ICP Features Used

### **Smart Contracts**
- **Motoko Language**: Primary smart contract development language
- **Canister Management**: Deployed using DFX for ICP network
- **Identity Management**: User authentication and verification
- **Job Storage**: Decentralized job posting and management
- **Chat Sessions**: Persistent chat history on blockchain

### **ICP Network Integration**
- **Internet Identity**: Secure user authentication
- **Cycles Management**: Efficient resource allocation
- **Canister Communication**: Inter-canister calls for data sharing
- **Upgradeable Contracts**: Smart contract evolution capabilities

## 🤖 Fetch.ai Features Used

### **uAgents Framework**
- **ASI:1 Protocol**: Agent communication standard
- **Autonomous Agents**: Self-executing job search and matching
- **Agentverse Integration**: Discoverable on Fetch.ai ecosystem
- **Mailbox System**: Asynchronous message handling
- **Agent Identity**: Unique cryptographic agent addresses

### **Advanced Features**
- **Chat Protocol**: Natural language interaction with agents
- **HTTP Outcalls**: External API integration for job data
- **Timer Functions**: Scheduled job updates and notifications
- **Multi-Agent Coordination**: Collaborative job matching

## 🎯 Technical Difficulty & Advanced Features

### **Complexity Level: Advanced**
This project demonstrates significant technical complexity through:

- **Multi-Platform Integration**: Seamless connection between frontend, backend, blockchain, and AI services
- **Real-time Communication**: WebSocket connections for live updates and chat
- **AI-Powered Parsing**: Natural language processing for job requirement extraction
- **Blockchain Smart Contracts**: Motoko-based contract development and deployment
- **Agent Communication**: Fetch.ai uAgents with ASI:1 protocol implementation

### **Advanced Features Implemented**
- ✅ **HTTP Outcalls**: External API integration for job scraping
- ✅ **Timer Functions**: Automated job updates and notifications
- ✅ **Chat Protocol**: Natural language agent interaction
- ✅ **Multi-Agent Coordination**: Collaborative job matching
- ✅ **Real-time Updates**: WebSocket-based live data streaming
- ✅ **AI Integration**: LLM-powered job matching and filtering

## 🏆 Challenges Faced During Hackathon

### **Technical Challenges**
1. **Integration Complexity**: Coordinating multiple technologies (ICP, Fetch.ai, AI APIs, frontend)
2. **Real-time Communication**: Implementing WebSocket connections for live updates
3. **AI Model Integration**: Optimizing Grok API for job-related queries
4. **Blockchain Deployment**: Managing ICP canister deployment and cycles
5. **Agent Communication**: Implementing Fetch.ai uAgents with proper error handling

### **Solutions Implemented**
- **Modular Architecture**: Separated concerns for easier debugging and development
- **Comprehensive Testing**: Built test suites for each component
- **Error Handling**: Robust error handling with user-friendly messages
- **Documentation**: Detailed setup and deployment guides
- **Security Focus**: Automated security scanning and best practices

## 🔮 Future Plans

### **Short-term (3-6 months)**
- **Mobile App**: React Native application for iOS and Android
- **Enhanced AI**: Fine-tuned models for specific job categories
- **Payment Integration**: ICP-based payment system for premium features
- **User Analytics**: Advanced user behavior tracking and insights

### **Medium-term (6-12 months)**
- **Multi-Chain Support**: Integration with other blockchain networks
- **Enterprise Features**: Corporate job posting and candidate management
- **AI Training**: Custom AI models trained on job market data
- **API Marketplace**: Third-party integrations and plugins

### **Long-term (1+ years)**
- **Global Expansion**: Multi-language support and regional job markets
- **Advanced Matching**: Machine learning for predictive job matching
- **Decentralized Identity**: Self-sovereign identity management
- **Ecosystem Growth**: Developer tools and community-driven features

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
