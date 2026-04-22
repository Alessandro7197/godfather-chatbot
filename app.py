import streamlit as st
import anthropic
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Godfather — Interview Chatbot",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #1a1206; }
    section[data-testid="stSidebar"] { background-color: #0f0b06; }
    h1 { color: #d4a843 !important; font-family: Georgia, serif !important; }
    h2, h3 { color: #c9a84c !important; font-family: Georgia, serif !important; }
    .stSidebar p, .stSidebar label, .stSidebar div { color: #c9b87a !important; }
    .stChatMessage { background-color: #241a0a !important; border: 1px solid #3d2e0f !important; }
    .stChatInputContainer { background-color: #1a1206 !important; }
    .stChatInput { background-color: #241a0a !important; color: #f0e6c8 !important; }
    p, li, span { color: #f0e6c8 !important; }
    .stButton > button {
        background-color: #3d2e0f !important;
        color: #d4a843 !important;
        border: 1px solid #6b4f1a !important;
        font-family: Georgia, serif !important;
    }
    .stButton > button:hover { background-color: #6b4f1a !important; }
    .stRadio label { color: #c9b87a !important; font-size: 0.95rem !important; }
    .stAlert { background-color: #241a0a !important; border-color: #6b4f1a !important; }
    hr { border-color: #3d2e0f !important; }
    .persona-header {
        background: linear-gradient(135deg, #241a0a, #1a1206);
        border: 1px solid #6b4f1a;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Persona definitions ───────────────────────────────────────────────────────
PERSONAS = {
    "✍️  Mario Puzo  —  Author": {
        "short_name": "Mario Puzo",
        "icon": "✍️",
        "file": "author.txt",
        "description": "Interview Mario Puzo about writing the novel, his inspirations, characters, and themes.",
        "intro": "Good evening. I'm Mario Puzo. Ask me anything about the book — why I wrote it, how I built the characters, what I really think of Coppola's film. I'll be straight with you.",
        "system": """You are Mario Puzo, author of The Godfather (1969). Speak in first person as Mario Puzo himself.
You are being interviewed about your novel, your life, your writing process, and your views on the film adaptations.
Draw on the knowledge base provided to give authentic, detailed answers that reflect Puzo's known views, personality, and experiences.
Mario Puzo was candid, self-deprecating, humorous, and frank — especially about his commercial motivations.
He was Italian-American, grew up poor in Hell's Kitchen, New York, and wrote The Godfather primarily to pay off debts.
Stay in character at all times. Speak from the perspective of your life and career up to your death in July 1999.
Use a conversational, first-person voice. Be specific and anecdotal when you can.""",
        "sample_questions": [
            "Why did you really write The Godfather?",
            "How did you create the character of Vito Corleone?",
            "Were you happy with how Coppola directed the film?",
            "Which of your books do you consider your best work?",
        ]
    },
    "🎬  Francis Ford Coppola  —  Director": {
        "short_name": "Francis Ford Coppola",
        "icon": "🎬",
        "file": "director.txt",
        "description": "Interview Coppola about directing the film, his creative decisions, and working with Puzo.",
        "intro": "Hello. I'm Francis Coppola. I have strong opinions about The Godfather — about what I was trying to do, the battles I had to fight, what it all means. Please, ask me anything.",
        "system": """You are Francis Ford Coppola, director of The Godfather (1972) and The Godfather Part II (1974).
Speak in first person as Coppola being interviewed about your films.
Draw on the knowledge base to give authentic answers reflecting Coppola's known views, decisions, and artistic vision.
Coppola is passionate, intellectual, artistic, and occasionally combative. He fought fiercely for his creative vision against Paramount.
Discuss your collaboration with Puzo, your casting choices, cinematographic decisions, and what the films mean to you.
Stay in character. Speak from the perspective of your career and known statements.""",
        "sample_questions": [
            "Why did you fight so hard to cast Marlon Brando?",
            "How did you and Puzo work together on the screenplay?",
            "What is the significance of the baptism sequence?",
            "Is The Godfather Part II better than the original?",
        ]
    },
    "📚  Literary Critic": {
        "short_name": "Literary Critic",
        "icon": "📚",
        "file": "literary_critic.txt",
        "description": "Discuss the novel's themes, literary significance, and place in American literature.",
        "intro": "Welcome. I represent a composite of critical and scholarly perspectives on Puzo's novel. I'm here to discuss The Godfather as literature — its themes, its craft, its cultural significance. What would you like to explore?",
        "system": """You are a composite literary critic and scholar specializing in American literature.
You synthesize critical studies, essays, and academic works from your knowledge base.
You analyze The Godfather as a literary work — its themes, narrative structure, character development, prose style,
and its place in American literature and culture.
Engage in a scholarly but accessible discussion. Reference specific passages, characters, and themes from the novel.
Draw on multiple critical perspectives: cultural studies, American literature, immigrant experience, genre theory, feminist criticism.
You are not a single person but a synthesis of informed critical voices.""",
        "sample_questions": [
            "What does The Godfather say about the American Dream?",
            "Is The Godfather serious literature or just popular fiction?",
            "How does Puzo use the family as a literary device?",
            "What is the significance of Michael Corleone's transformation?",
        ]
    },
    "🎥  Film Critic": {
        "short_name": "Film Critic",
        "icon": "🎥",
        "file": "film_critic.txt",
        "description": "Discuss the film's cinematography, performances, cultural impact, and why it endures.",
        "intro": "Hello. I'm here as a composite voice of film criticism on The Godfather — drawing on decades of critical writing, scholarship, and analysis of Coppola's film. Let's talk cinema. What aspect of the film interests you most?",
        "system": """You are a composite film critic and reviewer, drawing on critical studies, reviews,
and film scholarship about The Godfather (1972) and its adaptations.
You analyze the film as a cinematic work — cinematography, direction, performances, score, screenplay, and cultural impact.
Engage in thoughtful critical discussion. Reference specific scenes, technical choices, and real critics' perspectives.
Compare the film to the novel where relevant. Be enthusiastic but analytical, accessible but knowledgeable.""",
        "sample_questions": [
            "How does Gordon Willis's cinematography shape the film?",
            "Why is Brando's performance considered one of the greatest ever?",
            "How does the film compare to the novel?",
            "Why is The Godfather still considered one of the greatest films ever made?",
        ]
    },
}

# ── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_persona" not in st.session_state:
    st.session_state.current_persona = None
if "api_key" not in st.session_state:
    st.session_state.api_key = os.environ.get("ANTHROPIC_API_KEY", "")

# ── Helpers ──────────────────────────────────────────────────────────────────
def load_knowledge_base(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"[Knowledge base file '{filepath}' not found.]"


def get_claude_response(messages: list, system_prompt: str, knowledge_base: str) -> str:
    client = anthropic.Anthropic(api_key=st.session_state.api_key)
    full_system = (
        f"{system_prompt}\n\n"
        "=== KNOWLEDGE BASE ===\n"
        f"{knowledge_base}\n"
        "=== END KNOWLEDGE BASE ===\n\n"
        "Use the knowledge base to inform your responses. "
        "Be specific and stay in character."
    )
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=full_system,
        messages=messages,
    )
    return response.content[0].text

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎭 The Godfather\n### Interview Chatbot")
    st.markdown("---")

    # Only show API key input if not already set via secrets
    if not st.session_state.api_key:
        api_key_input = st.text_input(
            "🔑 Anthropic API Key",
            type="password",
            value="",
            help="Get your key at console.anthropic.com",
            placeholder="sk-ant-..."
        )
        if api_key_input:
            st.session_state.api_key = api_key_input

    st.markdown("---")
    st.markdown("### 🎭 Choose Your Subject")

    selected_persona_key = st.radio(
        "Who would you like to interview?",
        options=list(PERSONAS.keys()),
        label_visibility="collapsed",
    )

    # Reset conversation when persona changes
    if selected_persona_key != st.session_state.current_persona:
        st.session_state.current_persona = selected_persona_key
        st.session_state.messages = []
        st.rerun()

    persona = PERSONAS[selected_persona_key]

    st.markdown("---")
    st.markdown("**About:**")
    st.info(persona["description"])

    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 💡 Sample Questions")
    for q in persona["sample_questions"]:
        if st.button(f"❝ {q}", key=f"sq_{q}", use_container_width=True):
            if not st.session_state.api_key:
                st.error("Please enter your API key first.")
            else:
                with st.spinner(f"{persona['short_name']} is thinking…"):
                    st.session_state.messages.append({"role": "user", "content": q})
                    kb = load_knowledge_base(persona["file"])
                    reply = get_claude_response(
                        st.session_state.messages,
                        persona["system"],
                        kb,
                    )
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="persona-header">
        <h2 style="margin:0;">{persona['icon']} &nbsp; Now interviewing: <strong>{persona['short_name']}</strong></h2>
        <p style="margin:0.3rem 0 0 0; color:#9a8050 !important;">{persona['description']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Display chat history
if not st.session_state.messages:
    with st.chat_message("assistant", avatar=persona["icon"]):
        st.markdown(f"*{persona['intro']}*")
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar=persona["icon"]):
                st.markdown(msg["content"])

# Chat input
if not st.session_state.api_key:
    st.warning("⚠️ Please enter your **Anthropic API key** in the sidebar to begin the interview.")
else:
    if prompt := st.chat_input(f"Ask {persona['short_name']} a question…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=persona["icon"]):
            with st.spinner(f"{persona['short_name']} is thinking…"):
                kb = load_knowledge_base(persona["file"])
                reply = get_claude_response(
                    st.session_state.messages,
                    persona["system"],
                    kb,
                )
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
