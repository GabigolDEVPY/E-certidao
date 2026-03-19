function switchTab(tab) {
  const isLogin = tab === 'login';
  document.getElementById('panel-register').style.display = isLogin ? 'none' : 'block';
  document.getElementById('panel-login').style.display    = isLogin ? 'block' : 'none';
  document.getElementById('tab-register').classList.toggle('active', !isLogin);
  document.getElementById('tab-login').classList.toggle('active', isLogin);
  document.getElementById('tabIndicator').classList.toggle('at-login', isLogin);
}

function togglePass(id, btn) {
  const el = document.getElementById(id);
  if (!el) return;
  const hide = el.type === 'text';
  el.type = hide ? 'password' : 'text';
  btn.style.color = hide ? '' : 'var(--ink)';
}

switchTab('{{ active_tab|default:"register" }}');