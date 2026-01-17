# AI-First Agent Mode Boilerplate

Welcome to the AI-First Agent Mode Boilerplate. This project is designed to be fully autonomous, with a team of AI agents (Role-Playing Agents) embedded directly into the repository to assist with planning, development, and testing.

## Tech Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: Zustand
- **Testing**: Vitest + React Testing Library
- **AI Orchestration**: CrewAI (Python)

## Project Structure

```
.
├── .agent/                 # AI Agent logic
│   ├── configs/            # Agent roles and tech stack definitions
│   ├── tools/              # Custom AI tools (e.g., Aider, Browser)
│   ├── run.py              # Main script to kickoff the agents
│   └── ...
├── src/                    # React Application Source
│   ├── components/         # UI Components
│   ├── lib/                # Utilities (cn, etc.)
│   ├── test/               # Test setup
│   └── ...
├── vite.config.ts          # Vite Configuration
├── tailwind.config.js      # Tailwind Configuration
└── ...
```

## How to Use This Project

### 1. Prerequisites

- Node.js (v18+)
- Python (v3.10+)
- OpenAI API Key (or other LLM provider)

### 2. Setup

1.  **Install JS Dependencies**:
    ```bash
    npm install
    ```
2.  **Install Python Dependencies**:

    First, install `aider` globally (recommended via pipx for speed):

    ```bash
    brew install pipx
    pipx ensurepath
    pipx install aider-chat
    ```

    Then install the agent dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

3.  **Set Environment Variables**:
    - Copy the example environment file:
      ```bash
      cp .env.example .env
      ```
    - Open `.env` and paste your OpenAI API Key:
      ```env
      OPENAI_API_KEY=sk-proj-12345...
      ```

### 3. Running the AI Crew

The AI agents are orchestrated via the `.agent/run.py` script. The default flow reads a task from `TZ.txt` (Technical Zone/Task Zone) and executes it.

1.  **Define your Task (TZ.txt)**:
    - Create a file named `TZ.txt` in the **root directory** of the project.
    - Write your task description inside.
    - _Note: This file is persistent. The agents read from it every time you run the script._

    **Handling Completed Tasks**:
    - **Automatic Archiving**: When the script finishes successfully, the `TZ.txt` file is automatically moved to `tasks/archive/YYYY-MM-DD_TaskName.txt`.
    - A new, placeholder `TZ.txt` is created for your next task.

2.  **Launch the Agents**:

    ```bash
    python3 .agent/run.py
    ```

    The agents will:
    - **Product Manager**: Analyzes your request and creates a Feature Spec.
    - **Architect**: Plans the files and structure based on the Spec.
    - **Developer**: Writes the code using Aider/Tools.
    - **QA**: Runs tests and fixes bugs.
    - **Archiving**: The task is moved to `tasks/archive/` and `TZ.txt` is reset.

### 4. Feedback & Iteration (Bugs/Changes)

Since the agents are stateless between runs (other than reading the codebase), reporting a bug is simply a **new task**.

1.  Open the freshly reset `TZ.txt`.
2.  Write your feedback:
    ```text
    The Todo List component isn't persisting to local storage correctly. Fix it.
    Also, please change the delete button color to red.
    ```
3.  Run `python .agent/run.py` again.

### 5. Developing Manually

You can still work on the project manually as a standard React app:

```bash
npm run dev
```

## Troubleshooting

- **Tests Failing**: Check `src/test/setup.ts` and ensure Vitest is configured correctly.
- **Agent Errors**: Check `.agent/configs/agents.yaml` for role definitions and ensure `tools` are correctly implemented.

---

**Happy Coding with your AI Crew!**
