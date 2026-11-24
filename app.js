// ==========================================
// GEN AI EXAM MASTER - APPLICATION ENGINE V2
// ==========================================

const APP_STATE = {
  view: 'home', // home, exam, result, study, mistakes, theory
  examConfig: {
    mode: 'mock', // mock (40q, 50m), custom (10-100q), instant_learn
    questionCount: 40,
    domainFilter: 'all', // all, 1, 2, 3, 4
    typeFilter: 'all', // all, single_choice, multi_choice, true_false, ordering, matching
    timeLimitMinutes: 50,
    instantFeedback: false // FALSE = Thi thử (nộp bài mới chấm), TRUE = Học tập (chọn là hiện đáp án & giải thích)
  },
  activeExam: null, // { questions, currentIndex, answers, flagged, startTime, timeRemaining, timerInterval }
  history: [],
  mistakeIds: new Set(),
  darkMode: false,
  soundEnabled: true,
  currentTheoryTab: 'doc1_ebook'
};

// --- AUDIO SYNTHESIZER (Web Audio API) ---
class SoundManager {
  constructor() {
    this.ctx = null;
  }
  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) this.ctx = new AudioContext();
    }
  }
  playCorrect() {
    if (!APP_STATE.soundEnabled) return;
    try {
      this.init();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(587.33, this.ctx.currentTime); // D5
      osc.frequency.setValueAtTime(880, this.ctx.currentTime + 0.1); // A5
      gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.35);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.35);
    } catch (e) {}
  }
  playIncorrect() {
    if (!APP_STATE.soundEnabled) return;
    try {
      this.init();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(260, this.ctx.currentTime);
      osc.frequency.setValueAtTime(196, this.ctx.currentTime + 0.12);
      gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.3);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.3);
    } catch (e) {}
  }
}
const sound = new SoundManager();

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
  loadStoredData();
  setupNavigation();
  setupConfigListeners();
  renderDashboard();
  renderStudyGuide();
  renderTheoryLibrary();
  updateMistakesCount();
  initTheme();
});

function loadStoredData() {
  try {
    const savedMistakes = localStorage.getItem('genai_exam_mistakes');
    if (savedMistakes) {
      APP_STATE.mistakeIds = new Set(JSON.parse(savedMistakes));
    }
    const savedHistory = localStorage.getItem('genai_exam_history');
    if (savedHistory) {
      APP_STATE.history = JSON.parse(savedHistory);
    }
  } catch (e) {
    console.error('Error loading stored data:', e);
  }
}

function saveMistakes() {
  try {
    localStorage.setItem('genai_exam_mistakes', JSON.stringify([...APP_STATE.mistakeIds]));
    updateMistakesCount();
  } catch (e) {}
}

function saveHistoryEntry(entry) {
  try {
    APP_STATE.history.unshift(entry);
    if (APP_STATE.history.length > 30) APP_STATE.history.pop();
    localStorage.setItem('genai_exam_history', JSON.stringify(APP_STATE.history));
  } catch (e) {}
}

function updateMistakesCount() {
  const el = document.getElementById('nav-mistakes-count');
  if (el) el.textContent = APP_STATE.mistakeIds.size;
  const badge = document.getElementById('dash-mistakes-badge');
  if (badge) badge.textContent = `${APP_STATE.mistakeIds.size} câu`;
}

function initTheme() {
  const isDark = localStorage.getItem('genai_theme') === 'dark' || 
    (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  setTheme(isDark);
  document.getElementById('theme-toggle')?.addEventListener('click', () => {
    setTheme(!APP_STATE.darkMode);
  });
}

function setTheme(isDark) {
  APP_STATE.darkMode = isDark;
  if (isDark) {
    document.documentElement.classList.add('dark');
    localStorage.setItem('genai_theme', 'dark');
  } else {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('genai_theme', 'light');
  }
}

// --- NAVIGATION ---
function setupNavigation() {
  document.querySelectorAll('[data-view-target]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const target = btn.getAttribute('data-view-target');
      switchView(target);
    });
  });
}

function switchView(viewName) {
  if (APP_STATE.view === 'exam' && viewName !== 'exam' && APP_STATE.activeExam && !APP_STATE.activeExam.submitted) {
    if (!confirm('Bạn đang trong bài thi. Rời khỏi trang sẽ tạm dừng hoặc hủy bài làm này. Bạn có chắc muốn chuyển trang?')) {
      return;
    }
    clearInterval(APP_STATE.activeExam.timerInterval);
  }

  APP_STATE.view = viewName;
  document.querySelectorAll('.view-section').forEach(sec => sec.classList.add('hidden'));
  const currentSec = document.getElementById(`view-${viewName}`);
  if (currentSec) currentSec.classList.remove('hidden');

  document.querySelectorAll('[data-view-target]').forEach(b => {
    if (b.getAttribute('data-view-target') === viewName) {
      b.classList.add('text-blue-600', 'border-b-2', 'border-blue-600', 'font-bold');
      b.classList.remove('text-slate-500');
    } else {
      b.classList.remove('text-blue-600', 'border-b-2', 'border-blue-600', 'font-bold');
      b.classList.add('text-slate-500');
    }
  });

  if (viewName === 'home') renderDashboard();
  if (viewName === 'study') renderStudyGuide();
  if (viewName === 'theory') renderTheoryLibrary();
  if (viewName === 'mistakes') renderMistakesList();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// --- DASHBOARD & CONFIGURATION ---
function setupConfigListeners() {
  const slider = document.getElementById('cfg-q-count');
  const countDisplay = document.getElementById('cfg-q-count-val');
  if (slider && countDisplay) {
    slider.addEventListener('input', (e) => {
      countDisplay.textContent = e.target.value;
      APP_STATE.examConfig.questionCount = parseInt(e.target.value, 10);
    });
  }

  document.querySelectorAll('.count-preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const val = parseInt(btn.getAttribute('data-count'), 10);
      if (slider) slider.value = val;
      if (countDisplay) countDisplay.textContent = val;
      APP_STATE.examConfig.questionCount = val;
      document.querySelectorAll('.count-preset-btn').forEach(b => b.classList.remove('bg-blue-600', 'text-white'));
      btn.classList.add('bg-blue-600', 'text-white');
    });
  });

  // MODE A: BẮT ĐẦU THI THỬ (NỘP BÀI MỚI XEM KẾT QUẢ)
  document.getElementById('btn-start-mock')?.addEventListener('click', () => {
    startExam({
      mode: 'mock',
      questionCount: 40,
      domainFilter: 'all',
      typeFilter: 'all',
      timeLimitMinutes: 50,
      instantFeedback: false // THI THỬ: KHÔNG HIỆN ĐÁP ÁN KHI LÀM
    });
  });

  // MODE B: BẮT ĐẦU HỌC TẬP & ÔN TẬP TỨC THÌ (CHỌN LÀ HIỆN ĐÁP ÁN & GIẢI THÍCH NGAY)
  document.getElementById('btn-start-instant-learn')?.addEventListener('click', () => {
    startExam({
      mode: 'instant_learn',
      questionCount: 40,
      domainFilter: 'all',
      typeFilter: 'all',
      timeLimitMinutes: 0,
      instantFeedback: true // HỌC TẬP: HIỆN ĐÁP ÁN & GIẢI THÍCH NGAY KHI CHỌN
    });
  });

  // Start custom exam with user config
  document.getElementById('btn-start-custom')?.addEventListener('click', () => {
    const domainFilter = document.getElementById('cfg-domain')?.value || 'all';
    const typeFilter = document.getElementById('cfg-type')?.value || 'all';
    const timeLimit = parseInt(document.getElementById('cfg-time')?.value || '50', 10);
    const instantFeedback = document.getElementById('cfg-instant-feedback')?.checked || false;
    const qCount = parseInt(document.getElementById('cfg-q-count')?.value || '40', 10);

    startExam({
      mode: 'custom',
      questionCount: qCount,
      domainFilter,
      typeFilter,
      timeLimitMinutes: timeLimit,
      instantFeedback
    });
  });

  // Start mistakes exam
  document.getElementById('btn-start-mistakes-exam')?.addEventListener('click', () => {
    if (APP_STATE.mistakeIds.size === 0) {
      alert('Sổ tay câu sai hiện đang trống! Bạn hãy làm bài thi để hệ thống tự động ghi nhận những câu cần ôn tập.');
      return;
    }
    startMistakesExam();
  });
}

function renderDashboard() {
  const totalAttempts = APP_STATE.history.length;
  document.getElementById('dash-total-exams').textContent = totalAttempts;

  if (totalAttempts > 0) {
    const passCount = APP_STATE.history.filter(h => h.passed).length;
    const passRate = Math.round((passCount / totalAttempts) * 100);
    document.getElementById('dash-pass-rate').textContent = `${passRate}%`;

    const avgScore = Math.round(APP_STATE.history.reduce((a, b) => a + b.score, 0) / totalAttempts);
    document.getElementById('dash-avg-score').textContent = `${avgScore}/1000`;
  } else {
    document.getElementById('dash-pass-rate').textContent = '0%';
    document.getElementById('dash-avg-score').textContent = 'Chưa thi';
  }

  const historyList = document.getElementById('dash-history-list');
  if (historyList) {
    if (totalAttempts === 0) {
      historyList.innerHTML = `<div class="p-6 text-center text-slate-400">Chưa có lịch sử làm bài. Hãy chọn 1 trong 2 chế độ thi thử hoặc học tập ở trên!</div>`;
    } else {
      historyList.innerHTML = APP_STATE.history.slice(0, 5).map(h => `
        <div class="flex items-center justify-between p-3.5 border-b border-slate-200 dark:border-slate-800 last:border-none hover:bg-slate-50 dark:hover:bg-slate-800/40 rounded-lg transition">
          <div>
            <div class="font-semibold text-sm flex items-center gap-2">
              <span>${h.title}</span>
              <span class="px-2 py-0.5 text-xs rounded-full ${h.passed ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 font-bold' : 'bg-rose-100 text-rose-700 dark:bg-rose-950/60 dark:text-rose-400 font-bold'}">
                ${h.passed ? 'ĐẠT (PASS)' : 'CHƯA ĐẠT'}
              </span>
            </div>
            <div class="text-xs text-slate-400 mt-0.5">${h.date} • ${h.correctCount}/${h.totalQuestions} câu đúng (${h.percentage}%) • Thời gian: ${h.timeSpent}</div>
          </div>
          <div class="text-right">
            <span class="text-base font-extrabold ${h.passed ? 'text-emerald-600' : 'text-rose-600'}">${h.score}</span>
            <span class="text-xs text-slate-400">/1000đ</span>
          </div>
        </div>
      `).join('');
    }
  }
}

// --- EXAM GENERATION ENGINE ---
function startExam(config) {
  let pool = [...QUESTIONS_BANK];

  if (config.domainFilter !== 'all') {
    const dId = parseInt(config.domainFilter, 10);
    pool = pool.filter(q => q.domain_id === dId);
  }

  if (config.typeFilter !== 'all') {
    pool = pool.filter(q => q.type === config.typeFilter);
  }

  if (pool.length === 0) {
    alert('Không tìm thấy câu hỏi phù hợp với bộ lọc bạn chọn. Vui lòng mở rộng điều kiện lọc!');
    return;
  }

  let selectedQuestions = [];

  if (config.mode === 'mock') {
    const d1 = QUESTIONS_BANK.filter(q => q.domain_id === 1);
    const d2 = QUESTIONS_BANK.filter(q => q.domain_id === 2);
    const d3 = QUESTIONS_BANK.filter(q => q.domain_id === 3);
    const d4 = QUESTIONS_BANK.filter(q => q.domain_id === 4);

    selectedQuestions = [
      ...shuffleArray(d1).slice(0, 10),
      ...shuffleArray(d2).slice(0, 12),
      ...shuffleArray(d3).slice(0, 10),
      ...shuffleArray(d4).slice(0, 8)
    ];

    if (selectedQuestions.length < 40) {
      const addedIds = new Set(selectedQuestions.map(q => q.id));
      const rest = QUESTIONS_BANK.filter(q => !addedIds.has(q.id));
      selectedQuestions.push(...shuffleArray(rest).slice(0, 40 - selectedQuestions.length));
    }
    selectedQuestions = shuffleArray(selectedQuestions);
  } else {
    const count = Math.min(config.questionCount, pool.length);
    selectedQuestions = shuffleArray(pool).slice(0, count);
  }

  initExamState(selectedQuestions, config);
}

function startMistakesExam() {
  const mistakeQuestions = QUESTIONS_BANK.filter(q => APP_STATE.mistakeIds.has(q.id));
  if (mistakeQuestions.length === 0) {
    alert('Không có câu hỏi sai nào!');
    return;
  }

  initExamState(shuffleArray(mistakeQuestions), {
    mode: 'mistakes',
    questionCount: mistakeQuestions.length,
    domainFilter: 'all',
    typeFilter: 'all',
    timeLimitMinutes: 0,
    instantFeedback: true
  });
}

function startExamByLesson(lessonNum) {
  const lessonQuestions = QUESTIONS_BANK.filter(q => q.lesson_title && q.lesson_title.startsWith(`Bài ${lessonNum}:`));
  if (lessonQuestions.length === 0) {
    alert(`Chưa có câu hỏi riêng cho Bài ${lessonNum}. Đang mở ôn tập theo Domain!`);
    return;
  }

  initExamState(shuffleArray(lessonQuestions), {
    mode: 'lesson_practice',
    questionCount: lessonQuestions.length,
    domainFilter: 'all',
    typeFilter: 'all',
    timeLimitMinutes: 0,
    instantFeedback: true
  });
}

function initExamState(questions, config) {
  const timeLimitSeconds = config.timeLimitMinutes > 0 ? config.timeLimitMinutes * 60 : 0;

  APP_STATE.activeExam = {
    config,
    questions,
    currentIndex: 0,
    answers: {},
    flagged: new Set(),
    checkedQuestions: new Set(),
    startTime: Date.now(),
    timeRemaining: timeLimitSeconds,
    timeSpent: 0,
    timerInterval: null,
    submitted: false
  };

  if (timeLimitSeconds > 0) {
    APP_STATE.activeExam.timerInterval = setInterval(updateExamTimer, 1000);
  }

  switchView('exam');
  renderExamArena();
  renderPalette();
  renderQuestion(0);
}

function updateExamTimer() {
  const exam = APP_STATE.activeExam;
  if (!exam || exam.submitted) return;

  exam.timeRemaining--;
  const timerBadge = document.getElementById('exam-timer');
  const timerContainer = document.getElementById('exam-timer-container');

  if (exam.timeRemaining <= 0) {
    clearInterval(exam.timerInterval);
    alert('Hết giờ làm bài! Hệ thống sẽ tự động nộp bài của bạn.');
    submitExam();
    return;
  }

  const mins = Math.floor(exam.timeRemaining / 60);
  const secs = exam.timeRemaining % 60;
  const timeStr = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

  if (timerBadge) timerBadge.textContent = timeStr;

  if (exam.timeRemaining < 300) {
    timerContainer?.classList.add('bg-red-500/20', 'text-red-600', 'animate-pulse');
  } else {
    timerContainer?.classList.remove('bg-red-500/20', 'text-red-600', 'animate-pulse');
  }
}

// --- RENDER EXAM ARENA & MODE SWITCHER ---
function renderExamArena() {
  const exam = APP_STATE.activeExam;
  document.getElementById('exam-total-q-badge').textContent = `${exam.questions.length} câu`;
  
  renderArenaModeToggle();

  document.getElementById('btn-prev-q').onclick = () => navigateQuestion(exam.currentIndex - 1);
  document.getElementById('btn-next-q').onclick = () => navigateQuestion(exam.currentIndex + 1);
  
  const flagBtn = document.getElementById('btn-flag-q');
  flagBtn.onclick = () => toggleFlagCurrentQuestion();

  document.getElementById('btn-submit-exam').onclick = () => {
    const unansweredCount = exam.questions.length - Object.keys(exam.answers).length;
    let confirmMsg = 'Bạn có chắc chắn muốn nộp bài để xem điểm?';
    if (unansweredCount > 0) {
      confirmMsg = `Bạn còn ${unansweredCount} câu hỏi chưa làm! Bạn có chắc chắn muốn nộp bài ngay bây giờ?`;
    }
    if (confirm(confirmMsg)) {
      submitExam();
    }
  };
}

function renderArenaModeToggle() {
  const exam = APP_STATE.activeExam;
  const toggleContainer = document.getElementById('exam-arena-mode-toggle');
  if (!toggleContainer) return;

  const isInstant = exam.config.instantFeedback;
  toggleContainer.innerHTML = `
    <div class="flex items-center gap-2 p-1 bg-slate-200 dark:bg-slate-800 rounded-xl">
      <button class="px-3 py-1 text-xs font-bold rounded-lg transition ${!isInstant ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:text-blue-500'}" onclick="setExamArenaMode(false)">
        ⏱️ Thi Thử (Nộp bài mới chấm)
      </button>
      <button class="px-3 py-1 text-xs font-bold rounded-lg transition ${isInstant ? 'bg-emerald-600 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:text-emerald-500'}" onclick="setExamArenaMode(true)">
        🎓 Học Tập (Hiện giải thích ngay)
      </button>
    </div>
  `;
}

function setExamArenaMode(instantFeedback) {
  if (!APP_STATE.activeExam) return;
  APP_STATE.activeExam.config.instantFeedback = instantFeedback;
  renderArenaModeToggle();
  renderQuestion(APP_STATE.activeExam.currentIndex);
}

function renderPalette() {
  const exam = APP_STATE.activeExam;
  const palContainer = document.getElementById('exam-palette');
  if (!palContainer) return;

  palContainer.innerHTML = exam.questions.map((q, idx) => {
    const isAnswered = isQuestionAnswered(q.id);
    const isFlagged = exam.flagged.has(q.id);
    const isCurrent = idx === exam.currentIndex;

    let classes = 'pal-btn';
    if (isCurrent) classes += ' current';
    if (isAnswered) classes += ' answered';
    if (isFlagged) classes += ' flagged';

    return `<button class="${classes}" data-index="${idx}" onclick="navigateQuestion(${idx})">${idx + 1}</button>`;
  }).join('');

  updateProgressSummary();
}

function updateProgressSummary() {
  const exam = APP_STATE.activeExam;
  const answeredCount = Object.keys(exam.answers).filter(id => isQuestionAnswered(id)).length;
  document.getElementById('exam-answered-count').textContent = `${answeredCount}/${exam.questions.length}`;
  const pct = Math.round((answeredCount / exam.questions.length) * 100);
  const bar = document.getElementById('exam-progress-bar');
  if (bar) bar.style.width = `${pct}%`;
}

function isQuestionAnswered(qId) {
  const ans = APP_STATE.activeExam?.answers[qId];
  if (ans === undefined || ans === null) return false;
  if (Array.isArray(ans)) return ans.length > 0;
  if (typeof ans === 'object') return Object.keys(ans).length > 0;
  return ans !== '';
}

function navigateQuestion(idx) {
  const exam = APP_STATE.activeExam;
  if (idx < 0 || idx >= exam.questions.length) return;
  exam.currentIndex = idx;
  renderPalette();
  renderQuestion(idx);
  window.scrollTo({ top: 100, behavior: 'smooth' });
}

function toggleFlagCurrentQuestion() {
  const exam = APP_STATE.activeExam;
  const currentQ = exam.questions[exam.currentIndex];
  if (exam.flagged.has(currentQ.id)) {
    exam.flagged.delete(currentQ.id);
  } else {
    exam.flagged.add(currentQ.id);
  }
  updateFlagButton();
  renderPalette();
}

function updateFlagButton() {
  const exam = APP_STATE.activeExam;
  const currentQ = exam.questions[exam.currentIndex];
  const btn = document.getElementById('btn-flag-q');
  const isFlagged = exam.flagged.has(currentQ.id);

  if (isFlagged) {
    btn.innerHTML = `
      <svg class="w-5 h-5 fill-amber-500 text-amber-500 inline mr-1" viewBox="0 0 24 24"><path d="M5 21V4a1 1 0 0 1 1-1h11a1 1 0 0 1 .8 1.6L14.25 9l3.55 4.4A1 1 0 0 1 17 15H7v6a1 1 0 0 1-2 0z"/></svg>
      <span>Bỏ cờ</span>
    `;
    btn.classList.add('bg-amber-100', 'text-amber-800', 'border-amber-300', 'dark:bg-amber-950/50', 'dark:text-amber-300');
  } else {
    btn.innerHTML = `
      <svg class="w-5 h-5 text-slate-400 inline mr-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"/></svg>
      <span>Đặt cờ (Xem lại)</span>
    `;
    btn.classList.remove('bg-amber-100', 'text-amber-800', 'border-amber-300', 'dark:bg-amber-950/50', 'dark:text-amber-300');
  }
}

// --- RENDER QUESTION CARD ---
function isQuestionFullyAnswered(q, ans) {
  if (ans === undefined || ans === null) return false;
  if (q.type === 'single_choice' || q.type === 'visual') {
    return ans !== '';
  }
  if (q.type === 'multi_choice') {
    return Array.isArray(ans) && ans.length === (q.required_count || 2);
  }
  if (q.type === 'true_false') {
    return typeof ans === 'object' && ans !== null && q.items.every(it => ans[it.id] !== undefined);
  }
  if (q.type === 'ordering') {
    return Array.isArray(ans) && ans.length === q.items.length;
  }
  if (q.type === 'matching') {
    return typeof ans === 'object' && ans !== null && Object.keys(ans).length === q.left_items.length;
  }
  return false;
}

function getQuestionCompletionStatus(q, ans) {
  if (q.type === 'single_choice' || q.type === 'visual') {
    const done = (ans !== undefined && ans !== null && ans !== '');
    return { isComplete: done, text: done ? 'Đã chọn 1 đáp án' : 'Chưa chọn đáp án' };
  }
  if (q.type === 'multi_choice') {
    const count = Array.isArray(ans) ? ans.length : 0;
    const req = q.required_count || 2;
    return {
      isComplete: count === req,
      text: count === req ? `Đã chọn đủ ${count}/${req} đáp án` : `Đã chọn ${count}/${req} (cần chọn thêm ${req - count})`
    };
  }
  if (q.type === 'true_false') {
    const answeredCount = typeof ans === 'object' && ans !== null ? Object.keys(ans).length : 0;
    const total = q.items.length;
    return {
      isComplete: answeredCount === total,
      text: answeredCount === total ? `Đã đánh dấu đủ ${total}/${total} ý` : `Đã đánh dấu ${answeredCount}/${total} ý (cần chọn hết cả 4 ý)`
    };
  }
  if (q.type === 'ordering') {
    return { isComplete: true, text: 'Đã sẵn sàng kiểm tra thứ tự' };
  }
  if (q.type === 'matching') {
    const matchedCount = typeof ans === 'object' && ans !== null ? Object.keys(ans).length : 0;
    const total = q.left_items.length;
    return {
      isComplete: matchedCount === total,
      text: matchedCount === total ? `Đã ghép đủ ${total}/${total} cặp` : `Đã ghép ${matchedCount}/${total} cặp (cần ghép đủ ${total} cặp)`
    };
  }
  return { isComplete: false, text: '' };
}

function renderQuestion(idx) {
  const exam = APP_STATE.activeExam;
  if (!exam) return;
  if (!exam.checkedQuestions) exam.checkedQuestions = new Set();
  const q = exam.questions[idx];

  document.getElementById('q-number-display').textContent = `Câu ${idx + 1}/${exam.questions.length}`;
  document.getElementById('q-domain-badge').textContent = `Domain ${q.domain_id}: ${q.domain_name}`;
  document.getElementById('q-lesson-badge').textContent = q.lesson_title;

  const typeLabels = {
    single_choice: 'Chọn 1 đáp án',
    multi_choice: `Chọn nhiều đáp án (${q.required_count || 2} đáp án)`,
    true_false: 'Đúng / Sai theo từng ý',
    ordering: 'Sắp xếp thứ tự các bước',
    matching: 'Kéo thả / Ghép nối thuật ngữ',
    visual: 'Quan sát sơ đồ / hình ảnh'
  };
  document.getElementById('q-type-badge').textContent = typeLabels[q.type] || 'Trắc nghiệm';
  document.getElementById('q-prompt-text').textContent = q.question;

  const imgBox = document.getElementById('q-image-container');
  if (q.image_url) {
    imgBox.classList.remove('hidden');
    imgBox.innerHTML = `
      <div class="p-3 bg-slate-100 dark:bg-slate-800 rounded-xl text-center">
        <img src="${q.image_url}" alt="Sơ đồ câu hỏi" class="max-h-72 mx-auto rounded-lg shadow-sm border border-slate-200 dark:border-slate-700 cursor-pointer hover:opacity-95 transition" onclick="openImageModal('${q.image_url}')">
        <span class="text-xs text-slate-500 mt-2 block italic">Nhấn vào hình để phóng to kích thước đầy đủ</span>
      </div>
    `;
  } else {
    imgBox.classList.add('hidden');
    imgBox.innerHTML = '';
  }

  const inputContainer = document.getElementById('q-interactive-input');
  inputContainer.innerHTML = '';

  const currentAnswer = exam.answers[q.id];
  const isInstant = exam.config.instantFeedback;
  const isChecked = isInstant && exam.checkedQuestions.has(q.id);

  if (q.type === 'single_choice' || q.type === 'visual') {
    renderSingleChoiceInput(q, currentAnswer, inputContainer, isChecked);
  } else if (q.type === 'multi_choice') {
    renderMultiChoiceInput(q, currentAnswer, inputContainer, isChecked);
  } else if (q.type === 'true_false') {
    renderTrueFalseInput(q, currentAnswer, inputContainer, isChecked);
  } else if (q.type === 'ordering') {
    renderOrderingInput(q, currentAnswer, inputContainer, isChecked);
  } else if (q.type === 'matching') {
    renderMatchingInput(q, currentAnswer, inputContainer, isChecked);
  }

  // Render Check Action Bar & Feedback in Instant Mode
  const fbContainer = document.getElementById('q-instant-feedback');
  if (isInstant) {
    if (isChecked) {
      // User has checked: show the full feedback card & retake button
      renderInstantFeedbackCard(q, currentAnswer, fbContainer);
    } else {
      // User has NOT checked: render the Check Button
      renderCheckActionBar(q, currentAnswer, fbContainer);
    }
  } else {
    fbContainer.classList.add('hidden');
    fbContainer.innerHTML = '';
  }

  updateFlagButton();

  document.getElementById('btn-prev-q').disabled = (idx === 0);
  document.getElementById('btn-next-q').disabled = (idx === exam.questions.length - 1);
}

// Check Action Bar (Appears in Instant Mode BEFORE checking)
function renderCheckActionBar(q, currentAnswer, container) {
  const status = getQuestionCompletionStatus(q, currentAnswer);
  container.classList.remove('hidden');

  container.innerHTML = `
    <div class="mt-6 p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-900/50 flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full ${status.isComplete ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}"></span>
        <span class="text-xs font-semibold text-slate-700 dark:text-slate-300">${status.text}</span>
      </div>
      <div>
        <button onclick="checkCurrentQuestionAnswer()" 
          class="px-5 py-2.5 rounded-xl font-black text-xs transition flex items-center gap-2 ${
            status.isComplete 
              ? 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-md transform hover:-translate-y-0.5 cursor-pointer' 
              : 'bg-slate-200 dark:bg-slate-800 text-slate-400 dark:text-slate-600 cursor-not-allowed opacity-75'
          }" 
          ${status.isComplete ? '' : 'disabled'}>
          <span>🔍 Kiểm Tra Đáp Án & Xem Lời Giải</span>
          ${status.isComplete ? '➜' : ''}
        </button>
      </div>
    </div>
  `;
}

function checkCurrentQuestionAnswer() {
  const exam = APP_STATE.activeExam;
  if (!exam) return;
  const q = exam.questions[exam.currentIndex];
  const userAns = exam.answers[q.id];

  if (!isQuestionFullyAnswered(q, userAns)) {
    alert('Vui lòng hoàn thành đầy đủ câu hỏi trước khi kiểm tra đáp án!');
    return;
  }

  exam.checkedQuestions.add(q.id);
  const isCorrect = evaluateQuestionScore(q, userAns);
  if (isCorrect) sound.playCorrect();
  else sound.playIncorrect();

  renderPalette();
  renderQuestion(exam.currentIndex);
}

function resetCurrentQuestionAnswer() {
  const exam = APP_STATE.activeExam;
  if (!exam) return;
  const q = exam.questions[exam.currentIndex];
  exam.checkedQuestions.delete(q.id);
  delete exam.answers[q.id];
  matchingSelectedLeft = null;
  renderPalette();
  renderQuestion(exam.currentIndex);
}

// 1. Single Choice Input
function renderSingleChoiceInput(q, currentAnswer, container, isChecked) {
  const isAnswered = (currentAnswer !== undefined && currentAnswer !== null && currentAnswer !== '');

  const optionsHtml = Object.entries(q.options).map(([letter, text]) => {
    const isSelected = (currentAnswer === letter);
    let stateClasses = '';

    if (isChecked) {
      if (letter === q.answer) {
        stateClasses = 'border-emerald-500 bg-emerald-50/80 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-200 ring-2 ring-emerald-500/40';
      } else if (isSelected && letter !== q.answer) {
        stateClasses = 'border-rose-500 bg-rose-50/80 dark:bg-rose-950/40 text-rose-900 dark:text-rose-200 ring-2 ring-rose-500/40';
      }
    } else if (isSelected) {
      stateClasses = 'selected';
    }

    return `
      <div class="option-card p-4 rounded-xl flex items-start gap-3.5 ${stateClasses}" onclick="${isChecked ? '' : `selectSingleChoice('${q.id}', '${letter}')`}">
        <div class="w-7 h-7 rounded-full flex items-center justify-center font-bold text-sm shrink-0 border ${
          isChecked && letter === q.answer 
            ? 'bg-emerald-600 text-white border-emerald-600' 
            : (isChecked && isSelected 
              ? 'bg-rose-600 text-white border-rose-600' 
              : (isSelected 
                ? 'bg-blue-600 text-white border-blue-600' 
                : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-600'))
        }">
          ${isChecked && letter === q.answer ? '✓' : (isChecked && isSelected ? '✗' : letter)}
        </div>
        <div class="text-sm font-medium leading-relaxed pt-0.5 text-slate-800 dark:text-slate-100 flex-1">
          ${text}
        </div>
        ${isChecked && letter === q.answer ? `<span class="px-2 py-0.5 text-xs font-bold rounded bg-emerald-600 text-white shrink-0">ĐÁP ÁN ĐÚNG</span>` : ''}
      </div>
    `;
  }).join('');

  container.innerHTML = `<div class="space-y-3">${optionsHtml}</div>`;
}

function selectSingleChoice(qId, letter) {
  APP_STATE.activeExam.answers[qId] = letter;
  renderPalette();
  renderQuestion(APP_STATE.activeExam.currentIndex);
}

// 2. Multiple Choice Input
function renderMultiChoiceInput(q, currentAnswer, container, isChecked) {
  const selectedList = Array.isArray(currentAnswer) ? currentAnswer : [];
  const reqCount = q.required_count || 2;

  const optionsHtml = Object.entries(q.options).map(([letter, text]) => {
    const isSelected = selectedList.includes(letter);
    const isCorrectChoice = q.answer.includes(letter);

    let stateClasses = '';
    if (isChecked) {
      if (isCorrectChoice) {
        stateClasses = 'border-emerald-500 bg-emerald-50/80 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-200';
      } else if (isSelected && !isCorrectChoice) {
        stateClasses = 'border-rose-500 bg-rose-50/80 dark:bg-rose-950/40 text-rose-900 dark:text-rose-200';
      }
    } else if (isSelected) {
      stateClasses = 'selected';
    }

    return `
      <div class="option-card p-4 rounded-xl flex items-start gap-3.5 ${stateClasses}" onclick="${isChecked ? '' : `toggleMultiChoice('${q.id}', '${letter}', ${reqCount})`}">
        <div class="w-6 h-6 rounded-md flex items-center justify-center font-bold text-sm shrink-0 border ${
          isChecked && isCorrectChoice 
            ? 'bg-emerald-600 text-white border-emerald-600' 
            : (isChecked && isSelected 
              ? 'bg-rose-600 text-white border-rose-600' 
              : (isSelected 
                ? 'bg-blue-600 text-white border-blue-600' 
                : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-600'))
        }">
          ${isChecked && isCorrectChoice ? '✓' : (isChecked && isSelected ? '✗' : (isSelected ? '✓' : letter))}
        </div>
        <div class="text-sm font-medium leading-relaxed pt-0.5 text-slate-800 dark:text-slate-100 flex-1">
          ${text}
        </div>
        ${isChecked && isCorrectChoice ? `<span class="px-2 py-0.5 text-xs font-bold rounded bg-emerald-600 text-white shrink-0">ĐÚNG</span>` : ''}
      </div>
    `;
  }).join('');

  container.innerHTML = `
    <div class="mb-3 flex justify-between items-center text-xs font-semibold text-blue-600 dark:text-blue-400">
      <span>Đã chọn: ${selectedList.length}/${reqCount} đáp án</span>
      ${isChecked ? `<span class="font-bold text-emerald-600">Đáp án chuẩn: ${q.answer.join(', ')}</span>` : ''}
    </div>
    <div class="space-y-3">${optionsHtml}</div>
  `;
}

function toggleMultiChoice(qId, letter, reqCount) {
  const current = APP_STATE.activeExam.answers[qId] || [];
  let updated;
  if (current.includes(letter)) {
    updated = current.filter(x => x !== letter);
  } else {
    if (current.length >= reqCount) {
      updated = [...current.slice(1), letter];
    } else {
      updated = [...current, letter];
    }
  }
  APP_STATE.activeExam.answers[qId] = updated;
  renderPalette();
  renderQuestion(APP_STATE.activeExam.currentIndex);
}

// 3. True / False Matrix Input
function renderTrueFalseInput(q, currentAnswer, container, isChecked) {
  const currentObj = currentAnswer || {};

  const rowsHtml = q.items.map(item => {
    const userVal = currentObj[item.id];
    const correctVal = q.answer[item.id];

    let rowBadge = '';
    if (isChecked && userVal !== undefined) {
      const isItemCorrect = (userVal === correctVal);
      rowBadge = isItemCorrect 
        ? `<span class="text-xs font-bold text-emerald-600 ml-2">✓ Đúng</span>` 
        : `<span class="text-xs font-bold text-rose-600 ml-2">✗ Sai (Đáp án: ${correctVal ? 'ĐÚNG' : 'SAI'})</span>`;
    }

    return `
      <tr class="border-b border-slate-200 dark:border-slate-800">
        <td class="py-3.5 px-3 font-semibold text-sm w-8 text-blue-600 dark:text-blue-400">${item.id}</td>
        <td class="py-3.5 px-3 text-sm text-slate-800 dark:text-slate-200">
          ${item.text} ${rowBadge}
        </td>
        <td class="py-3.5 px-3 text-center w-28">
          <button ${isChecked ? 'disabled' : ''} class="px-3.5 py-1.5 text-xs font-bold rounded-lg border transition ${userVal === true ? 'bg-blue-600 text-white border-blue-600 shadow-sm' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border-slate-300 dark:border-slate-700 hover:border-blue-500'}" onclick="setTrueFalse('${q.id}', '${item.id}', true)">
            ĐÚNG
          </button>
        </td>
        <td class="py-3.5 px-3 text-center w-28">
          <button ${isChecked ? 'disabled' : ''} class="px-3.5 py-1.5 text-xs font-bold rounded-lg border transition ${userVal === false ? 'bg-blue-600 text-white border-blue-600 shadow-sm' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border-slate-300 dark:border-slate-700 hover:border-blue-500'}" onclick="setTrueFalse('${q.id}', '${item.id}', false)">
            SAI
          </button>
        </td>
      </tr>
    `;
  }).join('');

  container.innerHTML = `
    <div class="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-700">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-slate-100/70 dark:bg-slate-800/70 text-xs font-bold uppercase tracking-wider text-slate-600 dark:text-slate-400">
            <th class="py-2.5 px-3">Ý</th>
            <th class="py-2.5 px-3">Nội dung</th>
            <th class="py-2.5 px-3 text-center">Đúng</th>
            <th class="py-2.5 px-3 text-center">Sai</th>
          </tr>
        </thead>
        <tbody>
          ${rowsHtml}
        </tbody>
      </table>
    </div>
  `;
}

function setTrueFalse(qId, itemId, val) {
  if (!APP_STATE.activeExam.answers[qId]) {
    APP_STATE.activeExam.answers[qId] = {};
  }
  APP_STATE.activeExam.answers[qId][itemId] = val;
  renderPalette();
  renderQuestion(APP_STATE.activeExam.currentIndex);
}

// 4. Ordering Steps Input
function renderOrderingInput(q, currentAnswer, container, isChecked) {
  const itemsOrder = currentAnswer || q.items.map(it => it.id);
  const itemsMap = Object.fromEntries(q.items.map(it => [it.id, it.text]));

  const listHtml = itemsOrder.map((stepId, orderIdx) => `
    <div class="order-item p-3.5 rounded-xl flex items-center justify-between border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800/80 shadow-xs">
      <div class="flex items-center gap-3">
        <span class="w-7 h-7 rounded-full bg-blue-600 text-white font-bold text-xs flex items-center justify-center shrink-0">
          ${orderIdx + 1}
        </span>
        <span class="font-bold text-sm text-blue-600 dark:text-blue-400">(${stepId})</span>
        <span class="text-sm text-slate-800 dark:text-slate-200">${itemsMap[stepId] || ''}</span>
      </div>
      <div class="flex items-center gap-1 shrink-0">
        <button class="p-1.5 rounded-md hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 disabled:opacity-30" ${orderIdx === 0 || isChecked ? 'disabled' : ''} onclick="moveOrderItem('${q.id}', ${orderIdx}, -1)">
          ▲
        </button>
        <button class="p-1.5 rounded-md hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 disabled:opacity-30" ${orderIdx === itemsOrder.length - 1 || isChecked ? 'disabled' : ''} onclick="moveOrderItem('${q.id}', ${orderIdx}, 1)">
          ▼
        </button>
      </div>
    </div>
  `).join('');

  container.innerHTML = `
    <div class="mb-2 text-xs text-slate-500 italic">
      Sử dụng nút mũi tên ▲ ▼ để di chuyển và sắp xếp các bước theo đúng trình tự từ đầu đến cuối:
    </div>
    <div class="space-y-2.5">${listHtml}</div>
    <div class="mt-4 p-3 bg-blue-50 dark:bg-blue-950/40 rounded-lg text-xs font-semibold text-blue-700 dark:text-blue-300 flex justify-between items-center">
      <span>Trình tự của bạn: ${itemsOrder.join(' → ')}</span>
      ${isChecked ? `<span class="font-bold text-emerald-600">Thứ tự đúng: ${q.answer.join(' → ')}</span>` : ''}
    </div>
  `;
}

function moveOrderItem(qId, fromIdx, dir) {
  const current = APP_STATE.activeExam.answers[qId] || APP_STATE.activeExam.questions[APP_STATE.activeExam.currentIndex].items.map(it => it.id);
  const arr = [...current];
  const toIdx = fromIdx + dir;
  if (toIdx < 0 || toIdx >= arr.length) return;
  const temp = arr[fromIdx];
  arr[fromIdx] = arr[toIdx];
  arr[toIdx] = temp;

  APP_STATE.activeExam.answers[qId] = arr;
  renderPalette();
  renderQuestion(APP_STATE.activeExam.currentIndex);
}

// 5. Matching Columns Input
let matchingSelectedLeft = null;
function renderMatchingInput(q, currentAnswer, container, isChecked) {
  const pairs = currentAnswer || {};

  const leftHtml = q.left_items.map(item => {
    const targetRight = pairs[item.id];
    const isSelected = (matchingSelectedLeft === item.id);
    const correctRight = q.answer[item.id];

    let matchClass = '';
    let badgeText = '';

    if (isChecked) {
      if (targetRight === correctRight) {
        matchClass = 'border-emerald-500 bg-emerald-50/60 dark:bg-emerald-950/30';
        badgeText = `<span class="inline-block mt-1 px-2 py-0.5 text-xs rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 font-bold">✓ Ghép đúng với: ${targetRight.toUpperCase()}</span>`;
      } else {
        matchClass = 'border-rose-500 bg-rose-50/60 dark:bg-rose-950/30';
        badgeText = `<span class="inline-block mt-1 px-2 py-0.5 text-xs rounded bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 font-bold">✗ Ghép: ${targetRight ? targetRight.toUpperCase() : 'chưa ghép'} (Đúng là: ${correctRight.toUpperCase()})</span>`;
      }
    } else if (targetRight) {
      matchClass = 'border-blue-500 bg-blue-50/60 dark:bg-blue-950/30';
      badgeText = `<span class="inline-block mt-1 px-2 py-0.5 text-xs rounded bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 font-bold">➜ Đã nối với: ${targetRight.toUpperCase()}</span>`;
    }

    return `
      <div class="match-item ${isSelected ? 'active-select' : ''} ${matchClass}" onclick="${isChecked ? '' : `selectLeftMatchItem('${q.id}', '${item.id}')`}">
        <div class="font-semibold text-sm text-slate-900 dark:text-slate-100">${item.text}</div>
        ${badgeText}
      </div>
    `;
  }).join('');

  const rightHtml = q.right_items.map(item => {
    const matchedBy = Object.entries(pairs).find(([lId, rId]) => rId === item.id);
    const matchClass = matchedBy ? (isChecked ? 'border-emerald-500 bg-emerald-50/30' : 'border-blue-500 bg-blue-50/30') : '';

    return `
      <div class="match-item ${matchClass}" onclick="${isChecked ? '' : `selectRightMatchItem('${q.id}', '${item.id}')`}">
        <div class="text-sm text-slate-800 dark:text-slate-200">${item.text}</div>
        ${matchedBy ? `<span class="inline-block mt-1 px-2 py-0.5 text-xs rounded ${isChecked ? 'bg-emerald-100 text-emerald-800' : 'bg-blue-100 text-blue-800'} dark:bg-blue-950 dark:text-blue-300 font-bold">✓ Cặp với mục ${matchedBy[0]}</span>` : ''}
      </div>
    `;
  }).join('');

  container.innerHTML = `
    <div class="mb-3 text-xs text-slate-500 italic">
      Cách ghép: Nhấn vào 1 mục ở Cột 1 (bên trái), sau đó nhấn vào 1 định nghĩa ở Cột 2 (bên phải) để nối cặp.
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <h4 class="font-bold text-xs uppercase tracking-wider text-slate-500 mb-2">Cột 1: Thuật ngữ / Khái niệm</h4>
        <div class="space-y-2.5">${leftHtml}</div>
      </div>
      <div>
        <h4 class="font-bold text-xs uppercase tracking-wider text-slate-500 mb-2">Cột 2: Định nghĩa / Vai trò</h4>
        <div class="space-y-2.5">${rightHtml}</div>
      </div>
    </div>
    <div class="mt-4 flex justify-between items-center text-xs">
      <span class="font-semibold text-slate-600 dark:text-slate-400">Đã ghép: ${Object.keys(pairs).length}/${q.left_items.length} cặp</span>
      ${isChecked ? '' : `<button class="px-2.5 py-1 text-xs text-rose-600 hover:underline" onclick="clearMatching('${q.id}')">Xóa các cặp đã ghép để làm lại</button>`}
    </div>
  `;
}

function selectLeftMatchItem(qId, leftId) {
  matchingSelectedLeft = leftId;
  renderQuestion(APP_STATE.activeExam.currentIndex);
}

function selectRightMatchItem(qId, rightId) {
  if (!matchingSelectedLeft) {
    alert('Vui lòng chọn 1 mục ở cột bên trái trước!');
    return;
  }
  if (!APP_STATE.activeExam.answers[qId]) {
    APP_STATE.activeExam.answers[qId] = {};
  }
  APP_STATE.activeExam.answers[qId][matchingSelectedLeft] = rightId;
  matchingSelectedLeft = null;
  renderPalette();
  renderQuestion(APP_STATE.activeExam.currentIndex);
}

function clearMatching(qId) {
  APP_STATE.activeExam.answers[qId] = {};
  matchingSelectedLeft = null;
  renderPalette();
  renderQuestion(APP_STATE.activeExam.currentIndex);
}

// 6. Instant Feedback Card (Học Tập & Ôn Luyện - Only shown after user checks)
function renderInstantFeedbackCard(q, userAnswer, container) {
  const isCorrect = evaluateQuestionScore(q, userAnswer);

  container.classList.remove('hidden');
  container.innerHTML = `
    <div class="mt-6 p-5 rounded-2xl border ${isCorrect ? 'bg-emerald-50/90 border-emerald-300 dark:bg-emerald-950/50 dark:border-emerald-800' : 'bg-rose-50/90 border-rose-300 dark:bg-rose-950/50 dark:border-rose-800'} shadow-sm">
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center gap-2 font-black text-base ${isCorrect ? 'text-emerald-700 dark:text-emerald-300' : 'text-rose-700 dark:text-rose-300'}">
          <span>${isCorrect ? '✓ CHÍNH XÁC!' : '✗ CHƯA CHÍNH XÁC!'}</span>
        </div>
        <button onclick="resetCurrentQuestionAnswer()" class="px-3 py-1 rounded-lg text-xs font-bold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 transition flex items-center gap-1">
          <span>🔄 Thử làm lại câu này</span>
        </button>
      </div>
      <div class="text-sm text-slate-800 dark:text-slate-200 mb-2">
        <span class="font-bold text-slate-900 dark:text-white">Đáp án đúng chuẩn:</span> 
        <span class="font-extrabold text-blue-600 dark:text-blue-400">${formatCorrectAnswerText(q)}</span>
      </div>
      <div class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed bg-white/90 dark:bg-slate-900/80 p-4 rounded-xl border border-slate-200/80 dark:border-slate-800">
        <span class="font-bold text-slate-900 dark:text-white">💡 Giải thích chi tiết từ giáo trình:</span> ${q.explanation}
      </div>
    </div>
  `;
}

function formatCorrectAnswerText(q) {
  if (q.type === 'single_choice' || q.type === 'visual') {
    return `${q.answer}. ${q.options[q.answer] || ''}`;
  }
  if (q.type === 'multi_choice') {
    return q.answer.map(a => `${a}`).join(', ');
  }
  if (q.type === 'true_false') {
    return Object.entries(q.answer).map(([k, v]) => `${k.toUpperCase()}: ${v ? 'ĐÚNG' : 'SAI'}`).join(' | ');
  }
  if (q.type === 'ordering') {
    return q.answer.join(' → ');
  }
  if (q.type === 'matching') {
    return Object.entries(q.answer).map(([k, v]) => `${k}-${v}`).join(', ');
  }
  return String(q.answer);
}

// --- EVALUATE QUESTION SCORING ENGINE ---
function evaluateQuestionScore(q, userAns) {
  if (!userAns) return false;

  if (q.type === 'single_choice' || q.type === 'visual') {
    return userAns === q.answer;
  }

  if (q.type === 'multi_choice') {
    if (!Array.isArray(userAns)) return false;
    if (userAns.length !== q.answer.length) return false;
    const sortedUser = [...userAns].sort();
    const sortedCorrect = [...q.answer].sort();
    return sortedUser.every((val, idx) => val === sortedCorrect[idx]);
  }

  if (q.type === 'true_false') {
    if (typeof userAns !== 'object') return false;
    for (const [key, correctVal] of Object.entries(q.answer)) {
      if (userAns[key] !== correctVal) return false;
    }
    return true;
  }

  if (q.type === 'ordering') {
    if (!Array.isArray(userAns)) return false;
    if (userAns.length !== q.answer.length) return false;
    return userAns.every((val, idx) => val === q.answer[idx]);
  }

  if (q.type === 'matching') {
    if (typeof userAns !== 'object') return false;
    for (const [leftKey, correctRightKey] of Object.entries(q.answer)) {
      if (userAns[leftKey] !== correctRightKey) return false;
    }
    return true;
  }

  return false;
}
// --- SUBMIT EXAM & GENERATE RESULT ---
function submitExam() {
  const exam = APP_STATE.activeExam;
  if (!exam) return;
  clearInterval(exam.timerInterval);
  exam.submitted = true;

  const totalQ = exam.questions.length;
  let correctCount = 0;
  const domainStats = { 1: { c: 0, t: 0 }, 2: { c: 0, t: 0 }, 3: { c: 0, t: 0 }, 4: { c: 0, t: 0 } };

  exam.questions.forEach(q => {
    const userAns = exam.answers[q.id];
    const isCorrect = evaluateQuestionScore(q, userAns);

    if (domainStats[q.domain_id]) {
      domainStats[q.domain_id].t++;
      if (isCorrect) domainStats[q.domain_id].c++;
    }

    if (isCorrect) {
      correctCount++;
      APP_STATE.mistakeIds.delete(q.id);
    } else {
      APP_STATE.mistakeIds.add(q.id);
    }
  });

  saveMistakes();

  const score = Math.round((correctCount / totalQ) * 1000);
  const passed = score >= 700;

  const timeSpentSecs = exam.config.timeLimitMinutes > 0 
    ? (exam.config.timeLimitMinutes * 60 - exam.timeRemaining) 
    : Math.floor((Date.now() - exam.startTime) / 1000);
  const spentMins = Math.floor(timeSpentSecs / 60);
  const spentSecs = timeSpentSecs % 60;
  const timeSpentStr = `${spentMins}m ${spentSecs}s`;

  const historyEntry = {
    title: exam.config.mode === 'mock' ? 'Thi Thử Gmetrix (40 câu)' : (exam.config.mode === 'instant_learn' ? 'Học tập tức thì' : `Ôn tập (${totalQ} câu)`),
    date: new Date().toLocaleDateString('vi-VN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }),
    score,
    passed,
    correctCount,
    totalQuestions: totalQ,
    percentage: Math.round((correctCount / totalQ) * 100),
    timeSpent: timeSpentStr,
    domainStats
  };
  saveHistoryEntry(historyEntry);

  renderResultScreen(exam, historyEntry);
  switchView('result');
}

// --- RENDER RESULT SCREEN ---
function renderResultScreen(exam, result) {
  const scoreEl = document.getElementById('res-score');
  const statusEl = document.getElementById('res-status-badge');
  const detailsEl = document.getElementById('res-summary-details');

  scoreEl.textContent = result.score;
  scoreEl.className = `text-5xl font-black ${result.passed ? 'text-emerald-600' : 'text-rose-600'}`;

  statusEl.textContent = result.passed ? 'ĐẠT CHỨNG CHỈ (PASS)' : 'CHƯA ĐẠT (CẦN ÔN LẠI)';
  statusEl.className = `px-4 py-1.5 rounded-full text-sm font-extrabold ${result.passed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'}`;

  detailsEl.innerHTML = `
    Đúng <span class="font-bold text-emerald-600">${result.correctCount}/${result.totalQuestions}</span> câu (${result.percentage}%) • 
    Thời gian làm bài: <span class="font-bold text-slate-800 dark:text-slate-200">${result.timeSpent}</span> • 
    Chuẩn đỗ: <span class="font-bold text-blue-600">700/1000 điểm</span> (tương đương 28/40 câu)
  `;

  const domainBars = document.getElementById('res-domain-bars');
  const domainNames = {
    1: 'Domain 1: Phương pháp và mô hình Generative AI',
    2: 'Domain 2: Kỹ thuật xây dựng Prompt cơ bản',
    3: 'Domain 3: Tinh chỉnh Prompt & Đánh giá mô hình',
    4: 'Domain 4: Đạo đức, Pháp luật & Tác động xã hội'
  };

  domainBars.innerHTML = [1, 2, 3, 4].map(dId => {
    const stat = result.domainStats[dId] || { c: 0, t: 0 };
    const pct = stat.t > 0 ? Math.round((stat.c / stat.t) * 100) : 0;
    return `
      <div>
        <div class="flex justify-between text-xs font-semibold mb-1">
          <span>${domainNames[dId]}</span>
          <span class="${pct >= 70 ? 'text-emerald-600' : 'text-amber-600'} font-bold">${stat.c}/${stat.t} câu (${pct}%)</span>
        </div>
        <div class="w-full bg-slate-200 dark:bg-slate-700 h-2.5 rounded-full overflow-hidden">
          <div class="h-full rounded-full transition-all duration-500 ${pct >= 70 ? 'bg-emerald-500' : (pct >= 50 ? 'bg-amber-500' : 'bg-rose-500')}" style="width: ${pct}%"></div>
        </div>
      </div>
    `;
  }).join('');

  renderReviewQuestions(exam, 'all');

  document.querySelectorAll('[data-review-filter]').forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll('[data-review-filter]').forEach(b => b.classList.remove('bg-blue-600', 'text-white'));
      btn.classList.add('bg-blue-600', 'text-white');
      renderReviewQuestions(exam, btn.getAttribute('data-review-filter'));
    };
  });
}

function renderReviewQuestions(exam, filter) {
  const container = document.getElementById('res-questions-review');
  if (!container) return;

  const filtered = exam.questions.filter((q, idx) => {
    const isCorrect = evaluateQuestionScore(q, exam.answers[q.id]);
    if (filter === 'correct') return isCorrect;
    if (filter === 'incorrect') return !isCorrect;
    if (filter === 'flagged') return exam.flagged.has(q.id);
    return true;
  });

  if (filtered.length === 0) {
    container.innerHTML = `<div class="p-8 text-center text-slate-400">Không có câu hỏi nào trong mục lọc này.</div>`;
    return;
  }

  container.innerHTML = filtered.map((q, filteredIdx) => {
    const originalIdx = exam.questions.findIndex(x => x.id === q.id);
    const userAns = exam.answers[q.id];
    const isCorrect = evaluateQuestionScore(q, userAns);

    return `
      <div class="p-5 rounded-xl border ${isCorrect ? 'border-emerald-200 dark:border-emerald-900/60 bg-emerald-50/20 dark:bg-emerald-950/10' : 'border-rose-200 dark:border-rose-900/60 bg-rose-50/20 dark:bg-rose-950/10'} card-glass">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-2">
            <span class="w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs ${isCorrect ? 'bg-emerald-600 text-white' : 'bg-rose-600 text-white'}">
              ${isCorrect ? '✓' : '✗'}
            </span>
            <span class="font-bold text-sm">Câu ${originalIdx + 1}</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-medium">Domain ${q.domain_id}</span>
          </div>
          <span class="text-xs font-semibold ${isCorrect ? 'text-emerald-600' : 'text-rose-600'}">
            ${isCorrect ? '+25 điểm' : '0 điểm'}
          </span>
        </div>

        <div class="text-sm font-medium text-slate-900 dark:text-white mb-3">
          ${q.question}
        </div>

        ${q.image_url ? `
          <div class="mb-3 text-center">
            <img src="${q.image_url}" class="max-h-48 mx-auto rounded border border-slate-200 dark:border-slate-700 cursor-pointer" onclick="openImageModal('${q.image_url}')">
          </div>
        ` : ''}

        <div class="p-3 bg-white dark:bg-slate-800/80 rounded-lg text-xs space-y-1.5 border border-slate-200/80 dark:border-slate-700/80">
          <div><span class="font-bold text-slate-700 dark:text-slate-300">Câu trả lời của bạn:</span> <span class="font-bold ${isCorrect ? 'text-emerald-600' : 'text-rose-600'}">${formatUserAnswerText(q, userAns)}</span></div>
          <div><span class="font-bold text-slate-700 dark:text-slate-300">Đáp án chuẩn Certiport:</span> <span class="font-extrabold text-blue-600 dark:text-blue-400">${formatCorrectAnswerText(q)}</span></div>
        </div>

        <div class="mt-3 p-3 bg-slate-100/70 dark:bg-slate-800/50 rounded-lg text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
          <span class="font-bold text-slate-800 dark:text-slate-200">💡 Giải thích chi tiết:</span> ${q.explanation}
        </div>
      </div>
    `;
  }).join('');
}

function formatUserAnswerText(q, userAns) {
  if (!userAns) return '<span class="italic text-slate-400">Chưa trả lời (Bỏ trống)</span>';
  if (q.type === 'single_choice' || q.type === 'visual') {
    return `${userAns}. ${q.options[userAns] || ''}`;
  }
  if (q.type === 'multi_choice') {
    return Array.isArray(userAns) ? userAns.join(', ') : String(userAns);
  }
  if (q.type === 'true_false') {
    return Object.entries(userAns).map(([k, v]) => `${k.toUpperCase()}: ${v ? 'Đúng' : 'Sai'}`).join(' | ');
  }
  if (q.type === 'ordering') {
    return Array.isArray(userAns) ? userAns.join(' → ') : '';
  }
  if (q.type === 'matching') {
    return Object.entries(userAns).map(([k, v]) => `${k}-${v}`).join(', ');
  }
  return String(userAns);
}

// --- COMPREHENSIVE 4-FILE THEORY LIBRARY VIEW ---
function renderTheoryLibrary() {
  const container = document.getElementById('theory-library-content');
  const docs = (typeof THEORY_DOCS !== 'undefined' ? THEORY_DOCS : window.THEORY_DOCS);
  if (!container || !docs) {
    if (container) container.innerHTML = '<div class="p-8 text-center text-rose-500 font-bold">Đang tải dữ liệu lý thuyết... Vui lòng kiểm tra file theory_library.js</div>';
    return;
  }

  const activeTab = APP_STATE.currentTheoryTab;

  document.querySelectorAll('[data-theory-tab]').forEach(tabBtn => {
    const tabKey = tabBtn.getAttribute('data-theory-tab');
    if (tabKey === activeTab) {
      tabBtn.className = 'px-4 py-2.5 rounded-xl font-black text-xs bg-blue-600 text-white shadow-md transition';
    } else {
      tabBtn.className = 'px-4 py-2.5 rounded-xl font-bold text-xs bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 hover:border-blue-500 transition';
    }
  });

  if (activeTab === 'doc1_ebook') {
    const doc = docs.doc1_ebook;
    container.innerHTML = `
      <div class="mb-6 p-6 card-glass rounded-2xl bg-gradient-to-r from-blue-50/60 to-indigo-50/60 dark:from-slate-900/60 dark:to-slate-800/60 border border-blue-200/60 dark:border-blue-900/40">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-blue-600 text-white">Giáo Trình Cốt Lõi</span>
              <span class="text-xs text-slate-500 dark:text-slate-400">99 trang • IIG Vietnam</span>
            </div>
            <h3 class="font-black text-xl text-blue-700 dark:text-blue-400">${doc.title}</h3>
            <p class="text-xs text-slate-600 dark:text-slate-300 mt-1 max-w-2xl">${doc.description}</p>
          </div>
          <div class="flex flex-wrap gap-2">
            <a href="${encodeURI(doc.source)}" target="_blank" class="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-black text-xs rounded-xl shadow-md transition flex items-center gap-2">
              <span>📄 Mở File PDF Gốc Trong Trình Duyệt</span>
              <span>↗</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Embedded PDF Preview Toggle -->
      <details class="mb-6 card-glass rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800">
        <summary class="p-4 cursor-pointer font-bold text-xs text-blue-600 dark:text-blue-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 flex items-center justify-between">
          <span>👁️ Nhấn vào đây để xem trực tiếp toàn văn file PDF gốc (${doc.source}) ngay trên trang</span>
          <span class="text-xs text-slate-400">Xem file PDF ▾</span>
        </summary>
        <div class="p-2 bg-slate-100 dark:bg-slate-900">
          <iframe src="${encodeURI(doc.source)}" class="w-full h-[650px] rounded-xl border border-slate-300 dark:border-slate-700" title="PDF Viewer"></iframe>
        </div>
      </details>

      <div class="space-y-6">
        ${doc.domains.map(dom => `
          <div class="card-glass p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
            <h4 class="font-extrabold text-base text-slate-900 dark:text-white mb-4 pb-2 border-b border-slate-200 dark:border-slate-800 flex items-center gap-2">
              <span class="w-7 h-7 rounded-lg bg-blue-600 text-white flex items-center justify-center font-bold text-xs">${dom.id}</span>
              ${dom.name}
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              ${dom.lessons.map(l => `
                <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200/80 dark:border-slate-800 flex flex-col justify-between">
                  <div>
                    <div class="flex items-center justify-between mb-2">
                      <span class="font-extrabold text-sm text-blue-600 dark:text-blue-400">Bài ${l.num}: ${l.title}</span>
                    </div>
                    <p class="text-xs text-slate-700 dark:text-slate-300 mb-2 leading-relaxed">${l.summary}</p>
                    <div class="text-[11px] text-slate-500 mb-2 italic"><strong>So sánh/Phân biệt:</strong> ${l.diff}</div>
                    <div class="p-2.5 bg-amber-50 dark:bg-amber-950/40 rounded-lg text-[11px] text-amber-800 dark:text-amber-300 font-medium border border-amber-200/60 dark:border-amber-900/40">
                      🎯 <strong>Bẫy đề thi:</strong> ${l.exam_pointer}
                    </div>
                  </div>
                  <div class="mt-4 pt-3 border-t border-slate-200/60 dark:border-slate-800 flex justify-end">
                    <button class="px-3.5 py-1.5 text-xs font-bold rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition flex items-center gap-1.5 shadow-xs" onclick="startExamByLesson(${l.num})">
                      <span>Luyện câu hỏi bài này</span> ➜
                    </button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `).join('')}
      </div>
    `;
  } else if (activeTab === 'doc2_practical') {
    const doc = docs.doc2_practical;
    container.innerHTML = `
      <div class="mb-6 p-6 card-glass rounded-2xl bg-gradient-to-r from-emerald-50/60 to-teal-50/60 dark:from-slate-900/60 dark:to-slate-800/60 border border-emerald-200/60 dark:border-emerald-900/40">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-emerald-600 text-white">Thực Hành & Dự Án</span>
              <span class="text-xs text-slate-500 dark:text-slate-400">15 trang • 57 bài tập + Capstone Project</span>
            </div>
            <h3 class="font-black text-xl text-emerald-700 dark:text-emerald-400">${doc.title}</h3>
            <p class="text-xs text-slate-600 dark:text-slate-300 mt-1 max-w-2xl">${doc.description}</p>
          </div>
          <div>
            <a href="${encodeURI(doc.source)}" target="_blank" class="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-black text-xs rounded-xl shadow-md transition flex items-center gap-2">
              <span>📄 Mở File PDF Gốc Trong Trình Duyệt</span>
              <span>↗</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Embedded PDF Preview Toggle -->
      <details class="mb-6 card-glass rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800">
        <summary class="p-4 cursor-pointer font-bold text-xs text-emerald-600 dark:text-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 flex items-center justify-between">
          <span>👁️ Nhấn vào đây để xem trực tiếp toàn văn file PDF gốc (${doc.source}) ngay trên trang</span>
          <span class="text-xs text-slate-400">Xem file PDF ▾</span>
        </summary>
        <div class="p-2 bg-slate-100 dark:bg-slate-900">
          <iframe src="${encodeURI(doc.source)}" class="w-full h-[650px] rounded-xl border border-slate-300 dark:border-slate-700" title="PDF Viewer"></iframe>
        </div>
      </details>

      <div class="space-y-4">
        ${doc.projects_overview.map(proj => `
          <div class="card-glass p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
            <h4 class="font-bold text-sm text-emerald-700 dark:text-emerald-400 mb-3 flex items-center gap-2">
              <span>🛠️</span> ${proj.lesson}
            </h4>
            <div class="space-y-2">
              ${proj.tasks.map(t => `
                <div class="p-3 bg-slate-50 dark:bg-slate-900/40 rounded-xl text-xs text-slate-700 dark:text-slate-300 border border-slate-200/60 dark:border-slate-800 flex items-start gap-2">
                  <span class="text-emerald-600 font-bold">✓</span>
                  <span class="leading-relaxed">${t}</span>
                </div>
              `).join('')}
            </div>
          </div>
        `).join('')}
      </div>
    `;
  } else if (activeTab === 'doc3_teacher_guide') {
    const doc = docs.doc3_teacher_guide;
    container.innerHTML = `
      <div class="mb-6 p-6 card-glass rounded-2xl bg-gradient-to-r from-purple-50/60 to-indigo-50/60 dark:from-slate-900/60 dark:to-slate-800/60 border border-purple-200/60 dark:border-purple-900/40">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-purple-600 text-white">Sư Phạm & Bẫy Đề Thi</span>
              <span class="text-xs text-slate-500 dark:text-slate-400">198 trang • Chuẩn Pearson Certiport</span>
            </div>
            <h3 class="font-black text-xl text-purple-700 dark:text-purple-400">${doc.title}</h3>
            <p class="text-xs text-slate-600 dark:text-slate-300 mt-1 max-w-2xl">${doc.description}</p>
          </div>
          <div>
            <a href="${encodeURI(doc.source)}" target="_blank" class="px-4 py-2.5 bg-purple-600 hover:bg-purple-700 text-white font-black text-xs rounded-xl shadow-md transition flex items-center gap-2">
              <span>📄 Mở File PDF Gốc Trong Trình Duyệt</span>
              <span>↗</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Embedded PDF Preview Toggle -->
      <details class="mb-6 card-glass rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800">
        <summary class="p-4 cursor-pointer font-bold text-xs text-purple-600 dark:text-purple-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 flex items-center justify-between">
          <span>👁️ Nhấn vào đây để xem trực tiếp toàn văn file PDF gốc (${doc.source}) ngay trên trang</span>
          <span class="text-xs text-slate-400">Xem file PDF ▾</span>
        </summary>
        <div class="p-2 bg-slate-100 dark:bg-slate-900">
          <iframe src="${encodeURI(doc.source)}" class="w-full h-[650px] rounded-xl border border-slate-300 dark:border-slate-700" title="PDF Viewer"></iframe>
        </div>
      </details>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        ${doc.key_sections.map(sec => `
          <div class="card-glass p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
            <h4 class="font-bold text-sm text-purple-700 dark:text-purple-400 mb-2">${sec.title}</h4>
            <p class="text-xs text-slate-700 dark:text-slate-300 leading-relaxed">${sec.content}</p>
          </div>
        `).join('')}
      </div>
    `;
  } else if (activeTab === 'doc4_practice_exercises') {
    const doc = docs.doc4_practice_exercises;
    container.innerHTML = `
      <div class="mb-6 p-6 card-glass rounded-2xl bg-gradient-to-r from-amber-50/60 to-orange-50/60 dark:from-slate-900/60 dark:to-slate-800/60 border border-amber-200/60 dark:border-amber-900/40">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-amber-600 text-white">Bài Tập Chuyên Sâu</span>
              <span class="text-xs text-slate-500 dark:text-slate-400">127 trang • Tình huống & Rubric</span>
            </div>
            <h3 class="font-black text-xl text-amber-700 dark:text-amber-400">${doc.title}</h3>
            <p class="text-xs text-slate-600 dark:text-slate-300 mt-1 max-w-2xl">${doc.description}</p>
          </div>
          <div>
            <a href="${encodeURI(doc.source)}" target="_blank" class="px-4 py-2.5 bg-amber-600 hover:bg-amber-700 text-white font-black text-xs rounded-xl shadow-md transition flex items-center gap-2">
              <span>📄 Mở File PDF Gốc Trong Trình Duyệt</span>
              <span>↗</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Embedded PDF Preview Toggle -->
      <details class="mb-6 card-glass rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800">
        <summary class="p-4 cursor-pointer font-bold text-xs text-amber-600 dark:text-amber-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 flex items-center justify-between">
          <span>👁️ Nhấn vào đây để xem trực tiếp toàn văn file PDF gốc (${doc.source}) ngay trên trang</span>
          <span class="text-xs text-slate-400">Xem file PDF ▾</span>
        </summary>
        <div class="p-2 bg-slate-100 dark:bg-slate-900">
          <iframe src="${encodeURI(doc.source)}" class="w-full h-[650px] rounded-xl border border-slate-300 dark:border-slate-700" title="PDF Viewer"></iframe>
        </div>
      </details>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        ${doc.core_skills.map(sk => `
          <div class="card-glass p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
            <h4 class="font-bold text-sm text-amber-700 dark:text-amber-400 mb-2">🎯 ${sk.skill}</h4>
            <p class="text-xs text-slate-700 dark:text-slate-300 leading-relaxed">${sk.detail}</p>
          </div>
        `).join('')}
      </div>
    `;
  }
}
function switchTheoryTab(tabKey) {
  APP_STATE.currentTheoryTab = tabKey;
  renderTheoryLibrary();
}

// --- STUDY GUIDE & TRAPS EXPLORER ---
function renderStudyGuide() {
  const container = document.getElementById('study-guide-container');
  const sGuide = (typeof STUDY_GUIDE !== 'undefined' ? STUDY_GUIDE : window.STUDY_GUIDE);
  if (!container || !sGuide) return;

  const domainsHtml = sGuide.map(domain => `
    <div class="card-glass p-6 rounded-2xl mb-6">
      <div class="flex items-center gap-3 mb-2">
        <span class="w-8 h-8 rounded-lg bg-blue-600 text-white font-black flex items-center justify-center text-sm">
          ${domain.domain_id}
        </span>
        <h3 class="text-lg font-bold text-slate-900 dark:text-white">${domain.domain_name}</h3>
      </div>
      <p class="text-xs text-slate-500 mb-4">${domain.description}</p>
      
      <div class="space-y-4">
        ${domain.lessons.map(l => `
          <div class="border border-slate-200 dark:border-slate-800 rounded-xl p-4 bg-slate-50/50 dark:bg-slate-900/30">
            <h4 class="font-bold text-sm text-blue-600 dark:text-blue-400 mb-2">Bài ${l.id}: ${l.title}</h4>
            <ul class="list-disc list-inside space-y-1.5 text-xs text-slate-700 dark:text-slate-300">
              ${l.key_points.map(pt => `<li>${pt}</li>`).join('')}
            </ul>
          </div>
        `).join('')}
      </div>
    </div>
  `).join('');

  const trapsHtml = (window.TRAPS_GUIDE || []).map(t => `
    <div class="p-4 rounded-xl border border-amber-200 dark:border-amber-900/60 bg-amber-50/40 dark:bg-amber-950/20 card-glass">
      <div class="flex items-center gap-2 font-bold text-sm text-amber-800 dark:text-amber-400 mb-1.5">
        <span>⚠️ ${t.title}</span>
      </div>
      <div class="text-xs text-slate-700 dark:text-slate-300 mb-2">
        <span class="font-semibold">Tình huống ra đề:</span> ${t.trap_content}
      </div>
      <div class="p-2.5 bg-rose-50 dark:bg-rose-950/40 rounded-lg text-xs text-rose-700 dark:text-rose-300 mb-2">
        <span class="font-bold">❌ Bẫy nhầm lẫn thường gặp:</span> ${t.mistake}
      </div>
      <div class="p-2.5 bg-emerald-50 dark:bg-emerald-950/40 rounded-lg text-xs text-emerald-700 dark:text-emerald-300 font-medium">
        <span class="font-bold">✅ Quy tắc chọn đúng chuẩn:</span> ${t.correct_rule}
      </div>
    </div>
  `).join('');

  container.innerHTML = `
    <div class="mb-8">
      <h3 class="text-xl font-black mb-4 flex items-center gap-2">
        <span class="text-amber-500">🎯</span> Cẩm Nang 7 Bẫy Đề Thi Certiport / Gmetrix Hay Gặp
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        ${trapsHtml}
      </div>
    </div>
    <div>
      <h3 class="text-xl font-black mb-4 flex items-center gap-2">
        <span class="text-blue-600">📚</span> Toàn Bộ Lý Thuyết Cốt Lõi 19 Bài Học Theo 4 Domain
      </h3>
      ${domainsHtml}
    </div>
  `;
}

// --- MISTAKES NOTEBOOK VIEW ---
function renderMistakesList() {
  const container = document.getElementById('mistakes-container');
  if (!container) return;

  const mistakeQuestions = QUESTIONS_BANK.filter(q => APP_STATE.mistakeIds.has(q.id));

  if (mistakeQuestions.length === 0) {
    container.innerHTML = `
      <div class="p-12 text-center card-glass rounded-2xl">
        <div class="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto text-3xl mb-3">
          ✓
        </div>
        <h3 class="text-lg font-bold mb-1">Sổ tay câu sai đang trống!</h3>
        <p class="text-xs text-slate-400 max-w-md mx-auto">
          Tuyệt vời! Bạn chưa có câu hỏi nào làm sai hoặc đã hoàn thành ôn tập toàn bộ các câu sai trước đó.
        </p>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="mb-6 flex flex-wrap items-center justify-between gap-4 card-glass p-5 rounded-2xl">
      <div>
        <h3 class="font-bold text-base">Hiện có ${mistakeQuestions.length} câu hỏi cần củng cố lại</h3>
        <p class="text-xs text-slate-400">Các câu hỏi này được tự động thu thập từ các lần bạn làm bài thi chưa chính xác.</p>
      </div>
      <div class="flex gap-2.5">
        <button class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl shadow-sm transition" onclick="startMistakesExam()">
          🚀 Luyện tập lại tất cả câu sai
        </button>
        <button class="px-3.5 py-2 border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-semibold rounded-xl transition" onclick="clearAllMistakes()">
          Xóa toàn bộ sổ tay
        </button>
      </div>
    </div>

    <div class="space-y-4">
      ${mistakeQuestions.map((q, idx) => `
        <div class="p-5 card-glass rounded-xl border border-slate-200 dark:border-slate-800">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-blue-600 dark:text-blue-400">Domain ${q.domain_id} • ${q.lesson_title}</span>
            <button class="text-xs text-slate-400 hover:text-rose-600" onclick="removeSingleMistake('${q.id}')">✕ Bỏ khỏi sổ tay</button>
          </div>
          <div class="font-semibold text-sm mb-3 text-slate-900 dark:text-white">${idx + 1}. ${q.question}</div>
          <div class="p-3 bg-slate-50 dark:bg-slate-800/60 rounded-lg text-xs mb-2">
            <span class="font-bold">Đáp án chuẩn:</span> <span class="font-extrabold text-emerald-600">${formatCorrectAnswerText(q)}</span>
          </div>
          <div class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
            <span class="font-bold">Giải thích:</span> ${q.explanation}
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

function clearAllMistakes() {
  if (confirm('Bạn có chắc muốn xóa sạch toàn bộ câu sai khỏi sổ tay?')) {
    APP_STATE.mistakeIds.clear();
    saveMistakes();
    renderMistakesList();
  }
}

function removeSingleMistake(qId) {
  APP_STATE.mistakeIds.delete(qId);
  saveMistakes();
  renderMistakesList();
}

// --- PRINT / EXPORT EXAM SHEET ---
function openPrintView(includeAnswers = false) {
  const exam = APP_STATE.activeExam || {
    questions: QUESTIONS_BANK.slice(0, 40)
  };

  const printArea = document.getElementById('printable-exam-content');
  if (!printArea) return;

  const questionsHtml = exam.questions.map((q, idx) => `
    <div class="mb-6 page-break-inside-avoid">
      <div class="font-bold text-sm mb-1">
        Câu ${idx + 1}. (${q.lesson_title}) [25 điểm]
      </div>
      <div class="text-sm mb-2 text-justify">${q.question}</div>
      ${q.options ? `
        <div class="grid grid-cols-1 gap-1 text-xs pl-4">
          ${Object.entries(q.options).map(([k, v]) => `
            <div><strong>${k}.</strong> ${v}</div>
          `).join('')}
        </div>
      ` : ''}
      ${includeAnswers ? `
        <div class="mt-2 p-2 bg-gray-100 text-xs rounded border">
          <strong>Đáp án đúng:</strong> ${formatCorrectAnswerText(q)}<br>
          <strong>Giải thích:</strong> ${q.explanation}
        </div>
      ` : ''}
    </div>
  `).join('');

  printArea.innerHTML = `
    <div class="border-b-2 border-black pb-4 mb-6">
      <div class="text-center">
        <h3 class="text-base font-bold uppercase">SỞ GIÁO DỤC VÀ ĐÀO TẠO NGHỆ AN – TRƯỜNG THPT NGHI LỘC 3</h3>
        <h2 class="text-lg font-black uppercase mt-1">ĐỀ THI ÔN LUYỆN CUỘC THI AI OR BEHIND 2026–2027</h2>
        <p class="text-xs italic mt-0.5">Bài thi mô phỏng: Gmetrix Generative AI Foundations (Gen AI) • Thời gian: 50 phút • Thang điểm: 1000 điểm</p>
      </div>
      <div class="flex justify-between text-xs mt-4 pt-2 border-t">
        <span>Họ và tên thí sinh: ............................................................................</span>
        <span>Lớp: .................</span>
        <span>Số báo danh: .................</span>
      </div>
    </div>
    <div>${questionsHtml}</div>
  `;

  window.print();
}

// --- MODAL IMAGE VIEWER ---
function openImageModal(imgSrc) {
  const modal = document.getElementById('image-zoom-modal');
  const img = document.getElementById('image-zoom-img');
  if (modal && img) {
    img.src = imgSrc;
    modal.classList.remove('hidden');
  }
}
function closeImageModal() {
  document.getElementById('image-zoom-modal')?.classList.add('hidden');
}

// Utility: Array shuffle (Fisher-Yates)
function shuffleArray(arr) {
  const copy = [...arr];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

// Global Window Exports
window.switchView = switchView;
window.switchTheoryTab = switchTheoryTab;
window.setExamArenaMode = setExamArenaMode;
window.navigateQuestion = navigateQuestion;
window.toggleFlagCurrentQuestion = toggleFlagCurrentQuestion;
window.selectSingleChoice = selectSingleChoice;
window.toggleMultiChoice = toggleMultiChoice;
window.setTrueFalse = setTrueFalse;
window.moveOrderItem = moveOrderItem;
window.selectLeftMatchItem = selectLeftMatchItem;
window.selectRightMatchItem = selectRightMatchItem;
window.clearMatching = clearMatching;
window.checkCurrentQuestionAnswer = checkCurrentQuestionAnswer;
window.resetCurrentQuestionAnswer = resetCurrentQuestionAnswer;
window.startExamByLesson = startExamByLesson;
window.openImageModal = openImageModal;
window.closeImageModal = closeImageModal;
window.openPrintView = openPrintView;
