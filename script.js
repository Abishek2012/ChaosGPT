const display = document.querySelector('#display');
const historyLine = document.querySelector('#history');
const keys = document.querySelectorAll('.key');

let expression = '';
let justCalculated = false;

const operators = new Set(['+', '-', '*', '/', '%']);
const visibleOperators = { '*': '×', '/': '÷', '-': '−' };

function prettify(value) {
  return value.replace(/[*/-]/g, (operator) => visibleOperators[operator] || operator);
}

function updateDisplay(message = '') {
  display.textContent = expression ? prettify(expression) : '0';
  historyLine.textContent = message || (expression ? 'Typing…' : 'Ready');
}

function appendValue(value) {
  if (justCalculated && !operators.has(value)) {
    expression = '';
  }

  justCalculated = false;
  const last = expression.at(-1);

  if (value === '.' && expression.split(/[+\-*/%]/).at(-1).includes('.')) return;
  if (operators.has(value) && (!expression || operators.has(last))) {
    expression = expression.slice(0, -1) + value;
  } else {
    expression += value;
  }

  updateDisplay();
}

function calculate() {
  if (!expression || operators.has(expression.at(-1))) return;

  try {
    const sanitized = expression.replace(/%/g, '/100');
    const total = Function(`"use strict"; return (${sanitized})`)();

    if (!Number.isFinite(total)) throw new Error('Invalid calculation');

    const rounded = Number.parseFloat(total.toFixed(10)).toString();
    historyLine.textContent = `${prettify(expression)} =`;
    expression = rounded;
    display.textContent = rounded;
    justCalculated = true;
  } catch {
    historyLine.textContent = 'Check the expression and try again';
    display.textContent = 'Error';
    expression = '';
    justCalculated = true;
  }
}

function clearCalculator() {
  expression = '';
  justCalculated = false;
  updateDisplay();
}

function backspace() {
  expression = expression.slice(0, -1);
  updateDisplay();
}

keys.forEach((key) => {
  key.addEventListener('click', () => {
    const { value, action } = key.dataset;
    if (action === 'clear') clearCalculator();
    if (action === 'backspace') backspace();
    if (action === 'calculate') calculate();
    if (value) appendValue(value);
  });
});

document.addEventListener('keydown', (event) => {
  if (/^[0-9.+\-*/%]$/.test(event.key)) appendValue(event.key);
  if (event.key === 'Enter' || event.key === '=') calculate();
  if (event.key === 'Backspace') backspace();
  if (event.key === 'Escape') clearCalculator();
});

updateDisplay();
