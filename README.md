# CareerVerse - Web3 Job Agent Frontend

A modern Web3 job marketplace frontend built with **Next.js (App Router)**, **TailwindCSS**, and **Framer Motion**, featuring a premium Neo Aura glass morphism design.  
This is the **frontend-only** implementation of the CareerVerse platform.

## Project Architecture

```
frontend/
├── .next/                 # Build output (ignored in git)
├── node_modules/          # Dependencies (ignored in git)
├── public/                # Static assets (logo, images, icons)
├── src/
│   ├── app/               # Next.js App Router pages
│   │   ├── page.tsx       # Landing page
│   │   ├── analytics/     # Analytics page with charts
│   │   ├── jobs/          # Job board page
│   │   └── layout.tsx     # Root layout
│   ├── components/        # UI components
│   │   ├── home/          # Hero, Features, Stats sections
│   │   ├── dashboard/     # Dashboard, StatsCards, Activity
│   │   ├── analytics/     # Analytics chart components
│   │   ├── layout/        # Sidebar, TopNavigation
│   │   └── ui/            # Button, Card, Input, Avatar
│   └── lib/               # Utilities
├── tailwind.config.ts     # TailwindCSS configuration
├── next.config.js         # Next.js configuration
├── package.json
└── README.md
```

## Tech Stack

- **Framework**: Next.js 13+ (React 18, App Router)  
- **Styling**: TailwindCSS + Neo Aura theme  
- **Animations**: Framer Motion micro-interactions  
- **Icons**: Lucide React  
- **Charts**: Custom SVG-based analytics  

## Key Features

- 🎨 **Premium UI/UX**: Neo Aura glassmorphism design with smooth animations  
- 📊 **Analytics Dashboard**: On-chain style metrics & charts  
- 📱 **Responsive Layout**: Mobile-first adaptive design  
- ⚡ **Next.js 13**: App Router, fast builds, optimized assets  

## Getting Started

### Prerequisites
- Node.js 18+  
- npm or yarn  

### Installation

1. **Clone and setup**
   ```bash
   git clone https://github.com/michaelmgp/Kelompok-8.git
   cd Kelompok-8/frontend
   npm install
   ```

2. **Run in development mode**
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000)

3. **Build for production**
   ```bash
   npm run build
   npm start
   ```

## Environment Variables

Create `.env.local` in `frontend/` (optional, if later integrating APIs):

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_CHATBOT_URL=http://localhost:8001
```

## Development Workflow

- ✅ Setup project with Next.js + TailwindCSS  
- ✅ Add Neo Aura design system & components  
- ✅ Implement landing page, job board, analytics  
- 🚧 API integration (backend/AI/ICP) pending  

## Contributing

1. Use modular component structure (`src/components/`)  
2. Follow TailwindCSS utility-first styling  
3. Maintain Neo Aura UI consistency  
4. Keep `.gitignore` clean (ignore `.next/`, `node_modules/`, etc.)  

## License

MIT License - Frontend implementation for **CareerVerse**.

---

✨ **CareerVerse** — A decentralized, AI-powered job ecosystem with beautiful design.  
