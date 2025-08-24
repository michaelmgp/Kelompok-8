CareerVerse Frontend

Frontend aplikasi CareerVerse - Web3 Job Agent Platform, dibangun dengan Next.js (App Router), TailwindCSS, dan desain premium Neo Aura (glassmorphism + animasi Framer Motion).

🚀 Fitur Utama

Landing Page & Dashboard dengan desain Neo Aura

Komponen modular: Hero, Sidebar, Dashboard, Analytics, Job Board

Analytics Page: grafik on-chain metrics (SVG custom charts)

Responsive Design (mobile-first)

Animasi halus dengan Framer Motion

Ikon modern dari Lucide React

🛠️ Tech Stack

Framework: Next.js 13+ (App Router)

Styling: TailwindCSS

Animations: Framer Motion

Icons: Lucide React

📦 Instalasi & Menjalankan
Prasyarat

Node.js 18+

npm atau yarn

Langkah Setup

Clone repository & masuk ke folder frontend

git clone https://github.com/michaelmgp/Kelompok-8.git
cd Kelompok-8/frontend


Install dependencies

npm install
# atau
yarn install


Jalankan development server

npm run dev


Akses di: http://localhost:3000

Build untuk production

npm run build
npm start

⚙️ Environment Variables

Buat file .env.local di folder frontend/ (opsional, jika nanti ada integrasi API):

NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_CHATBOT_URL=http://localhost:8001

📂 Struktur Folder
frontend/
├── .next/                
├── node_modules/


🧪 Testing (opsional)
npm run lint