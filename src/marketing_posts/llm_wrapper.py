import json
import sys
from crewai import LLM
import litellm
from json_repair import repair_json
from typing import Any, List, Dict, Union

class JSONCleaningLLM(LLM):
    """
    A wrapper around CrewAI LLM that forces usage of custom call method 
    to robustly clean JSON output using json_repair.
    """
    real_model_name: str = "gemini/gemini-pro-latest"
    
    def __init__(self, model="gemini/gemini-pro-latest"):
        # We pass a known valid model name (but not Gemini) to avoid CrewAI auto-replacement logic.
        # We override call() anyway so this model name is just a placeholder.
        super().__init__(model="gpt-4")
        self.real_model_name = model
        print(f"DEBUG: JSONCleaningLLM Initialized (Real Model: {self.real_model_name})")

    def call(self, messages: Union[str, List[Dict[str, str]]], callbacks: List[Any] = None) -> str:
        # sys.stderr.write(f"DEBUG: JSONCleaningLLM.call executing for {self.real_model_name}\n")
        # sys.stderr.flush()
        
        try:
            # LiteLLM expects messages list. If string, wrap it.
            if isinstance(messages, str):
                messages = [{"role": "user", "content": messages}]
            
            response = litellm.completion(
                model=self.real_model_name,
                messages=messages,
            )
            
            content = response.choices[0].message.content
            
            # Use json_repair
            try:
                # print(f"[DEBUG] Raw content length: {len(content)}")
                cleaned_json_str = repair_json(content, return_objects=False)
                if cleaned_json_str:
                    # sys.stderr.write(f"[DEBUG] JSON Repair success for content length {len(content)}\n")
                    # sys.stderr.flush()
                    return cleaned_json_str
            except Exception as e:
                print(f"[JSONCleaningLLM] Repair failed: {e}")
                
            return content

        except Exception as e:
            print(f"LLM Call Error: {e}")
            raise e
