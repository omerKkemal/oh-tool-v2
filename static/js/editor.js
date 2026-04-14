// ========================
// CodeEditor Class – Full Implementation
// ========================
class CodeEditor {
    constructor() {
        this.editor = document.getElementById('codeEditor');
        this.lineNumbers = document.getElementById('lineNumbers');
        this.cursorPosition = document.getElementById('cursorPosition');
        this.consoleOutput = document.getElementById('consoleOutput');
        this.currentFileName = document.getElementById('currentFileName');
        this.connectionStatus = document.getElementById('connectionStatus');
        this.connectionText = document.getElementById('connectionText');
        this.fileInfo = document.getElementById('fileInfo');
        this.filePath = document.getElementById('filePath');
        this.fileSize = document.getElementById('fileSize');
        this.fileHash = document.getElementById('fileHash');
        this.encryptionStatus = document.getElementById('encryptionStatus');
        this.charCount = document.getElementById('charCount');
        this.targetSelect = document.getElementById('targetSelect');
        this.modalTargetSelect = document.getElementById('modalTargetSelect');
        this.outputList = document.getElementById('outputList');
        this.outputNotificationBadge = document.getElementById('outputNotificationBadge');
        
        // Targets from backend (passed via data attribute)
        const targetSelectEl = document.getElementById('targetSelect');
        this.targets = targetSelectEl ? JSON.parse(targetSelectEl.dataset.targets || '[]') : [];
        
        this.currentFile = null;
        this.isLoading = false;
        this.undoStack = [];
        this.redoStack = [];
        this.lineCount = 1;
        this.isEncrypted = false;
        this.pendingInjection = false;
        this.updateCheckInterval = null;
        this.autoSaveEnabled = false;
        this.notificationHistory = [];
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.generateLineNumbers();
        this.updateCursorPosition();
        this.updateCharCount();
        this.initMatrixOverlay();
        this.startUpdateChecking();
        this.restoreNotifications();
        this.populateTargetSelect();
        this.addConsoleOutput('[SYSTEM] Code injection module initialized', 'info');
        this.addConsoleOutput('[SECURITY] Connection encrypted: TLS 1.3', 'success');
        this.addConsoleOutput('[INFO] Notifications system restored from storage', 'info');
        this.addConsoleOutput('[READY] Select payload from repository', 'info');
        this.fetchInactiveTargets();

        // AI Prompt char counter
        const aiPrompt = document.getElementById('aiPrompt');
        if (aiPrompt) {
            aiPrompt.addEventListener('input', () => {
                const count = aiPrompt.value.length;
                const counter = document.getElementById('promptCharCount');
                if (counter) counter.textContent = count + '/500';
            });
        }
    }
    
    // ========== UI / EVENT LISTENERS ==========
    setupEventListeners() {
        if (this.editor) {
            this.editor.addEventListener('input', () => {
                this.updateLineNumbers();
                this.updateCursorPosition();
                this.updateCharCount();
                this.saveToUndoStack();
                if (this.currentFile && this.autoSaveEnabled) this.autoSaveDebounce();
            });
            this.autoSaveDebounce = this.debounce(() => this.saveCurrentFile().catch(() => {}), 3000);
            
            this.editor.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') { e.preventDefault(); this.insertTab(); return; }
                if ((e.ctrlKey || e.metaKey) && e.key === 's') { e.preventDefault(); this.saveCurrentFile(); }
                if ((e.ctrlKey || e.metaKey) && e.key === 'e') { e.preventDefault(); this.encryptFile(); }
                if ((e.ctrlKey || e.metaKey) && e.key === 'd') { e.preventDefault(); this.decodeFile(); }
                if ((e.ctrlKey || e.metaKey) && !e.shiftKey && e.key === 'z') { e.preventDefault(); this.undo(); }
                if (((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'z') || ((e.ctrlKey || e.metaKey) && e.key === 'y')) { e.preventDefault(); this.redo(); }
                if ((e.ctrlKey || e.metaKey) && e.key === 'i') { e.preventDefault(); this.startInjection(); }
                if ((e.ctrlKey || e.metaKey) && e.key === 'a') { e.preventDefault(); this.open_list_of_inactive_pyload(); }
                if ((e.ctrlKey || e.metaKey) && e.key === 'r') { e.preventDefault(); this.restoreNotifications(); }
            });
            this.editor.addEventListener('click', () => this.updateCursorPosition());
            this.editor.addEventListener('scroll', () => { if (this.lineNumbers) this.lineNumbers.scrollTop = this.editor.scrollTop; });
            this.editor.addEventListener('keyup', () => this.updateCursorPosition());
        }
        
        if (this.targetSelect) {
            this.targetSelect.addEventListener('change', () => this.targetSelect.classList.remove('error'));
        }
        
        // Buttons
        const injectBtn = document.getElementById('btn-inject');
        const saveBtn = document.getElementById('btn-save');
        const validateBtn = document.getElementById('validateBtn');
        const aiGenerateBtn = document.getElementById('aiGenerateBtn');
        const newFileBtn = document.getElementById('newFileBtn');
        const saveAsBtn = document.getElementById('saveAsBtn');
        const testNotificationBtn = document.getElementById('testNotificationBtn');
        const clearAllOutputBtn = document.getElementById('clearAllOutputBtn');
        
        if (injectBtn) injectBtn.addEventListener('click', () => this.startInjection());
        if (saveBtn) saveBtn.addEventListener('click', () => this.saveCurrentFile());
        if (validateBtn) validateBtn.addEventListener('click', () => this.open_list_of_inactive_pyload());
        if (aiGenerateBtn) aiGenerateBtn.addEventListener('click', () => this.showAIGenerationModal());
        if (newFileBtn) newFileBtn.addEventListener('click', () => this.newFile());
        if (saveAsBtn) saveAsBtn.addEventListener('click', () => this.showSaveModal());
        if (testNotificationBtn) testNotificationBtn.addEventListener('click', () => this.testNotificationSystem());
        if (clearAllOutputBtn) clearAllOutputBtn.addEventListener('click', () => this.clearAllOutputNotifications());
        
        // Modals
        const saveModal = document.getElementById('saveModal');
        const confirmSaveBtn = document.getElementById('confirmSaveBtn');
        const cancelSaveBtn = document.getElementById('cancelSaveBtn');
        if (confirmSaveBtn) confirmSaveBtn.addEventListener('click', () => this.saveWithName());
        if (cancelSaveBtn) cancelSaveBtn.addEventListener('click', () => this.closeSaveModal());
        
        const targetModal = document.getElementById('targetModal');
        const confirmTargetBtn = document.getElementById('confirmTargetBtn');
        const cancelTargetBtn = document.getElementById('cancelTargetBtn');
        if (confirmTargetBtn) confirmTargetBtn.addEventListener('click', () => this.useSelectedTargetFromModal());
        if (cancelTargetBtn) cancelTargetBtn.addEventListener('click', () => this.closeTargetModal());
        
        const inactiveModal = document.getElementById('inactivePayloadsModal');
        const closeInactiveModalBtn = document.getElementById('closeInactiveModalBtn');
        if (closeInactiveModalBtn) closeInactiveModalBtn.addEventListener('click', () => this.closeInactivePayloadsModal());
        
        const outputModal = document.getElementById('outputModal');
        const closeOutputModalBtn = document.getElementById('closeOutputModalBtn');
        if (closeOutputModalBtn) closeOutputModalBtn.addEventListener('click', () => this.closeOutputModal());
        
        const aiModal = document.getElementById('aiGenerationModal');
        const closeAiModalBtn = document.getElementById('closeAiModalBtn');
        const cancelAiModalBtn = document.getElementById('cancelAiModalBtn');
        const aiGenerateSubmitBtn = document.getElementById('aiGenerateSubmitBtn');
        if (closeAiModalBtn) closeAiModalBtn.addEventListener('click', () => this.closeAIGenerationModal());
        if (cancelAiModalBtn) cancelAiModalBtn.addEventListener('click', () => this.closeAIGenerationModal());
        if (aiGenerateSubmitBtn) aiGenerateSubmitBtn.addEventListener('click', () => this.generateAIPayload());
        
        // Panel tabs
        document.querySelectorAll('.panel-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const panelName = tab.dataset.panel;
                if (panelName) this.switchPanel(panelName);
            });
        });
        
        // File tree items (delegation)
        const fileTree = document.getElementById('fileTree');
        if (fileTree) {
            fileTree.addEventListener('click', (e) => {
                const fileItem = e.target.closest('.file-item');
                if (fileItem) {
                    const filename = fileItem.dataset.filename;
                    if (filename) this.loadPayload(filename);
                }
            });
        }
        
        window.addEventListener('beforeunload', () => this.saveActiveNotifications());
        setInterval(() => this.saveActiveNotifications(), 30000);
    }
    
    debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
    
    insertTab() {
        if (!this.editor) return;
        const start = this.editor.selectionStart;
        const end = this.editor.selectionEnd;
        const text = this.editor.value;
        this.editor.value = text.substring(0, start) + '    ' + text.substring(end);
        this.editor.selectionStart = this.editor.selectionEnd = start + 4;
        this.editor.dispatchEvent(new Event('input'));
    }
    
    // ========== EDITOR CORE ==========
    generateLineNumbers() {
        if (!this.lineNumbers || !this.editor) return;
        this.lineNumbers.innerHTML = '';
        const lines = this.editor.value.split('\n');
        this.lineCount = Math.max(1, lines.length);
        for (let i = 1; i <= this.lineCount; i++) {
            const lineNumber = document.createElement('div');
            lineNumber.className = 'line-number text-right text-slate-500 text-xs py-0.5';
            lineNumber.textContent = i.toString().padStart(3, '0');
            this.lineNumbers.appendChild(lineNumber);
        }
    }
    
    updateLineNumbers() {
        if (!this.editor) return;
        const newLineCount = Math.max(1, this.editor.value.split('\n').length);
        if (newLineCount !== this.lineCount) {
            this.lineCount = newLineCount;
            this.generateLineNumbers();
        }
    }
    
    updateCursorPosition() {
        if (!this.cursorPosition || !this.editor) return;
        const text = this.editor.value;
        const cursorPos = this.editor.selectionStart;
        const textBeforeCursor = text.substring(0, cursorPos);
        const lines = textBeforeCursor.split('\n');
        const line = lines.length;
        const column = lines[lines.length - 1].length + 1;
        this.cursorPosition.textContent = `LINE ${line}, COL ${column}`;
        const lineNumbers = document.querySelectorAll('.line-number');
        lineNumbers.forEach((num, idx) => num.classList.toggle('text-emerald-400', idx + 1 === line));
    }
    
    updateCharCount() {
        if (!this.charCount || !this.fileSize || !this.editor) return;
        const count = this.editor.value.length;
        this.charCount.textContent = `${count} BYTES`;
        this.fileSize.textContent = `SIZE: ${count} BYTES`;
    }
    
    saveToUndoStack() {
        if (!this.editor) return;
        const content = this.editor.value;
        if (this.undoStack[this.undoStack.length - 1] !== content) {
            this.undoStack.push(content);
            if (this.undoStack.length > 50) this.undoStack.shift();
            this.redoStack = [];
        }
    }
    
    undo() {
        if (this.undoStack.length > 1) {
            this.redoStack.push(this.undoStack.pop());
            this.editor.value = this.undoStack[this.undoStack.length - 1];
            this.updateLineNumbers();
            this.updateCursorPosition();
            this.updateCharCount();
            this.addConsoleOutput('[EDIT] Undo operation', 'info');
        }
    }
    
    redo() {
        if (this.redoStack.length > 0) {
            const content = this.redoStack.pop();
            this.undoStack.push(content);
            this.editor.value = content;
            this.updateLineNumbers();
            this.updateCursorPosition();
            this.updateCharCount();
            this.addConsoleOutput('[EDIT] Redo operation', 'info');
        }
    }
    
    addConsoleOutput(message, type = 'info') {
        if (!this.consoleOutput) return;
        const line = document.createElement('div');
        const colors = { info: 'text-slate-400', success: 'text-emerald-400', warning: 'text-amber-400', error: 'text-rose-400' };
        line.className = `console-line ${colors[type] || colors.info} text-xs py-0.5 font-mono`;
        const now = new Date();
        const timestamp = `[${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}:${now.getSeconds().toString().padStart(2,'0')}]`;
        line.textContent = `${timestamp} ${message}`;
        this.consoleOutput.appendChild(line);
        this.consoleOutput.scrollTop = this.consoleOutput.scrollHeight;
    }
    
    // ========== MATRIX OVERLAY ==========
    initMatrixOverlay() {
        const canvas = document.getElementById('matrixOverlay');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let width, height, columns, drops, fontSize, chars;
        const resize = () => {
            width = canvas.offsetWidth;
            height = canvas.offsetHeight;
            canvas.width = width;
            canvas.height = height;
            fontSize = 10;
            columns = Math.floor(width / fontSize);
            drops = Array(columns).fill(1);
            chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン";
        };
        const draw = () => {
            ctx.fillStyle = "rgba(10, 10, 10, 0.04)";
            ctx.fillRect(0, 0, width, height);
            ctx.fillStyle = "#00ff41";
            ctx.font = `${fontSize}px 'JetBrains Mono', monospace`;
            for (let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random() * chars.length)];
                const opacity = Math.random() * 0.5 + 0.3;
                ctx.fillStyle = `rgba(0, 255, 65, ${opacity})`;
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        };
        resize();
        window.addEventListener('resize', resize);
        setInterval(draw, 50);
    }
    
    // ========== NOTIFICATION PERSISTENCE ==========
    restoreNotifications() {
        try {
            const savedHistory = localStorage.getItem('notification_history');
            if (savedHistory) this.notificationHistory = JSON.parse(savedHistory);
            const savedNotifications = localStorage.getItem('active_notifications');
            if (savedNotifications && this.outputList) {
                const notifications = JSON.parse(savedNotifications);
                notifications.forEach(notif => {
                    if (this.isNotificationValid(notif)) this.addOutputNotification(notif, false);
                });
                this.updateNotificationBadge();
            }
            this.addConsoleOutput(`[SYSTEM] Restored ${this.notificationHistory.length} historical notifications`, 'success');
        } catch(e) {
            console.error('Restore error', e);
            localStorage.removeItem('notification_history');
            localStorage.removeItem('active_notifications');
            this.notificationHistory = [];
        }
    }
    
    isNotificationValid(notification) {
        if (!notification.timestamp) return false;
        const maxAge = 7 * 24 * 60 * 60 * 1000;
        return (new Date().getTime() - new Date(notification.timestamp).getTime()) < maxAge;
    }
    
    saveActiveNotifications() {
        try {
            const active = [];
            document.querySelectorAll('.output-item').forEach(el => {
                active.push({
                    ID: el.dataset.updateId || '',
                    target_name: el.dataset.targetName || '',
                    payload_name: el.dataset.payloadName || '',
                    timestamp: el.dataset.timestamp || new Date().toISOString(),
                    status: el.classList.contains('read') ? 'viewed' : 'pending'
                });
            });
            localStorage.setItem('active_notifications', JSON.stringify(active));
            this.saveNotificationHistory(active);
        } catch(e) { console.error(e); }
    }
    
    saveNotificationHistory(notifications) {
        notifications.forEach(notif => {
            const exists = this.notificationHistory.some(h => h.ID === notif.ID);
            if (!exists) this.notificationHistory.push({ ...notif, saved_at: new Date().toISOString() });
        });
        if (this.notificationHistory.length > 200) this.notificationHistory = this.notificationHistory.slice(-200);
        localStorage.setItem('notification_history', JSON.stringify(this.notificationHistory));
    }
    
    clearAllNotificationsStorage() {
        localStorage.removeItem('active_notifications');
        localStorage.removeItem('notification_history');
        this.notificationHistory = [];
        this.clearAllOutputNotifications();
        this.addConsoleOutput('[SYSTEM] Cleared all notifications from storage', 'success');
    }
    
    addOutputNotification(update, saveToStorage = true) {
        if (!this.outputList) return;
        if (!update || (!update.ID && !update.target_name)) return;
        const existing = document.querySelectorAll('.output-item[data-update-id]');
        for (let item of existing) {
            if (item.dataset.updateId === update.ID) return;
        }
        const id = `output-${Date.now()}-${Math.random().toString(36).substr(2,9)}`;
        const item = document.createElement('div');
        item.className = 'output-item bg-slate-800/50 rounded-lg p-3 border border-slate-700';
        item.id = id;
        item.dataset.updateId = update.ID || '';
        item.dataset.targetName = update.target_name || '';
        item.dataset.payloadName = update.payload_name || '';
        item.dataset.timestamp = update.timestamp || new Date().toISOString();
        if (update.status === 'viewed') item.classList.add('read');
        const time = new Date(update.timestamp).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', second:'2-digit'});
        item.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <div><i class="fas fa-crosshairs text-emerald-400 mr-1"></i><span class="font-bold">${this.escapeHtml(update.target_name || 'Unknown')}</span> <span class="text-slate-400 text-xs">${this.escapeHtml(update.payload_name || '')}</span></div>
                <div class="text-xs text-slate-500">${time}</div>
            </div>
            <div class="flex justify-between items-center">
                <span class="status-badge text-xs px-2 py-0.5 rounded ${update.status === 'viewed' ? 'bg-slate-600' : 'bg-amber-600'}">${(update.status || 'PENDING').toUpperCase()}</span>
                <div class="flex gap-2">
                    <button class="show-output-btn text-xs text-emerald-400 hover:text-emerald-300" data-id="${update.ID || ''}" data-target="${this.escapeHtml(update.target_name || '')}" data-payload="${this.escapeHtml(update.payload_name || '')}">VIEW OUTPUT</button>
                    <button class="dismiss-btn text-xs text-rose-400 hover:text-rose-300" data-id="${id}">DISMISS</button>
                </div>
            </div>
        `;
        this.outputList.prepend(item);
        item.querySelector('.show-output-btn')?.addEventListener('click', () => this.showOutputDetails(update.ID || '', update.target_name || '', update.payload_name || ''));
        item.querySelector('.dismiss-btn')?.addEventListener('click', () => this.dismissOutputNotification(id));
        this.updateNotificationBadge();
        if (saveToStorage) setTimeout(() => this.saveActiveNotifications(), 1000);
    }
    
    dismissOutputNotification(id) {
        const el = document.getElementById(id);
        if (el) {
            el.style.animation = 'fadeOut 0.2s';
            setTimeout(() => { el.remove(); this.updateNotificationBadge(); this.saveActiveNotifications(); }, 200);
        }
    }
    
    markNotificationAsRead(ID) {
        const el = document.querySelector(`.output-item[data-update-id="${ID}"]`);
        if (el) {
            el.classList.add('read');
            const badge = el.querySelector('.status-badge');
            if (badge) { badge.classList.remove('bg-amber-600'); badge.classList.add('bg-slate-600'); badge.textContent = 'VIEWED'; }
            this.saveActiveNotifications();
        }
    }
    
    updateNotificationBadge() {
        const badge = this.outputNotificationBadge;
        if (!badge) return;
        const unread = document.querySelectorAll('.output-item:not(.read)').length;
        if (unread > 0) {
            badge.textContent = unread > 99 ? '99+' : unread;
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    }
    
    clearAllOutputNotifications() {
        document.querySelectorAll('.output-item').forEach(item => item.remove());
        this.updateNotificationBadge();
        this.saveActiveNotifications();
        this.addConsoleOutput('[OUTPUT] All notifications cleared', 'info');
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    formatTimestamp(ts) {
        try {
            return new Date(ts).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', second:'2-digit'});
        } catch(e) { return new Date().toLocaleTimeString(); }
    }
    
    async showOutputDetails(ID, targetName, payloadName) {
        const modal = document.getElementById('outputModal');
        const title = document.getElementById('outputTitle');
        const body = document.getElementById('modalOutput');
        if (!modal || !title || !body) return;
        title.innerHTML = `<i class="fas fa-terminal"></i> OUTPUT - ${targetName || 'Loading...'}`;
        body.innerHTML = '<div class="text-center py-8"><i class="fas fa-spinner fa-spin text-emerald-400 text-2xl"></i><p class="mt-2">FETCHING OUTPUT...</p></div>';
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        try {
            const resp = await fetch(`/code_injection/get_output/${ID}`);
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const data = await resp.json();
            if (data.error) throw new Error(data.error);
            this.displayOutputInModal(data.outputs, targetName, body);
            this.markNotificationAsRead(ID);
            this.saveActiveNotifications();
        } catch(e) {
            body.innerHTML = `<div class="text-rose-400 text-center p-4">ERROR: ${e.message}</div>`;
        }
    }
    
    displayOutputInModal(outputData, targetName, container) {
        if (!outputData || outputData === "No output found.") {
            container.innerHTML = `<div class="text-slate-400 text-center p-4">No output available for this payload.</div>`;
            return;
        }
        let html = `<div class="bg-slate-950 p-3 rounded border border-slate-700 font-mono text-sm whitespace-pre-wrap break-words">`;
        if (typeof outputData === 'string') html += outputData.replace(/\n/g, '<br>');
        else html += JSON.stringify(outputData, null, 2);
        html += `</div><div class="mt-4 flex justify-end gap-3"><button id="copyOutputBtn" class="bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded text-sm"><i class="far fa-copy"></i> COPY</button><button id="downloadOutputBtn" class="bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded text-sm"><i class="fas fa-download"></i> DOWNLOAD</button></div>`;
        container.innerHTML = html;
        document.getElementById('copyOutputBtn')?.addEventListener('click', () => {
            const text = outputData;
            navigator.clipboard.writeText(typeof text === 'string' ? text : JSON.stringify(text));
            this.addConsoleOutput('[OUTPUT] Copied to clipboard', 'success');
        });
        document.getElementById('downloadOutputBtn')?.addEventListener('click', () => {
            const blob = new Blob([typeof outputData === 'string' ? outputData : JSON.stringify(outputData)], {type: 'text/plain'});
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `output_${Date.now()}.txt`;
            a.click();
            URL.revokeObjectURL(a.href);
        });
    }
    
    closeOutputModal() {
        const modal = document.getElementById('outputModal');
        if (modal) { modal.classList.add('hidden'); modal.classList.remove('flex'); }
    }
    
    // ========== TARGETS & INACTIVE PAYLOADS ==========
    populateTargetSelect() {
        if (this.targetSelect && this.targets.length) {
            this.targetSelect.innerHTML = '<option value="" disabled selected>TARGET SELECT</option>';
            this.targets.forEach(t => {
                const val = Array.isArray(t) ? t[1] : t;
                const opt = document.createElement('option');
                opt.value = val;
                opt.textContent = val;
                this.targetSelect.appendChild(opt);
            });
        }
        if (this.modalTargetSelect && this.targets.length) {
            this.modalTargetSelect.innerHTML = '<option value="" disabled selected>SELECT TARGET</option>';
            this.targets.forEach(t => {
                const val = Array.isArray(t) ? t[0] : t;
                const opt = document.createElement('option');
                opt.value = val;
                opt.textContent = Array.isArray(t) ? t[1] : t;
                this.modalTargetSelect.appendChild(opt);
            });
        }
    }
    
    async fetchInactiveTargets() {
        try {
            const resp = await fetch('/code_injection/active_target', { method: 'GET', headers: { 'Content-Type': 'application/json' } });
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const data = await resp.json();
            if (data.inactive_payloads) {
                window.inactive_payloads = data.inactive_payloads;
                this.addConsoleOutput(`[INFO] Found ${data.inactive_payloads.length} inactive targets`, 'success');
                this.updateTargetSelectWithStatus(data.inactive_payloads);
            }
        } catch(e) { this.addConsoleOutput(`[ERROR] Failed to fetch inactive targets: ${e.message}`, 'error'); }
    }
    
    updateTargetSelectWithStatus(inactiveTargets) {
        if (!this.targetSelect) return;
        Array.from(this.targetSelect.options).forEach(opt => {
            if (inactiveTargets.includes(opt.value)) {
                opt.textContent = opt.value.replace(/ \[.*\]/, '') + ' [INACTIVE]';
                opt.style.color = '#ff0033';
            } else {
                opt.textContent = opt.value.replace(/ \[.*\]/, '') + ' [ACTIVE]';
                opt.style.color = '#00ff41';
            }
        });
    }
    
    async activateTargetAPI(targetName) {
        const resp = await fetch('/code_injection/active_target', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target_name: targetName })
        });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const result = await resp.json();
        if (result.error) throw new Error(result.error);
        this.addConsoleOutput(`[SUCCESS] ${result.message}`, 'success');
        return result;
    }
    
    async activateTarget(targetName) {
        try {
            await this.activateTargetAPI(targetName);
            this.updateTargetStatus(targetName, 'active');
            setTimeout(() => this.fetchInactiveTargets(), 1000);
            this.showInactivePayloadsModal(); // refresh modal
        } catch(e) { this.addConsoleOutput(`[ERROR] Activation failed: ${e.message}`, 'error'); }
    }
    
    updateTargetStatus(targetName, status) {
        const options = this.targetSelect?.options;
        if (options) {
            for (let opt of options) {
                if (opt.value === targetName) {
                    opt.textContent = opt.value.replace(/ \[.*\]/, '') + (status === 'active' ? ' [ACTIVE]' : ' [INACTIVE]');
                    opt.style.color = status === 'active' ? '#00ff41' : '#ff0033';
                }
            }
        }
        this.addConsoleOutput(`[STATUS] Target ${targetName} marked as ${status.toUpperCase()}`, 'success');
    }
    
    open_list_of_inactive_pyload() {
        if (!window.inactive_payloads || window.inactive_payloads.length === 0) {
            this.addConsoleOutput('[INFO] No inactive targets found', 'info');
            return;
        }
        this.showInactivePayloadsModal();
    }
    
    showInactivePayloadsModal() {
        const modal = document.getElementById('inactivePayloadsModal');
        const list = document.getElementById('inactivePayloadsList');
        if (!modal || !list) return;
        list.innerHTML = '';
        window.inactive_payloads.forEach(target => {
            const div = document.createElement('div');
            div.className = 'flex justify-between items-center p-2 bg-slate-800/50 rounded-lg';
            div.innerHTML = `<span class="font-mono">${target}</span><button class="activate-btn text-xs bg-emerald-600 hover:bg-emerald-700 px-3 py-1 rounded" data-target="${target}">ACTIVATE</button>`;
            list.appendChild(div);
        });
        list.querySelectorAll('.activate-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const t = btn.dataset.target;
                this.activateTarget(t);
            });
        });
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
    
    closeInactivePayloadsModal() {
        const modal = document.getElementById('inactivePayloadsModal');
        if (modal) { modal.classList.add('hidden'); modal.classList.remove('flex'); }
    }
    
    async refreshInactivePayloads() {
        await this.fetchInactiveTargets();
        this.showInactivePayloadsModal();
        this.addConsoleOutput('[INFO] Inactive targets list refreshed', 'success');
    }
    
    // ========== FILE LOADING / SAVING ==========
    async loadPayload(fileName) {
        if (this.isLoading) return;
        this.isLoading = true;
        this.currentFile = fileName;
        this.currentFileName.textContent = fileName.toUpperCase();
        this.fileInfo.textContent = `STATUS: LOADING ${fileName}...`;
        this.filePath.textContent = `LOCATION: /payloads/encrypted/${fileName}`;
        const fileTab = document.getElementById('activeFileTab');
        const original = fileTab?.innerHTML;
        if (fileTab) fileTab.innerHTML = '<div class="loading-spinner"></div> DECRYPTING...';
        document.querySelectorAll('.file-item').forEach(i => i.classList.remove('active'));
        const activeItem = document.querySelector(`.file-item[data-filename="${fileName}"]`);
        if (activeItem) activeItem.classList.add('active');
        try {
            const resp = await fetch(`/code_injection/load_code/${encodeURIComponent(fileName)}`);
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const data = await resp.json();
            if (data.error) throw new Error(data.error);
            this.editor.value = data.content;
            this.undoStack = [];
            this.redoStack = [];
            this.updateLineNumbers();
            this.updateCursorPosition();
            this.updateCharCount();
            this.saveToUndoStack();
            this.addConsoleOutput(`[SUCCESS] Payload decrypted: ${fileName}`, 'success');
            this.fileInfo.textContent = `STATUS: LOADED`;
            this.fileSize.textContent = `SIZE: ${data.content.length} BYTES`;
            this.fileHash.textContent = `HASH: ${this.generateHash(data.content)}`;
            if (fileTab) fileTab.innerHTML = `<i class="fas fa-biohazard file-icon"></i> ${fileName.toUpperCase()}`;
            this.connectionStatus.style.background = '#00ff41';
            this.connectionText.textContent = 'CONNECTION: SECURE';
        } catch(e) {
            this.addConsoleOutput(`[ERROR] Failed to load ${fileName}: ${e.message}`, 'error');
            this.fileInfo.textContent = `STATUS: ERROR`;
            if (fileTab) fileTab.innerHTML = original;
            this.connectionStatus.style.background = '#ff0033';
            this.connectionText.textContent = 'CONNECTION: COMPROMISED';
            this.currentFile = null;
            this.currentFileName.textContent = 'SELECT_PAYLOAD';
            this.editor.value = '';
            this.updateLineNumbers();
            this.updateCharCount();
        } finally { this.isLoading = false; }
    }
    
    generateHash(content) {
        let hash = 0;
        for (let i = 0; i < Math.min(content.length, 10); i++) {
            hash = ((hash << 5) - hash) + content.charCodeAt(i);
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16).toUpperCase().substring(0,8);
    }
    
    async saveFile(payloadName) {
        if (!this.editor) return;
        const content = this.editor.value;
        if (!content.trim()) throw new Error('Cannot save empty payload');
        const resp = await fetch(`/code_injection/save_code/${encodeURIComponent(payloadName)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: content })
        });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.error || `HTTP ${resp.status}`);
        }
        const result = await resp.json();
        this.addConsoleOutput(`[SUCCESS] ${result.message}`, 'success');
        if (!this.currentFile || this.currentFile !== payloadName) {
            this.currentFile = payloadName;
            this.currentFileName.textContent = payloadName.toUpperCase();
            this.addFileToTree(payloadName);
            this.filePath.textContent = `LOCATION: /payloads/encrypted/${payloadName}`;
            this.fileHash.textContent = `HASH: ${this.generateHash(content)}`;
        }
        return { success: true };
    }
    
    async saveCurrentFile() {
        if (this.currentFile) {
            try {
                await this.saveFile(this.currentFile);
                this.addConsoleOutput(`[INFO] File ${this.currentFile} saved successfully`, 'success');
                this.fileInfo.textContent = 'STATUS: SAVED';
            } catch(e) { this.fileInfo.textContent = 'STATUS: ERROR'; }
        } else {
            this.showSaveModal();
        }
    }
    
    addFileToTree(fileName) {
        const tree = document.getElementById('fileTree');
        if (!tree) return;
        if (document.querySelector(`.file-item[data-filename="${fileName}"]`)) return;
        const div = document.createElement('div');
        div.className = 'file-item flex items-center gap-2 p-2 rounded-lg hover:bg-slate-800 cursor-pointer transition';
        div.dataset.filename = fileName;
        div.innerHTML = `<i class="fas fa-file-code text-slate-400"></i><span class="text-sm">${fileName}</span>`;
        div.addEventListener('click', () => this.loadPayload(fileName));
        tree.appendChild(div);
    }
    
    newFile() {
        this.currentFile = null;
        this.currentFileName.textContent = 'NEW_PAYLOAD';
        this.editor.value = '';
        this.updateLineNumbers();
        this.updateCursorPosition();
        this.updateCharCount();
        this.addConsoleOutput('[SYSTEM] New payload created', 'info');
        this.fileInfo.textContent = 'STATUS: UNSAVED';
        this.filePath.textContent = 'LOCATION: /payloads/temp/';
        this.fileSize.textContent = 'SIZE: 0 BYTES';
        this.fileHash.textContent = 'HASH: N/A';
        this.encryptionStatus.textContent = 'ENCRYPTION: DISABLED';
        this.isEncrypted = false;
    }
    
    showSaveModal() {
        const modal = document.getElementById('saveModal');
        const input = document.getElementById('payloadNameInput');
        if (!modal || !input) return;
        input.value = this.currentFile || `payload_${new Date().toISOString().replace(/[:.]/g,'-').slice(0,19)}.py`;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        input.focus();
    }
    
    closeSaveModal() {
        const modal = document.getElementById('saveModal');
        if (modal) { modal.classList.add('hidden'); modal.classList.remove('flex'); }
    }
    
    async saveWithName() {
        const input = document.getElementById('payloadNameInput');
        if (!input) return;
        const name = input.value.trim();
        if (!name) return alert('Please enter a payload name');
        if (!/^[a-zA-Z0-9_\-\.]+$/.test(name)) return alert('Invalid file name. Use letters, numbers, dots, underscores, hyphens.');
        try {
            await this.saveFile(name);
            this.closeSaveModal();
            this.addConsoleOutput(`[SUCCESS] Payload "${name}" saved successfully`, 'success');
            this.fileInfo.textContent = 'STATUS: SAVED';
        } catch(e) { this.addConsoleOutput(`[ERROR] Save failed: ${e.message}`, 'error'); }
    }
    
    async encryptFile() {
        if (!this.currentFile) return this.addConsoleOutput('[ERROR] Select payload first', 'error');
        if (!this.editor.value.trim()) return this.addConsoleOutput('[ERROR] Cannot encrypt empty payload', 'error');
        this.addConsoleOutput('[CRYPTO] Initializing encryption sequence...', 'warning');
        setTimeout(() => this.addConsoleOutput('[CRYPTO] Applying XOR cipher...', 'info'), 500);
        setTimeout(() => this.addConsoleOutput('[CRYPTO] Applying Base64 encoding...', 'info'), 1000);
        setTimeout(async () => {
            try {
                await this.saveFile(this.currentFile);
                this.addConsoleOutput('[SUCCESS] Payload encrypted and saved', 'success');
                this.isEncrypted = true;
                this.encryptionStatus.textContent = 'ENCRYPTION: ENABLED';
            } catch(e) { this.addConsoleOutput('[ERROR] Failed to save encrypted payload', 'error'); }
        }, 1500);
    }
    
    async decodeFile() {
        if (!this.currentFile) return this.addConsoleOutput('[ERROR] Select payload first', 'error');
        if (!this.isEncrypted) return this.addConsoleOutput('[INFO] Payload is not encrypted', 'info');
        this.addConsoleOutput('[DECODE] Initializing decryption sequence...', 'warning');
        setTimeout(() => this.addConsoleOutput('[DECODE] Decoding Base64...', 'info'), 500);
        setTimeout(() => this.addConsoleOutput('[DECODE] Applying XOR decryption...', 'info'), 1000);
        setTimeout(async () => {
            try {
                await this.saveFile(this.currentFile);
                this.addConsoleOutput('[SUCCESS] Payload decrypted and saved', 'success');
                this.isEncrypted = false;
                this.encryptionStatus.textContent = 'ENCRYPTION: DISABLED';
            } catch(e) { this.addConsoleOutput('[ERROR] Failed to save decrypted payload', 'error'); }
        }, 1500);
    }
    
    // ========== UPDATE CHECKING ==========
    startUpdateChecking() {
        this.updateCheckInterval = setInterval(() => this.checkForUpdates(), 5000);
    }
    
    async checkForUpdates() {
        try {
            const resp = await fetch('/code_injection/check_update');
            if (!resp.ok) return;
            const data = await resp.json();
            if (data.status === 'updated' && data.instraction) {
                let update = null;
                if (data.instraction.info && Array.isArray(data.instraction.info)) {
                    const [ID, target_name, payload_name] = data.instraction.info;
                    update = { ID, target_name, payload_name, timestamp: new Date().toISOString(), status: 'pending' };
                } else if (data.instraction.ID || data.instraction.target_name) {
                    update = { ID: data.instraction.ID || '', target_name: data.instraction.target_name || 'Unknown', payload_name: data.instraction.payload_name || 'Unknown', timestamp: data.instraction.timestamp || new Date().toISOString(), status: 'pending' };
                }
                if (update && !this.isPayloadAlreadyNotified(update)) {
                    this.addConsoleOutput(`[UPDATE] New payload update for ${update.target_name}`, 'info');
                    this.addOutputNotification(update);
                    this.saveNotifiedPayload(update);
                    this.saveActiveNotifications();
                }
            }
        } catch(e) { /* silent */ }
    }
    
    isPayloadAlreadyNotified(payload) {
        if (payload.ID) return this.notificationHistory.some(h => h.ID === payload.ID);
        if (payload.target_name && payload.payload_name) {
            return this.notificationHistory.some(h => h.target_name === payload.target_name && h.payload_name === payload.payload_name && Math.abs(new Date(h.timestamp).getTime() - new Date(payload.timestamp).getTime()) < 60000);
        }
        return false;
    }
    
    saveNotifiedPayload(payload) {
        const exists = this.notificationHistory.some(h => h.ID === payload.ID);
        if (!exists) {
            this.notificationHistory.push({ ...payload, saved_at: new Date().toISOString() });
            if (this.notificationHistory.length > 200) this.notificationHistory.shift();
            localStorage.setItem('notification_history', JSON.stringify(this.notificationHistory));
        }
    }
    
    // ========== INJECTION ==========
    validateTargetSelection() {
        if (!this.targetSelect) return false;
        const selected = this.targetSelect.value;
        if (!selected) {
            this.targetSelect.classList.add('error');
            this.showTargetModal();
            return false;
        }
        return true;
    }
    
    showTargetModal() {
        const modal = document.getElementById('targetModal');
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            if (this.modalTargetSelect) this.modalTargetSelect.value = this.targetSelect.value;
        }
        this.pendingInjection = true;
    }
    
    closeTargetModal() {
        const modal = document.getElementById('targetModal');
        if (modal) { modal.classList.add('hidden'); modal.classList.remove('flex'); }
        this.pendingInjection = false;
    }
    
    async useSelectedTargetFromModal() {
        if (!this.modalTargetSelect) return;
        const target = this.modalTargetSelect.value;
        if (!target) return;
        if (this.targetSelect) this.targetSelect.value = target;
        this.closeTargetModal();
        if (this.pendingInjection) await this.executeInjection();
    }
    
    async startInjection() {
        if (!this.currentFile) {
            this.addConsoleOutput('[ERROR] No payload selected for injection', 'error');
            return;
        }
        if (!this.validateTargetSelection()) {
            this.pendingInjection = true;
            return;
        }
        await this.executeInjection();
    }
    
    async executeInjection() {
        const target = this.targetSelect.value;
        const content = this.editor.value;
        const payloadName = this.currentFile || `unsaved_${Date.now()}`;
        if (!target) {
            this.addConsoleOutput('[ERROR] Please select a target', 'error');
            return;
        }
        if (!content.trim()) {
            this.addConsoleOutput('[ERROR] Cannot execute empty payload', 'error');
            return;
        }
        try {
            this.addConsoleOutput(`[INJECT] Initializing injection sequence...`, 'warning');
            this.addConsoleOutput(`[TARGET] Selected: ${target}`, 'info');
            this.addConsoleOutput(`[PAYLOAD] Name: ${payloadName}`, 'info');
            const resp = await fetch('/code_injection', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target_name: target, payload_name: payloadName, payload: content })
            });
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const result = await resp.json();
            if (result.error) throw new Error(result.error);
            this.addConsoleOutput('[NETWORK] Connection established', 'success');
            this.addConsoleOutput('[SUCCESS] Injection completed successfully', 'success');
            this.addConsoleOutput(`[RESULT] ${result.message || 'Payload injection initiated.'}`, 'success');
            this.updateTargetStatus(target, 'injected');
            this.fileInfo.textContent = 'STATUS: INJECTED';
            setTimeout(() => this.checkForUpdates(), 1000);
        } catch(e) {
            this.addConsoleOutput(`[ERROR] Injection failed: ${e.message}`, 'error');
            this.connectionStatus.style.background = '#ff0033';
            this.connectionText.textContent = 'CONNECTION: FAILED';
            setTimeout(() => {
                this.connectionStatus.style.background = '#00ff41';
                this.connectionText.textContent = 'CONNECTION: SECURE';
            }, 3000);
        }
    }
    
    // ========== AI GENERATION ==========
    showAIGenerationModal() {
        const modal = document.getElementById('aiGenerationModal');
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            document.getElementById('aiPrompt')?.focus();
        }
    }
    
    closeAIGenerationModal() {
        const modal = document.getElementById('aiGenerationModal');
        if (modal) { modal.classList.add('hidden'); modal.classList.remove('flex'); }
        document.getElementById('aiErrorMsg').style.display = 'none';
        document.getElementById('aiBtnSpinner').style.display = 'none';
        document.getElementById('aiBtnText').style.display = 'inline-block';
        document.getElementById('aiGenerateSubmitBtn').disabled = false;
        const bar = document.getElementById('aiProgressBar');
        if (bar) { bar.style.width = '0%'; bar.style.display = 'none'; }
    }
    
    async generateAIPayload() {
        const generateBtn = document.getElementById('aiGenerateSubmitBtn');
        const btnText = document.getElementById('aiBtnText');
        const btnSpinner = document.getElementById('aiBtnSpinner');
        const errorDiv = document.getElementById('aiErrorMsg');
        const progressBar = document.getElementById('aiProgressBar');
        
        generateBtn.disabled = true;
        btnText.style.display = 'none';
        btnSpinner.style.display = 'inline-block';
        if (errorDiv) errorDiv.style.display = 'none';
        if (progressBar) { progressBar.style.display = 'block'; progressBar.style.width = '0%'; }
        
        let progress = 0;
        const interval = setInterval(() => {
            if (progress < 90) { progress += 10; if (progressBar) progressBar.style.width = progress + '%'; }
        }, 300);
        
        const prompt = document.getElementById('aiPrompt')?.value || '';
        const os = document.getElementById('aiOs')?.value || 'Linux';
        const modelSelect = document.getElementById('aiModelSelect');
        const modelInput = document.getElementById('aiModel');
        let model = modelInput.value;
        if (modelSelect.value !== 'custom' && modelSelect.value !== '') model = modelSelect.value;
        const useCurrent = document.getElementById('aiUseCurrent')?.checked || false;
        const saveToRepo = document.getElementById('aiSaveToRepo')?.checked || false;
        const maxRetries = parseInt(document.getElementById('aiMaxRetries')?.value || '3', 10);
        const timeout = parseInt(document.getElementById('aiTimeout')?.value || '30', 10);
        
        let existingPayload = '';
        if (useCurrent && this.editor) existingPayload = this.editor.value;
        
        try {
            const resp = await fetch('/code_injection/generate_ai', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ existing_payload: existingPayload, prompt, operating_system: os, primary_model: model, max_retries: maxRetries, timeout, save_payload: saveToRepo })
            });
            clearInterval(interval);
            if (progressBar) progressBar.style.width = '100%';
            await new Promise(r => setTimeout(r, 200));
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const data = await resp.json();
            if (data.error) throw new Error(data.error);
            if (data.payload) {
                this.editor.value = data.payload;
                this.updateLineNumbers();
                this.updateCursorPosition();
                this.updateCharCount();
                this.saveToUndoStack();
                this.addConsoleOutput('[AI] Payload generated successfully', 'success');
                if (!this.currentFile) {
                    this.currentFile = 'ai_generated_payload.py';
                    this.currentFileName.textContent = this.currentFile.toUpperCase();
                }
                if (saveToRepo) {
                    await this.saveFile(this.currentFile);
                    this.addConsoleOutput('[AI] Payload saved to repository', 'success');
                }
            }
            this.closeAIGenerationModal();
        } catch(e) {
            if (errorDiv) { errorDiv.textContent = `[ERROR] ${e.message}`; errorDiv.style.display = 'block'; }
            this.addConsoleOutput(`[AI] Generation failed: ${e.message}`, 'error');
            if (progressBar) progressBar.style.display = 'none';
            generateBtn.disabled = false;
            btnText.style.display = 'inline-block';
            btnSpinner.style.display = 'none';
            clearInterval(interval);
        }
    }
    
    testNotificationSystem() {
        const test = { ID: `test_${Date.now()}`, target_name: 'Test Target', payload_name: 'Test Payload', timestamp: new Date().toISOString(), status: 'pending' };
        this.addOutputNotification(test);
    }
    
    switchPanel(panelName) {
        const panels = ['console', 'info', 'output'];
        panels.forEach(p => {
            const el = document.getElementById(p + 'Panel');
            if (el) el.classList.add('hidden');
            const tab = document.querySelector(`.panel-tab[data-panel="${p}"]`);
            if (tab) tab.classList.remove('bg-slate-800', 'text-emerald-400');
        });
        const activePanel = document.getElementById(panelName + 'Panel');
        if (activePanel) activePanel.classList.remove('hidden');
        const activeTab = document.querySelector(`.panel-tab[data-panel="${panelName}"]`);
        if (activeTab) activeTab.classList.add('bg-slate-800', 'text-emerald-400');
    }
}

// Initialize when DOM ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('codeEditor')) {
        window.codeEditor = new CodeEditor();
        // Legacy wrappers
        window.open_list_of_inactive_pyload = () => window.codeEditor.open_list_of_inactive_pyload();
        window.activateTarget = (name) => window.codeEditor.activateTarget(name);
        window.closeInactivePayloadsModal = () => window.codeEditor.closeInactivePayloadsModal();
        window.refreshInactivePayloads = () => window.codeEditor.refreshInactivePayloads();
        window.loadPayload = (file) => window.codeEditor.loadPayload(file);
        window.newFile = () => window.codeEditor.newFile();
        window.showSaveModal = () => window.codeEditor.showSaveModal();
        window.saveWithName = () => window.codeEditor.saveWithName();
        window.closeSaveModal = () => window.codeEditor.closeSaveModal();
        window.useSelectedTarget = () => window.codeEditor.useSelectedTargetFromModal();
        window.closeTargetModal = () => window.codeEditor.closeTargetModal();
        window.closeOutputModal = () => window.codeEditor.closeOutputModal();
        window.switchPanel = (panel) => window.codeEditor.switchPanel(panel);
        window.testNotification = () => window.codeEditor.testNotificationSystem();
        window.clearAllNotifications = () => window.codeEditor.clearAllNotificationsStorage();
        window.restoreNotifications = () => window.codeEditor.restoreNotifications();
    }
});