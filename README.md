# Web3 Job Agent Platform

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
├── frontend/                    # Frontend Application (Next.js 13+)
│   ├── src/                     # App source code (App Router)
│   ├── public/                  # Static assets
│   ├── package.json             # Frontend dependencies
│   └── ...
│
├── client/                      # Current React frontend (legacy)
└── server/                      # Current Express backend (legacy)
```

## Menjalankan Frontend (Next.js)

1. **Masuk ke folder frontend:**
	```
	cd frontend
	```

2. **Install dependencies:**
	```
	npm install
	```

3. **Jalankan development server:**
	```
	npm run dev
	```

4. **Buka di browser:**
	Buka [http://localhost:5000](http://localhost:5000) untuk melihat aplikasi.

5. **Akses halaman Register:**
	Buka [http://localhost:5000/register](http://localhost:5000/register) untuk halaman pendaftaran user baru.

---
