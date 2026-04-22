# 🎭 The Godfather — Interview Chatbot
### A Literary & Film Analysis Tool powered by Claude AI

Simulate interviews with Mario Puzo (author), Francis Ford Coppola (director),
a composite Literary Critic, and a Film Critic — all grounded in curated knowledge bases.

---

## 📁 Project Structure

```
godfather_chatbot/
│
├── app.py                        ← Main application (run this)
├── requirements.txt              ← Python dependencies
├── SAMPLE_INTERVIEWS.md          ← Pre-generated Q&A for the assignment
│
└── knowledge_base/
    ├── author.txt                ← Mario Puzo biography, quotes, creative process
    ├── director.txt              ← Francis Ford Coppola, casting, production
    ├── literary_critic.txt       ← Scholarly analysis of the novel
    └── film_critic.txt           ← Cinematic analysis of the 1972 film
```

---

## 🚀 Setup Instructions (Step by Step)

### Step 1 — Install Python

If you don't have Python installed:
1. Go to https://www.python.org/downloads/
2. Download the latest version (3.11 or higher recommended)
3. Run the installer — **check the box that says "Add Python to PATH"**
4. Click Install Now

To verify, open a terminal (Command Prompt on Windows, Terminal on Mac) and type:
```
python --version
```
You should see something like `Python 3.11.x`

---

### Step 2 — Get an Anthropic API Key

1. Go to https://console.anthropic.com
2. Create a free account (or sign in)
3. Click **"API Keys"** in the left sidebar
4. Click **"Create Key"**, give it a name (e.g. "Godfather Chatbot")
5. Copy the key — it starts with `sk-ant-...`
6. **Save it somewhere safe** — you won't be able to see it again

> ⚠️ Note: The Anthropic API requires a small amount of credit. You can add $5 which is more than enough for this assignment. Go to "Billing" in the console to add credit.

---

### Step 3 — Install Dependencies

Open a terminal (Command Prompt on Windows, Terminal on Mac/Linux).

Navigate to the project folder:
```bash
cd path/to/godfather_chatbot
```
(Replace `path/to/` with the actual location where you saved the folder)

Install the required packages:
```bash
pip install -r requirements.txt
```

Wait for the installation to complete (may take 1-2 minutes).

---

### Step 4 — Run the App

In the same terminal, run:
```bash
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501` with the chatbot running.

If the browser doesn't open automatically, copy that address and paste it into your browser.

---

### Step 5 — Enter Your API Key

In the sidebar on the left, you'll see a field labeled **"🔑 Anthropic API Key"**.

Paste your API key there (the `sk-ant-...` key from Step 2).

You're ready to go!

---

## 🎭 How to Use the Chatbot

1. **Select a persona** from the sidebar radio buttons:
   - ✍️ Mario Puzo (Author)
   - 🎬 Francis Ford Coppola (Director)
   - 📚 Literary Critic
   - 🎥 Film Critic

2. **Ask questions** by typing in the chat box at the bottom, OR click any of the **sample questions** in the sidebar.

3. **Switch personas** at any time using the radio buttons. The conversation resets when you switch.

4. **Clear conversation** with the "🔄 Clear Conversation" button if you want to start fresh.

---

## 📚 Expanding the Knowledge Bases

Each persona draws from a `.txt` file in the `knowledge_base/` folder.
You can add more information to any file to make the chatbot more knowledgeable.

For example, to add more information to Mario Puzo's knowledge base:
1. Open `knowledge_base/author.txt` in any text editor (Notepad, TextEdit, VS Code)
2. Add new information at the bottom — quotes, biographical facts, critical observations
3. Save the file
4. The chatbot will use the new information immediately (no restart needed)

Suggested additions:
- **author.txt**: More of Puzo's interviews, his other novels, his thoughts on Hollywood
- **director.txt**: More of Coppola's interviews, his other films, his winery and business
- **literary_critic.txt**: Specific academic papers, more feminist criticism, postcolonial readings
- **film_critic.txt**: More specific scene analysis, comparisons to other crime films, technical details

---

## 📝 Assignment Deliverable — Sample Interviews

The file `SAMPLE_INTERVIEWS.md` contains four pre-generated interview questions
with full responses — one per persona — as required by the assignment.

You can open this file in any text editor or Markdown viewer.

---

## 🔧 Troubleshooting

**"Command not found: streamlit"**
→ Try: `python -m streamlit run app.py`

**"No module named 'anthropic'"**
→ Run: `pip install anthropic` and try again

**"Invalid API key"**
→ Make sure you copied the full key including `sk-ant-` at the start

**"Knowledge base file not found"**
→ Make sure you're running the app from inside the `godfather_chatbot/` folder

**The browser doesn't open**
→ Manually go to `http://localhost:8501` in your browser

---

## 🤖 How It Works (Technical Overview)

1. The user selects a persona and types a question
2. The app loads that persona's knowledge base (`.txt` file) into memory
3. A system prompt tells Claude to roleplay as that persona, grounded in the knowledge base
4. The full conversation history is sent to the Claude API with each message
5. Claude generates a response in character, using the knowledge base as its source material
6. The response is displayed in the chat interface

The knowledge bases function as the "database" your professor referenced —
they are the curated information that the AI draws on to simulate each voice authentically.
