import os
import logging
from langchain_groq import ChatGroq

logger = logging.getLogger(__name__)

def get_llm():
    model_type = os.getenv("MODEL_TYPE", "grok").lower()
    logger.info(f"🤖 Initializing LLM with type: {model_type}")
    
    if model_type == "grok":
        # Grok API - lightweight and fast
        api_key = os.getenv("GROK_API_KEY")
        if not api_key:
            logger.error("❌ GROK_API_KEY environment variable is required for Grok")
            raise ValueError("GROK_API_KEY environment variable is required for Grok")
        
        model_name = os.getenv("GROK_MODEL", "llama3-8b-8192")
        logger.info(f"🚀 Using Grok API with model: {model_name}")
        
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name,
            temperature=0.2
        )
        logger.info("✅ Grok LLM initialized successfully")
        return llm
    
    elif model_type == "openai":
        # OpenAI - cloud-based
        logger.info("☁️ Using OpenAI API")
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("❌ OPENAI_API_KEY environment variable is required for OpenAI")
            raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI")
        
        model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        logger.info(f"🚀 Using OpenAI with model: {model_name}")
        
        llm = ChatOpenAI(
            openai_api_key=api_key,
            model_name=model_name,
            temperature=0.2
        )
        logger.info("✅ OpenAI LLM initialized successfully")
        return llm
    
    else:
        logger.error(f"❌ Unsupported MODEL_TYPE: {model_type}")
        raise ValueError(f"Unsupported MODEL_TYPE: {model_type}. Use 'grok' (recommended) or 'openai'")
