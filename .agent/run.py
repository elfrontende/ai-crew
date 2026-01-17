import os
import sys
import yaml
import litellm
from typing import Optional, List, Any, Dict
from dotenv import load_dotenv
import warnings

# Suppress warnings from dependencies (like Pydantic/HTTPX deprecations)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
# Specific httpx suppression
warnings.filterwarnings("ignore", module="httpx")
warnings.filterwarnings("ignore", message="Use 'content=<...>' to upload raw bytes/text content")

# CrewAI imports
from crewai import Agent, Task, Crew, Process, LLM

# Tools
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tools.aider_proxy import execute_code_change

# Load Environment Variables
load_dotenv()

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'configs', 'agents.yaml')
TECH_STACK_PATH = os.path.join(BASE_DIR, 'configs', 'tech_stack.yaml')

# Enable Litellm callbacks for logging (optional, we'll do visible printing manually)
litellm.success_callback = []
litellm.failure_callback = []

# --- UTILITIES ---

def prune_context(text: str, max_chars: int = 10000) -> str:
    """
    Truncates text to a maximum length to save tokens.
    Keeps the beginning and the end, which are usually most important.
    """
    if len(text) <= max_chars:
        return text
    
    half = max_chars // 2
    return text[:half] + "\n...[CONTENT PRUNED FOR COST OPTIMIZATION]...\n" + text[-half:]



# Global cost accumulator
total_session_cost = 0.0

def track_cost_callback(kwargs, completion_response, start_time, end_time):
    """
    Global LiteLLM success callback to track and print costs.
    """
    global total_session_cost
    try:
        cost = litellm.completion_cost(completion_response)
        total_session_cost += cost
        if cost > 0:
            print(f"\033[92m[$$] Cost: ${cost:.6f} | Session Total: ${total_session_cost:.6f}\033[0m")
    except Exception:
        pass

litellm.success_callback = [track_cost_callback]


# --- SMART ROUTER ---

def get_smart_llm(complexity: str = 'low'):
    """
    Returns a CrewAI LLM configured for the given complexity level.
    Implements Smart Routing logic.
    """
    
    # Routing Logic
    if complexity == 'high':
        # Primary: GPT-4o for complex tasks
        model_name = "openai/gpt-4o"
        temperature = 0.1
    else:
        # Low Complexity: GPT-4o-mini for fast, cheap tasks
        # (Switched from Gemini due to free tier rate limits)
        model_name = "openai/gpt-4o-mini"
        temperature = 0.3

    print(f"\033[94m[Router] Initializing {complexity.upper()} agent with {model_name}\033[0m")

    # Create CrewAI native LLM instance
    llm = LLM(
        model=model_name,
        temperature=temperature,
        max_retries=2,
    )
    
    return llm

# --- AGENT FACTORY ---

def create_agent_from_config(agent_key: str, agents_config: Dict) -> Agent:
    conf = agents_config.get(agent_key)
    if not conf:
        raise ValueError(f"Agent {agent_key} not found in config")
    
    complexity = conf.get('complexity', 'low')
    
    # Construct System Prompt with caching enabled (simulated by structure)
    # Gemini supports caching if content > 32k tokens usually, but strictly speaking 
    # we just pass the role/backstory to CrewAI.
    backstory_pruned = prune_context(conf.get('backstory', ''))
    
    return Agent(
        role=conf['role'],
        goal=conf['goal'],
        backstory=backstory_pruned,
        verbose=True,
        llm=get_smart_llm(complexity),
        allow_delegation=False,
        max_iter=50, # Effectively unlimited
        max_execution_time=None, # Unlimited execution time
        tools=[aider_tool_instance] if agent_key in ['developer', 'qa_engineer'] else []
    )

# --- MAIN EXECUTION ---

def load_agents_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

def run_smart_crew(task_description: str):
    config = load_agents_config()
    
    # Instantiate Agents using Factory
    pm_agent = create_agent_from_config('product_manager', config)
    arch_agent = create_agent_from_config('architect', config)
    dev_agent = create_agent_from_config('developer', config)
    qa_agent = create_agent_from_config('qa_engineer', config)
    
    # Ensure specs directory
    os.makedirs("docs/specs", exist_ok=True)
    
    # --- DEFINE TASKS ---
    
    # 1. PM Analysis
    spec_task = Task(
        description=f"Analyze Request: '{prune_context(task_description)}'. Create detailed Feature Spec.",
        expected_output="Markdown Feature Spec with Acceptance Criteria.",
        agent=pm_agent,
        output_file="docs/specs/feature_spec.md"
    )
    
    # 2. Architecture
    plan_task = Task(
        description="Create technical implementation plan based on Feature Spec.",
        expected_output="JSON/Markdown File Logic & Schema.",
        agent=arch_agent,
        context=[spec_task],
        output_file="docs/specs/implementation_plan.md"
    )
    
    # 3. Development
    dev_task = Task(
        description="Implement code in src/ based on the Plan. You MUST use Aider to edit files. You MUST modify App.tsx to include the new features. Do not stop until the code is fully implemented and compiled.",
        expected_output="Source code execution logs.",
        agent=dev_agent,
        context=[plan_task, spec_task]
    )
    
    # 4. QA
    qa_task = Task(
        description="Write and run Vitest tests. Fix if failed.",
        expected_output="Test Results Log.",
        agent=qa_agent,
        context=[dev_task]
    )
    
    # --- CREW ---
    crew = Crew(
        agents=[pm_agent, arch_agent, dev_agent, qa_agent],
        tasks=[spec_task, plan_task, dev_task, qa_task],
        process=Process.sequential,
        verbose=True
    )
    
    print("\n\033[95m[Crew] Launching Smart Agent Workflow...\033[0m")
    result = crew.kickoff()
    
    return result

# --- ENTRY POINT ---

if __name__ == "__main__":
    aider_tool_instance = execute_code_change
    
    # Check for TZ.txt or create dummy
    tz_file = "TZ.txt"
    if not os.path.exists(tz_file):
        with open(tz_file, "w") as f:
            f.write("Print 'Hello, World!' to console.")
            
    with open(tz_file, "r") as f:
        user_request = f.read()
        
    final_output = run_smart_crew(user_request)
    
    print(f"\n\n\033[92m[DONE] Final Session Cost: ${total_session_cost:.6f}\033[0m")
    
    # Archiving Logic
    import datetime
    import shutil
    import re
    
    archive_dir = "tasks/archive"
    os.makedirs(archive_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_topic = re.sub(r'[^a-zA-Z0-9]', '_', user_request[:30])
    shutil.move(tz_file, os.path.join(archive_dir, f"{timestamp}_{safe_topic}.txt"))
    
    with open(tz_file, "w") as f:
        f.write("Enter next task...")