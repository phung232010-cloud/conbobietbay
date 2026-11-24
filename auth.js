// ==========================================
// AUTHENTICATION & ACCESS CONTROL SYSTEM
// Cuộc thi AI or Behind 2026-2027
// ==========================================

const DEFAULT_WHITELIST = [
  "Vương Thị Yến Nhi",
  "Nguyễn Hữu Xuân Bắc",
  "Nguyễn Minh Thắng",
  "Nguyễn Trần Trung Kiên",
  "Nguyễn Tiến Dũng"
];

const ADMIN_KEY = "Thangcyrus";

const AUTH_STATE = {
  currentUser: null, // { name, role: 'student' | 'admin', ip, loginAt }
  clientIp: 'Đang kiểm tra IP...',
  whitelist: [],
  blockedIps: new Set(),
  ipBindings: {}, // { ip: registeredName }
  isGateOpen: false
};

// --- INITIALIZE AUTH SYSTEM ---
async function initAuthSystem() {
  loadAuthStorage();
  AUTH_STATE.clientIp = await detectClientIP();
  updateAuthUI();
  checkCurrentSession();
}

function loadAuthStorage() {
  try {
    // 1. Load whitelist
    const savedWhitelist = localStorage.getItem('genai_auth_whitelist');
    if (savedWhitelist) {
      AUTH_STATE.whitelist = JSON.parse(savedWhitelist);
    } else {
      AUTH_STATE.whitelist = [...DEFAULT_WHITELIST];
      saveWhitelist();
    }

    // 2. Load blocked IPs
    const savedBlocked = localStorage.getItem('genai_auth_blocked_ips');
    if (savedBlocked) {
      AUTH_STATE.blockedIps = new Set(JSON.parse(savedBlocked));
    }

    // 3. Load IP bindings { ip: studentName }
    const savedBindings = localStorage.getItem('genai_auth_ip_bindings');
    if (savedBindings) {
      AUTH_STATE.ipBindings = JSON.parse(savedBindings);
    }

    // 4. Load saved session
    const savedSession = localStorage.getItem('genai_auth_session');
    if (savedSession) {
      AUTH_STATE.currentUser = JSON.parse(savedSession);
    }
  } catch (e) {
    console.error('Error loading auth storage:', e);
  }
}

function saveWhitelist() {
  localStorage.setItem('genai_auth_whitelist', JSON.stringify(AUTH_STATE.whitelist));
}

function saveBlockedIps() {
  localStorage.setItem('genai_auth_blocked_ips', JSON.stringify([...AUTH_STATE.blockedIps]));
}

function saveIpBindings() {
  localStorage.setItem('genai_auth_ip_bindings', JSON.stringify(AUTH_STATE.ipBindings));
}

function saveSession(userObj) {
  AUTH_STATE.currentUser = userObj;
  localStorage.setItem('genai_auth_session', JSON.stringify(userObj));
}

function clearSession() {
  AUTH_STATE.currentUser = null;
  localStorage.removeItem('genai_auth_session');
  showAuthModal();
  updateUserBadge();
}

// --- DETECT IP ADDRESS ---
async function detectClientIP() {
  let ip = '';
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2500);
    const res = await fetch('https://api.ipify.org?format=json', { signal: controller.signal });
    clearTimeout(timeoutId);
    if (res.ok) {
      const data = await res.json();
      ip = data.ip || '';
    }
  } catch (e) {
    console.log('IP lookup fallback to persistent device ID');
  }

  // Fallback if offline or blocked by browser/network
  if (!ip) {
    let localFingerprint = localStorage.getItem('genai_device_ip');
    if (!localFingerprint) {
      localFingerprint = '192.168.1.' + Math.floor(10 + Math.random() * 240);
      localStorage.setItem('genai_device_ip', localFingerprint);
    }
    ip = localFingerprint;
  }

  return ip;
}

function updateAuthUI() {
  const badge = document.getElementById('auth-ip-display');
  if (badge) badge.textContent = AUTH_STATE.clientIp;
  const blockedBadge = document.getElementById('blocked-ip-display');
  if (blockedBadge) blockedBadge.textContent = AUTH_STATE.clientIp;
}

// --- NAME NORMALIZATION HELPER ---
function normalizeName(str) {
  if (!str) return '';
  return str.trim().toLowerCase().replace(/\s+/g, ' ');
}

// --- CHECK LOGIN SESSION ---
function checkCurrentSession() {
  const ip = AUTH_STATE.clientIp;

  // Check if IP is currently blocked
  if (AUTH_STATE.blockedIps.has(ip)) {
    // If current session is admin, allow
    if (AUTH_STATE.currentUser && AUTH_STATE.currentUser.role === 'admin') {
      unlockApp();
      return;
    }
    showBlockedModal();
    return;
  }

  // If already logged in
  if (AUTH_STATE.currentUser) {
    unlockApp();
    return;
  }

  // Not logged in -> show login gate
  showAuthModal();
}

// --- HANDLE LOGIN SUBMISSION ---
function handleAuthLogin() {
  const nameInput = (document.getElementById('auth-name-input')?.value || '').trim();
  const keyInput = (document.getElementById('auth-key-input')?.value || '').trim();
  const currentIp = AUTH_STATE.clientIp;

  hideAuthError();

  // Case 1: Admin Key Login (bypasses name requirements)
  if (keyInput === ADMIN_KEY) {
    const adminUser = {
      name: nameInput || 'Quản Trị Viên (Admin)',
      role: 'admin',
      ip: currentIp,
      loginAt: new Date().toLocaleString('vi-VN')
    };
    saveSession(adminUser);
    unlockApp();
    alert('Chào mừng Quản trị viên! Bạn có toàn quyền quản lý danh sách thí sinh, mở khóa IP và điều phối hệ thống.');
    return;
  }

  // Case 2: Student Login Check
  const normInput = normalizeName(nameInput);
  if (!normInput) {
    showAuthError('Vui lòng nhập họ và tên của bạn để tiếp tục!');
    return;
  }

  // Match against whitelist
  const matchedOriginalName = AUTH_STATE.whitelist.find(w => normalizeName(w) === normInput);

  if (!matchedOriginalName) {
    // WRONG NAME -> BLOCK IP IMMEDIATELY!
    AUTH_STATE.blockedIps.add(currentIp);
    saveBlockedIps();
    showBlockedModal();
    return;
  }

  // Check IP-to-Name 1-to-1 binding rule:
  // "mỗi ip, tên thì chỉ 1 người được sử dụng thôi người khác không sử dụng được đổi thiết bị khác thì vẫn được nhé miễn ip tại nơi đó"
  const boundNameForThisIp = AUTH_STATE.ipBindings[currentIp];
  if (boundNameForThisIp && normalizeName(boundNameForThisIp) !== normInput) {
    showAuthError(`Địa chỉ IP này (${currentIp}) hiện đã được cố định cho thí sinh "${boundNameForThisIp}". Thí sinh khác không được phép sử dụng chung IP này. Vui lòng liên hệ Admin để giải phóng IP!`);
    return;
  }

  // Bind IP to this student
  AUTH_STATE.ipBindings[currentIp] = matchedOriginalName;
  saveIpBindings();

  // Save session (tự động lưu cho lần sau không cần nhập lại)
  const studentUser = {
    name: matchedOriginalName,
    role: 'student',
    ip: currentIp,
    loginAt: new Date().toLocaleString('vi-VN')
  };
  saveSession(studentUser);
  unlockApp();
}

function showAuthError(msg) {
  const el = document.getElementById('auth-error-msg');
  if (el) {
    el.textContent = msg;
    el.classList.remove('hidden');
  }
}

function hideAuthError() {
  const el = document.getElementById('auth-error-msg');
  if (el) {
    el.textContent = '';
    el.classList.add('hidden');
  }
}

// --- MODAL CONTROLS ---
function showAuthModal() {
  const overlay = document.getElementById('auth-modal-overlay');
  const modal = document.getElementById('auth-modal');
  const blocked = document.getElementById('auth-blocked-modal');
  
  if (overlay) overlay.classList.remove('hidden');
  if (modal) modal.classList.remove('hidden');
  if (blocked) blocked.classList.add('hidden');
  document.body.classList.add('overflow-hidden');

  updateAuthUI();
}

function showBlockedModal() {
  const overlay = document.getElementById('auth-modal-overlay');
  const modal = document.getElementById('auth-modal');
  const blocked = document.getElementById('auth-blocked-modal');
  
  if (overlay) overlay.classList.remove('hidden');
  if (modal) modal.classList.add('hidden');
  if (blocked) blocked.classList.remove('hidden');
  document.body.classList.add('overflow-hidden');

  updateAuthUI();
}

function unlockApp() {
  const overlay = document.getElementById('auth-modal-overlay');
  const modal = document.getElementById('auth-modal');
  const blocked = document.getElementById('auth-blocked-modal');
  
  if (overlay) overlay.classList.add('hidden');
  if (modal) modal.classList.add('hidden');
  if (blocked) blocked.classList.add('hidden');
  document.body.classList.remove('overflow-hidden');

  updateUserBadge();
}

function updateUserBadge() {
  const container = document.getElementById('user-session-badge');
  if (!container) return;

  if (!AUTH_STATE.currentUser) {
    container.innerHTML = `
      <button onclick="showAuthModal()" class="px-3 py-1.5 rounded-xl bg-blue-600 text-white font-bold text-xs hover:bg-blue-700 transition shadow-sm">
        Đăng nhập
      </button>
    `;
    return;
  }

  const u = AUTH_STATE.currentUser;
  const isAdmin = (u.role === 'admin');

  container.innerHTML = `
    <div class="flex items-center gap-2 pl-3 border-l border-slate-200 dark:border-slate-800">
      <div class="w-8 h-8 rounded-full ${isAdmin ? 'bg-amber-500 text-white shadow-amber-500/20' : 'bg-gradient-to-tr from-blue-600 to-indigo-600 text-white'} flex items-center justify-center font-black text-xs shadow-md">
        ${isAdmin ? '👑' : u.name.charAt(0)}
      </div>
      <div class="hidden sm:block text-left text-xs">
        <div class="font-extrabold text-slate-800 dark:text-slate-100 flex items-center gap-1.5 leading-tight">
          <span>${u.name}</span>
          ${isAdmin ? '<span class="px-1.5 py-0.2 rounded-full bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300 text-[10px] font-black border border-amber-300 dark:border-amber-700">ADMIN</span>' : ''}
        </div>
        <div class="text-[10px] text-slate-400 font-mono">IP: ${u.ip}</div>
      </div>
      ${isAdmin ? `
        <button onclick="openAdminPanel()" title="Bảng quản trị hệ thống" class="px-2.5 py-1 rounded-lg bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 font-bold text-xs border border-amber-200 dark:border-amber-800 hover:bg-amber-100 transition flex items-center gap-1">
          <span>⚙️ Quản trị</span>
        </button>
      ` : ''}
      <button onclick="logoutUser()" title="Đăng xuất khỏi thiết bị này" class="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400 hover:text-rose-600 transition">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
      </button>
    </div>
  `;
}

function logoutUser() {
  if (confirm('Bạn có chắc chắn muốn đăng xuất tài khoản? Lần sau đăng nhập từ IP này vẫn được hỗ trợ.')) {
    clearSession();
  }
}

// --- ADMIN BYPASS FROM BLOCKED SCREEN ---
function adminBypassFromBlocked() {
  const adminKey = prompt('Nhập mã bảo mật Quản trị viên (Admin Key) để mở khóa:');
  if (adminKey === ADMIN_KEY) {
    // Unblock this IP
    AUTH_STATE.blockedIps.delete(AUTH_STATE.clientIp);
    saveBlockedIps();
    // Log in as admin
    const adminUser = {
      name: 'Quản Trị Viên (Admin)',
      role: 'admin',
      ip: AUTH_STATE.clientIp,
      loginAt: new Date().toLocaleString('vi-VN')
    };
    saveSession(adminUser);
    unlockApp();
    alert('Đã giải phóng địa chỉ IP và đăng nhập quyền Quản trị viên thành công!');
  } else if (adminKey !== null) {
    alert('Mã bảo mật Quản trị viên không chính xác!');
  }
}

// --- ADMIN PANEL MODAL ---
function openAdminPanel() {
  const panel = document.getElementById('admin-panel-modal');
  const overlay = document.getElementById('auth-modal-overlay');
  if (!panel || !overlay) return;

  overlay.classList.remove('hidden');
  panel.classList.remove('hidden');
  renderAdminPanelContent();
}

function closeAdminPanel() {
  const panel = document.getElementById('admin-panel-modal');
  const overlay = document.getElementById('auth-modal-overlay');
  if (panel) panel.classList.add('hidden');
  if (overlay && AUTH_STATE.currentUser) {
    overlay.classList.add('hidden');
  }
}

function renderAdminPanelContent() {
  const container = document.getElementById('admin-panel-body');
  if (!container) return;

  // 1. Whitelist list
  const whitelistHtml = AUTH_STATE.whitelist.map((name, idx) => `
    <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs">
      <div class="flex items-center gap-2">
        <span class="w-5 h-5 rounded-full bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-300 flex items-center justify-center font-bold text-[10px]">${idx + 1}</span>
        <span class="font-bold text-slate-800 dark:text-slate-100">${name}</span>
      </div>
      <button class="px-2 py-1 text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40 rounded font-semibold text-xs transition" onclick="removeWhitelistName('${name}')">Xóa</button>
    </div>
  `).join('');

  // 2. Blocked IPs list
  const blockedArr = [...AUTH_STATE.blockedIps];
  const blockedHtml = blockedArr.length === 0 
    ? '<div class="text-xs text-slate-400 italic p-3 text-center bg-slate-50 dark:bg-slate-800/50 rounded-xl">Không có địa chỉ IP nào đang bị khóa.</div>'
    : blockedArr.map(ip => `
      <div class="flex items-center justify-between p-2.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 text-xs">
        <div class="flex items-center gap-2">
          <span class="text-rose-600">🚫</span>
          <span class="font-mono font-bold text-rose-700 dark:text-rose-300">${ip}</span>
        </div>
        <button class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg transition text-xs shadow-xs" onclick="unblockIp('${ip}')">
          Mở khóa IP
        </button>
      </div>
    `).join('');

  // 3. IP Bindings list
  const bindingsEntries = Object.entries(AUTH_STATE.ipBindings);
  const bindingsHtml = bindingsEntries.length === 0
    ? '<div class="text-xs text-slate-400 italic p-3 text-center bg-slate-50 dark:bg-slate-800/50 rounded-xl">Chưa có liên kết IP nào.</div>'
    : bindingsEntries.map(([ip, name]) => `
      <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs">
        <div>
          <span class="font-bold text-blue-600 dark:text-blue-400">${name}</span>
          <span class="font-mono text-slate-400 ml-2">(${ip})</span>
        </div>
        <div class="flex items-center gap-2">
          <button class="px-2 py-1 text-blue-600 hover:underline font-semibold text-xs" onclick="reassignIpBinding('${ip}')">Đổi thí sinh</button>
          <button class="px-2 py-1 text-rose-600 hover:underline font-semibold text-xs" onclick="resetIpBinding('${ip}')">Hủy liên kết</button>
        </div>
      </div>
    `).join('');

  container.innerHTML = `
    <div class="space-y-6">
      
      <!-- Top Stats Bar -->
      <div class="grid grid-cols-3 gap-3">
        <div class="p-3 rounded-2xl bg-blue-50 dark:bg-blue-950/40 border border-blue-100 dark:border-blue-900 text-center">
          <div class="text-[11px] font-bold text-blue-600 dark:text-blue-400">Thí Sinh Được Phép</div>
          <div class="text-xl font-black text-slate-800 dark:text-white">${AUTH_STATE.whitelist.length}</div>
        </div>
        <div class="p-3 rounded-2xl bg-rose-50 dark:bg-rose-950/40 border border-rose-100 dark:border-rose-900 text-center">
          <div class="text-[11px] font-bold text-rose-600 dark:text-rose-400">IP Đang Bị Khóa</div>
          <div class="text-xl font-black text-rose-600 dark:text-rose-400">${blockedArr.length}</div>
        </div>
        <div class="p-3 rounded-2xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-100 dark:border-emerald-900 text-center">
          <div class="text-[11px] font-bold text-emerald-600 dark:text-emerald-400">Liên Kết IP Đã Gán</div>
          <div class="text-xl font-black text-emerald-600 dark:text-emerald-400">${bindingsEntries.length}</div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <!-- Whitelist Manager -->
        <div class="card-glass p-5 rounded-2xl border border-slate-200 dark:border-slate-800 flex flex-col">
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-black text-sm text-slate-900 dark:text-white flex items-center gap-1.5">
              <span>📋 Danh Sách Thí Sinh</span>
              <span class="px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-300 text-xs">${AUTH_STATE.whitelist.length}</span>
            </h4>
            <button class="px-2.5 py-1 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition shadow-xs" onclick="addWhitelistName()">+ Thêm tên</button>
          </div>
          <div class="space-y-2 max-h-56 overflow-y-auto pr-1 flex-1">
            ${whitelistHtml}
          </div>
        </div>

        <!-- Blocked IPs Manager -->
        <div class="card-glass p-5 rounded-2xl border border-slate-200 dark:border-slate-800 flex flex-col">
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-black text-sm text-rose-700 dark:text-rose-400 flex items-center gap-1.5">
              <span>🚫 Danh Sách IP Bị Khóa</span>
              <span class="px-2 py-0.5 rounded-full bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300 text-xs">${blockedArr.length}</span>
            </h4>
            ${blockedArr.length > 0 ? `<button class="text-xs text-rose-600 hover:underline font-bold" onclick="unblockAllIps()">Mở khóa tất cả</button>` : ''}
          </div>
          <div class="space-y-2 max-h-56 overflow-y-auto pr-1 flex-1">
            ${blockedHtml}
          </div>
        </div>

      </div>

      <!-- IP Bindings Manager -->
      <div class="card-glass p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
        <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
          <div>
            <h4 class="font-black text-sm text-slate-900 dark:text-white">🔗 Quản Lý Liên Kết IP Với Thí Sinh (1 IP - 1 Người)</h4>
            <p class="text-[11px] text-slate-400">Admin có thể giải phóng hoặc gán bất kỳ IP nào cho thí sinh tùy ý</p>
          </div>
          <div class="flex items-center gap-2">
            <button class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-200 text-xs font-bold transition" onclick="bindCustomIp()">+ Gán IP thủ công</button>
            <button class="text-xs text-rose-600 hover:underline font-bold" onclick="clearAllBindings()">Đặt lại tất cả</button>
          </div>
        </div>
        <div class="space-y-2 max-h-56 overflow-y-auto pr-1">
          ${bindingsHtml}
        </div>
      </div>

    </div>
  `;
}

function addWhitelistName() {
  const name = prompt('Nhập họ và tên thí sinh mới cần cấp quyền vào hệ thống:');
  if (name && name.trim()) {
    const cleanName = name.trim();
    if (!AUTH_STATE.whitelist.some(w => normalizeName(w) === normalizeName(cleanName))) {
      AUTH_STATE.whitelist.push(cleanName);
      saveWhitelist();
      renderAdminPanelContent();
      alert(`Đã thêm thí sinh "${cleanName}" thành công!`);
    } else {
      alert(`Thí sinh "${cleanName}" đã có trong danh sách.`);
    }
  }
}

function removeWhitelistName(name) {
  if (confirm(`Bạn có chắc muốn xóa thí sinh "${name}" khỏi danh sách được phép? Thí sinh này sẽ không thể đăng nhập lại.`)) {
    AUTH_STATE.whitelist = AUTH_STATE.whitelist.filter(n => n !== name);
    saveWhitelist();
    renderAdminPanelContent();
  }
}

function unblockIp(ip) {
  AUTH_STATE.blockedIps.delete(ip);
  saveBlockedIps();
  renderAdminPanelContent();
  alert(`Đã mở khóa thành công cho địa chỉ IP: ${ip}`);
}

function unblockAllIps() {
  if (confirm('Bạn có chắc muốn mở khóa cho toàn bộ các địa chỉ IP đang bị chặn?')) {
    AUTH_STATE.blockedIps.clear();
    saveBlockedIps();
    renderAdminPanelContent();
    alert('Đã mở khóa toàn bộ IP!');
  }
}

function resetIpBinding(ip) {
  const name = AUTH_STATE.ipBindings[ip];
  if (confirm(`Bạn có muốn giải phóng liên kết giữa IP ${ip} và thí sinh "${name}"? Thí sinh có thể đổi IP khác sau thao tác này.`)) {
    delete AUTH_STATE.ipBindings[ip];
    saveIpBindings();
    renderAdminPanelContent();
  }
}

function reassignIpBinding(ip) {
  const currentBound = AUTH_STATE.ipBindings[ip] || '';
  const newName = prompt(`Nhập tên thí sinh mới muốn gán cho IP ${ip} (Hiện tại: ${currentBound}):`);
  if (newName && newName.trim()) {
    const cleanName = newName.trim();
    AUTH_STATE.ipBindings[ip] = cleanName;
    saveIpBindings();
    renderAdminPanelContent();
    alert(`Đã gán thành công IP ${ip} cho thí sinh "${cleanName}"!`);
  }
}

function bindCustomIp() {
  const ip = prompt('Nhập địa chỉ IP cần gán (Ví dụ: 192.168.1.100 hoặc 113.185.20.15):');
  if (!ip || !ip.trim()) return;
  const name = prompt(`Nhập họ và tên thí sinh cho IP ${ip.trim()}:`);
  if (!name || !name.trim()) return;

  AUTH_STATE.ipBindings[ip.trim()] = name.trim();
  saveIpBindings();
  renderAdminPanelContent();
  alert(`Đã gán thành công IP ${ip.trim()} cho thí sinh "${name.trim()}"!`);
}

function clearAllBindings() {
  if (confirm('Bạn có chắc muốn giải phóng tất cả các liên kết IP? Sau khi giải phóng, các thí sinh có thể đăng nhập từ địa chỉ IP mới.')) {
    AUTH_STATE.ipBindings = {};
    saveIpBindings();
    renderAdminPanelContent();
    alert('Đã giải phóng toàn bộ liên kết IP!');
  }
}

// --- SETUP EVENT LISTENERS ON LOAD ---
document.addEventListener('DOMContentLoaded', () => {
  initAuthSystem();

  // Support Enter key on login inputs
  const nameInput = document.getElementById('auth-name-input');
  const keyInput = document.getElementById('auth-key-input');
  if (nameInput) {
    nameInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') handleAuthLogin();
    });
  }
  if (keyInput) {
    keyInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') handleAuthLogin();
    });
  }
});

// Global exports
window.initAuthSystem = initAuthSystem;
window.handleAuthLogin = handleAuthLogin;
window.adminBypassFromBlocked = adminBypassFromBlocked;
window.openAdminPanel = openAdminPanel;
window.closeAdminPanel = closeAdminPanel;
window.logoutUser = logoutUser;
window.addWhitelistName = addWhitelistName;
window.removeWhitelistName = removeWhitelistName;
window.unblockIp = unblockIp;
window.unblockAllIps = unblockAllIps;
window.resetIpBinding = resetIpBinding;
window.reassignIpBinding = reassignIpBinding;
window.bindCustomIp = bindCustomIp;
window.clearAllBindings = clearAllBindings;
window.showAuthModal = showAuthModal;
