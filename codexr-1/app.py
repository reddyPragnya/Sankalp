import streamlit as st
from src.llm_service import get_response
import json
import re

st.set_page_config(
    page_title="CodeXR: AI Coding Assistant for AR/VR Developers",
    page_icon="🕶️",
    layout="centered",
)

st.title("🕶️ CodeXR: AI Coding Assistant for AR/VR Developers")
st.markdown("Ask me anything about **Unity, Unreal, or Shaders!**")

# User input
prompt = st.text_input("Enter your developer question:", "")

def detect_language(code: str) -> str:
    """Simple heuristic-based language detection for AR/VR snippets."""
    code = code.lower()

    if "#include" in code or "uclass" in code or "uproperty" in code:
        return "cpp"  # Unreal Engine (C++)
    if "shader" in code or "sampler2d" in code or "float4" in code:
        return "hlsl"  # Shader code
    if "glsl" in code or "uniform" in code:
        return "glsl"
    if "public class" in code or "monobehaviour" in code:
        return "csharp"  # Unity C#
    if "function" in code and "blueprint" in code:
        return "python"  # Unreal Blueprints pseudo-Python

    return "csharp"  # Default fallback


if st.button("Get Answer") and prompt.strip():
    with st.spinner("Generating response..."):
        response = get_response(prompt)

    # ---- Subtasks ----
    st.subheader("📝 Subtasks")
    if response.get("subtasks"):
        for task in response["subtasks"]:
            st.markdown(f"- {task}")
    else:
        st.warning("Could not parse structured subtasks")

    # ---- Code Snippet ----
    st.subheader("💻 Code Snippet")
    code_block = response.get("code", "").strip()

    if code_block:
        # Clean accidental "Question:" / "Answer:" text
        cleaned = "\n".join(
            line for line in code_block.splitlines()
            if not line.startswith("Question:") and not line.startswith("Answer:")
        )
        lang = detect_language(cleaned)
        st.code(cleaned, language=lang)
    else:
        st.info("No code snippet was generated.")

    # ---- Gotchas / Best Practices ----
    st.subheader("⚠️ Gotchas / Best Practices")
    if response.get("gotchas"):
        for g in response["gotchas"]:
            st.markdown(f"- {g}")
    else:
        st.info("No best practices extracted")

    # ---- Difficulty ----
    st.subheader("🎯 Difficulty Rating")
    difficulty = response.get("difficulty", "Unknown").lower()

    if "beginner" in difficulty:
        st.markdown("🟢 **Beginner**")
    elif "intermediate" in difficulty:
        st.markdown("🟠 **Intermediate**")
    elif "advanced" in difficulty:
        st.markdown("🔴 **Advanced**")
    else:
        st.markdown("⚪ Unknown")

    # ---- Docs Link ----
    st.subheader("📖 Documentation Link")
    docs_link = response.get("docs_link", "").strip()
    if docs_link and docs_link != "#":
        st.markdown(f"[Official Docs]({docs_link})")
    else:
        st.markdown("[Unity Docs](https://docs.unity.com/) | [Unreal Docs](https://docs.unrealengine.com/)")

    # ---- Raw JSON ----
    st.subheader("🛠️ Raw JSON Output")
    st.json(response)
