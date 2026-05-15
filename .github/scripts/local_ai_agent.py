import os
import json
import subprocess
import urllib.request

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing: {command}\n{result.stderr}")
    return result.stdout.strip()

def query_local_ai(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen2.5-coder:1.5b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    }
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get("response", "").strip()
    except Exception as e:
        print(f"Failed to communicate with local AI: {e}")
        return None

def main():
    print("Reading repository files...")
    target_file = "src/main.py"
    
    if not os.path.exists(target_file):
        print(f"Target file {target_file} not found. Creating default buggy file to test.")
        os.makedirs("src", exist_ok=True)
        with open(target_file, "w") as f:
            f.write("def calc(a):\n    return sum(a)/len(a)\nprint(calc([]))")
        code_content = "def calc(a):\n    return sum(a)/len(a)\nprint(calc([]))"
    else:
        with open(target_file, "r") as f:
            code_content = f.read()

    system_prompt = (
        "You are an expert developer. Analyze the provided code for bugs. "
        "Output the completely fixed, working file. Do NOT include markdown blocks, explanations, or backticks. "
        f"Output raw code only.\n\nReview and patch this code:\n\n{code_content}"
    )

    print("Processing code locally using Qwen2.5-Coder...")
    patched_code = query_local_ai(system_prompt)
    
    if not patched_code:
        print("Empty or failed response from local AI. Exiting.")
        return

    if "```" in patched_code:
        lines = patched_code.splitlines()
        cleaned = [l for l in lines if not l.strip().startswith("```")]
        patched_code = "\n".join(cleaned).strip()

    print("Applying local AI patches to codebase...")
    with open(target_file, "w") as f:
        f.write(patched_code)

    print("Pushing modifications back to GitHub...")
    run_command("git config --global user.name 'Local-AI-Automation-Bot'")
    run_command("git config --global user.email 'local-ai-bot@internal.automation'")
    run_command(f"git add {target_file}")
    
    status = run_command("git status --porcelain")
    if status:
        run_command("git commit -m '🤖 Local AI offline optimization and bug patch'")
        run_command("git push origin main")
        print("✅ Code successfully analyzed, patched, and pushed locally!")
    else:
        print("✅ Local AI reviewed the code: No changes needed.")

if __name__ == "__main__":
    main()
