// Mac OS Simulator JavaScript - Fixed Version

class MacOSSimulator {
    constructor() {
        this.windows = new Map();
        this.activeWindow = null;
        this.windowCounter = 0;
        this.zIndexCounter = 100;
        this.isDragging = false;
        this.dragOffset = { x: 0, y: 0 };
        this.notes = this.loadNotes();
        this.currentNote = null;
        this.musicTracks = [
            { title: "Demo Track 1", artist: "Sample Artist", album: "Web Demo", duration: "3:45" },
            { title: "Demo Track 2", artist: "Another Artist", album: "Digital Collection", duration: "4:12" }
        ];
        this.currentTrack = 0;
        this.isPlaying = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateTime();
        this.loadSampleNotes();
        setInterval(() => this.updateTime(), 1000);
    }

    setupEventListeners() {
        // Dock app launches - improved reliability
        document.querySelectorAll('.dock-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const appName = item.dataset.app;
                
                // Prevent multiple rapid clicks
                if (item.classList.contains('launching')) return;
                
                this.launchApp(appName, item);
            });
        });

        // Right-click context menu
        document.addEventListener('contextmenu', this.handleContextMenu.bind(this));
        
        // Window management
        document.addEventListener('mousedown', this.handleMouseDown.bind(this));
        document.addEventListener('mousemove', this.handleMouseMove.bind(this));
        document.addEventListener('mouseup', this.handleMouseUp.bind(this));

        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
        
        // Click outside to dismiss context menu
        document.addEventListener('click', this.dismissContextMenu.bind(this));
    }

    updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const timeElement = document.getElementById('currentTime');
        if (timeElement) {
            timeElement.textContent = timeString;
        }
    }

    launchApp(appName, dockItem) {
        // Add bounce animation
        dockItem.classList.add('launching');
        
        // Create window immediately but with slight delay for visual feedback
        setTimeout(() => {
            switch(appName) {
                case 'calculator':
                    this.createCalculatorWindow();
                    break;
                case 'notes':
                    this.createNotesWindow();
                    break;
                case 'sketch':
                    this.createSketchWindow();
                    break;
                case 'music':
                    this.createMusicWindow();
                    break;
                case 'terminal':
                    this.createTerminalWindow();
                    break;
                case 'finder':
                    this.createFinderWindow();
                    break;
            }
        }, 100);
        
        // Remove bounce animation
        setTimeout(() => {
            dockItem.classList.remove('launching');
        }, 800);
    }

    createWindow(title, content, width = 400, height = 300) {
        const windowId = `window-${this.windowCounter++}`;
        const template = document.getElementById('window-template');
        const windowElement = template.content.cloneNode(true);
        const window = windowElement.querySelector('.window');
        
        window.id = windowId;
        window.style.width = `${width}px`;
        window.style.height = `${height}px`;
        
        // Better window positioning to avoid overlaps
        const offsetX = (this.windowCounter % 5) * 40 + 50;
        const offsetY = (this.windowCounter % 5) * 40 + 50;
        window.style.left = `${offsetX}px`;
        window.style.top = `${offsetY}px`;
        window.style.zIndex = this.zIndexCounter++;
        
        const titleElement = window.querySelector('.window-title');
        const contentElement = window.querySelector('.window-content');
        
        titleElement.textContent = title;
        contentElement.appendChild(content);
        
        // Window controls
        const closeBtn = window.querySelector('.close-btn');
        const minimizeBtn = window.querySelector('.minimize-btn');
        const maximizeBtn = window.querySelector('.maximize-btn');
        
        closeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.closeWindow(windowId);
        });
        minimizeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.minimizeWindow(windowId);
        });
        maximizeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.maximizeWindow(windowId);
        });
        
        // Window activation - improved
        window.addEventListener('mousedown', (e) => {
            if (!e.target.closest('.window-header')) return;
            this.activateWindow(windowId);
        });
        
        document.getElementById('windows-container').appendChild(window);
        
        // Opening animation
        window.classList.add('opening');
        setTimeout(() => window.classList.remove('opening'), 400);
        
        this.windows.set(windowId, window);
        this.activateWindow(windowId);
        
        return { window, windowId };
    }

    closeWindow(windowId) {
        const window = this.windows.get(windowId);
        if (window) {
            window.classList.add('closing');
            setTimeout(() => {
                if (window.parentNode) {
                    window.remove();
                }
                this.windows.delete(windowId);
                if (this.activeWindow === windowId) {
                    this.activeWindow = null;
                    // Activate the topmost remaining window
                    this.activateTopWindow();
                }
            }, 300);
        }
    }

    minimizeWindow(windowId) {
        const window = this.windows.get(windowId);
        if (window) {
            window.style.transform = 'scale(0.1) translateY(100px)';
            window.style.opacity = '0';
            window.style.pointerEvents = 'none';
            setTimeout(() => {
                window.style.display = 'none';
            }, 300);
        }
    }

    maximizeWindow(windowId) {
        const window = this.windows.get(windowId);
        if (window) {
            if (window.dataset.maximized === 'true') {
                // Restore
                window.style.width = window.dataset.originalWidth;
                window.style.height = window.dataset.originalHeight;
                window.style.left = window.dataset.originalLeft;
                window.style.top = window.dataset.originalTop;
                window.style.transform = 'none';
                window.dataset.maximized = 'false';
            } else {
                // Maximize
                window.dataset.originalWidth = window.style.width;
                window.dataset.originalHeight = window.style.height;
                window.dataset.originalLeft = window.style.left;
                window.dataset.originalTop = window.style.top;
                
                window.style.width = 'calc(100vw - 32px)';
                window.style.height = 'calc(100vh - 60px)';
                window.style.left = '16px';
                window.style.top = '16px';
                window.style.transform = 'none';
                window.dataset.maximized = 'true';
            }
        }
    }

    activateWindow(windowId) {
        // Deactivate all windows
        this.windows.forEach(window => {
            window.classList.remove('active');
        });
        
        // Activate selected window
        const window = this.windows.get(windowId);
        if (window) {
            window.classList.add('active');
            window.style.zIndex = this.zIndexCounter++;
            this.activeWindow = windowId;
        }
    }

    activateTopWindow() {
        let topWindow = null;
        let topZIndex = 0;
        
        this.windows.forEach((window, windowId) => {
            const zIndex = parseInt(window.style.zIndex) || 0;
            if (zIndex > topZIndex) {
                topZIndex = zIndex;
                topWindow = windowId;
            }
        });
        
        if (topWindow) {
            this.activateWindow(topWindow);
        }
    }

    handleContextMenu(e) {
        e.preventDefault();
        this.dismissContextMenu();
        
        const contextMenu = document.createElement('div');
        contextMenu.id = 'context-menu';
        contextMenu.style.cssText = `
            position: fixed;
            top: ${e.clientY}px;
            left: ${e.clientX}px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            padding: 8px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            z-index: 9999;
            min-width: 120px;
            font-size: 13px;
        `;
        
        const menuItems = [
            { text: 'New Folder', action: () => console.log('New Folder') },
            { text: 'Get Info', action: () => console.log('Get Info') },
            { text: 'Change Desktop Background', action: () => this.changeBackground() }
        ];
        
        menuItems.forEach(item => {
            const menuItem = document.createElement('div');
            menuItem.textContent = item.text;
            menuItem.style.cssText = `
                padding: 6px 16px;
                cursor: pointer;
                transition: background 0.2s ease;
            `;
            menuItem.addEventListener('mouseenter', () => {
                menuItem.style.background = 'rgba(0, 122, 255, 0.1)';
            });
            menuItem.addEventListener('mouseleave', () => {
                menuItem.style.background = 'none';
            });
            menuItem.addEventListener('click', () => {
                item.action();
                this.dismissContextMenu();
            });
            contextMenu.appendChild(menuItem);
        });
        
        document.body.appendChild(contextMenu);
    }

    dismissContextMenu() {
        const existingMenu = document.getElementById('context-menu');
        if (existingMenu) {
            existingMenu.remove();
        }
    }

    changeBackground() {
        const backgrounds = [
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
        ];
        
        const currentBg = document.querySelector('.desktop-background').style.background;
        const currentIndex = backgrounds.findIndex(bg => bg === currentBg);
        const nextIndex = (currentIndex + 1) % backgrounds.length;
        
        document.querySelector('.desktop-background').style.background = backgrounds[nextIndex];
    }

    handleMouseDown(e) {
        const window = e.target.closest('.window');
        if (window && e.target.closest('.window-header') && !e.target.closest('.control-btn')) {
            this.isDragging = true;
            this.activateWindow(window.id);
            
            const rect = window.getBoundingClientRect();
            this.dragOffset.x = e.clientX - rect.left;
            this.dragOffset.y = e.clientY - rect.top;
            
            window.style.cursor = 'grabbing';
            e.preventDefault();
        }
    }

    handleMouseMove(e) {
        if (this.isDragging && this.activeWindow) {
            const window = this.windows.get(this.activeWindow);
            if (window) {
                const x = Math.max(0, Math.min(window.parentElement.clientWidth - window.offsetWidth, e.clientX - this.dragOffset.x));
                const y = Math.max(0, Math.min(window.parentElement.clientHeight - window.offsetHeight, e.clientY - this.dragOffset.y));
                
                window.style.left = `${x}px`;
                window.style.top = `${y}px`;
            }
        }
    }

    handleMouseUp() {
        if (this.isDragging && this.activeWindow) {
            const window = this.windows.get(this.activeWindow);
            if (window) {
                window.style.cursor = 'default';
            }
        }
        this.isDragging = false;
    }

    handleKeyDown(e) {
        // Cmd+W to close window
        if (e.metaKey && e.key === 'w' && this.activeWindow) {
            e.preventDefault();
            this.closeWindow(this.activeWindow);
        }
        // Escape to dismiss context menu
        if (e.key === 'Escape') {
            this.dismissContextMenu();
        }
    }

    // Notes functionality - improved storage
    loadNotes() {
        try {
            return JSON.parse(localStorage.getItem('macOSNotes') || '[]');
        } catch (e) {
            return [];
        }
    }

    loadSampleNotes() {
        if (this.notes.length === 0) {
            this.notes = [
                {
                    id: Date.now(),
                    title: "Welcome to Notes",
                    content: "This is your first note! You can create, edit, and organize your thoughts here.",
                    created: new Date().toISOString()
                },
                {
                    id: Date.now() + 1,
                    title: "Meeting Notes",
                    content: "Remember to discuss project timeline and deliverables in tomorrow's meeting.",
                    created: new Date().toISOString()
                }
            ];
            this.saveNotes();
        }
    }

    saveNotes() {
        try {
            localStorage.setItem('macOSNotes', JSON.stringify(this.notes));
        } catch (e) {
            console.warn('Could not save notes to localStorage');
        }
    }

    // Calculator App
    createCalculatorWindow() {
        const template = document.getElementById('calculator-template');
        const content = template.content.cloneNode(true);
        const { window, windowId } = this.createWindow('Calculator', content, 280, 400);
        
        this.setupCalculator(window);
    }

    setupCalculator(window) {
        const display = window.querySelector('.display-value');
        const buttons = window.querySelectorAll('.calc-btn');
        let currentValue = '0';
        let operator = null;
        let waitingForNewValue = false;
        let previousValue = null;

        const updateDisplay = () => {
            display.textContent = currentValue;
        };

        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                const value = button.textContent;
                
                if (button.classList.contains('number')) {
                    if (waitingForNewValue) {
                        currentValue = value;
                        waitingForNewValue = false;
                    } else {
                        currentValue = currentValue === '0' ? value : currentValue + value;
                    }
                } else if (button.classList.contains('operator')) {
                    if (operator && !waitingForNewValue) {
                        const result = this.calculate(previousValue, currentValue, operator);
                        currentValue = String(result);
                        previousValue = result;
                    } else {
                        previousValue = parseFloat(currentValue);
                    }
                    
                    operator = value;
                    waitingForNewValue = true;
                } else if (button.classList.contains('equals')) {
                    if (operator && !waitingForNewValue) {
                        const result = this.calculate(previousValue, currentValue, operator);
                        currentValue = String(result);
                        operator = null;
                        previousValue = null;
                        waitingForNewValue = true;
                    }
                } else if (button.classList.contains('clear')) {
                    currentValue = '0';
                    operator = null;
                    previousValue = null;
                    waitingForNewValue = false;
                }
                
                updateDisplay();
            });
        });

        // Keyboard support
        window.addEventListener('keydown', (e) => {
            if (window.classList.contains('active')) {
                const key = e.key;
                if (/[0-9.]/.test(key)) {
                    const btn = Array.from(buttons).find(b => b.textContent === key);
                    if (btn) btn.click();
                } else if (key === '+' || key === '-') {
                    const btn = Array.from(buttons).find(b => b.textContent === (key === '+' ? '+' : '−'));
                    if (btn) btn.click();
                } else if (key === '*') {
                    const btn = Array.from(buttons).find(b => b.textContent === '×');
                    if (btn) btn.click();
                } else if (key === '/') {
                    e.preventDefault();
                    const btn = Array.from(buttons).find(b => b.textContent === '÷');
                    if (btn) btn.click();
                } else if (key === 'Enter' || key === '=') {
                    const btn = Array.from(buttons).find(b => b.textContent === '=');
                    if (btn) btn.click();
                } else if (key === 'Escape') {
                    const btn = Array.from(buttons).find(b => b.textContent === 'AC');
                    if (btn) btn.click();
                }
            }
        });
    }

    calculate(prev, current, operator) {
        const a = parseFloat(prev);
        const b = parseFloat(current);
        
        switch (operator) {
            case '+': return a + b;
            case '−': return a - b;
            case '×': return a * b;
            case '÷': return b !== 0 ? a / b : 0;
            case '%': return a % b;
            default: return b;
        }
    }

    // Notes App
    createNotesWindow() {
        const template = document.getElementById('notes-template');
        const content = template.content.cloneNode(true);
        const { window, windowId } = this.createWindow('Notes', content, 600, 400);
        
        this.setupNotes(window);
    }

    setupNotes(window) {
        const notesList = window.querySelector('.notes-list');
        const newNoteBtn = window.querySelector('.new-note-btn');
        const titleInput = window.querySelector('.note-title');
        const contentInput = window.querySelector('.note-content');

        const renderNotes = () => {
            notesList.innerHTML = '';
            this.notes.forEach(note => {
                const noteItem = document.createElement('div');
                noteItem.className = 'note-item';
                noteItem.textContent = note.title || 'Untitled';
                noteItem.addEventListener('click', () => this.selectNote(note.id, window));
                notesList.appendChild(noteItem);
            });
        };

        newNoteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const newNote = {
                id: Date.now(),
                title: '',
                content: '',
                created: new Date().toISOString()
            };
            this.notes.unshift(newNote);
            renderNotes();
            this.selectNote(newNote.id, window);
        });

        titleInput.addEventListener('input', () => {
            if (this.currentNote) {
                this.currentNote.title = titleInput.value;
                renderNotes();
                this.saveNotes();
            }
        });

        contentInput.addEventListener('input', () => {
            if (this.currentNote) {
                this.currentNote.content = contentInput.value;
                this.saveNotes();
            }
        });

        renderNotes();
        if (this.notes.length > 0) {
            this.selectNote(this.notes[0].id, window);
        }
    }

    selectNote(noteId, window) {
        this.currentNote = this.notes.find(note => note.id === noteId);
        if (this.currentNote) {
            const titleInput = window.querySelector('.note-title');
            const contentInput = window.querySelector('.note-content');
            const noteItems = window.querySelectorAll('.note-item');
            
            titleInput.value = this.currentNote.title;
            contentInput.value = this.currentNote.content;
            
            noteItems.forEach(item => item.classList.remove('active'));
            const activeItem = Array.from(noteItems).find(item => 
                item.textContent === (this.currentNote.title || 'Untitled')
            );
            if (activeItem) activeItem.classList.add('active');
        }
    }

    // Sketch App
    createSketchWindow() {
        const template = document.getElementById('sketch-template');
        const content = template.content.cloneNode(true);
        const { window, windowId } = this.createWindow('Sketch', content, 700, 500);
        
        this.setupSketch(window);
    }

    setupSketch(window) {
        const canvas = window.querySelector('.sketch-canvas');
        const ctx = canvas.getContext('2d');
        const toolBtns = window.querySelectorAll('.tool-btn');
        const colorPicker = window.querySelector('.color-picker');
        const sizeSlider = window.querySelector('.size-slider');
        const clearBtn = window.querySelector('.clear-btn');
        
        let isDrawing = false;
        let currentTool = 'pen';
        let currentColor = '#000000';
        let currentSize = 3;

        // Set canvas background
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        toolBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                toolBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentTool = btn.dataset.tool;
                
                if (currentTool === 'eraser') {
                    canvas.style.cursor = 'cell';
                } else {
                    canvas.style.cursor = 'crosshair';
                }
            });
        });

        colorPicker.addEventListener('change', (e) => {
            currentColor = e.target.value;
        });

        sizeSlider.addEventListener('input', (e) => {
            currentSize = e.target.value;
        });

        clearBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            ctx.fillStyle = 'white';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        });

        const startDrawing = (e) => {
            isDrawing = true;
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            ctx.beginPath();
            ctx.moveTo(x, y);
        };

        const draw = (e) => {
            if (!isDrawing) return;
            
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            ctx.lineWidth = currentSize;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            
            if (currentTool === 'eraser') {
                ctx.globalCompositeOperation = 'destination-out';
            } else {
                ctx.globalCompositeOperation = 'source-over';
                ctx.strokeStyle = currentColor;
            }
            
            ctx.lineTo(x, y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(x, y);
        };

        const stopDrawing = () => {
            isDrawing = false;
            ctx.beginPath();
        };

        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('mouseout', stopDrawing);
    }

    // Music App
    createMusicWindow() {
        const template = document.getElementById('music-template');
        const content = template.content.cloneNode(true);
        const { window, windowId } = this.createWindow('Music', content, 400, 500);
        
        this.setupMusic(window);
    }

    setupMusic(window) {
        const playBtn = window.querySelector('.play-btn');
        const prevBtn = window.querySelector('.prev-btn');
        const nextBtn = window.querySelector('.next-btn');
        const progressTrack = window.querySelector('.progress-track');
        const progressFill = window.querySelector('.progress-fill');
        const currentTimeSpan = window.querySelector('.current-time');
        const totalTimeSpan = window.querySelector('.total-time');
        const trackTitle = window.querySelector('.track-title');
        const trackArtist = window.querySelector('.track-artist');
        const playlistItems = window.querySelector('.playlist-items');
        const volumeSlider = window.querySelector('.volume-slider');

        let currentTime = 0;
        let duration = 225; // 3:45 in seconds
        let progressInterval;

        const updateTrackInfo = () => {
            const track = this.musicTracks[this.currentTrack];
            trackTitle.textContent = track.title;
            trackArtist.textContent = track.artist;
            totalTimeSpan.textContent = track.duration;
            duration = this.parseDuration(track.duration);
            currentTime = 0;
        };

        const renderPlaylist = () => {
            playlistItems.innerHTML = '';
            this.musicTracks.forEach((track, index) => {
                const item = document.createElement('div');
                item.className = 'playlist-item';
                if (index === this.currentTrack && this.isPlaying) {
                    item.classList.add('playing');
                }
                item.innerHTML = `
                    <div>${track.title}</div>
                    <div style="font-size: 12px; color: #666;">${track.artist}</div>
                `;
                item.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.currentTrack = index;
                    updateTrackInfo();
                    updateProgress();
                    renderPlaylist();
                });
                playlistItems.appendChild(item);
            });
        };

        const updateProgress = () => {
            const percentage = (currentTime / duration) * 100;
            progressFill.style.width = `${Math.min(100, percentage)}%`;
            currentTimeSpan.textContent = this.formatTime(currentTime);
        };

        const startProgress = () => {
            if (progressInterval) clearInterval(progressInterval);
            progressInterval = setInterval(() => {
                currentTime += 1;
                if (currentTime >= duration) {
                    this.nextTrack(window);
                    return;
                }
                updateProgress();
            }, 1000);
        };

        const stopProgress = () => {
            if (progressInterval) {
                clearInterval(progressInterval);
                progressInterval = null;
            }
        };

        playBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.isPlaying = !this.isPlaying;
            playBtn.textContent = this.isPlaying ? '⏸️' : '▶️';
            
            if (this.isPlaying) {
                startProgress();
            } else {
                stopProgress();
            }
            renderPlaylist();
        });

        prevBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.currentTrack = (this.currentTrack - 1 + this.musicTracks.length) % this.musicTracks.length;
            updateTrackInfo();
            updateProgress();
            renderPlaylist();
        });

        nextBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.currentTrack = (this.currentTrack + 1) % this.musicTracks.length;
            updateTrackInfo();
            updateProgress();
            renderPlaylist();
        });

        progressTrack.addEventListener('click', (e) => {
            e.stopPropagation();
            const rect = progressTrack.getBoundingClientRect();
            const percentage = (e.clientX - rect.left) / rect.width;
            currentTime = Math.max(0, Math.min(duration, percentage * duration));
            updateProgress();
        });

        updateTrackInfo();
        renderPlaylist();
        updateProgress();
    }

    parseDuration(duration) {
        const parts = duration.split(':');
        return parseInt(parts[0]) * 60 + parseInt(parts[1]);
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    // Terminal App
    createTerminalWindow() {
        const template = document.getElementById('terminal-template');
        const content = template.content.cloneNode(true);
        const { window, windowId } = this.createWindow('Terminal', content, 600, 400);
        
        this.setupTerminal(window);
    }

    setupTerminal(window) {
        const output = window.querySelector('.terminal-output');
        const input = window.querySelector('.terminal-input');
        let commandHistory = [];
        let historyIndex = -1;

        const addOutput = (text, isCommand = false) => {
            const line = document.createElement('div');
            line.className = 'terminal-line';
            if (isCommand) {
                line.innerHTML = `<span style="color: #00ff00;">user@macOS-Simulator ~ % </span>${text}`;
            } else {
                line.textContent = text;
            }
            output.appendChild(line);
            output.scrollTop = output.scrollHeight;
        };

        const processCommand = (command) => {
            addOutput(command, true);
            if (command.trim()) {
                commandHistory.unshift(command);
                historyIndex = -1;
            }

            const cmd = command.toLowerCase().trim();
            switch (cmd) {
                case 'help':
                    addOutput('Available commands:');
                    addOutput('  help    - Show this help message');
                    addOutput('  ls      - List directory contents');
                    addOutput('  pwd     - Print working directory');
                    addOutput('  date    - Show current date and time');
                    addOutput('  clear   - Clear terminal output');
                    addOutput('  whoami  - Display current user');
                    addOutput('  uname   - System information');
                    addOutput('  echo    - Display message');
                    break;
                case 'ls':
                    addOutput('Desktop     Documents   Downloads   Applications');
                    addOutput('Pictures    Music       Movies      Library');
                    break;
                case 'pwd':
                    addOutput('/Users/user');
                    break;
                case 'date':
                    addOutput(new Date().toString());
                    break;
                case 'clear':
                    output.innerHTML = '';
                    break;
                case 'whoami':
                    addOutput('user');
                    break;
                case 'uname':
                    addOutput('macOS Simulator Web Edition 14.0');
                    break;
                default:
                    if (cmd.startsWith('echo ')) {
                        addOutput(command.substring(5));
                    } else if (cmd) {
                        addOutput(`command not found: ${cmd}`);
                    }
            }
        };

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                processCommand(input.value);
                input.value = '';
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (historyIndex < commandHistory.length - 1) {
                    historyIndex++;
                    input.value = commandHistory[historyIndex] || '';
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (historyIndex > 0) {
                    historyIndex--;
                    input.value = commandHistory[historyIndex] || '';
                } else if (historyIndex === 0) {
                    historyIndex = -1;
                    input.value = '';
                }
            }
        });

        // Focus input when window is active
        window.addEventListener('mousedown', () => {
            setTimeout(() => input.focus(), 100);
        });

        // Initial message
        addOutput('Welcome to macOS Simulator Terminal');
        addOutput('Type "help" for available commands');
        input.focus();
    }

    // Finder App
    createFinderWindow() {
        const template = document.getElementById('finder-template');
        const content = template.content.cloneNode(true);
        const { window, windowId } = this.createWindow('Finder', content, 700, 500);
        
        this.setupFinder(window);
    }

    setupFinder(window) {
        const sidebarItems = window.querySelectorAll('.sidebar-item');
        const fileGrid = window.querySelector('.file-grid');
        const pathDisplay = window.querySelector('.path-display');
        const viewBtns = window.querySelectorAll('.view-btn');
        const backBtn = window.querySelector('.back-btn');
        const forwardBtn = window.querySelector('.forward-btn');

        const fileStructure = {
            '/': [
                { name: 'Applications', type: 'folder', icon: '📁' },
                { name: 'Documents', type: 'folder', icon: '📁' },
                { name: 'Downloads', type: 'folder', icon: '📁' },
                { name: 'Pictures', type: 'folder', icon: '📁' },
                { name: 'Music', type: 'folder', icon: '📁' },
                { name: 'Sample.txt', type: 'file', icon: '📄' }
            ],
            '/applications': [
                { name: 'Calculator.app', type: 'app', icon: '🧮' },
                { name: 'Notes.app', type: 'app', icon: '📝' },
                { name: 'Music.app', type: 'app', icon: '🎵' },
                { name: 'Sketch.app', type: 'app', icon: '🎨' },
                { name: 'Terminal.app', type: 'app', icon: '⚫' },
                { name: 'Finder.app', type: 'app', icon: '📁' }
            ],
            '/documents': [
                { name: 'Resume.pdf', type: 'file', icon: '📄' },
                { name: 'Project Plans', type: 'folder', icon: '📁' },
                { name: 'Notes.txt', type: 'file', icon: '📄' }
            ],
            '/downloads': [
                { name: 'installer.dmg', type: 'file', icon: '💿' },
                { name: 'screenshot.png', type: 'file', icon: '🖼️' },
                { name: 'archive.zip', type: 'file', icon: '🗜️' }
            ]
        };

        let currentPath = '/';
        let pathHistory = ['/'];
        let historyIndex = 0;

        const renderFiles = () => {
            fileGrid.innerHTML = '';
            const files = fileStructure[currentPath] || [];
            
            files.forEach(file => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item';
                fileItem.innerHTML = `
                    <div class="file-icon">${file.icon}</div>
                    <div class="file-name">${file.name}</div>
                `;
                
                if (file.type === 'folder') {
                    fileItem.addEventListener('dblclick', (e) => {
                        e.stopPropagation();
                        const newPath = `${currentPath}${file.name.toLowerCase()}`.replace('//', '/');
                        if (fileStructure[newPath]) {
                            currentPath = newPath;
                            pathHistory = pathHistory.slice(0, historyIndex + 1);
                            pathHistory.push(currentPath);
                            historyIndex = pathHistory.length - 1;
                            pathDisplay.textContent = file.name;
                            renderFiles();
                            updateNavButtons();
                        }
                    });
                }
                
                fileGrid.appendChild(fileItem);
            });
        };

        const updateNavButtons = () => {
            backBtn.disabled = historyIndex <= 0;
            forwardBtn.disabled = historyIndex >= pathHistory.length - 1;
        };

        sidebarItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                sidebarItems.forEach(si => si.classList.remove('active'));
                item.classList.add('active');
                currentPath = item.dataset.path;
                pathDisplay.textContent = item.textContent;
                pathHistory = pathHistory.slice(0, historyIndex + 1);
                pathHistory.push(currentPath);
                historyIndex = pathHistory.length - 1;
                renderFiles();
                updateNavButtons();
            });
        });

        backBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (historyIndex > 0) {
                historyIndex--;
                currentPath = pathHistory[historyIndex];
                const pathName = currentPath === '/' ? 'Desktop' : currentPath.split('/').pop();
                pathDisplay.textContent = pathName;
                renderFiles();
                updateNavButtons();
            }
        });

        forwardBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (historyIndex < pathHistory.length - 1) {
                historyIndex++;
                currentPath = pathHistory[historyIndex];
                const pathName = currentPath === '/' ? 'Desktop' : currentPath.split('/').pop();
                pathDisplay.textContent = pathName;
                renderFiles();
                updateNavButtons();
            }
        });

        viewBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                viewBtns.forEach(vb => vb.classList.remove('active'));
                btn.classList.add('active');
                
                if (btn.dataset.view === 'list') {
                    fileGrid.style.gridTemplateColumns = '1fr';
                    fileGrid.style.gap = '4px';
                } else {
                    fileGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(80px, 1fr))';
                    fileGrid.style.gap = '16px';
                }
            });
        });

        renderFiles();
        updateNavButtons();
    }
}

// Initialize the Mac OS Simulator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new MacOSSimulator();
});