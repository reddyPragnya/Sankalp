# import streamlit as st
# import json
# import time

# # --- Streamlit UI Layout ---
# st.set_page_config(layout="wide", page_title="CodeXR: AI Coding Assistant")

# st.markdown("""
#     <div style="text-align: center;">
#         <h1 style="font-size: 3.5rem; font-weight: bold; background: linear-gradient(to right, #8b5cf6, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
#             CodeXR
#         </h1>
#         <p style="font-size: 1.25rem; color: #a1a1aa;">
#             Your AI coding partner for AR/VR development.
#         </p>
#     </div>
#     <hr style="border: 1px solid #3f3f46;"/>
# """, unsafe_allow_html=True)

# st.header("1. Input Query")

# # Use st.session_state to manage the current state and query
# if 'query' not in st.session_state:
#     st.session_state.query = ""

# query_input = st.text_area(
#     "Enter your AR/VR development question:",
#     height=150,
#     placeholder="e.g., How do I add teleport locomotion in Unity VR?",
#     value=st.session_state.query
# )

# # --- Demo Scenarios ---
# st.markdown("### Or try one of our demo queries:")
# col1, col2, col3 = st.columns(3)

# with col1:
#     if st.button("Unity: Teleport Locomotion"):
#         st.session_state.query = "How do I add teleport locomotion in Unity VR?"
#         st.rerun()
# with col2:
#     if st.button("Unreal: Multiplayer Setup"):
#         st.session_state.query = "How do I set up multiplayer in Unreal VR?"
#         st.rerun()
# with col3:
#     if st.button("Shader: AR Occlusion"):
#         st.session_state.query = "Which shader works best for AR occlusion?"
#         st.rerun()

# # --- Functions for Placeholder Responses ---
# def get_placeholder_response(query):
#     """Returns a hardcoded response for specific demo queries."""
#     if "unity" in query.lower():
#         return {
#             "platform": "Unity",
#             "topic": "Teleport Locomotion",
#             "difficulty": "Easy",
#             "docs_link": "https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@1.0/manual/teleportation.html",
#             "steps": [
#                 "Install the XR Interaction Toolkit package from the Unity Package Manager.",
#                 "Add an XR Rig to your scene. You can use the 'Add XR Origin' button under GameObject > XR.",
#                 "Add a 'Teleportation Provider' component to your XR Origin.",
#                 "Add a 'Teleportation Anchor' or 'Teleportation Area' to the ground where you want the player to be able to teleport.",
#                 "Assign the 'Teleportation Provider' to the provider field of your 'Teleportation Anchor' or 'Teleportation Area'."
#             ],
#             "code_snippet": """
# // This is a simple C# script for a Teleportation Anchor in Unity.
# // It is not required for the basic setup but can be used for custom logic.

# using UnityEngine;
# using UnityEngine.XR.Interaction.Toolkit;

# public class CustomTeleportationAnchor : MonoBehaviour
# {
#     // The teleportation provider that will handle the teleportation request.
#     public TeleportationProvider teleportationProvider;

#     public void TeleportPlayer(XRBaseInteractor interactor)
#     {
#         if (teleportationProvider != null)
#         {
#             TeleportRequest teleportRequest = new TeleportRequest();
#             teleportRequest.destinationPosition = transform.position;
#             teleportationProvider.QueueTeleportRequest(teleportationRequest);
#         }
#     }
# }
# """,
#             "gotchas": [
#                 "Ensure your scene has a valid 'Nav Mesh' baked for the teleportation to work correctly.",
#                 "Check that the XR Interaction Toolkit package is up-to-date in your Project Manager.",
#                 "Make sure your XR Rig has the correct 'Teleportation Provider' component assigned."
#             ]
#         }
#     elif "unreal" in query.lower():
#         return {
#             "platform": "Unreal Engine",
#             "topic": "Multiplayer Setup",
#             "difficulty": "Medium",
#             "docs_link": "https://docs.unrealengine.com/5.3/en-US/networking-and-multiplayer-in-unreal-engine/",
#             "steps": [
#                 "Create a new C++ or Blueprint project and enable the 'Online Subsystem' plugin.",
#                 "Configure your `DefaultEngine.ini` file to specify the networking settings.",
#                 "Create a Player Controller and Game State and set them to replicate across the network.",
#                 "Use the 'Listen Server' or 'Dedicated Server' approach to host your game.",
#                 "Call the 'Create Session' and 'Find Sessions' nodes/functions to manage connections between clients."
#             ],
#             "code_snippet": """
# // This is a basic C++ function to create a new session in Unreal Engine.
# // It is part of the Online Subsystem and requires proper configuration.

# void UYourGameInstance::HostGame()
# {
#     IOnlineSubsystem* Subsystem = IOnlineSubsystem::Get();
#     if (Subsystem)
#     {
#         IOnlineSessionPtr SessionInterface = Subsystem->GetSessionInterface();
#         if (SessionInterface.IsValid())
#         {
#             FOnlineSessionSettings SessionSettings;
#             SessionSettings.bIsDedicated = false;
#             SessionSettings.bShouldAdvertise = true;
#             SessionSettings.bIsLANMatch = true;
#             SessionSettings.NumPublicConnections = 4;

#             SessionInterface->CreateSession(0, NAME_GameSession, SessionSettings);
#         }
#     }
# }
# """,
#             "gotchas": [
#                 "All multiplayer-related code must be placed in a 'Replicated' actor or component to sync across the network.",
#                 "Be aware of the difference between a 'Listen Server' (player hosts) and a 'Dedicated Server' (server hosts).",
#                 "Firewall settings can block player connections. Ensure ports are open for testing."
#             ]
#         }
#     elif "shader" in query.lower():
#         return {
#             "platform": "ARCore/ARKit",
#             "topic": "AR Occlusion",
#             "difficulty": "Advanced",
#             "docs_link": "https://developers.google.com/ar/develop/unity/depth/occlusion",
#             "steps": [
#                 "Ensure your AR device supports a depth API (e.g., ARCore's Depth API).",
#                 "Obtain the depth map from the AR camera. This is often a texture provided by the AR framework.",
#                 "Write a custom shader that uses the depth map to compare the virtual object's depth with the real world's depth.",
#                 "If a real-world object's pixel is closer than the virtual object's pixel, discard the virtual object's pixel.",
#                 "Apply this shader to your virtual object's material."
#             ],
#             "code_snippet": """
# // This is a simplified GLSL shader for AR occlusion.
# // It assumes you have a depth texture (`_CurrentDepthTexture`) and an AR camera's projection matrix.

# Shader "Custom/AROcclusionShader"
# {
#     Properties
#     {
#         _MainTex ("Texture", 2D) = "white" {}
#     }
#     SubShader
#     {
#         Pass
#         {
#             CGPROGRAM
#             #pragma vertex vert
#             #pragma fragment frag
#             #include "UnityCG.cginc"

#             sampler2D _MainTex;
#             sampler2D _CurrentDepthTexture;

#             struct appdata
#             {
#                 float4 vertex : POSITION;
#                 float2 uv : TEXCOORD0;
#             };

#             struct v2f
#             {
#                 float2 uv : TEXCOORD0;
#                 float4 vertex : SV_POSITION;
#             };

#             v2f vert (appdata v)
#             {
#                 v2f o;
#                 o.vertex = UnityObjectToClipPos(v.vertex);
#                 o.uv = v.uv;
#                 return o;
#             }

#             fixed4 frag (v2f i) : SV_Target
#             {
#                 // Get the depth from the real world (from the depth texture)
#                 float realWorldDepth = tex2D(_CurrentDepthTexture, i.uv).r;

#                 // Get the depth of the virtual object at this pixel
#                 float virtualObjectDepth = i.vertex.z;

#                 // If the real world is closer, discard the virtual object's pixel
#                 if (realWorldDepth < virtualObjectDepth)
#                 {
#                     discard;
#                 }

#                 fixed4 col = tex2D(_MainTex, i.uv);
#                 return col;
#             }
#             ENDCG
#         }
#     }
# }
# """,
#             "gotchas": [
#                 "Depth maps are often low-resolution and can be noisy, leading to imperfect occlusion.",
#                 "Make sure your AR framework and hardware support the Depth API.",
#                 "The shader logic might need to be adjusted based on the specific depth map format (e.g., LDR vs HDR)."
#             ]
#         }
#     else:
#         return None

# def display_response(response):
#     """Parses and displays the structured JSON response."""
#     st.markdown("---")
#     st.header("2. AI-Generated Solution")
    
#     # Basic info
#     st.markdown(f"**Platform:** `{response.get('platform', 'N/A')}` | **Difficulty:** `{response.get('difficulty', 'N/A')}`")
#     st.markdown(f"**Topic:** `{response.get('topic', 'N/A')}`")
#     st.link_button("View Official Docs", url=response.get('docs_link', '#'), type="secondary")

#     # Steps
#     st.subheader("Subtasks")
#     steps = response.get("steps", [])
#     if steps:
#         for i, step in enumerate(steps):
#             st.markdown(f"**{i+1}.** {step}")
#     else:
#         st.warning("No subtasks provided.")

#     # Code Snippet
#     st.subheader("Code Snippet")
#     code = response.get("code_snippet", "")
#     if code:
#         # Infer language for syntax highlighting
#         lang = "csharp" if "unity" in response.get("platform", "").lower() else "cpp" if "unreal" in response.get("platform", "").lower() else "glsl"
#         st.code(code, language=lang)
#     else:
#         st.warning("No code snippet provided.")

#     # Gotchas
#     st.subheader("Gotchas & Best Practices")
#     gotchas = response.get("gotchas", [])
#     if gotchas:
#         for gotcha in gotchas:
#             st.info(f"💡 {gotcha}")
#     else:
#         st.info("No specific pitfalls or best practices to highlight.")

#     # Raw JSON Expander
#     with st.expander("Show Raw JSON Output"):
#         st.json(response)

# if st.button("Generate Code", use_container_width=True, type="primary"):
#     if not st.session_state.query.strip():
#         st.warning("Please select a valid demo query or enter a query.")
#     else:
#         with st.spinner("Generating your response..."):
#             response = get_placeholder_response(st.session_state.query)
#             if response:
#                 display_response(response)
#             else:
#                 st.warning("Please select a valid demo query or enter a query.")

# st.markdown("---")
# st.markdown("""
# <style>
#     .stButton>button {
#         width: 100%;
#         margin-bottom: 10px;
#     }
# </style>
# """, unsafe_allow_html=True)





import streamlit as st
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import time

# --- Streamlit UI Layout ---
# THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(layout="wide", page_title="CodeXR: AI Coding Assistant")

# --- Load Environment Variables and Configure Gemini API ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Define the JSON Schemas for structured output ---
CODE_GEN_SCHEMA = {
    "type": "object",
    "properties": {
        "platform": {"type": "string", "description": "The development platform (e.g., 'Unity', 'Unreal Engine', 'Shader')."},
        "topic": {"type": "string", "description": "A brief, descriptive topic of the solution."},
        "steps": {
            "type": "array",
            "items": {"type": "string"},
            "description": "A list of clear, step-by-step instructions for the developer."
        },
        "code_snippet": {"type": "string", "description": "A ready-to-paste code snippet with comments."},
        "gotchas": {
            "type": "array",
            "items": {"type": "string"},
            "description": "A list of common pitfalls or best practices."
        },
        "difficulty": {"type": "string", "enum": ["Easy", "Medium", "Hard"], "description": "The difficulty level of the task."},
        "docs_link": {"type": "string", "description": "A direct URL to relevant official documentation."}
    },
    "required": ["platform", "topic", "steps", "code_snippet", "gotchas", "difficulty", "docs_link"]
}

DEBUG_SCHEMA = {
    "type": "object",
    "properties": {
        "error_type": {"type": "string", "description": "The specific name of the error (e.g., 'NullReferenceException', 'Access Violation')."},
        "platform": {"type": "string", "description": "The development platform (e.g., 'Unity', 'Unreal Engine')."},
        "likely_cause": {"type": "string", "description": "A concise explanation of the most likely cause of the error."},
        "solution_steps": {
            "type": "array",
            "items": {"type": "string"},
            "description": "A list of clear, actionable steps to fix the error."
        },
        "fixed_code_snippet": {"type": "string", "description": "The corrected or recommended code snippet, if applicable. Can be empty if the fix is not code-based."}
    },
    "required": ["error_type", "platform", "likely_cause", "solution_steps"]
}

# --- Load the RAG Vector Store and Metadata ---
@st.cache_resource
def load_rag_assets():
    """Loads the FAISS index and metadata for RAG."""
    try:
        index = faiss.read_index("vector_store/docs.index")
        with open("vector_store/metadata.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        return index, metadata, model
    except FileNotFoundError:
        st.error("RAG assets not found. Please run `vectorize_and_store.py` first.")
        return None, None, None

index, metadata, embed_model = load_rag_assets()

# --- Streamlit UI Components ---
st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 3.5rem; font-weight: bold; background: linear-gradient(to right, #8b5cf6, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            CodeXR
        </h1>
        <p style="font-size: 1.25rem; color: #a1a1aa;">
            Your AI coding partner for AR/VR development.
        </p>
    </div>
    <hr style="border: 1px solid #3f3f46;"/>
""", unsafe_allow_html=True)

# --- Mode Selection ---
st.header("1. Choose a Mode")
mode = st.radio(
    "Select the task:",
    ('Code Generation', 'Error Debugging'),
    horizontal=True,
    key='mode'
)

# --- Input Area based on Mode ---
if mode == 'Code Generation':
    st.header("2. Input Query")
    if 'query' not in st.session_state:
        st.session_state.query = ""
    query_input = st.text_area(
        "Enter your AR/VR development question:",
        height=150,
        placeholder="e.g., How do I add teleport locomotion in Unity VR?",
        value=st.session_state.query,
        key='code_query'
    )
    # --- Demo Scenarios ---
    st.markdown("### Or try one of our demo queries:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Unity: Teleport Locomotion"):
            st.session_state.query = "How do I add teleport locomotion in Unity VR?"
            st.rerun()
    with col2:
        if st.button("Unreal: Multiplayer Setup"):
            st.session_state.query = "How do I set up multiplayer in Unreal VR?"
            st.rerun()
    with col3:
        if st.button("Shader: AR Occlusion"):
            st.session_state.query = "Which shader works best for AR occlusion?"
            st.rerun()
    user_input = st.session_state.query
    submit_button_label = "Generate Code"
    
elif mode == 'Error Debugging':
    st.header("2. Input Error Log")
    user_input = st.text_area(
        "Paste your error message or log here:",
        height=200,
        placeholder="e.g., NullReferenceException: Object reference not set to an instance of an object...",
        key='error_log'
    )
    st.header("3. (Optional) Paste Code Snippet")
    code_snippet = st.text_area(
        "Paste the relevant code snippet:",
        height=200,
        placeholder="e.g., myObject.transform.position = newPos;",
        key='code_snippet'
    )
    user_input += "\n\n<Code Snippet>\n" + code_snippet + "\n</Code Snippet>"
    submit_button_label = "Find Solution"

# --- Functions for Dynamic Response (Gemini API) ---

def get_gemini_response(user_input, mode, max_retries=3):
    """
    Sends the user query/error to the Gemini model with a mode-specific prompt.
    """
    if index is None or metadata is None or embed_model is None:
        st.error("RAG system is not loaded. Please check the vector store files.")
        return None

    model = genai.GenerativeModel(
        'gemini-1.5-flash',
        generation_config={"response_mime_type": "application/json"}
    )
    
    # RAG - Search for relevant documentation
    query_embedding = embed_model.encode([user_input])
    D, I = index.search(np.array(query_embedding).astype('float32'), k=3)
    
    context = ""
    for i in I[0]:
        context += metadata[i]['text'] + "\n---\n"
    
    if mode == 'Code Generation':
        system_instruction = f"""
        You are CodeXR, an AI-powered coding assistant for AR/VR developers. Your task is to provide a comprehensive, step-by-step solution for a given AR/VR development query. Your response must be in a strict JSON format.

        Use the provided documentation context below to inform your answer. If the documentation does not contain the answer, you can use your own knowledge.

        <Documentation Context>
        {context}
        </Documentation Context>

        - Decompose the request into manageable subtasks.
        - Provide a complete and ready-to-paste code snippet.
        - Highlight common pitfalls, gotchas, and best practices.
        - Determine the difficulty level of the task.
        - Include a link to relevant official documentation.

        The response MUST conform to the following JSON schema:
        """
        json_schema_str = json.dumps(CODE_GEN_SCHEMA, indent=2)

    elif mode == 'Error Debugging':
        system_instruction = f"""
        You are an expert AR/VR debugging assistant. Your task is to analyze a provided error log and code snippet (if available) to diagnose the problem and provide a clear solution. Your response must be in a strict JSON format.

        Use the provided documentation context below to inform your answer. If the documentation does not contain the answer, you can use your own knowledge.

        <Documentation Context>
        {context}
        </Documentation Context>

        - Analyze the error log and code to identify the likely cause.
        - Provide a clear, actionable plan to fix the error.
        - Provide a corrected or recommended code snippet if the solution involves a code change.

        The response MUST conform to the following JSON schema:
        """
        json_schema_str = json.dumps(DEBUG_SCHEMA, indent=2)

    full_prompt = (
        f"{system_instruction}\n"
        f"```json\n{json_schema_str}\n```\n\n"
        f"Developer Input: {user_input}\n\n"
        "Respond ONLY with the JSON object. Do not include any additional text, explanations, or markdown outside the JSON."
    )

    for attempt in range(max_retries):
        try:
            response = model.generate_content(full_prompt)
            response_text = response.text.strip()
            
            with st.expander(f"Show Raw API Response (Attempt {attempt + 1})"):
                st.code(response_text, language='json')
                
            start_index = response_text.find('{')
            end_index = response_text.rfind('}')
            
            if start_index != -1 and end_index != -1:
                json_string = response_text[start_index:end_index + 1]
                return json.loads(json_string)
            else:
                raise ValueError("AI response does not contain a valid JSON object.")

        except (json.JSONDecodeError, ValueError) as e:
            st.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {2 ** attempt} seconds...")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
        except Exception as e:
            st.error(f"An unexpected error occurred during API call: {e}")
            return None

    st.error(f"All {max_retries} attempts to get a valid response failed.")
    st.warning("Please check your API key, your quota, and try a different query.")
    return None

def display_response(response):
    """Parses and displays the structured JSON response based on the response type."""
    st.markdown("---")
    st.header("2. AI-Generated Solution")
    
    # Check for the presence of keys from the CODE_GEN_SCHEMA
    if "platform" in response and "difficulty" in response:
        # Display as a Code Generation response
        st.markdown(f"**Platform:** `{response.get('platform', 'N/A')}` | **Difficulty:** `{response.get('difficulty', 'N/A')}`")
        st.markdown(f"**Topic:** `{response.get('topic', 'N/A')}`")
        st.link_button("View Official Docs", url=response.get('docs_link', '#'), type="secondary")

        st.subheader("Subtasks")
        steps = response.get("steps", [])
        if steps:
            for i, step in enumerate(steps):
                st.markdown(f"**{i+1}.** {step}")
        else:
            st.warning("No subtasks provided.")

        st.subheader("Code Snippet")
        code = response.get("code_snippet", "")
        if code:
            lang = "csharp" if "unity" in response.get("platform", "").lower() else "cpp" if "unreal" in response.get("platform", "").lower() else "glsl"
            st.code(code, language=lang)
        else:
            st.warning("No code snippet provided.")

        st.subheader("Gotchas & Best Practices")
        gotchas = response.get("gotchas", [])
        if gotchas:
            for gotcha in gotchas:
                st.info(f"💡 {gotcha}")
        else:
            st.info("No specific pitfalls or best practices to highlight.")

    # Check for the presence of keys from the DEBUG_SCHEMA
    elif "error_type" in response and "likely_cause" in response:
        # Display as a Debugging response
        st.markdown(f"**Error Type:** `{response.get('error_type', 'N/A')}` | **Platform:** `{response.get('platform', 'N/A')}`")
        st.markdown(f"**Likely Cause:** {response.get('likely_cause', 'N/A')}")
        
        st.subheader("Solution Steps")
        solution_steps = response.get("solution_steps", [])
        if solution_steps:
            for i, step in enumerate(solution_steps):
                st.markdown(f"**{i+1}.** {step}")
        else:
            st.warning("No solution steps provided.")

        st.subheader("Fixed Code Snippet")
        code = response.get("fixed_code_snippet", "")
        if code:
            lang = "csharp" if "unity" in response.get("platform", "").lower() else "cpp" if "unreal" in response.get("platform", "").lower() else "glsl"
            st.code(code, language=lang)
        else:
            st.info("The solution does not require a code change or a specific snippet was not provided.")

    else:
        st.error("Unsupported response format from the model.")
        
    with st.expander("Show Raw JSON Output"):
        st.json(response)


# --- Main Logic ---
st.markdown("---")
if st.button(submit_button_label, use_container_width=True, type="primary"):
    if not user_input.strip():
        st.warning("Please enter some text in the input area.")
    else:
        with st.spinner("Generating your response..."):
            response = get_gemini_response(user_input, mode)
            if response:
                display_response(response)

st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)