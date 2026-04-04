"""
Groq API Client Utility
Provides a reusable interface for interacting with Groq API
"""

import os
from groq import Groq


class GroqClient:
    """Initialize and manage Groq API client"""
    
    def __init__(self, api_key: str = None, model: str = "mixtral-8x7b-32768"):
        """
        Initialize Groq client
        
        Args:
            api_key (str): Groq API key. If None, uses GROQ_API_KEY env var
            model (str): Model name to use (default: mixtral-8x7b-32768)
        """
        if api_key is None:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError(
                    "GROQ_API_KEY not provided and not found in environment variables. "
                    "Please set GROQ_API_KEY environment variable or pass it directly."
                )
        
        self.api_key = api_key
        self.model = model
        self.client = Groq(api_key=api_key)
    
    def chat(self, messages: list, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """
        Send a chat message to Groq API
        
        Args:
            messages (list): List of message dicts with 'role' and 'content'
            temperature (float): Sampling temperature (0-2)
            max_tokens (int): Maximum tokens in response
        
        Returns:
            str: Response content from the model
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    def chat_with_system(self, user_message: str, system_message: str = None, 
                        temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """
        Convenience method for simple chat with optional system message
        
        Args:
            user_message (str): User message content
            system_message (str): Optional system message to set context
            temperature (float): Sampling temperature (0-2)
            max_tokens (int): Maximum tokens in response
        
        Returns:
            str: Response content from the model
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": user_message})
        
        return self.chat(messages, temperature, max_tokens)


def get_groq_client(api_key: str = None, model: str = "mixtral-8x7b-32768") -> GroqClient:
    """
    Factory function to get a Groq client instance
    
    Args:
        api_key (str): Groq API key. If None, uses GROQ_API_KEY env var
        model (str): Model name to use
    
    Returns:
        GroqClient: Initialized Groq client
    """
    return GroqClient(api_key=api_key, model=model)
