# 🚀 How to Use This Bootstrap for New Projects

This is an **AI-First Agent Mode Boilerplate** that sets up a fully autonomous development environment with CrewAI-powered agents (Product Manager, Architect, Developer, QA) built into your repo.

---

## Creating a New Project

### Method 1: Clone via GitHub (Recommended)

```bash
# 1. Clone the repository to a new project folder
git clone https://github.com/<your-username>/ai-crew.git my-new-project

# 2. Navigate to the new project
cd my-new-project

# 3. Remove the existing git history (for a fresh start)
rm -rf .git
git init

# 4. Update remote to your new repository
git remote add origin https://github.com/<your-username>/my-new-project.git
```

### Method 2: Copy Locally

```bash
# Copy the folder
cp -r /path/to/ai-crew ~/Developer/my-new-project

# Navigate and clean up
cd ~/Developer/my-new-project
rm -rf .git node_modules .venv dist .aider* tasks/archive/*
git init
```

### Method 3: Use as GitHub Template

1. Go to your `ai-crew` repository on GitHub
2. Click **Settings** → Check **"Template repository"**
3. Now you can click **"Use this template"** → **"Create a new repository"** to create new projects instantly

---

## Setup Steps for the New Project

### 1. Install JS Dependencies

```bash
npm install
```

### 2. Install Python Dependencies

First, install `aider` globally (if not already installed):

```bash
brew install pipx
pipx ensurepath
pipx install aider-chat
```

Then install the agent dependencies:

```bash
pip3 install -r requirements.txt
```

### 3. Set Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API key(s):

```env
# Choose one or more:
OPENAI_API_KEY=sk-proj-...
# or
GOOGLE_API_KEY=AIza...
# or
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Create Your First Task

Open/create `TZ.txt` in the root directory and describe your feature:

```text
Build a landing page with a hero section, features grid, and contact form.
```

### 5. Run the AI Crew

```bash
python3 .agent/run.py
```

---

## Project Structure

| Directory/File    | Purpose                                             |
| ----------------- | --------------------------------------------------- |
| `.agent/`         | AI Agent orchestration (configs, tools, run script) |
| `.agent/configs/` | Agent roles and tech stack definitions              |
| `.agent/tools/`   | Custom AI tools (Aider, Browser, etc.)              |
| `.agent/run.py`   | Main script to kickoff the agents                   |
| `src/`            | React application source code                       |
| `TZ.txt`          | Your task file (read by agents)                     |
| `tasks/archive/`  | Completed tasks auto-archived here                  |
| `docs/`           | Documentation and context                           |

---

## Agent Workflow

When you run `python3 .agent/run.py`, the agents execute in sequence:

1. **Product Manager** — Analyzes your request and creates a Feature Spec
2. **Architect** — Plans the files and structure based on the Spec
3. **Developer** — Writes the code using Aider/Tools
4. **QA** — Runs tests and fixes bugs
5. **Archiving** — Task is moved to `tasks/archive/` and `TZ.txt` is reset

---

## Workflow Tips

| ✅ Do                                        | ❌ Don't                                   |
| -------------------------------------------- | ------------------------------------------ |
| Write clear, detailed tasks in `TZ.txt`      | Leave `TZ.txt` empty or vague              |
| Run `python3 .agent/run.py` to execute       | Manually edit agent configs unless needed  |
| Use `npm run dev` for manual development     | Forget to set up `.env` with API keys      |
| Report bugs/changes as new tasks in `TZ.txt` | Expect agents to remember previous context |

---

## Feedback & Iteration

Since the agents are stateless between runs, reporting a bug is simply a **new task**:

1. Open the freshly reset `TZ.txt`
2. Write your feedback:
   ```text
   The Todo List component isn't persisting to local storage correctly. Fix it.
   Also, please change the delete button color to red.
   ```
3. Run `python3 .agent/run.py` again

---

## Manual Development

You can still work on the project manually as a standard React app:

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run lint     # Run linter
npm run test     # Run tests
```

---

## Troubleshooting

| Issue               | Solution                                                                           |
| ------------------- | ---------------------------------------------------------------------------------- |
| Tests Failing       | Check `src/test/setup.ts` and Vitest config                                        |
| Agent Errors        | Check `.agent/configs/agents.yaml` for role definitions                            |
| Missing API Key     | Ensure `.env` has valid `OPENAI_API_KEY`, `GOOGLE_API_KEY`, or `ANTHROPIC_API_KEY` |
| Python Dependencies | Run `pip3 install -r requirements.txt`                                             |
| Aider Not Found     | Run `pipx install aider-chat`                                                      |

---

## Quick Start Checklist

- [ ] Clone/copy the repository to a new folder
- [ ] Remove old `.git` and initialize fresh: `rm -rf .git && git init`
- [ ] Install dependencies: `npm install && pip3 install -r requirements.txt`
- [ ] Set up environment: `cp .env.example .env` and add API keys
- [ ] Clean up: remove old files from `tasks/archive/`, `dist/`, etc.
- [ ] Create your first task in `TZ.txt`
- [ ] Run `python3 .agent/run.py`

---

**Happy Coding with your AI Crew! 🤖**
