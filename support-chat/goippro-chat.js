/**
 * GoIPPro AI Support Chat Widget v1.0
 * Self-contained chat widget — drop into any page
 */
(function() {
  'use strict';

  const CONFIG = {
    apiUrl: 'https://goippro.com/support-chat/chat-proxy.php',
    position: 'bottom-right',
    brandColor: '#0D9488',
    brandColorHover: '#0B7E73',
    title: 'GoIPPro Support',
    subtitle: 'AI Assistant',
    placeholder: 'Ask anything about GoIPPro...',
    welcomeMessage: null, // set per language
    poweredBy: 'GoIPPro AI',
  };

  // ── i18n ──────────────────────────────────────────
  const i18n = {
    en: { title: 'GoIPPro Support', subtitle: 'AI Assistant • Online', placeholder: 'Ask anything about GoIPPro...', welcome: "Hi! 👋 I'm GoIPPro's AI assistant. I can help with:\n\n• **How to get started** and connect your GoIP\n• **Earnings estimates** for your country\n• **Technical setup** and troubleshooting\n• **Payments** in USDT/USDC\n\nWhat would you like to know?", send: 'Send', typing: 'Thinking...', error: 'Something went wrong. Try again or contact @goippro_support', offline: 'Offline — try Telegram: @goippro_support' },
    ru: { title: 'Поддержка GoIPPro', subtitle: 'AI Ассистент • Онлайн', placeholder: 'Задайте вопрос о GoIPPro...', welcome: "Привет! 👋 Я AI-ассистент GoIPPro. Могу помочь с:\n\n• **Как начать** и подключить GoIP\n• **Расчёт заработка** для вашей страны\n• **Техническая настройка** и проблемы\n• **Выплаты** в USDT/USDC\n\nЧто хотите узнать?", send: 'Отправить', typing: 'Думаю...', error: 'Ошибка. Попробуйте снова или пишите @goippro_support', offline: 'Офлайн — пишите в Telegram: @goippro_support' },
    pt: { title: 'Suporte GoIPPro', subtitle: 'Assistente IA • Online', placeholder: 'Pergunte sobre GoIPPro...', welcome: "Olá! 👋 Sou o assistente IA da GoIPPro. Posso ajudar com:\n\n• **Como começar** e conectar seu GoIP\n• **Estimativa de ganhos** para o seu país\n• **Configuração técnica** e solução de problemas\n• **Pagamentos** em USDT/USDC\n\nO que gostaria de saber?", send: 'Enviar', typing: 'Pensando...', error: 'Erro. Tente novamente ou contate @goippro_support', offline: 'Offline — Telegram: @goippro_support' },
    es: { title: 'Soporte GoIPPro', subtitle: 'Asistente IA • En línea', placeholder: 'Pregunta sobre GoIPPro...', welcome: "¡Hola! 👋 Soy el asistente IA de GoIPPro. Puedo ayudarte con:\n\n• **Cómo empezar** y conectar tu GoIP\n• **Estimación de ganancias** para tu país\n• **Configuración técnica** y problemas\n• **Pagos** en USDT/USDC\n\n¿Qué te gustaría saber?", send: 'Enviar', typing: 'Pensando...', error: 'Error. Intenta de nuevo o contacta @goippro_support', offline: 'Fuera de línea — Telegram: @goippro_support' },
    ar: { title: 'دعم GoIPPro', subtitle: 'مساعد ذكاء اصطناعي • متصل', placeholder: '...اسأل عن GoIPPro', welcome: "مرحبًا! 👋 أنا مساعد GoIPPro الذكي. يمكنني المساعدة في:\n\n• **كيفية البدء** وتوصيل جهاز GoIP\n• **تقدير الأرباح** لبلدك\n• **الإعداد التقني** واستكشاف الأخطاء\n• **المدفوعات** بـ USDT/USDC\n\nماذا تريد أن تعرف؟", send: 'إرسال', typing: '...جارٍ التفكير', error: 'خطأ. حاول مرة أخرى أو تواصل مع @goippro_support', offline: 'غير متصل — Telegram: @goippro_support' },
    tr: { title: 'GoIPPro Destek', subtitle: 'AI Asistan • Çevrimiçi', placeholder: 'GoIPPro hakkında sorun...', welcome: "Merhaba! 👋 Ben GoIPPro'nun AI asistanıyım. Yardımcı olabileceğim konular:\n\n• **Nasıl başlanır** ve GoIP bağlantısı\n• **Kazanç tahmini** ülkeniz için\n• **Teknik kurulum** ve sorun giderme\n• **Ödemeler** USDT/USDC ile\n\nNe öğrenmek istersiniz?", send: 'Gönder', typing: 'Düşünüyorum...', error: 'Hata. Tekrar deneyin veya @goippro_support ile iletişime geçin', offline: 'Çevrimdışı — Telegram: @goippro_support' },
  };

  function detectLang() {
    const path = window.location.pathname;
    const m = path.match(/^\/(ru|pt|es|ar|tr|fa|zh|ur|ko|fr)\//);
    if (m) {
      const code = m[1];
      if (i18n[code]) return code;
    }
    const htmlLang = document.documentElement.lang || '';
    if (i18n[htmlLang]) return htmlLang;
    return 'en';
  }

  const lang = detectLang();
  const t = i18n[lang] || i18n.en;
  const isRTL = (lang === 'ar');

  // ── State ─────────────────────────────────────────
  let isOpen = false;
  let sessionId = localStorage.getItem('goippro_chat_session') || null;
  let messages = [];
  let isLoading = false;

  // ── Styles ────────────────────────────────────────
  const CSS = `
    #gip-chat-fab {
      position: fixed; bottom: 24px; right: 24px; z-index: 99999;
      width: 60px; height: 60px; border-radius: 50%;
      background: ${CONFIG.brandColor}; border: none; cursor: pointer;
      box-shadow: 0 4px 20px rgba(13,148,136,0.4);
      display: flex; align-items: center; justify-content: center;
      transition: all 0.3s cubic-bezier(.4,0,.2,1);
      animation: gip-pulse 2s infinite;
    }
    #gip-chat-fab:hover { transform: scale(1.1); background: ${CONFIG.brandColorHover}; }
    #gip-chat-fab svg { width: 28px; height: 28px; fill: white; transition: transform 0.3s; }
    #gip-chat-fab.open svg { transform: rotate(90deg); }
    @keyframes gip-pulse {
      0%, 100% { box-shadow: 0 4px 20px rgba(13,148,136,0.4); }
      50% { box-shadow: 0 4px 30px rgba(13,148,136,0.6); }
    }

    #gip-chat-window {
      position: fixed; bottom: 96px; right: 24px; z-index: 99998;
      width: 380px; max-width: calc(100vw - 32px); height: 520px; max-height: calc(100vh - 120px);
      background: #fff; border-radius: 16px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.15);
      display: flex; flex-direction: column;
      opacity: 0; transform: translateY(20px) scale(0.95);
      pointer-events: none; transition: all 0.3s cubic-bezier(.4,0,.2,1);
      overflow: hidden; font-family: 'Inter', -apple-system, sans-serif;
      direction: ${isRTL ? 'rtl' : 'ltr'};
    }
    #gip-chat-window.open {
      opacity: 1; transform: translateY(0) scale(1); pointer-events: all;
    }

    .gip-header {
      background: linear-gradient(135deg, ${CONFIG.brandColor}, #0B7E73);
      color: white; padding: 16px 20px; display: flex; align-items: center; gap: 12px;
      flex-shrink: 0;
    }
    .gip-header-icon {
      width: 40px; height: 40px; background: rgba(255,255,255,0.2);
      border-radius: 10px; display: flex; align-items: center; justify-content: center;
      font-size: 20px; flex-shrink: 0;
    }
    .gip-header-text h3 { margin: 0; font-size: 15px; font-weight: 600; }
    .gip-header-text p { margin: 2px 0 0; font-size: 12px; opacity: 0.85; }
    .gip-header-dot { width: 8px; height: 8px; background: #4ADE80; border-radius: 50%; display: inline-block; margin-${isRTL ? 'left' : 'right'}: 4px; }

    .gip-messages {
      flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px;
      scroll-behavior: smooth;
    }
    .gip-messages::-webkit-scrollbar { width: 4px; }
    .gip-messages::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 2px; }

    .gip-msg {
      max-width: 85%; padding: 10px 14px; border-radius: 14px;
      font-size: 14px; line-height: 1.5; word-wrap: break-word;
      animation: gip-fadeIn 0.3s ease;
    }
    .gip-msg.bot {
      align-self: flex-start; background: #f1f5f9; color: #1e293b;
      border-bottom-${isRTL ? 'right' : 'left'}-radius: 4px;
    }
    .gip-msg.user {
      align-self: flex-end; background: ${CONFIG.brandColor}; color: white;
      border-bottom-${isRTL ? 'left' : 'right'}-radius: 4px;
    }
    .gip-msg.bot strong { font-weight: 600; }
    .gip-msg.bot p { margin: 4px 0; }
    .gip-msg.bot ul, .gip-msg.bot ol { margin: 4px 0; padding-${isRTL ? 'right' : 'left'}: 20px; }
    .gip-msg.bot li { margin: 2px 0; }
    .gip-msg.bot code { background: #e2e8f0; padding: 1px 4px; border-radius: 3px; font-size: 13px; }

    .gip-typing {
      align-self: flex-start; padding: 10px 14px; background: #f1f5f9;
      border-radius: 14px; border-bottom-${isRTL ? 'right' : 'left'}-radius: 4px;
      font-size: 13px; color: #64748b; display: none;
    }
    .gip-typing.show { display: block; animation: gip-fadeIn 0.2s ease; }
    .gip-typing-dots { display: inline-flex; gap: 4px; }
    .gip-typing-dots span {
      width: 6px; height: 6px; background: #94a3b8; border-radius: 50%;
      animation: gip-bounce 1.4s infinite;
    }
    .gip-typing-dots span:nth-child(2) { animation-delay: 0.2s; }
    .gip-typing-dots span:nth-child(3) { animation-delay: 0.4s; }

    .gip-input-area {
      padding: 12px 16px; border-top: 1px solid #e2e8f0;
      display: flex; gap: 8px; align-items: center; flex-shrink: 0;
      background: #fafafa;
    }
    .gip-input {
      flex: 1; border: 1px solid #e2e8f0; border-radius: 10px;
      padding: 10px 14px; font-size: 14px; outline: none;
      font-family: inherit; resize: none; max-height: 80px;
      transition: border-color 0.2s; direction: ${isRTL ? 'rtl' : 'ltr'};
    }
    .gip-input:focus { border-color: ${CONFIG.brandColor}; }
    .gip-send-btn {
      width: 40px; height: 40px; border: none; border-radius: 10px;
      background: ${CONFIG.brandColor}; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      transition: all 0.2s; flex-shrink: 0;
    }
    .gip-send-btn:hover { background: ${CONFIG.brandColorHover}; }
    .gip-send-btn:disabled { background: #cbd5e1; cursor: not-allowed; }
    .gip-send-btn svg { width: 18px; height: 18px; fill: white; }

    .gip-quick-btns {
      display: flex; flex-wrap: wrap; gap: 6px; padding: 0 16px 12px;
    }
    .gip-quick-btn {
      padding: 6px 12px; border: 1px solid #e2e8f0; border-radius: 20px;
      background: white; cursor: pointer; font-size: 12px; color: #475569;
      transition: all 0.2s; font-family: inherit;
    }
    .gip-quick-btn:hover { border-color: ${CONFIG.brandColor}; color: ${CONFIG.brandColor}; background: #f0fdfa; }

    @keyframes gip-fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes gip-bounce { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-4px); } }

    @media (max-width: 480px) {
      #gip-chat-window { width: calc(100vw - 16px); right: 8px; bottom: 80px; height: calc(100vh - 100px); border-radius: 12px; }
      #gip-chat-fab { bottom: 16px; right: 16px; width: 54px; height: 54px; }
    }
  `;

  // ── Simple Markdown Parser ────────────────────────
  function parseMd(text) {
    return text
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/`(.+?)`/g, '<code>$1</code>')
      .replace(/^### (.+)$/gm, '<strong>$1</strong>')
      .replace(/^## (.+)$/gm, '<strong>$1</strong>')
      .replace(/^# (.+)$/gm, '<strong>$1</strong>')
      .replace(/^\- (.+)$/gm, '• $1')
      .replace(/^\* (.+)$/gm, '• $1')
      .replace(/\n/g, '<br>');
  }

  // ── Build DOM ─────────────────────────────────────
  function init() {
    // Inject CSS
    const style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    // FAB button
    const fab = document.createElement('button');
    fab.id = 'gip-chat-fab';
    fab.setAttribute('aria-label', 'Open support chat');
    fab.innerHTML = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/><path d="M7 9h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/></svg>';
    fab.onclick = toggle;
    document.body.appendChild(fab);

    // Chat window
    const win = document.createElement('div');
    win.id = 'gip-chat-window';
    win.innerHTML = `
      <div class="gip-header">
        <div class="gip-header-icon">🤖</div>
        <div class="gip-header-text">
          <h3>${t.title}</h3>
          <p><span class="gip-header-dot"></span>${t.subtitle}</p>
        </div>
      </div>
      <div class="gip-messages" id="gip-msgs"></div>
      <div class="gip-quick-btns" id="gip-quick"></div>
      <div class="gip-input-area">
        <textarea class="gip-input" id="gip-input" rows="1" placeholder="${t.placeholder}"></textarea>
        <button class="gip-send-btn" id="gip-send" aria-label="${t.send}">
          <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
        </button>
      </div>
    `;
    document.body.appendChild(win);

    // Quick buttons
    const quickBtns = getQuickButtons();
    const quickEl = document.getElementById('gip-quick');
    quickBtns.forEach(q => {
      const btn = document.createElement('button');
      btn.className = 'gip-quick-btn';
      btn.textContent = q;
      btn.onclick = () => { sendMessage(q); quickEl.style.display = 'none'; };
      quickEl.appendChild(btn);
    });

    // Input handlers
    const input = document.getElementById('gip-input');
    const sendBtn = document.getElementById('gip-send');
    sendBtn.onclick = () => sendFromInput();
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendFromInput(); }
    });
    input.addEventListener('input', () => {
      input.style.height = 'auto';
      input.style.height = Math.min(input.scrollHeight, 80) + 'px';
    });
  }

  function getQuickButtons() {
    const btns = {
      en: ['How to start?', 'How much can I earn?', 'Supported devices', 'Payment info'],
      ru: ['Как начать?', 'Сколько можно заработать?', 'Какие устройства?', 'Как оплата?'],
      pt: ['Como começar?', 'Quanto posso ganhar?', 'Dispositivos suportados', 'Pagamentos'],
      es: ['¿Cómo empezar?', '¿Cuánto puedo ganar?', 'Dispositivos', 'Pagos'],
      ar: ['كيف أبدأ؟', 'كم يمكنني أن أكسب؟', 'الأجهزة المدعومة', 'معلومات الدفع'],
      tr: ['Nasıl başlarım?', 'Ne kadar kazanabilirim?', 'Desteklenen cihazlar', 'Ödeme bilgisi'],
    };
    return btns[lang] || btns.en;
  }

  function toggle() {
    isOpen = !isOpen;
    document.getElementById('gip-chat-window').classList.toggle('open', isOpen);
    document.getElementById('gip-chat-fab').classList.toggle('open', isOpen);
    if (isOpen && messages.length === 0) {
      addBotMessage(t.welcome);
    }
    if (isOpen) {
      setTimeout(() => document.getElementById('gip-input').focus(), 300);
    }
  }

  function addBotMessage(text) {
    messages.push({ role: 'bot', text });
    renderMessages();
  }

  function addUserMessage(text) {
    messages.push({ role: 'user', text });
    renderMessages();
  }

  function renderMessages() {
    const container = document.getElementById('gip-msgs');
    container.innerHTML = messages.map(m =>
      `<div class="gip-msg ${m.role}">${m.role === 'bot' ? parseMd(m.text) : escHtml(m.text)}</div>`
    ).join('') + `<div class="gip-typing ${isLoading ? 'show' : ''}" id="gip-typing">
      <div class="gip-typing-dots"><span></span><span></span><span></span></div>
    </div>`;
    container.scrollTop = container.scrollHeight;
  }

  function escHtml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  function sendFromInput() {
    const input = document.getElementById('gip-input');
    const text = input.value.trim();
    if (!text || isLoading) return;
    input.value = '';
    input.style.height = 'auto';
    sendMessage(text);
  }

  async function sendMessage(text) {
    addUserMessage(text);
    isLoading = true;
    renderMessages();
    document.getElementById('gip-send').disabled = true;

    try {
      const resp = await fetch(CONFIG.apiUrl + '?path=api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: sessionId }),
      });

      const data = await resp.json();
      if (data.session_id) {
        sessionId = data.session_id;
        try { localStorage.setItem('goippro_chat_session', sessionId); } catch(e) {}
      }
      addBotMessage(data.answer || t.error);
    } catch (err) {
      console.error('GoIPPro chat error:', err);
      addBotMessage(t.error);
    }

    isLoading = false;
    renderMessages();
    document.getElementById('gip-send').disabled = false;
  }

  // ── Init on DOM ready ─────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
