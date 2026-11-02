document.querySelectorAll('.confirm-delete').forEach(a =>
  a.addEventListener('click', e => { if (!confirm('¿Borrar este viaje?')) e.preventDefault(); }));

const plan = document.getElementById('plan');
if (plan) {
  const count = document.getElementById('count');
  const update = () => {
    count.textContent = plan.value.length;
    count.parentElement.classList.toggle('over', plan.value.length > 40);
  };
  plan.addEventListener('input', update); update();
}

const start = document.getElementById('start_date'), end = document.getElementById('end_date');
if (start && end) {
  const today = new Date().toISOString().split('T')[0];
  start.min = today;
  start.addEventListener('change', () => { end.min = start.value; });
}
