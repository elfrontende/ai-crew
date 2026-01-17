# Choosing the Right AI Service

This boilerplate uses CrewAI, which is model-agnostic via LangChain. You can configure different LLMs for different agents to optimize for cost, speed, or reasoning capability.

## Where to Configure

The configuration is primarily located in `.agent/run.py`.

```python
# .agent/run.py
from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic # Example for Claude

# High-Reasoning Model (e.g., for Architect)
llm_architect = ChatOpenAI(model="gpt-4o", temperature=0.1)

# Coding Model (e.g., for Developer)
llm_developer = ChatOpenAI(model="gpt-4o", temperature=0.1)
# or use Claude 3.5 Sonnet for better coding:
# llm_developer = ChatAnthropic(model="claude-3-5-sonnet-20240620")
```

## Recommended Layout

### 1. Architect (The Planner)

**Requirement**: High reasoning, context window, and ability to follow instruction.

- **Best Choice**: `GPT-4o` or `o1-preview` (OpenAI), `Claude 3.5 Sonnet` (Anthropic).
- **Why**: Needs to understand complex requirements and split them into chunks.

### 2. Developer (The Coder)

**Requirement**: Excellent code generation, understanding of syntax, and library knowledge.

- **Best Choice**: `Claude 3.5 Sonnet` (Currently SOTA for coding), `GPT-4o`.
- **Why**: Produces fewer bugs and cleaner code.

### 3. QA Engineer (The Tester)

**Requirement**: Analytic skills, attention to detail.

- **Best Choice**: `GPT-4o` or `GPT-4-turbo`.
- **Why**: Good at analyzing logs and inferring root causes.

## Cost Optimization

For simple tasks, you can swap the **Developer** or **QA** to smaller models if the task is well-defined.

- **Cost-effective**: `Note: Llama 3 70B` (via Groq or similar) can be fast and cheap for simple logic, but might struggle with complex React patterns.

## Switching Providers

To switch providers (e.g., to Anthropic or Gemini):

1.  Install the LangChain integration package (e.g., `pip install langchain-anthropic`).
2.  Update imports in `.agent/run.py`.
3.  Set the corresponding API Key env var (e.g., `ANTHROPIC_API_KEY`).
