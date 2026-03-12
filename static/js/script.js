// services.js

function loadServicesFromDOM() {
  return Array.from(document.querySelectorAll('#servicesData .service-data')).map(el => ({
    categories: el.dataset.categories.split(','),
    title:      el.dataset.title,
    desc:       el.dataset.desc,
    iconId:     el.dataset.iconId,
  }));
}

const allServices = loadServicesFromDOM();
let currentTab    = 'imoveis';

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

  document.getElementById('tabTitle').textContent     = query ? `"${query}"` : (tabLabels[tab] || tab);
  document.getElementById('contentCount').textContent = `${filtered.length} serviço${filtered.length !== 1 ? 's' : ''}`;

  list.innerHTML = '';

  if (filtered.length === 0) {
    list.innerHTML = '<p style="padding:32px 0;color:#6b7585;font-size:14px;">Nenhum serviço encontrado.</p>';
    return;
  }

  filtered.forEach((s, i) => {
    const card = document.createElement('a');
    card.href      = '#';
    card.className = 'service-card';
    card.innerHTML = `
      <div class="service-icon">
        <svg width="20" height="20"><use href="#${s.iconId}"/></svg>
      </div>
      <span class="service-title">${s.title}</span>
      <span class="service-arrow">→</span>
    `;
    card.addEventListener('click', e => {
      e.preventDefault();
      openServiceModal(s);
    });
    list.appendChild(card);
  });
}

// ─── TABS DESKTOP ───
function setTab(btn, tab) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  currentTab = tab;
  clearSearch();
  renderServices(tab);
}

// ─── TABS MOBILE ───
function setTabMobile(item, tab, label) {
  document.querySelectorAll('.dropdown-item').forEach(i => i.classList.remove('active'));
  item.classList.add('active');
  document.getElementById('catDropdownLabel').textContent = label;
  currentTab = tab;
  clearSearch();
  renderServices(tab);
}

// ─── SEARCH ───
function filterServices(query) {
  renderServices(query ? 'todos' : currentTab, query);
}

function clearSearch() {
  const d = document.getElementById('searchInput');
  const m = document.getElementById('searchInputMobile');
  if (d) d.value = '';
  if (m) m.value = '';
}

// ─── MODAL SERVIÇO ───
function openServiceModal(service) {
  document.getElementById('modalServiceTitle').textContent = service.title;
  document.getElementById('modalServiceDesc').textContent  = service.desc;
  document.querySelectorAll('#modalService input').forEach(i => i.value = '');
  const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalService'));
  modal.show();
}

// ─── INIT ───
renderServices('imoveis');