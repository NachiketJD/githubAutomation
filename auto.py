import subprocess

input_code = """function greet(name) {
  const message = `Hello, ${name}! Welcome to the system.`;
  console.log(message);
}

function sum(a, b) {
  return a + b;
}

function isEven(n) {
  return n % 2 === 0;
}

for (let i = 0; i < 10; i++) {
  console.log(i, isEven(i) ? "Even" : "Odd");
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
