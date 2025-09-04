# # app.py

# import streamlit as st
# import json
# from src.llm_service import get_response, detect_language

# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

# # ------------------------------
# # Load LLM model
# # ------------------------------
# tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-mono")
# model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-mono")

# def real_generator(prompt, max_new_tokens=800, do_sample=True, temperature=0.7):
#     """
#     Real generator using HuggingFace model.
#     """
#     try:
#         inputs = tokenizer(prompt, return_tensors="pt")
#         outputs = model.generate(
#             **inputs, max_new_tokens=max_new_tokens, do_sample=do_sample, temperature=temperature
#         )
#         text = tokenizer.decode(outputs[0], skip_special_tokens=True)
#         return [{"generated_text": text}]
#     except Exception as e:
#         print(f"Generator error: {e}")
#         return []

# # ------------------------------
# # Optional dummy generator
# # ------------------------------
# def dummy_generator(prompt, max_new_tokens=100, do_sample=True, temperature=0.7):
#     return [{"generated_text": json.dumps({
#         "platform": "C#",
#         "topic": prompt,
#         "steps": ["Step 1", "Step 2", "Step 3"],
#         "code_snippet": "// Example code",
#         "gotchas": ["Gotcha 1", "Gotcha 2"],
#         "difficulty": "Easy",
#         "docs_link": "https://docs.unity3d.com/Manual/index.html"
#     })}]

# # ------------------------------
# # Streamlit App
# # ------------------------------
# def main():
#     st.set_page_config(page_title="CodeXR AI Assistant", page_icon="🤖")
#     st.title("CodeXR AI Assistant for AR/VR Developers")

#     st.markdown("Enter your programming problem or task below:")

#     prompt = st.text_area("Problem Prompt", height=150)
#     use_llm = st.checkbox("Use AI generator for dynamic response", value=False)

#     if st.button("Get Response") and prompt.strip():
#         generator_func = real_generator if use_llm else None

#         # Get dynamic response from llm_service
#         response = get_response(prompt, generator=generator_func)

#         # Display difficulty
#         st.subheader("✅ Difficulty")
#         st.info(response["difficulty"])

#         # Display steps/subtasks
#         st.subheader("📝 Steps")
#         for i, task in enumerate(response["steps"], start=1):
#             st.write(f"{i}. {task}")

#         # Display code snippet
#         st.subheader("💻 Code Snippet")
#         language = detect_language(prompt).lower()
#         if language == "c#":
#             st.code(response["code_snippet"], language="csharp")
#         elif language == "c++":
#             st.code(response["code_snippet"], language="cpp")
#         elif language == "python":
#             st.code(response["code_snippet"], language="python")
#         elif language == "javascript":
#             st.code(response["code_snippet"], language="javascript")
#         else:
#             st.code(response["code_snippet"], language="text")

#         # Display gotchas
#         st.subheader("⚠️ Gotchas / Best Practices")
#         for gotcha in response["gotchas"]:
#             st.write(f"- {gotcha}")

#         # Documentation link
#         st.subheader("📚 Documentation Link")
#         st.markdown(f"[Click here]({response['docs_link']})", unsafe_allow_html=True)

#         # Display raw JSON response
#         st.subheader("🗄 Raw JSON Response")
#         st.code(json.dumps(response, indent=2), language="json")

# if __name__ == "__main__":
#     main()




import streamlit as st
import json
from src.llm_service import get_response, detect_language
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ------------------------------
# Load LLM model
# ------------------------------
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-mono")
model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-mono")

def real_generator(prompt, max_new_tokens=800, do_sample=True, temperature=0.7):
    """
    Real generator using HuggingFace model.
    """
    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature,
            pad_token_id=tokenizer.eos_token_id
        )
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return [{"generated_text": text}]
    except Exception as e:
        print(f"Generator error: {e}")
        return []

# ------------------------------
# Streamlit App
# ------------------------------
def main():
    st.set_page_config(page_title="CodeXR AI Assistant", page_icon="🤖")
    st.title("CodeXR AI Assistant for AR/VR Developers")
    st.markdown("Enter your programming problem or task below:")

    prompt = st.text_area("Problem Prompt", height=150)

    if st.button("Get Response") and prompt.strip():
        # Always use AI generator now
        response = get_response(prompt, generator=real_generator)

        # Display difficulty
        st.subheader("✅ Difficulty")
        st.info(response["difficulty"])

        # Display steps/subtasks
        st.subheader("📝 Steps")
        for i, task in enumerate(response["steps"], start=1):
            st.write(f"{i}. {task}")

        # Display code snippet
        st.subheader("💻 Code Snippet")
        language = detect_language(prompt).lower()
        lang_map = {
            "c#": "csharp",
            "c++": "cpp",
            "python": "python",
            "javascript": "javascript"
        }
        st.code(response["code_snippet"], language=lang_map.get(language, "text"))

        # Display gotchas
        st.subheader("⚠️ Gotchas / Best Practices")
        for gotcha in response["gotchas"]:
            st.write(f"- {gotcha}")

        # Documentation link
        st.subheader("📚 Documentation Link")
        st.markdown(f"[Click here]({response['docs_link']})", unsafe_allow_html=True)

        # Display raw JSON response
        st.subheader("🗄 Raw JSON Response")
        st.code(json.dumps(response, indent=2), language="json")

if __name__ == "__main__":
    main()
