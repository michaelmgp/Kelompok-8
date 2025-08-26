"use client";

import { useState, useEffect } from 'react';
import { apiClient, ChatRequest, ChatResponse } from '@/lib/api';
import { MessageCircle, X, Minimize2, Send, Bot } from 'lucide-react';

interface Message {
  id: number;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
  filters?: any;
}

export default function FloatingAIAssistant() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'ai',
      content: "Hello! I'm your AI career assistant. How can I help you today?",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [isConnectionChecking, setIsConnectionChecking] = useState(true);
  const [connectionStatus, setConnectionStatus] = useState<'checking' | 'connected' | 'disconnected' | 'backend-only'>('checking');

  // Check API connection on component mount
  useEffect(() => {
    checkAPIConnection();
  }, []);

  const checkAPIConnection = async () => {
    setIsConnectionChecking(true);
    setConnectionStatus('checking');
    try {
      const connected = await apiClient.testConnection();
      setIsConnected(connected);
      setConnectionStatus(connected ? 'connected' : 'disconnected');
      
      if (connected) {
        console.log('✅ Connected to AI chatbot API');
      } else {
        console.log('❌ Failed to connect to AI chatbot API');
      }
    } catch (error) {
      console.error('❌ Error checking API connection:', error);
      
      // Check if it's a "backend running but agent not ready" error
      if (error instanceof Error && error.message.includes('AI agent is not ready')) {
        setConnectionStatus('backend-only');
        setIsConnected(false);
        console.log('⚠️ Backend is running but AI agent is not ready');
      } else {
        setConnectionStatus('disconnected');
        setIsConnected(false);
      }
    } finally {
      setIsConnectionChecking(false);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isTyping || isConnectionChecking || !isConnected) return;

    const userMessage: Message = {
      id: messages.length + 1,
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      const chatRequest: ChatRequest = {
        user_prompt: inputMessage,
        top_k: 5
      };

      const response: ChatResponse = await apiClient.chat(chatRequest);
      
      const aiResponse: Message = {
        id: messages.length + 2,
        type: 'ai',
        content: response.message,
        timestamp: new Date(),
        filters: response.filters
      };

      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage: Message = {
        id: messages.length + 2,
        type: 'ai',
        content: "I'm sorry, I'm having trouble connecting to my AI services right now or try again later.",
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleQuickAction = (action: string) => {
    if (action.includes("Find me job opportunities")) {
      // Special handling for Find Jobs action
      handleFindJobsAction();
    } else {
      // Regular quick action handling
      setInputMessage(action);
      setTimeout(() => {
        if (action === inputMessage) {
          sendMessage();
        }
      }, 100);
    }
  };

  const handleFindJobsAction = () => {
    // Extract job requirements from current conversation
    const jobRequirements = extractJobRequirementsFromChat();
    
    // Store the requirements in localStorage or context for the job board
    localStorage.setItem('chatbotJobRequirements', JSON.stringify(jobRequirements));
    
    // Navigate to the job board page
    window.location.href = '/jobs';
  };

  const extractJobRequirementsFromChat = () => {
    // Extract job requirements from the current conversation
    const requirements = {
      keywords: '',
      location: '',
      required_skills: [],
      experience_level: '',
      job_type: 'Full-time',
      industry: '',
      remote_preference: '',
      budget_min: null,
      budget_max: null
    };

    // Analyze the conversation messages to extract requirements
    messages.forEach(message => {
      if (message.type === 'user') {
        const text = message.content.toLowerCase();
        
        // Extract location mentions
        if (text.includes('in ') || text.includes('at ')) {
          const locationMatch = text.match(/(?:in|at)\s+([a-zA-Z\s,]+?)(?:\s|$|\.)/);
          if (locationMatch) {
            requirements.location = locationMatch[1].trim();
          }
        }
        
        // Extract skills
        const skills = ['react', 'python', 'javascript', 'java', 'node.js', 'aws', 'docker', 'kubernetes', 'machine learning', 'ai', 'blockchain'];
        skills.forEach(skill => {
          if (text.includes(skill)) {
            requirements.required_skills.push(skill);
          }
        });
        
        // Extract experience level
        if (text.includes('junior') || text.includes('entry')) {
          requirements.experience_level = 'Junior';
        } else if (text.includes('senior') || text.includes('lead')) {
          requirements.experience_level = 'Senior';
        } else if (text.includes('mid') || text.includes('intermediate')) {
          requirements.experience_level = 'Mid-level';
        }
        
        // Extract industry
        if (text.includes('blockchain')) {
          requirements.industry = 'Blockchain';
        } else if (text.includes('ai') || text.includes('machine learning')) {
          requirements.industry = 'AI/ML';
        } else if (text.includes('web') || text.includes('frontend') || text.includes('backend')) {
          requirements.industry = 'Web Development';
        }
        
        // Extract remote preference
        if (text.includes('remote')) {
          requirements.remote_preference = 'Remote';
        } else if (text.includes('hybrid')) {
          requirements.remote_preference = 'Hybrid';
        }
        
        // Extract budget information
        const budgetMatch = text.match(/(?:budget|salary|pay)\s*(\d+(?:,\d+)*)\s*(?:usd|dollar|dollars)?\s*[-–—]\s*(\d+(?:,\d+)*)\s*(?:usd|dollar|dollars)?/i);
        if (budgetMatch) {
          requirements.budget_min = parseInt(budgetMatch[1].replace(/,/g, ''));
          requirements.budget_max = parseInt(budgetMatch[2].replace(/,/g, ''));
        }
        
        // Extract experience years
        const experienceMatch = text.match(/(\d+)\s*(?:years?|yrs?)\s*experience/i);
        if (experienceMatch) {
          const years = parseInt(experienceMatch[1]);
          if (years <= 2) {
            requirements.experience_level = 'Junior';
          } else if (years <= 5) {
            requirements.experience_level = 'Mid-level';
          } else {
            requirements.experience_level = 'Senior';
          }
        }
      }
    });

    // Set default keywords based on extracted skills
    if (requirements.required_skills.length > 0) {
      requirements.keywords = `${requirements.required_skills[0]} Developer`;
    } else {
      requirements.keywords = 'Software Developer';
    }

    return requirements;
  };

  const toggleChat = () => {
    if (isOpen) {
      setIsMinimized(!isMinimized);
    } else {
      setIsOpen(true);
      setIsMinimized(false);
    }
  };

  const closeChat = () => {
    setIsOpen(false);
    setIsMinimized(false);
  };

  const getConnectionStatusText = () => {
    switch (connectionStatus) {
      case 'checking':
        return 'Checking connection...';
      case 'connected':
        return 'Connected to AI Backend';
      case 'disconnected':
        return 'Disconnected from AI Backend';
      case 'backend-only':
        return 'Backend Running (Agent Not Ready)';
      default:
        return 'Unknown status';
    }
  };

  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'checking':
        return 'bg-yellow-500';
      case 'connected':
        return 'bg-green-500';
      case 'disconnected':
        return 'bg-red-500';
      case 'backend-only':
        return 'bg-orange-500';
      default:
        return 'bg-gray-500';
    }
  };

  if (!isOpen) {
    return (
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={toggleChat}
          className="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-4 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-110"
          title="AI Career Assistant"
        >
          <Bot className="w-6 h-6" />
        </button>
        
        {/* Connection status indicator */}
        <div className={`absolute -top-1 -right-1 w-3 h-3 rounded-full ${
          getConnectionStatusColor()
        } border-2 border-white`}></div>
        
        {/* Status tooltip on hover */}
        <div className="absolute bottom-full right-0 mb-2 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
          {getConnectionStatusText()}
        </div>
        
        {/* Loading indicator when checking connection */}
        {isConnectionChecking && (
          <div className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-yellow-500 border-2 border-white animate-pulse"></div>
        )}
      </div>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Chat Window */}
      <div className={`bg-white rounded-lg shadow-2xl border border-gray-200 transition-all duration-300 ${
        isMinimized ? 'w-80 h-16' : 'w-96 h-[500px]'
      }`}>
        
        {/* Header */}
        <div className="bg-blue-600 text-white rounded-t-lg p-3 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bot className="w-5 h-5" />
            <span className="font-semibold">AI Career Assistant</span>
            <div className={`w-2 h-2 rounded-full ${
              getConnectionStatusColor()
            }`}></div>
          </div>
          
          <div className="flex items-center space-x-1">
            <button
              onClick={() => setIsMinimized(!isMinimized)}
              className="text-white hover:text-gray-200 p-1"
              title={isMinimized ? "Expand" : "Minimize"}
            >
              <Minimize2 className="w-4 h-4" />
            </button>
            <button
              onClick={closeChat}
              className="text-white hover:text-gray-200 p-1"
              title="Close"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {!isMinimized && (
          <>
            {/* Connection Status Display */}
            <div className="px-3 py-2 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">
                  Status: {getConnectionStatusText()}
                </span>
                <button
                  onClick={checkAPIConnection}
                  className="text-xs text-blue-600 hover:text-blue-800 underline"
                >
                  Refresh
                </button>
              </div>
              
              {/* Show specific instructions based on status */}
              {connectionStatus === 'backend-only' && (
                <div className="mt-2 p-2 bg-orange-50 border border-orange-200 rounded text-xs text-orange-800">
                  ⚠️ Backend is running but AI agent needs to be started. 
                  Run <code className="bg-orange-100 px-1 rounded">python3 agent.py</code> in your backend terminal.
                </div>
              )}
              
              {connectionStatus === 'disconnected' && (
                <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-xs text-red-800">
                  ❌ Cannot connect to backend. waiting for the service to start.
                </div>
              )}
            </div>

            {/* Messages Area */}
            <div className="flex-1 p-3 space-y-3 overflow-y-auto h-[300px]">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs px-3 py-2 rounded-lg text-sm ${
                      message.type === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <p>{message.content}</p>
                    
                    {/* Show job filters if available */}
                    {message.filters && message.type === 'ai' && (
                      <div className="mt-2 pt-2 border-t border-gray-200">
                        <p className="text-xs text-gray-600 mb-1">📋 Job Requirements:</p>
                        <div className="text-xs text-gray-700 space-y-1">
                          {message.filters.skills.length > 0 && (
                            <div><strong>Skills:</strong> {message.filters.skills.join(', ')}</div>
                          )}
                          {message.filters.keywords.length > 0 && (
                            <div><strong>Keywords:</strong> {message.filters.keywords.join(', ')}</div>
                          )}
                          {message.filters.budget_min && message.filters.budget_max && (
                            <div><strong>Budget:</strong> ${message.filters.budget_min}-${message.filters.budget_max}</div>
                          )}
                          {message.filters.remote !== null && (
                            <div><strong>Remote:</strong> {message.filters.remote ? 'Yes' : 'No'}</div>
                          )}
                        </div>
                      </div>
                    )}
                    
                    <p className={`text-xs mt-1 ${
                      message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                    }`}>
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}
              
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 text-gray-900 px-3 py-2 rounded-lg">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="px-3 pb-2">
              <div className="text-xs text-gray-600 mb-2">
                💡 Quick Actions:
              </div>
              <div className="flex space-x-2 mb-2">
                <button
                  onClick={() => handleQuickAction("Find me job opportunities in blockchain and AI")}
                  className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded hover:bg-blue-200 transition-colors"
                  disabled={!isConnected || isConnectionChecking}
                >
                  🔍 Find Jobs (Auto-start)
                </button>
                <button
                  onClick={() => handleQuickAction("Help me optimize my profile")}
                  className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded hover:bg-green-200 transition-colors"
                  disabled={!isConnected || isConnectionChecking}
                >
                  ⚡ Optimize
                </button>
              </div>
            </div>

            {/* Input Area */}
            <div className="border-t border-gray-200 p-3">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder="Ask about jobs, salary, profile..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  disabled={!isConnected || isConnectionChecking}
                />
                <button
                  onClick={sendMessage}
                  disabled={!inputMessage.trim() || isTyping || !isConnected || isConnectionChecking}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
