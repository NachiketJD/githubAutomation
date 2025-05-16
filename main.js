function greet(name) {
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
  console.log(i, isEven(i) ?