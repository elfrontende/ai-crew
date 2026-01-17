import subprocess
import os
from crewai.tools import tool
from pydantic import BaseModel, Field

# Створюємо схему вхідних даних для кращої валідації в CrewAI 1.x
class AiderToolInput(BaseModel):
    instruction: str = Field(..., description="Natural language description of what code to write/change.")
    files: str = Field(..., description="Space-separated list of file paths to edit.")

@tool("Aider_Coding_Tool")
def execute_code_change(instruction: str, files: str):
    """
    Invokes the Aider AI coding assistant to modify files based on instructions.
    Useful for implementing code, refactoring, or fixing bugs in specific files.
    """
    # Оскільки ми використовуємо pipx, 'aider' має бути просто в системному PATH.
    # Якщо ви хочете вказати конкретний шлях, можна використати зміну оточення.
    aider_command = "aider"

    command = [
        aider_command,
        "--message", instruction,
        "--yes",           # Неінтерактивний режим
        "--auto-commits",  # Авто-коміти
        "--no-dirty-commits"
    ] + files.split()

    print(f"\n\033[93m[AiderTool] Executing: {' '.join(command)}\033[0m")

    try:
        # Запускаємо Aider
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            timeout=600 
        )
        
        if result.returncode == 0:
            return f"Aider successfully executed. Output:\n{result.stdout}"
        else:
            return f"Aider failed (Exit {result.returncode}).\nError: {result.stderr}\nOutput: {result.stdout}"
            
    except FileNotFoundError:
        return "Error: 'aider' command not found. Please install it via 'pipx install aider-chat'."
    except Exception as e:
        return f"System error invoking Aider: {str(e)}"