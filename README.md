# DecentWork - Web3 Job Agent Platform

A comprehensive Web3 job discovery platform powered by Fetch.ai agents and AI chatbot capabilities, featuring a premium Neo Aura glass morphism design.

## Project Architecture

```
job-agent-platform/
│
├── ai_chatbot/                  # AI Engineer Module
│   ├── chatbot/                 
│   │   ├── model.py             # OpenAI/LangChain logic
│   │   ├── handlers.py          # Chat & intent detection
│   │   └── fetch_agent_client.py# API client to Backend Agent
│   ├── tests/
│   └── main.py                  # FastAPI chatbot server
│
├── backend_agent/               # Backend Developer Module
│   ├── agents/
│   │   ├── upwork_agent.py      # Fetch.ai agent for Upwork
│   │   ├── fiverr_agent.py      # Fetch.ai agent for Fiverr
│   │   └── coordinator.py       # Multi-platform coordinator
│   ├── api/
│   │   ├── routes.py            # FastAPI REST endpoints
│   │   └── icp_integration.py   # ICP blockchain integration
│   ├── services/
│   │   ├── scraper.py           # Job scraping orchestration
│   │   ├── job_formatter.py     # Data formatting & analytics
│   │   └── identity_manager.py  # User profile management
│   ├── tests/
│   └── main.py                  # FastAPI backend server
│
├── icp_contracts/               # ICP Smart Contracts
│   ├── src/
│   │   ├── job_contract.mo      # Motoko job management
│   │   └── identity_contract.mo # Motoko identity & reputation
│   └── dfx.json                 # ICP project configuration
│
├── frontend/                    # Frontend Application
│   ├── pages/
│   │   └── Dashboard.tsx        # Main dashboard page
│   ├── components/
│   │   └── Sidebar.tsx          # Navigation sidebar
│   └── api_client.js            # API communication layer
│
├── client/                      # Current React frontend (legacy)
└── server/                      # Current Express backend (legacy)
```

## Tech Stack

### Frontend
- **Framework**: React with Vite
- **Styling**: TailwindCSS + Neo Aura theme
- **Animations**: Framer Motion
- **Routing**: Wouter
- **Icons**: Lucide React
- **State Management**: TanStack Query

### Backend Agent System
- **Framework**: FastAPI (Python)
- **Agents**: Fetch.ai framework
- **Job Platforms**: Upwork, Fiverr, Freelancer
- **Database**: PostgreSQL + Drizzle ORM
- **Queue**: Redis (for job processing)

### AI Chatbot
- **Framework**: FastAPI (Python)
- **AI Models**: OpenAI GPT-4 / LangChain
- **WebSocket**: Real-time chat support
- **Intent Recognition**: Custom NLP pipeline

### Blockchain Integration
- **Platform**: Internet Computer Protocol (ICP)
- **Language**: Motoko
- **Features**: Job contracts, identity verification, reputation

## Key Features

### 🤖 Autonomous Job Agents
- **Upwork Agent**: Scrapes and filters Web3/blockchain jobs
- **Fiverr Agent**: Monitors gigs and buyer requests
- **Coordinator**: Deduplicates, ranks, and manages all job data

### 💬 AI-Powered Chatbot
- **Job Recommendations**: Personalized based on user skills
- **Career Guidance**: Skill development and career path advice
- **Real-time Chat**: WebSocket-based instant responses
- **Intent Detection**: Smart routing of user queries

### 🔗 Blockchain Integration
- **Job Records**: Immutable job listing verification
- **Identity Management**: Decentralized user profiles
- **Reputation System**: Transparent review and rating system
- **Smart Contracts**: Automated job completion and payments

### 🎨 Premium UI/UX
- **Neo Aura Design**: Dark glass morphism with radial gradients
- **Responsive Layout**: Mobile-first adaptive design
- **Smooth Animations**: Framer Motion micro-interactions
- **Real-time Updates**: Live job feed and agent status

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+ and pip
- PostgreSQL database
- Fetch.ai development environment
- DFX (for ICP development)

### Installation

1. **Clone and setup**
   ```bash
   cd job-agent-platform
   npm install
   ```

2. **Start the current frontend**
   ```bash
   npm run dev
   ```

3. **Setup AI Chatbot** (separate terminal)
   ```bash
   cd ai_chatbot
   pip install fastapi uvicorn openai langchain
   python main.py
   # Runs on http://localhost:8001
   ```

4. **Setup Backend Agent** (separate terminal)
   ```bash
   cd backend_agent
   pip install fastapi uvicorn fetch-ai-ledger
   python main.py
   # Runs on http://localhost:8000
   ```

5. **Deploy ICP Contracts** (optional)
   ```bash
   cd icp_contracts
   dfx start --background
   dfx deploy
   ```

## Environment Variables

Create `.env` files in respective directories:

### AI Chatbot (.env)
```
OPENAI_API_KEY=your_openai_api_key
BACKEND_AGENT_URL=http://localhost:8000
```

### Backend Agent (.env)
```
DATABASE_URL=postgresql://user:pass@localhost/decentwork
FETCH_AI_PRIVATE_KEY=your_fetch_ai_key
ICP_CANISTER_ID=your_canister_id
```

### Frontend (.env)
```
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_CHATBOT_URL=http://localhost:8001
```

## API Endpoints

### Backend Agent API (Port 8000)
- `POST /api/jobs/recommendations` - Get job recommendations
- `POST /api/search/trigger` - Trigger new job search
- `GET /api/agents/status` - Get agent status
- `POST /api/applications/submit` - Submit job application

### AI Chatbot API (Port 8001)
- `POST /api/chat/message` - Send chat message
- `POST /api/recommendations/jobs` - AI job recommendations
- `POST /api/advice/skills` - Get skill development advice
- `WS /ws/{user_id}` - WebSocket chat connection

## Development Workflow

### Phase 1: Core Infrastructure ✅
- [x] Project structure setup
- [x] AI chatbot with intent detection
- [x] Backend agent framework
- [x] Fetch.ai agent integration
- [x] ICP smart contracts

### Phase 2: Agent Development (In Progress)
- [ ] Production Upwork API integration
- [ ] Fiverr scraping implementation
- [ ] Job deduplication algorithms
- [ ] Real-time job feed

### Phase 3: Frontend Migration
- [ ] Migrate from legacy React to new structure
- [ ] Implement API client integration
- [ ] Add real-time WebSocket connections
- [ ] Complete responsive design

### Phase 4: Blockchain Integration
- [ ] Deploy ICP canisters to mainnet
- [ ] Integrate smart contract calls
- [ ] Implement reputation system
- [ ] Add decentralized identity

## Contributing

1. Follow the modular architecture
2. Update `replit.md` with any architectural changes
3. Ensure all APIs have proper error handling
4. Test agent integrations thoroughly
5. Maintain the Neo Aura design consistency

## Troubleshooting

### Linux Environment Note

If you are running this project on a Linux-based environment and encounter a `TypeError [ERR_INVALID_ARG_TYPE]` during `npm run dev`, the error might originate from `vite.config.ts` or `server/vite.ts`.

This is often caused by `import.meta.dirname` not being correctly resolved in some Node.js versions or configurations on Linux.

**Solution:**

The fix involves replacing the usage of `import.meta.dirname` with a more robust method using `import.meta.url`.

1.  **In `vite.config.ts` and `server/vite.ts`:**
    *   Add the following imports at the top of the file:
        ```typescript
        import path from "path";
        import { fileURLToPath } from "url";
        ```
    *   Define a `__dirname` constant right after the imports:
        ```typescript
        const __dirname = path.dirname(fileURLToPath(import.meta.url));
        ```
    *   Replace all instances of `import.meta.dirname` with the newly defined `__dirname` variable.

These changes ensure that file paths are resolved correctly across different environments.

## License

MIT License - Built for the Web3 ecosystem

---

**DecentWork** - Connecting Web3 talent with opportunities through intelligent automation and beautiful user experiences.