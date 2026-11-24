import re

with open('app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace initExamState to include checkedQuestions: new Set()
old_init = """  APP_STATE.activeExam = {
    config,
    questions,
    currentIndex: 0,
    answers: {},
    flagged: new Set(),
    startTime: Date.now(),
    timeRemaining: timeLimitSeconds,
    timeSpent: 0,
    timerInterval: null,
    submitted: false
  };"""

new_init = """  APP_STATE.activeExam = {
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
  };"""

assert old_init in code, "initExamState not found!"
code = code.replace(old_init, new_init)

# Now replace renderQuestion and input renderers and feedback
# Let's find from 'function renderQuestion(idx)' down to 'function submitExam()'
p_start = code.find('// --- RENDER QUESTION CARD ---')
p_end = code.find('// --- SUBMIT EXAM & GENERATE RESULT ---')
assert p_start != -1 and p_end != -1, "Section bounds not found!"

new_question_section = '''// --- RENDER QUESTION CARD ---
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
'''

code = code[:p_start] + new_question_section + code[p_end:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.js successfully with the new non-leaking check logic!")
