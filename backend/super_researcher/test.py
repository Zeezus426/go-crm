import subprocess
from pathlib import Path

def run_researcher(prompt: str, task_id=None):
    """
    Executes the 'adk' CLI tool with a given prompt.
    """
    working_dir = Path(__file__).resolve().parents[2]
    print("PATH: " + str(working_dir))
    command_to_run_cli = ["adk", "run", "backend/super_researcher/engine"]
    
    try:
        print(f"Starting researcher process: {' '.join(command_to_run_cli)}")
        print(f"Prompt: {prompt}")

        process = subprocess.Popen(
            command_to_run_cli,
            cwd=working_dir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send the prompt and wait for response with a timeout
        try:
            stdout, stderr = process.communicate(input=prompt, timeout=60)
            return_code = process.returncode

            print(f"Process finished with return code: {return_code}")

            if stderr:
                print("Error output:")
                print(stderr)  # Print full stderr to see what went wrong

            if return_code == 0 and stdout:
                print("Output received:")
                print(stdout[:500])  # Print first 500 chars to avoid huge output

            return {
                'stdout': stdout,
                'stderr': stderr,
                'return_code': return_code,
                'task_id': task_id  # Pass this as a parameter instead
            }
        except subprocess.TimeoutExpired:
            print("Process timed out after 60 seconds")
            process.kill()
            stdout, stderr = process.communicate()
            return {
                'stdout': stdout,
                'stderr': stderr,
                'return_code': -2,
                'task_id': task_id
            }

    except FileNotFoundError:
        error_msg = f"Error: 'adk' command was not found."
        print(error_msg)
        return {'stdout': None, 'stderr': error_msg, 'return_code': -1, 'task_id': task_id}

# Now this works:
run_researcher(prompt="You are a helpful research assistant. What is 1+1?")
