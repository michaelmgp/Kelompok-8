# CareerVerse Frontend

A modern frontend application built with Next.js 14 App Router, focusing on professional development and career management with AI-powered job assistance.

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI primitives
- **Icons**: Font Awesome & Lucide React
- **AI Integration**: Grok API via Fetch.ai uAgents

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- AI Chatbot Backend running on port 8081

### 1. Install Dependencies
```bash
npm install
# or
yarn install
```

### 2. Configure Environment
```bash
# Copy environment template
cp env.example .env.local

# Edit .env.local with your API configuration
NEXT_PUBLIC_API_URL=http://localhost:8081
```

### 3. Start Development Server
```bash
npm run dev
# or
yarn dev
```

Your app will be available at: http://localhost:5000

## 🔗 AI Integration

### Backend Requirements
- **AI Chatbot Service** must be running on port 8081
- **uAgents Service** should be active for blockchain communication
- **Grok API** configured and working

### API Endpoints Used
- `POST /chat` - Send chat messages to AI
- `POST /parse` - Parse job requirements from text
- `GET /health` - Check backend connectivity

### Features
- **Real-time AI Chat** - Powered by Grok API
- **Job Filter Parsing** - Automatic requirement extraction
- **Connection Status** - Visual backend connectivity indicator
- **Error Handling** - Graceful fallbacks when API is unavailable

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── ai-assistant/      # AI Chat Interface
│   ├── jobs/              # Job Listings
│   ├── analytics/         # Career Analytics
│   └── docs/              # Documentation
├── components/             # Reusable Components
│   ├── ai/                # AI-specific components
│   ├── ui/                # Base UI components
│   ├── layout/            # Layout components
│   └── jobs/              # Job-related components
└── lib/                   # Utilities and API clients
    └── api.ts             # AI Chatbot API client
```

## 🧪 Testing

```bash
# Run type checking
npm run type-check

# Run linting
npm run lint

# Build for production
npm run build
```

## 🌐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | AI Chatbot backend URL | `http://localhost:8081` |

## 🔧 Troubleshooting

### Common Issues

1. **"Disconnected from AI Backend"**
   - Ensure AI chatbot service is running on port 8081
   - Check if backend is accessible: `curl http://localhost:8081/health`

2. **API Errors**
   - Verify GROK_API_KEY is set in backend
   - Check backend logs for errors
   - Ensure virtual environment is activated

3. **CORS Issues**
   - Backend should allow requests from `http://localhost:5000`
   - Check CORS_ALLOW_ORIGINS in backend .env

## 🚀 Deployment

### Production Build
```bash
npm run build
npm run start
```

### Environment Configuration
```bash
# Set production API URL
NEXT_PUBLIC_API_URL=https://your-production-api.com
```

## 🤝 Contributing

1. Follow TypeScript best practices
2. Use Tailwind CSS for styling
3. Test AI integration thoroughly
4. Update documentation for new features

---

**Built with ❤️ for the CareerVerse ecosystem**

