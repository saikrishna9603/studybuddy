"""
⚠️ PLACEMENT AI FIX MODULE
Comprehensive debugging and fix for AI Placement features
Adds proper logging, error handling, and fallback mechanisms
"""

import os
import json
import logging
import re
from typing import Dict, List, Optional
from openai import OpenAI
import google.generativeai as genai

# Setup comprehensive logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize LLM clients with error handling
openai_client = None
try:
    api_key = os.environ.get('OPEN_API_KEY')
    if api_key:
        openai_client = OpenAI(api_key=api_key)
        logger.info("✅ OpenAI client initialized successfully")
    else:
        logger.warning("⚠️ OPEN_API_KEY not found in environment")
except Exception as e:
    logger.error(f"❌ OpenAI initialization failed: {e}")

# Gemini setup
gemini_key = os.environ.get('GEMINI_API_KEY')
try:
    if gemini_key:
        genai.configure(api_key=gemini_key)
        logger.info("✅ Gemini configured successfully")
    else:
        logger.warning("⚠️ GEMINI_API_KEY not found in environment")
except Exception as e:
    logger.error(f"❌ Gemini configuration failed: {e}")


class PlacementAIFix:
    """
    Central module for fixing and validating all placement AI features.
    Provides comprehensive logging and fallback mechanisms.
    """
    
    @staticmethod
    def extract_json_from_text(text: str) -> Optional[Dict]:
        """
        Extract JSON from LLM response, handling various formats.
        
        Args:
            text: LLM response text that may contain JSON
            
        Returns:
            Parsed JSON dict or None
        """
        logger.debug(f"Attempting JSON extraction from: {text[:100]}...")
        
        try:
            # Try direct JSON parsing
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        try:
            # Try extracting JSON block
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                return json.loads(json_match.group())
        except (json.JSONDecodeError, AttributeError):
            pass
        
        try:
            # Try extracting JSON with code block markers
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
            if json_match:
                return json.loads(json_match.group(1))
        except (json.JSONDecodeError, AttributeError, IndexError):
            pass
        
        logger.error(f"Failed to extract JSON from: {text[:100]}...")
        return None
    
    @staticmethod
    def call_openai(prompt: str, system_prompt: str = None, 
                   temperature: float = 0.7, max_tokens: int = 2000) -> Optional[str]:
        """
        Call OpenAI API with comprehensive error handling and logging.
        
        Args:
            prompt: User prompt
            system_prompt: System context
            temperature: Generation temperature
            max_tokens: Max tokens to generate
            
        Returns:
            Generated text or None if failed
        """
        logger.info(f"🔵 Calling OpenAI with prompt (first 100 chars): {prompt[:100]}...")
        
        if not openai_client:
            logger.error("❌ OpenAI client not initialized")
            return None
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            logger.info(f"✅ OpenAI response received ({len(result)} chars)")
            logger.debug(f"OpenAI response: {result[:200]}...")
            return result
            
        except Exception as e:
            logger.error(f"❌ OpenAI call failed: {e}")
            return None
    
    @staticmethod
    def call_gemini(prompt: str, system_prompt: str = None) -> Optional[str]:
        """
        Call Gemini API with comprehensive error handling and logging.
        
        Args:
            prompt: User prompt
            system_prompt: System context (note: Gemini handles differently)
            
        Returns:
            Generated text or None if failed
        """
        logger.info(f"🔵 Calling Gemini with prompt (first 100 chars): {prompt[:100]}...")
        
        if not gemini_key:
            logger.error("❌ Gemini API key not configured")
            return None
        
        try:
            full_prompt = ""
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            else:
                full_prompt = prompt
            
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(full_prompt)
            
            result = response.text
            logger.info(f"✅ Gemini response received ({len(result)} chars)")
            logger.debug(f"Gemini response: {result[:200]}...")
            return result
            
        except Exception as e:
            logger.error(f"❌ Gemini call failed: {e}")
            return None
    
    @staticmethod
    def get_ai_response(prompt: str, system_prompt: str = None,
                       prefer_openai: bool = True) -> Optional[str]:
        """
        Get AI response with automatic fallback.
        
        Args:
            prompt: User prompt
            system_prompt: System context
            prefer_openai: Try OpenAI first (True) or Gemini first (False)
            
        Returns:
            Generated text or None
        """
        logger.info("🚀 Starting AI response with fallback mechanism")
        
        if prefer_openai:
            logger.info("📍 Trying OpenAI first")
            result = PlacementAIFix.call_openai(prompt, system_prompt)
            if result:
                logger.info("✅ Using OpenAI response")
                return result
            
            logger.info("📍 OpenAI failed, trying Gemini fallback")
            result = PlacementAIFix.call_gemini(prompt, system_prompt)
            if result:
                logger.info("✅ Using Gemini response (fallback)")
                return result
        else:
            logger.info("📍 Trying Gemini first")
            result = PlacementAIFix.call_gemini(prompt, system_prompt)
            if result:
                logger.info("✅ Using Gemini response")
                return result
            
            logger.info("📍 Gemini failed, trying OpenAI fallback")
            result = PlacementAIFix.call_openai(prompt, system_prompt)
            if result:
                logger.info("✅ Using OpenAI response (fallback)")
                return result
        
        logger.error("❌ Both OpenAI and Gemini failed!")
        return None
    
    @staticmethod
    def validate_json_structure(data: Dict, required_keys: List[str]) -> bool:
        """
        Validate JSON structure has required keys.
        
        Args:
            data: Dictionary to validate
            required_keys: Required keys
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(data, dict):
            logger.error(f"❌ Data is not a dict: {type(data)}")
            return False
        
        missing = [k for k in required_keys if k not in data]
        if missing:
            logger.error(f"❌ Missing required keys: {missing}")
            return False
        
        logger.info(f"✅ JSON structure valid, all {len(required_keys)} keys present")
        return True


# Export the fix class for use in other modules
__all__ = ['PlacementAIFix', 'logger']
