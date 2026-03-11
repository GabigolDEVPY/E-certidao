// services.js

// ─── LEITURA DOS DADOS DO DOM ───
function loadServicesFromDOM() {
  return Array.from(document.querySelectorAll('#servicesData .service-data')).map(el => ({
    categories: el.dataset.categories.split(','),
    title:      el.dataset.title,
    desc:       el.dataset.desc,
    iconId:     el.dataset.iconId,
  }));
}

const allServices = loadServicesFromDOM();
let currentTab = 'imoveis';

const tabLabels = {
  todos:    'Todos os Serviços',
  registro: 'Registro Civil',
  imoveis:  'Imóveis',
  notas:    'Notas',
  protesto: 'Protesto',
  federais: 'Federais / Estaduais',
  pesquisa: 'Pesquisa',
  traducao: 'Tradução / Apostilamento',
};

// ─── RENDER ───
function renderServices(tab, query = '') {
  const list = document.getElementById('serviceList');

  const filtered = allServices.filter(s => {
    const matchTab   = s.categories.includes(tab);
    const q          = query.toLowerCase();
    const matchQuery = !q || s.title.toLowerCase().includes(q) || s.desc.toLowerCase().includes(q);
    return matchTab && matchQuery;
  });

  document.getElementById('tabTitle').textContent    = query ? `Resultados para "${query}"` : tabLabels[tab] || tab;
  document.getElementById('contentCount').textContent = `${filtered.length} serviço${filtered.length !== 1 ? 's' : ''}`;

  list.innerHTML = '';

  if (filtered.length === 0) {
    list.innerHTML = `<p style="padding:40px 0;color:#6b7585;font-size:14px;">Nenhum serviço encontrado.</p>`;
    return;
  }

  filtered.forEach((s, i) => {
    const card = document.createElement('a');
    card.href = '#';
    card.className = 'service-card';
    card.dataset.title = s.title;
    card.dataset.desc  = s.desc;

    card.innerHTML = `
      <span class="service-num">${String(i + 1).padStart(2, '0')}</span>
      <span class="service-title">${s.title}</span>
      <span class="service-arrow">→</span>
    `;

    card.addEventListener('click', e => {
      e.preventDefault();
      openModal('service', s);
    });

    list.appendChild(card);
  });
}

// ─── TABS ───
function setTab(btn, tab) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  currentTab = tab;
  document.getElementById('searchInput').value = '';
  renderServices(tab);
}

// ─── SEARCH ───
function filterServices(query) {
  renderServices(query ? 'todos' : currentTab, query);
}

// ─── MODAL ───
function showPanel(id) {
  document.querySelectorAll('.modal-panel').forEach(p => p.hidden = true);
  const panel = document.getElementById(`modal-${id}`);
  if (panel) panel.hidden = false;
}

function openModal(type, service = null) {
  if (type === 'service' && service) {
    document.getElementById('modal-service-title').textContent = service.title;
    document.getElementById('modal-service-desc').textContent  = service.desc;
    document.querySelectorAll('#modal-service input').forEach(i => i.value = '');
    showPanel('service');
  } else {
    showPanel(type);
  }
  document.getElementById('modalOverlay').classList.add('open');
}

function closeModal() {
  document.getElementById('modalOverlay').classList.remove('open');
}

function closeModalOutside(e) {
  if (e.target === document.getElementById('modalOverlay')) closeModal();
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});

// ─── INIT ───
renderServices('imoveis');