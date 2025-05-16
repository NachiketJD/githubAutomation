import subprocess
import time

input_code = """function hello() {
  console.log("Hello World");
}
"""

output_file = "main.js"

# Start with an empty file
with open(output_file, "w") as f:
    pass

buffer = ""

for i, char in enumerate(input_code):
    with open(output_file, "a") as f:
        f.write(char)
    buffer += char

    # Every 5 characters or at the end
    if len(buffer) == 5 or i == len(input_code) - 1:
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Add: {repr(buffer)}"], check=True)
            subprocess.run(["git", "push"], check=True)
            print(f"Committed: {repr(buffer)}")
        except subprocess.CalledProcessError as e:
            print(f"Git error: {e}")
            break
        buffer = ""
        # Optional: time.sleep(1)  # Add delay if needed
