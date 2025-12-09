import re
import json
from crewai import LLM
from typing import Any

class JSONCleaningLLM(LLM):
    def call(self, *args, **kwargs) -> str:
        try:
            # Call the original LLM
            response = super().call(*args, **kwargs)
            
            # Simple heuristic: if we expect JSON (based on context or just always try to clean)
            # We look for the first JSON block { ... } in the response.
            # This is a basic implementation.
            
            # Regex to find the first balanced JSON object (imperfect but better than nothing)
            # A more robust way involves json-repair lib, but let's stick to simple regex for now 
            # or relying on the fact that Gemini usually wraps in ```json ... ```
            
            # Strip markdown code blocks if present
            clean_response = response
            if "```" in response:
                 # Extract content between ```json and ``` or just ``` and ```
                match = re.search(r"```(?:json)?(.*?)```", response, re.DOTALL)
                if match:
                    clean_response = match.group(1).strip()
            
            # Further try to find the first '{' and last '}'
            start = clean_response.find('{')
            end = clean_response.rfind('}')
            
            if start != -1 and end != -1:
                json_str = clean_response[start:end+1]
                # Validate if it is loadable
                try:
                    json.loads(json_str)
                    return json_str
                except json.JSONDecodeError:
                    pass # Fallback to original if valid JSON not found in the substring

            return clean_response

        except Exception as e:
            # If the actual LLM call fails completely
            # Or if some other issue happens
            print(f"LLM Call Error: {e}")
            raise e
