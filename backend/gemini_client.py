import google.generativeai as genai
from typing import Optional

class GeminiClient:
    """
    Singleton pattern for Gemini API client
    Ensures only one instance of the API client is created
    """
    _instance: Optional['GeminiClient'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not GeminiClient._initialized:
            # Gemini API key
            API_KEY = "AIzaSyBnL1bKBns8QPO4KAQRqZGDBzEOKgjfsUg"
            genai.configure(api_key=API_KEY)
            
            # Store these for potential model switching
            self.available_models_list = []
            # Updated preference order - stable models first
            self.preferred_models = [
                'gemini-1.5-flash',
                'gemini-1.5-pro',
                'gemini-pro',
                'gemini-2.0-flash-exp'
            ]
            
            # First, list all available models to see what's actually available
            print("🔍 Listing available Gemini models...")
            try:
                # Convert generator to list to avoid 'generator has no len()' error
                all_models = list(genai.list_models())
                print(f"\n📋 Found {len(all_models)} total models")
                
                # Filter models that support generateContent
                for m in all_models:
                    if hasattr(m, 'supported_generation_methods') and 'generateContent' in m.supported_generation_methods:
                        model_name = m.name.split('/')[-1] if '/' in m.name else m.name
                        self.available_models_list.append(model_name)
                        print(f"  ✅ {model_name} - supports generateContent")
                
                if not self.available_models_list:
                    # If no models found with generateContent, try all models
                    print("⚠️  No models found with generateContent, trying all models...")
                    for m in all_models:
                        model_name = m.name.split('/')[-1] if '/' in m.name else m.name
                        self.available_models_list.append(model_name)
                        print(f"  📝 {model_name}")
                
                if not self.available_models_list:
                    raise Exception("No models found. Please check your API key and internet connection.")
                
                # Initial model setup
                self._setup_model()
                
                if self.model is None:
                    raise Exception(f"Failed to initialize any model. Available models: {self.available_models_list}")
                    
            except Exception as e:
                error_msg = f"Error listing/initializing models: {str(e)}"
                print(f"\n❌ {error_msg}")
                raise Exception(error_msg)
            
            # Strategy pattern: Different prompt strategies for different modes
            self.strategies = {
                'qa': self._qa_strategy,
                'explanation': self._explanation_strategy,
                'summary': self._summary_strategy
            }
            
            GeminiClient._initialized = True

    def _setup_model(self, skip_model=None):
        """Helper to setup the model, optionally skipping a failed one"""
        self.model = None
        
        # Filter out the model we want to skip
        models_to_try = [m for m in self.preferred_models if m != skip_model]
        
        # Try preferred models first
        for pref_model in models_to_try:
            if pref_model in self.available_models_list:
                try:
                    self.model = genai.GenerativeModel(pref_model)
                    self.current_model_name = pref_model
                    print(f"\n🤖 Current model set to: {pref_model}")
                    return
                except Exception as e:
                    print(f"⚠️  Could not initialize {pref_model}: {str(e)}")
                    continue
        
        # Fallback to any available model
        for model_name in self.available_models_list:
            if model_name != skip_model:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    self.current_model_name = model_name
                    print(f"\n🤖 Fallback model set to: {model_name}")
                    return
                except Exception as e:
                    print(f"⚠️  Could not initialize {model_name}: {str(e)}")
                    continue

    def _qa_strategy(self, user_message: str) -> str:
        """Q&A mode: Direct question answering"""
        prompt = f"""You are Vecho Ai, a helpful AI assistant designed for students.
Answer the following question clearly and concisely:

{user_message}

Provide a helpful, accurate answer:"""
        return prompt
    
    def _explanation_strategy(self, user_message: str) -> str:
        """Explanation mode: Detailed explanations in simple language"""
        prompt = f"""You are Vecho Ai, a helpful AI assistant designed for students.
Explain the following topic in simple, easy-to-understand language with examples:

{user_message}

Provide a clear, detailed explanation suitable for students:"""
        return prompt
    
    def _summary_strategy(self, user_message: str) -> str:
        """Summary mode: Generate summaries"""
        prompt = f"""You are Vecho Ai, a helpful AI assistant designed for students.
Create a concise summary of the following:

{user_message}

Provide a well-structured summary with key points:"""
        return prompt
    
    def get_response(self, user_message: str, mode: str = 'qa') -> str:
        """
        Get response from Gemini API using the specified strategy
        
        Args:
            user_message: The user's input message
            mode: Response mode ('qa', 'explanation', 'summary')
        
        Returns:
            AI-generated response string
        """
        try:
            # Get the appropriate strategy
            strategy = self.strategies.get(mode, self._qa_strategy)
            prompt = strategy(user_message)
            
            # Generate response
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                # If quota error, try to switch models once
                error_str = str(e)
                if "429" in error_str or "quota" in error_str.lower():
                    print(f"⚠️  Quota exceeded for {self.current_model_name}. Attempting to switch model...")
                    old_model = self.current_model_name
                    self._setup_model(skip_model=old_model)
                    
                    if self.model and self.current_model_name != old_model:
                        print(f"🔄 Switched to {self.current_model_name}. Retrying request...")
                        response = self.model.generate_content(prompt)
                        return response.text
                    else:
                        return "I've reached my free usage limit for all available models. Please try again in a few minutes."
                raise e
        
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                return "Usage limit reached. Please wait a moment before trying again."
            return f"I apologize, but I encountered an error: {error_msg}. Please try again."
