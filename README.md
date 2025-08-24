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
├── kelompok-8/                  # Next.js 14+ App Directory (repo ini)
│   ├── app/                     # App router & pages
│   │   ├── (auth)/              # Auth routes (login, register)
│   │   ├── layout.tsx           # Root layout
│   │   └── page.tsx             # Landing page
│   ├── components/              # UI components
│   ├── public/                  # Static assets
│   ├── package.json             # Project dependencies
│   └── ...
│
├── client/                      # Current React frontend (legacy)
└── server/                      # Current Express backend (legacy)

## Menjalankan Aplikasi (Next.js API & Frontend)

1. **Clone dan masuk ke folder repo ini:**
	```
	git clone <repo-url>
	cd kelompok-8
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
	Buka [http://localhost:3000](http://localhost:3000) untuk melihat aplikasi.

5. **Akses halaman Register:**
	Buka [http://localhost:3000/register](http://localhost:3000/register) untuk halaman pendaftaran user baru.

6. **Akses halaman Login:**
	Buka [http://localhost:3000/login](http://localhost:3000/login) untuk halaman Login user.

```
