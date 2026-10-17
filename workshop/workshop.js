(() => {
  'use strict';
  const form = document.getElementById('w-planner-form');
  if (!form) return;
  const result = document.getElementById('w-plan-result');
  const reflectionInputs = ['w-challenge', 'w-action', 'w-when'].map((id) => document.getElementById(id));
  reflectionInputs.forEach((input) => input.addEventListener('input', () => input.setCustomValidity('')));
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    reflectionInputs.forEach((input) => {
      input.setCustomValidity(input.value.trim() ? '' : 'Add a few words to make your next move clear.');
    });
    if (!form.reportValidity()) return;
    const values = [
      ['w-challenge', 'w-output-challenge'],
      ['w-action', 'w-output-action'],
      ['w-when', 'w-output-when']
    ];
    for (const [inputId, outputId] of values) {
      document.getElementById(outputId).textContent = document.getElementById(inputId).value.trim();
    }
    result.hidden = false;
    result.focus({ preventScroll: true });
    result.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'center' });
  });
  window.addEventListener('afterprint', () => document.body.classList.remove('w-printing-plan'));
  document.getElementById('w-print-plan').addEventListener('click', () => {
    document.body.classList.add('w-printing-plan');
    window.print();

  });
})();
