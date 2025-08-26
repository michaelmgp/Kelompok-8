// API client for communicating with the AI chatbot backend
export interface ChatRequest {
  user_prompt: string;
  top_k?: number;
}

export interface ChatResponse {
  message: string;
  filters?: any;
}

export interface ParseRequest {
  text: string;
}

export interface ParseResponse {
  parsed_data: any;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}

export interface AgentStatusResponse {
  ready: boolean;
  status: string;
  message: string;
}

class APIClient {
  private baseURL: string;
  private timeout: number;
  private maxRetries: number;

  constructor() {
    // Get configuration from environment variables
    this.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8081';
    this.timeout = parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '10000');
    this.maxRetries = parseInt(process.env.NEXT_PUBLIC_API_RETRIES || '3');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);
    config.signal = controller.signal;

    try {
      const response = await fetch(url, config);
      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }

  async chat(request: ChatRequest): Promise<ChatResponse> {
    return this.request<ChatResponse>('/chat', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async parse(request: ParseRequest): Promise<ParseResponse> {
    return this.request<ParseResponse>('/parse', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async health(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/health');
  }

  async agentStatus(): Promise<AgentStatusResponse> {
    return this.request<AgentStatusResponse>('/agent/ready');
  }

  async testConnection(): Promise<boolean> {
    try {
      // First check if backend is running
      const healthResponse = await this.health();
      
      if (healthResponse.status !== 'healthy') {
        return false;
      }

      // Then check if agent is ready using the new endpoint (no Grok API calls)
      try {
        const agentStatus = await this.agentStatus();
        
        if (agentStatus.ready) {
          console.log('✅ Backend is healthy and uAgent is ready');
          return true;
        } else {
          console.log('⚠️ Backend is healthy but uAgent is not ready:', agentStatus.message);
          // Throw error to indicate agent not ready
          throw new Error('AI agent is not ready');
        }
        
      } catch (error) {
        // If agent status check fails, backend is running but agent not ready
        if (error instanceof Error) {
          throw new Error('AI agent is not ready');
        }
        throw error;
      }
    } catch (error) {
      console.error('API connection test failed:', error);
      return false;
    }
  }
}

export const apiClient = new APIClient();

// Development logging
if (process.env.NODE_ENV === 'development') {
  console.log('🔌 API Client initialized with:', {
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8081',
    timeout: process.env.NEXT_PUBLIC_API_TIMEOUT || '10000',
    maxRetries: process.env.NEXT_PUBLIC_API_RETRIES || '3'
  });
}
