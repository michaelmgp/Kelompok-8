# Explorer Agent

An intelligent internet exploration agent that searches for public job listings across the web and streams real-time data to the frontend.

## Features

- **Web Scraping**: Automated job search across multiple job boards and websites
- **Real-time Streaming**: WebSocket-based data streaming to frontend
- **Intelligent Search**: AI-powered job matching and filtering
- **Multi-source Integration**: Support for LinkedIn, Indeed, Glassdoor, and more
- **Rate Limiting**: Respectful web scraping with configurable delays
- **Data Processing**: Clean, structured job data output
- **Scalable Architecture**: Built with FastAPI and async processing

## Architecture

```
explorer_agent/
├── core/           # Core agent logic and configuration
├── scrapers/       # Web scraping modules for different job sites
├── processors/     # Data processing and AI analysis
├── streamers/      # Real-time data streaming
├── api/           # FastAPI endpoints
├── models/        # Data models and schemas
└── utils/         # Utility functions and helpers
```

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. Run the agent:
   ```bash
   python main.py
   ```

4. Access the API at `http://localhost:8000`

## API Endpoints

- `GET /jobs/search` - Search for jobs with filters
- `GET /jobs/stream` - WebSocket endpoint for real-time job updates
- `POST /jobs/analyze` - AI-powered job analysis
- `GET /jobs/sources` - List available job sources

## Configuration

The agent can be configured via environment variables:

- `EXPLORER_AGENT_PORT` - API server port (default: 8000)
- `EXPLORER_AGENT_DEBUG` - Debug mode (default: False)
- `EXPLORER_AGENT_RATE_LIMIT` - Scraping rate limit in seconds (default: 2)
- `EXPLORER_AGENT_USER_AGENT` - Custom user agent for requests

## Security

- Rate limiting to prevent abuse
- User agent rotation
- Respectful web scraping practices
- Configurable delays between requests

