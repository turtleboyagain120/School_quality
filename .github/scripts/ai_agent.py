import os
import subprocess
from openai import OpenAI

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing: {command}\n{result.stderr}")
    return result.stdout.strip()

def main():
    # 1. Initialize the OpenAI Brain
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # 2. Gather modified files or target files (e.g., all Python files)
    print("Reading repository files...")
    target_file = "src/main.py"  # Change this to your main development file
    
    if not os.path.exists(target_file):
        print(f"Target file {target_file} not found. Skipping.")
        return

    with open(target_file, "r") as f:
        code_content = f.read()

    # 3. Prompt the AI to analyze, fix bugs, and return ONLY the pure code
    print("Communicating with AI brain...")
    response = client.chat.completions.create(
        model="gpt-4o",  # Uses robust analytical model
        messages=[
            {"role": "system", "content": "You are an expert developer. Analyze the provided code for bugs, logic errors, or inefficiencies. Output the completely fixed, working file. Do NOT include markdown blocks, explanations, or backticks. Output raw code only."},
            {"role": "user", "content": f"Review and patch this code:\n\n{code_content}"}
        ],
        temperature=0.2
    )
    
    patched_code = response.choices[0].message.content.strip()

    # 4. Write the AI's patches directly back over the file
    print("Applying AI patches to codebase...")
    with open(target_file, "w") as f:
        f.write(patched_code)

    # 5. Use your PAT authorization to stage, commit, and push back to main
    print("Pushing AI modifications back to GitHub...")
    run_command("git config --global user.name 'AI-Automation-Bot'")
    run_command("git config --global user.email 'ai-bot@internal.automation'")
    run_command(f"git add {target_file}")
    
    # Only commit if changes actually occurred
    status = run_command("git status --porcelain")
    if status:
        run_command("git commit -m '🤖 AI automated optimization and bug patch'")
        run_command("git push origin main")
        print("✅ Code successfully analyzed, patched, and pushed!")
    else:
        print("✅ AI reviewed the code: No bugs found. No changes needed.")

if __name__ == "__main__":
    main()
