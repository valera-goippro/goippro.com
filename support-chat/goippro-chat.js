/**
 * GoIPPro AI Support Chat + Voice Widget v2.0
 * Text chat + voice input with auto language detection
 */
(function() {
  'use strict';

  const CFG = {
    apiUrl: 'https://goippro.com/support-chat/chat-proxy.php',
    brandColor: '#0D9488',
    brandHover: '#0B7E73',
  };

  // ── i18n ──────────────────────────────────────────
  const i18n = {
    en: { title: 'GoIPPro Support', subtitle: 'AI Assistant • Online', placeholder: 'Ask anything about GoIPPro...', welcome: "Hi! 👋 I'm GoIPPro's AI assistant. I can help with:\n\n• **How to get started** and connect your GoIP\n• **Earnings estimates** for your country\n• **Technical setup** and troubleshooting\n• **Payments** in USDT/USDC\n\nAsk me anything — type or tap the 🎤 microphone!", send: 'Send', typing: 'Thinking...', error: 'Something went wrong. Try again or contact @goippro_support', listening: 'Listening...', processing: 'Processing voice...', micHint: 'Hold to speak', voiceError: 'Could not process voice. Try again or type your question.', humanBtn:'Talk to human',escalated:'Our team has been notified!',escalateAsk:'Would you like to speak with a live operator?' },
    ru: { title: 'Поддержка GoIPPro', subtitle: 'AI Ассистент • Онлайн', placeholder: 'Задайте вопрос о GoIPPro...', welcome: "Привет! 👋 Я AI-ассистент GoIPPro. Могу помочь с:\n\n• **Как начать** и подключить GoIP\n• **Расчёт заработка** для вашей страны\n• **Техническая настройка** и проблемы\n• **Выплаты** в USDT/USDC\n\nСпрашивайте — пишите или нажмите 🎤 микрофон!", send: 'Отправить', typing: 'Думаю...', error: 'Ошибка. Попробуйте снова или пишите @goippro_support', listening: 'Слушаю...', processing: 'Обрабатываю голос...', micHint: 'Удерживайте для записи', voiceError: 'Не удалось обработать голос. Попробуйте снова.', humanBtn:'Живой оператор',escalated:'Наша команда уведомлена!',escalateAsk:'Хотите связаться с оператором?' },
    pt: { title: 'Suporte GoIPPro', subtitle: 'Assistente IA • Online', placeholder: 'Pergunte sobre GoIPPro...', welcome: "Olá! 👋 Sou o assistente IA da GoIPPro. Posso ajudar com:\n\n• **Como começar** e conectar seu GoIP\n• **Estimativa de ganhos** para o seu país\n• **Configuração técnica** e problemas\n• **Pagamentos** em USDT/USDC\n\nPergunte — digite ou toque no 🎤 microfone!", send: 'Enviar', typing: 'Pensando...', error: 'Erro. Tente novamente ou contate @goippro_support', listening: 'Ouvindo...', processing: 'Processando voz...', micHint: 'Segure para falar', voiceError: 'Não foi possível processar a voz. Tente novamente.', humanBtn:'Falar com humano',escalated:'Nossa equipe foi notificada!',escalateAsk:'Deseja falar com um atendente?' },
    es: { title: 'Soporte GoIPPro', subtitle: 'Asistente IA • En línea', placeholder: 'Pregunta sobre GoIPPro...', welcome: "¡Hola! 👋 Soy el asistente IA de GoIPPro. Puedo ayudarte con:\n\n• **Cómo empezar** y conectar tu GoIP\n• **Estimación de ganancias** para tu país\n• **Configuración técnica** y problemas\n• **Pagos** en USDT/USDC\n\n¡Pregúntame — escribe o toca el 🎤 micrófono!", send: 'Enviar', typing: 'Pensando...', error: 'Error. Intenta de nuevo o contacta @goippro_support', listening: 'Escuchando...', processing: 'Procesando voz...', micHint: 'Mantén para hablar', voiceError: 'No se pudo procesar la voz. Intenta de nuevo.', humanBtn:'Hablar con humano',escalated:'Nuestro equipo ha sido notificado!',escalateAsk:'¿Desea hablar con un operador?' },
    ar: { title: 'دعم GoIPPro', subtitle: 'مساعد ذكاء اصطناعي • متصل', placeholder: '...اسأل عن GoIPPro', welcome: "مرحبًا! 👋 أنا مساعد GoIPPro الذكي. يمكنني المساعدة في:\n\n• **كيفية البدء** وتوصيل جهاز GoIP\n• **تقدير الأرباح** لبلدك\n• **الإعداد التقني** واستكشاف الأخطاء\n• **المدفوعات** بـ USDT/USDC\n\nاسأل — اكتب أو اضغط على 🎤 الميكروفون!", send: 'إرسال', typing: '...جارٍ التفكير', error: 'خطأ. حاول مرة أخرى', listening: '...أستمع', processing: '...جارٍ معالجة الصوت', micHint: 'اضغط مع الاستمرار للتحدث', voiceError: 'تعذرت معالجة الصوت.', humanBtn:'تحدث مع شخص',escalated:'تم إبلاغ فريقنا!',escalateAsk:'هل تريد التحدث مع شخص؟' },
    tr: { title: 'GoIPPro Destek', subtitle: 'AI Asistan • Çevrimiçi', placeholder: 'GoIPPro hakkında sorun...', welcome: "Merhaba! 👋 Ben GoIPPro AI asistanıyım. Yardımcı olabileceğim konular:\n\n• **Nasıl başlanır** ve GoIP bağlantısı\n• **Kazanç tahmini** ülkeniz için\n• **Teknik kurulum** ve sorun giderme\n• **Ödemeler** USDT/USDC ile\n\nSorun — yazın veya 🎤 mikrofona basın!", send: 'Gönder', typing: 'Düşünüyorum...', error: 'Hata. Tekrar deneyin.', listening: 'Dinliyorum...', processing: 'Ses işleniyor...', micHint: 'Konuşmak için basılı tutun', voiceError: 'Ses işlenemedi. Tekrar deneyin.', humanBtn:'Operatörle konuş',escalated:'Ekibimiz bilgilendirildi!',escalateAsk:'Bir operatörle konuşmak ister misiniz?' },
  };

  function detectLang() {
    const m = window.location.pathname.match(/^\/(ru|pt|es|ar|tr|fa|zh|ur|ko|fr)\//);
    if (m && i18n[m[1]]) return m[1];
    const h = document.documentElement.lang || '';
    if (i18n[h]) return h;
    return 'en';
  }

  const lang = detectLang();
  const t = i18n[lang] || i18n.en;
  const isRTL = (lang === 'ar');
  const S = isRTL ? 'right' : 'left'; // start side
  const E = isRTL ? 'left' : 'right'; // end side

  let isOpen = false, sessionId = null, messages = [], isLoading = false;
  let mediaRecorder = null, audioChunks = [], isRecording = false;

  try { sessionId = localStorage.getItem('goippro_chat_session'); } catch(e) {}

  // ── Styles ────────────────────────────────────────
  const CSS = `
    #gip-chat-fab {
      position:fixed; bottom:24px; ${E}:24px; z-index:99999;
      width:60px; height:60px; border-radius:50%;
      background:${CFG.brandColor}; border:none; cursor:pointer;
      box-shadow:0 4px 20px rgba(13,148,136,0.4);
      display:flex; align-items:center; justify-content:center;
      transition:all .3s cubic-bezier(.4,0,.2,1);
      animation:gip-pulse 2s infinite;
    }
    #gip-chat-fab:hover { transform:scale(1.1); background:${CFG.brandHover}; }
    #gip-chat-fab svg { width:28px; height:28px; fill:#fff; transition:transform .3s; }
    #gip-chat-fab.open svg { transform:rotate(90deg); }
    @keyframes gip-pulse { 0%,100%{box-shadow:0 4px 20px rgba(13,148,136,0.4)} 50%{box-shadow:0 4px 30px rgba(13,148,136,0.6)} }

    #gip-chat-window {
      position:fixed; bottom:96px; ${E}:24px; z-index:99998;
      width:400px; max-width:calc(100vw - 32px); height:560px; max-height:calc(100vh - 120px);
      background:#fff; border-radius:16px;
      box-shadow:0 8px 40px rgba(0,0,0,0.15);
      display:flex; flex-direction:column;
      opacity:0; transform:translateY(20px) scale(.95);
      pointer-events:none; transition:all .3s cubic-bezier(.4,0,.2,1);
      overflow:hidden; font-family:'Inter',-apple-system,sans-serif;
      direction:${isRTL?'rtl':'ltr'};
    }
    #gip-chat-window.open { opacity:1; transform:translateY(0) scale(1); pointer-events:all; }

    .gip-header {
      background:linear-gradient(135deg,${CFG.brandColor},#0B7E73);
      color:#fff; padding:16px 20px; display:flex; align-items:center; gap:12px; flex-shrink:0;
    }
    .gip-header-icon { width:40px; height:40px; background:rgba(255,255,255,0.2); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px; flex-shrink:0; }
    .gip-header-text h3 { margin:0; font-size:15px; font-weight:600; }
    .gip-header-text p { margin:2px 0 0; font-size:12px; opacity:.85; }
    .gip-header-dot { width:8px; height:8px; background:#4ADE80; border-radius:50%; display:inline-block; margin-${E}:4px; }

    .gip-messages { flex:1; overflow-y:auto; padding:16px; display:flex; flex-direction:column; gap:12px; scroll-behavior:smooth; }
    .gip-messages::-webkit-scrollbar { width:4px; }
    .gip-messages::-webkit-scrollbar-thumb { background:#cbd5e1; border-radius:2px; }

    .gip-msg { max-width:85%; padding:10px 14px; border-radius:14px; font-size:14px; line-height:1.5; word-wrap:break-word; animation:gip-fadeIn .3s ease; }
    .gip-msg.bot { align-self:flex-start; background:#f1f5f9; color:#1e293b; border-bottom-${S}-radius:4px; }
    .gip-msg.user { align-self:flex-end; background:${CFG.brandColor}; color:#fff; border-bottom-${E}-radius:4px; }
    .gip-msg.bot strong { font-weight:600; }
    .gip-msg.bot p { margin:4px 0; }

    .gip-msg .gip-voice-label { display:flex; align-items:center; gap:4px; font-size:11px; opacity:.7; margin-bottom:4px; }

    .gip-msg .gip-audio-player { margin-top:8px; }
    .gip-msg .gip-audio-player audio { width:100%; height:32px; border-radius:8px; }

    .gip-typing { align-self:flex-start; padding:10px 14px; background:#f1f5f9; border-radius:14px; border-bottom-${S}-radius:4px; font-size:13px; color:#64748b; display:none; }
    .gip-typing.show { display:block; animation:gip-fadeIn .2s ease; }
    .gip-typing-dots { display:inline-flex; gap:4px; }
    .gip-typing-dots span { width:6px; height:6px; background:#94a3b8; border-radius:50%; animation:gip-bounce 1.4s infinite; }
    .gip-typing-dots span:nth-child(2) { animation-delay:.2s; }
    .gip-typing-dots span:nth-child(3) { animation-delay:.4s; }

    .gip-input-area { padding:12px 16px; border-top:1px solid #e2e8f0; display:flex; gap:8px; align-items:center; flex-shrink:0; background:#fafafa; }
    .gip-input { flex:1; border:1px solid #e2e8f0; border-radius:10px; padding:10px 14px; font-size:14px; outline:none; font-family:inherit; resize:none; max-height:80px; transition:border-color .2s; direction:${isRTL?'rtl':'ltr'}; }
    .gip-input:focus { border-color:${CFG.brandColor}; }

    .gip-btn { width:40px; height:40px; border:none; border-radius:10px; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:all .2s; flex-shrink:0; }
    .gip-send-btn { background:${CFG.brandColor}; }
    .gip-send-btn:hover { background:${CFG.brandHover}; }
    .gip-send-btn:disabled { background:#cbd5e1; cursor:not-allowed; }
    .gip-send-btn svg { width:18px; height:18px; fill:#fff; }

    .gip-mic-btn { background:#f1f5f9; border:1px solid #e2e8f0; }
    .gip-mic-btn:hover { background:#e2e8f0; }
    .gip-mic-btn.recording { background:#EF4444; border-color:#EF4444; animation:gip-mic-pulse 1s infinite; }
    .gip-mic-btn svg { width:20px; height:20px; fill:#64748b; }
    .gip-mic-btn.recording svg { fill:#fff; }
    @keyframes gip-mic-pulse { 0%,100%{box-shadow:0 0 0 0 rgba(239,68,68,0.4)} 50%{box-shadow:0 0 0 8px rgba(239,68,68,0)} }

    .gip-voice-status { font-size:12px; color:#64748b; text-align:center; padding:4px 0; animation:gip-fadeIn .2s; }

    .gip-quick-btns { display:flex; flex-wrap:wrap; gap:6px; padding:0 16px 12px; }
    .gip-quick-btn { padding:6px 12px; border:1px solid #e2e8f0; border-radius:20px; background:#fff; cursor:pointer; font-size:12px; color:#475569; transition:all .2s; font-family:inherit; }
    .gip-quick-btn:hover { border-color:${CFG.brandColor}; color:${CFG.brandColor}; background:#f0fdfa; }

    
    .gip-human-btn { 
      margin-${isRTL?'right':'left'}:auto; background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.3); 
      border-radius:8px; color:#fff; padding:4px 10px; font-size:11px; cursor:pointer; 
      font-family:inherit; transition:all .2s; white-space:nowrap;
    }
    .gip-human-btn:hover { background:rgba(255,255,255,0.35); }
    .gip-escalated { background:#FEF3C7; border:1px solid #FCD34D; border-radius:10px; padding:10px 14px; 
      margin:8px 16px; font-size:13px; color:#92400E; text-align:center; animation:gip-fadeIn .3s; }

    @keyframes gip-fadeIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
    @keyframes gip-bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-4px)} }
    @media(max-width:480px) {
      #gip-chat-window { width:calc(100vw - 16px); ${E}:8px; bottom:80px; height:calc(100vh - 100px); border-radius:12px; }
      #gip-chat-fab { bottom:16px; ${E}:16px; width:54px; height:54px; }
    }
  `;

  function parseMd(text) {
    return text
      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
      .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
      .replace(/\*(.+?)\*/g,'<em>$1</em>')
      .replace(/`(.+?)`/g,'<code>$1</code>')
      .replace(/^### (.+)$/gm,'<strong>$1</strong>')
      .replace(/^## (.+)$/gm,'<strong>$1</strong>')
      .replace(/^# (.+)$/gm,'<strong>$1</strong>')
      .replace(/^\- (.+)$/gm,'• $1')
      .replace(/^\* (.+)$/gm,'• $1')
      .replace(/\n/g,'<br>');
  }
  function escHtml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  function init() {
    const style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    // FAB
    const fab = document.createElement('button');
    fab.id = 'gip-chat-fab';
    fab.setAttribute('aria-label','Open support chat');
    fab.innerHTML = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/><path d="M7 9h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/></svg>';
    fab.onclick = toggle;
    document.body.appendChild(fab);

    // Window
    const win = document.createElement('div');
    win.id = 'gip-chat-window';
    win.innerHTML = `
      <div class="gip-header">
        <div class="gip-header-icon">🤖</div>
        <div class="gip-header-text">
          <h3>${t.title}</h3>
          <p><span class="gip-header-dot"></span>${t.subtitle}</p>
        </div>
        <button class="gip-human-btn" id="gip-human" onclick="window._gipEscalate && window._gipEscalate()">${t.humanBtn || 'Talk to human'}</button>
      </div>
      <div class="gip-messages" id="gip-msgs"></div>
      <div class="gip-quick-btns" id="gip-quick"></div>
      <div id="gip-voice-status" class="gip-voice-status" style="display:none"></div>
      <div class="gip-input-area">
        <button class="gip-btn gip-mic-btn" id="gip-mic" aria-label="Voice input" title="${t.micHint}">
          <svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1-9c0-.55.45-1 1-1s1 .45 1 1v6c0 .55-.45 1-1 1s-1-.45-1-1V5z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
        </button>
        <textarea class="gip-input" id="gip-input" rows="1" placeholder="${t.placeholder}"></textarea>
        <button class="gip-btn gip-send-btn" id="gip-send" aria-label="${t.send}">
          <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
        </button>
      </div>`;
    document.body.appendChild(win);

    // Quick buttons
    const quickBtns = getQuickButtons();
    const quickEl = document.getElementById('gip-quick');
    quickBtns.forEach(q => {
      const btn = document.createElement('button');
      btn.className = 'gip-quick-btn'; btn.textContent = q;
      btn.onclick = () => { sendMessage(q); quickEl.style.display = 'none'; };
      quickEl.appendChild(btn);
    });

    // Input handlers
    const input = document.getElementById('gip-input');
    document.getElementById('gip-send').onclick = () => sendFromInput();
    input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendFromInput(); } });
    input.addEventListener('input', () => { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 80) + 'px'; });

    // Mic button — click to toggle recording
    const micBtn = document.getElementById('gip-mic');
    micBtn.addEventListener('click', toggleRecording);
  }

  function getQuickButtons() {
    const b = {
      en: ['How to start?','How much can I earn?','Supported devices','Payment info'],
      ru: ['Как начать?','Сколько можно заработать?','Какие устройства?','Как оплата?'],
      pt: ['Como começar?','Quanto posso ganhar?','Dispositivos','Pagamentos'],
      es: ['¿Cómo empezar?','¿Cuánto puedo ganar?','Dispositivos','Pagos'],
      ar: ['كيف أبدأ؟','كم يمكنني أن أكسب؟','الأجهزة المدعومة','معلومات الدفع'],
      tr: ['Nasıl başlarım?','Ne kadar kazanabilirim?','Cihazlar','Ödeme bilgisi'],
    };
    return b[lang] || b.en;
  }

  function toggle() {
    isOpen = !isOpen;
    document.getElementById('gip-chat-window').classList.toggle('open', isOpen);
    document.getElementById('gip-chat-fab').classList.toggle('open', isOpen);
    if (isOpen && messages.length === 0) addBotMessage(t.welcome);
    if (isOpen) setTimeout(() => document.getElementById('gip-input').focus(), 300);
  }

  function addBotMessage(text, audio) {
    messages.push({ role: 'bot', text, audio: audio || null });
    renderMessages();
  }
  function addUserMessage(text, isVoice) {
    messages.push({ role: 'user', text, isVoice: !!isVoice });
    renderMessages();
  }

  function renderMessages() {
    const c = document.getElementById('gip-msgs');
    c.innerHTML = messages.map(m => {
      let inner = '';
      if (m.role === 'bot') {
        inner = parseMd(m.text);
        if (m.audio) {
          inner += `<div class="gip-audio-player"><audio controls src="${m.audio}" preload="auto"></audio></div>`;
        }
      } else {
        if (m.isVoice) inner = '<div class="gip-voice-label">🎤 </div>' + escHtml(m.text);
        else inner = escHtml(m.text);
      }
      return `<div class="gip-msg ${m.role}">${inner}</div>`;
    }).join('') + `<div class="gip-typing ${isLoading?'show':''}" id="gip-typing"><div class="gip-typing-dots"><span></span><span></span><span></span></div></div>`;
    c.scrollTop = c.scrollHeight;
  }

  function sendFromInput() {
    const input = document.getElementById('gip-input');
    const text = input.value.trim();
    if (!text || isLoading) return;
    input.value = ''; input.style.height = 'auto';
    sendMessage(text);
  }

  async function sendMessage(text) {
    addUserMessage(text, false);
    isLoading = true; renderMessages();
    document.getElementById('gip-send').disabled = true;
    try {
      const resp = await fetch(CFG.apiUrl + '?path=api/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: sessionId }),
      });
      const data = await resp.json();
      if (data.session_id) { sessionId = data.session_id; try { localStorage.setItem('goippro_chat_session', sessionId); } catch(e) {} }
      addBotMessage(data.answer || t.error);
      // Auto-escalation triggered by AI
      if (data.escalated) {
        const banner = document.createElement('div');
        banner.className = 'gip-escalated';
        banner.innerHTML = '✅ ' + (t.escalated || 'Our team has been notified!');
        const msgs = document.getElementById('gip-msgs');
        msgs.parentNode.insertBefore(banner, msgs.nextSibling);
      }
    } catch (err) {
      console.error('GoIPPro chat error:', err);
      addBotMessage(t.error);
    }
    isLoading = false; renderMessages();
    document.getElementById('gip-send').disabled = false;
  }

  // ── Voice Recording ───────────────────────────────
  function showVoiceStatus(msg) {
    const el = document.getElementById('gip-voice-status');
    if (msg) { el.textContent = msg; el.style.display = 'block'; }
    else { el.style.display = 'none'; }
  }

  async function toggleRecording() {
    if (isRecording) {
      stopRecording();
    } else {
      await startRecording();
    }
  }

  async function startRecording() {
    const micBtn = document.getElementById('gip-mic');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks = [];

      // Try webm first, fallback to whatever is available
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus') ? 'audio/webm;codecs=opus'
        : MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm'
        : MediaRecorder.isTypeSupported('audio/mp4') ? 'audio/mp4' : '';

      mediaRecorder = new MediaRecorder(stream, mimeType ? { mimeType } : {});
      mediaRecorder.ondataavailable = e => { if (e.data.size > 0) audioChunks.push(e.data); };
      mediaRecorder.onstop = () => {
        stream.getTracks().forEach(t => t.stop());
        processVoice();
      };
      mediaRecorder.start(100);
      isRecording = true;
      micBtn.classList.add('recording');
      showVoiceStatus(t.listening);
    } catch (err) {
      console.error('Mic error:', err);
      showVoiceStatus('⚠️ Microphone access denied');
      setTimeout(() => showVoiceStatus(null), 3000);
    }
  }

  function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
    }
    isRecording = false;
    document.getElementById('gip-mic').classList.remove('recording');
    showVoiceStatus(t.processing);
  }

  async function processVoice() {
    if (audioChunks.length === 0) { showVoiceStatus(null); return; }

    const blob = new Blob(audioChunks, { type: mediaRecorder.mimeType || 'audio/webm' });
    if (blob.size < 1000) { showVoiceStatus(null); return; }

    isLoading = true; renderMessages();
    document.getElementById('gip-send').disabled = true;

    try {
      const formData = new FormData();
      const ext = (mediaRecorder.mimeType || '').includes('mp4') ? 'mp4' : 'webm';
      formData.append('audio', blob, `voice.${ext}`);
      formData.append('session_id', sessionId || '');

      const resp = await fetch(CFG.apiUrl + '?path=api/voice', { method: 'POST', body: formData });

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.error || 'Voice processing failed');
      }

      // Get transcripts from headers
      const userText = decodeURIComponent(resp.headers.get('X-Transcript-User') || '');
      const botText = decodeURIComponent(resp.headers.get('X-Transcript-Bot') || '');
      const newSession = resp.headers.get('X-Session-Id');
      if (newSession) { sessionId = newSession; try { localStorage.setItem('goippro_chat_session', sessionId); } catch(e) {} }

      // Get audio blob
      const audioBlob = await resp.blob();
      const audioUrl = URL.createObjectURL(audioBlob);

      // Show user message (voice transcript)
      if (userText) addUserMessage(userText, true);

      // Show bot message with audio player
      if (botText) addBotMessage(botText, audioUrl);

      // Auto-play response
      try {
        const audio = new Audio(audioUrl);
        audio.play().catch(() => {}); // may fail on mobile without user gesture
      } catch(e) {}

      // Hide quick buttons after first interaction
      const quickEl = document.getElementById('gip-quick');
      if (quickEl) quickEl.style.display = 'none';

    } catch (err) {
      console.error('Voice error:', err);
      addBotMessage(t.voiceError);
    }

    isLoading = false; renderMessages();
    document.getElementById('gip-send').disabled = false;
    showVoiceStatus(null);
  }


  // ── Escalation ────────────────────────────────────
  window._gipEscalate = async function() {
    if (isLoading) return;
    isLoading = true; renderMessages();

    try {
      const resp = await fetch(CFG.apiUrl + '?path=api/escalate', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, reason: 'User clicked Talk to human' }),
      });
      const data = await resp.json();
      if (data.session_id) { sessionId = data.session_id; try { localStorage.setItem('goippro_chat_session', sessionId); } catch(e) {} }
      addBotMessage(data.message || t.escalated);
      
      // Show escalated banner
      const banner = document.createElement('div');
      banner.className = 'gip-escalated';
      banner.innerHTML = '✅ ' + (t.escalated || 'Our team has been notified!');
      const msgs = document.getElementById('gip-msgs');
      msgs.parentNode.insertBefore(banner, msgs.nextSibling);
    } catch(err) {
      addBotMessage(t.error);
    }
    isLoading = false; renderMessages();
  };

  // ── Init ──────────────────────────────────────────
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
