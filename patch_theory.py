import re

with open('app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace renderTheoryLibrary with robust implementation
old_func_start = code.find('function renderTheoryLibrary()')
old_func_end = code.find('function switchTheoryTab(tabKey)')

assert old_func_start != -1 and old_func_end != -1, "renderTheoryLibrary bounds not found!"

new_func = '''function renderTheoryLibrary() {
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
'''

code = code[:old_func_start] + new_func + code[old_func_end:]

# Also update renderStudyGuide to use fallback:
code = code.replace("if (!container || !window.STUDY_GUIDE) return;", "const sGuide = (typeof STUDY_GUIDE !== 'undefined' ? STUDY_GUIDE : window.STUDY_GUIDE);\n  if (!container || !sGuide) return;")
code = code.replace("STUDY_GUIDE.map", "sGuide.map")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.js with robust theory library renderer & PDF viewer links!")
