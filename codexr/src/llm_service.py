# # src/llm_service.py

# import json
# import re

# # ------------------------------
# # Function: map_docs_link
# # ------------------------------
# def map_docs_link(prompt: str) -> str:
#     prompt_lower = prompt.lower()
    
#     if "unity" in prompt_lower or "c#" in prompt_lower:
#         return "https://docs.unity3d.com/Manual/index.html"
#     elif "unreal" in prompt_lower:
#         return "https://docs.unrealengine.com/"
#     elif "c++" in prompt_lower:
#         return "https://en.cppreference.com/w/"
#     elif "shader" in prompt_lower:
#         return "https://docs.unity3d.com/Manual/Shaders.html"
#     else:
#         return "https://developer.mozilla.org/en-US/"

# # ------------------------------
# # Function: classify_difficulty
# # ------------------------------
# def classify_difficulty(prompt: str, generator=None) -> str:
#     if generator:
#         ai_prompt = f"Classify this problem as Easy, Medium, or Hard:\n{prompt}\nAnswer:"
#         try:
#             output = generator(ai_prompt, max_new_tokens=50, do_sample=False)
#             text = output[0]["generated_text"].strip().lower()
#             if "easy" in text:
#                 return "Easy"
#             elif "medium" in text:
#                 return "Medium"
#             elif "hard" in text:
#                 return "Hard"
#         except Exception:
#             pass

#     # fallback rule-based
#     score = 0
#     prompt_lower = prompt.lower()
#     if any(word in prompt_lower for word in ["easy", "beginner", "basic"]):
#         score += 1
#     if any(word in prompt_lower for word in ["medium", "intermediate"]):
#         score += 2
#     if any(word in prompt_lower for word in ["hard", "advanced", "difficult"]):
#         score += 3
#     if any(word in prompt_lower for word in ["recursion", "shader", "multithreading", "optimization", "ai"]):
#         score += 2

#     if score <= 2:
#         return "Easy"
#     elif score <= 4:
#         return "Medium"
#     else:
#         return "Hard"

# # ------------------------------
# # Function: detect_language
# # ------------------------------
# def detect_language(prompt: str) -> str:
#     prompt_lower = prompt.lower()
#     if "c#" in prompt_lower or "unity" in prompt_lower:
#         return "C#"
#     elif "c++" in prompt_lower:
#         return "C++"
#     elif "python" in prompt_lower:
#         return "Python"
#     elif "javascript" in prompt_lower or "js" in prompt_lower:
#         return "JavaScript"
#     else:
#         return "Text"

# # ------------------------------
# # Function: detect_platform
# # ------------------------------
# def detect_platform(prompt: str) -> str:
#     prompt_lower = prompt.lower()
#     if "unity" in prompt_lower or "c#" in prompt_lower:
#         return "Unity"
#     elif "unreal" in prompt_lower or "ue4" in prompt_lower or "ue5" in prompt_lower:
#         return "Unreal"
#     elif "shader" in prompt_lower:
#         return "Shader"
#     elif "python" in prompt_lower:
#         return "Python"
#     elif "javascript" in prompt_lower or "js" in prompt_lower:
#         return "JavaScript"
#     else:
#         return "Generic"

# # ------------------------------
# # Function: generate_dynamic_content
# # ------------------------------
# def generate_dynamic_content(prompt: str, generator=None, max_retries=3) -> dict:
#     language = detect_language(prompt)
#     platform = detect_platform(prompt)
#     docs_link = map_docs_link(prompt)

#     if generator:
#         ai_prompt = f"""
# You are an AI coding assistant.

# For the following programming problem, generate a JSON in strict schema:

# {{
#   "platform": "{platform}",
#   "topic": "{prompt}",
#   "steps": [],        // 3-5 actionable subtasks
#   "code_snippet": "", // Working code snippet in {language}
#   "gotchas": [],      // 2-3 best practices or caveats
#   "difficulty": "",   // Easy, Medium, or Hard
#   "docs_link": "{docs_link}"
# }}

# Problem: {prompt}

# Output strictly in valid JSON format as shown above.
# """
#         for attempt in range(max_retries):
#             try:
#                 output = generator(ai_prompt, max_new_tokens=800, do_sample=True, temperature=0.7)
#                 raw_text = output[0]["generated_text"]
#                 match = re.search(r"\{.*\}", raw_text, re.DOTALL)
#                 if match:
#                     return json.loads(match.group())
#             except Exception:
#                 continue

#     # Fallback
#     return {
#         "platform": platform,
#         "topic": prompt,
#         "steps": [
#             f"Analyze the problem statement: {prompt}",
#             f"Break down {prompt} into smaller components",
#             f"Implement and test each component"
#         ],
#         "code_snippet": "// Example code unavailable",
#         "gotchas": [
#             f"Ensure proper memory management for {prompt}",
#             f"Validate performance and compatibility"
#         ],
#         "difficulty": classify_difficulty(prompt, generator),
#         "docs_link": docs_link
#     }

# # ------------------------------
# # Function: get_response
# # ------------------------------
# def get_response(prompt: str, generator=None) -> dict:
#     dynamic_content = generate_dynamic_content(prompt, generator)
#     # Already contains strict schema
#     return dynamic_content

# # ------------------------------
# # Optional test
# # ------------------------------
# if __name__ == "__main__":
#     test_prompt = "Write a C# script to move a player object in Unity with physics."
#     response = get_response(test_prompt)
#     print(json.dumps(response, indent=2))




import json
import re

# ------------------------------
# Function: map_docs_link
# ------------------------------
def map_docs_link(prompt: str) -> str:
    prompt_lower = prompt.lower()
    if "unity" in prompt_lower or "c#" in prompt_lower:
        return "https://docs.unity3d.com/Manual/index.html"
    elif "unreal" in prompt_lower:
        return "https://docs.unrealengine.com/"
    elif "c++" in prompt_lower:
        return "https://en.cppreference.com/w/"
    elif "shader" in prompt_lower:
        return "https://docs.unity3d.com/Manual/Shaders.html"
    else:
        return "https://developer.mozilla.org/en-US/"

# ------------------------------
# Function: classify_difficulty
# ------------------------------
def classify_difficulty(prompt: str, generator=None) -> str:
    if generator:
        ai_prompt = f"Classify this problem as Easy, Medium, or Hard:\n{prompt}\nAnswer:"
        try:
            output = generator(ai_prompt, max_new_tokens=50, do_sample=False)
            text = output[0]["generated_text"].strip().lower()
            if "easy" in text:
                return "Easy"
            elif "medium" in text:
                return "Medium"
            elif "hard" in text:
                return "Hard"
        except Exception:
            pass

    # fallback rule-based
    score = 0
    prompt_lower = prompt.lower()
    if any(word in prompt_lower for word in ["easy", "beginner", "basic"]):
        score += 1
    if any(word in prompt_lower for word in ["medium", "intermediate"]):
        score += 2
    if any(word in prompt_lower for word in ["hard", "advanced", "difficult"]):
        score += 3
    if any(word in prompt_lower for word in ["recursion", "shader", "multithreading", "optimization", "ai"]):
        score += 2

    if score <= 2:
        return "Easy"
    elif score <= 4:
        return "Medium"
    else:
        return "Hard"

# ------------------------------
# Function: detect_language
# ------------------------------
def detect_language(prompt: str) -> str:
    prompt_lower = prompt.lower()
    if "c#" in prompt_lower or "unity" in prompt_lower:
        return "C#"
    elif "c++" in prompt_lower:
        return "C++"
    elif "python" in prompt_lower:
        return "Python"
    elif "javascript" in prompt_lower or "js" in prompt_lower:
        return "JavaScript"
    else:
        return "Text"

# ------------------------------
# Function: detect_platform
# ------------------------------
def detect_platform(prompt: str) -> str:
    prompt_lower = prompt.lower()
    if "unity" in prompt_lower or "c#" in prompt_lower:
        return "Unity"
    elif "unreal" in prompt_lower or "ue4" in prompt_lower or "ue5" in prompt_lower:
        return "Unreal"
    elif "shader" in prompt_lower:
        return "Shader"
    elif "python" in prompt_lower:
        return "Python"
    elif "javascript" in prompt_lower or "js" in prompt_lower:
        return "JavaScript"
    else:
        return "Generic"

# ------------------------------
# Function: generate_dynamic_content
# ------------------------------
def generate_dynamic_content(prompt: str, generator=None, max_retries=3) -> dict:
    language = detect_language(prompt)
    platform = detect_platform(prompt)
    docs_link = map_docs_link(prompt)

    if generator:
        ai_prompt = f"""
You are an AI coding assistant.

For the following programming problem, generate a JSON in strict schema:

{{
  "platform": "{platform}",
  "topic": "{prompt}",
  "steps": [],        // 3-5 actionable subtasks
  "code_snippet": "", // Working code snippet in {language}
  "gotchas": [],      // 2-3 best practices or caveats
  "difficulty": "",   // Easy, Medium, or Hard
  "docs_link": "{docs_link}"
}}

Problem: {prompt}

Output strictly in valid JSON format as shown above.
"""
        for attempt in range(max_retries):
            try:
                output = generator(ai_prompt, max_new_tokens=800, do_sample=True, temperature=0.7)
                raw_text = output[0]["generated_text"]
                match = re.search(r"\{.*\}", raw_text, re.DOTALL)
                if match:
                    data = json.loads(match.group())
                    # Ensure code snippet formatting is clean
                    if "code_snippet" in data and data["code_snippet"]:
                        data["code_snippet"] = data["code_snippet"].strip()
                    return data
            except Exception:
                continue

    # Fallback
    return {
        "platform": platform,
        "topic": prompt,
        "steps": [
            f"Analyze the problem statement: {prompt}",
            f"Break down {prompt} into smaller components",
            f"Implement and test each component"
        ],
        "code_snippet": "// Example code unavailable",
        "gotchas": [
            f"Ensure proper memory management for {prompt}",
            f"Validate performance and compatibility"
        ],
        "difficulty": classify_difficulty(prompt, generator),
        "docs_link": docs_link
    }

# ------------------------------
# Function: get_response
# ------------------------------
def get_response(prompt: str, generator=None) -> dict:
    return generate_dynamic_content(prompt, generator)

# ------------------------------
# Optional test
# ------------------------------
if __name__ == "__main__":
    test_prompt = "Write a C# script to move a player object in Unity with physics."
    response = get_response(test_prompt, generator=None)
    print(json.dumps(response, indent=2))
