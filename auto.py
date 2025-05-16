import subprocess

input_code = """function hello() {
  console.log("Hello World");
}
"""

output_file = "main.js"
with open(output_file, "w") as f:
    pass

buffer = ""

for i, char in enumerate(input_code):
    with open(output_file, "a") as f:
        f.write(char)
    buffer += char

    if len(buffer) == 5 or i == len(input_code) - 1:
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Add: {repr(buffer)}"], check=True)
            # Try normal push first
            try:
                subprocess.run(["git", "push"], check=True)
            except subprocess.CalledProcessError:
                # Set upstream only once if needed
                subprocess.run(["git", "push", "--set-upstream", "origin", "master"], check=True)
            print(f"Committed: {repr(buffer)}")
        except subprocess.CalledProcessError as e:
            print(f"Git error: {e}")
        buffer = ""
