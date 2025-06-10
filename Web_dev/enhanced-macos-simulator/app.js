class MacOSSimulator {
    constructor() {
        this.windows = {};
        this.activeWindow = null;
        this.zIndex = 1000;
        this.isDragging = false;
        this.isResizing = false;
        this.dragOffset = { x: 0, y: 0 };
        this.resizeData = {};
        
        // Music player state
        this.audioFiles = [];
        this.currentTrackIndex = 0;
        this.isPlaying = false;
        
        // Calculator state
        this.calculatorState = {
            display: '0',
            previousValue: null,
            operation: null,
            waitingForOperand: false
        };
        
        // Sketch state
        this.isDrawing = false;
        this.brushSize = 5;
        this.brushColor = '#000000';
        
        // Terminal state
        this.terminalHistory = [];
        this.terminalCommands = {
            'help': 'Available commands: help, clear, ls, pwd, whoami, date, echo',
            'ls': 'Desktop  Documents  Downloads  Pictures  Music  Movies',
            'pwd': '/Users/user',
            'whoami': 'user',
            'clear': '',
            'date': new Date().toString()
        };
        
        this.init();
    }
    
    init() {
        this.updateTime();
        this.setupEventListeners();
        this.initializeApps();
    }
    
    updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        document.getElementById('menu-time').textContent = timeString;
        setTimeout(() => this.updateTime(), 1000);
    }
    
    setupEventListeners() {
        // Dock app clicks
        document.querySelectorAll('.dock__app').forEach(app => {
            app.addEventListener('click', (e) => {
                this.launchApp(app.dataset.app);
            });
        });
        
        // Window controls
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('window__control--close')) {
                this.closeWindow(e.target.closest('.window'));
            } else if (e.target.classList.contains('window__control--minimize')) {
                this.minimizeWindow(e.target.closest('.window'));
            } else if (e.target.classList.contains('window__control--maximize')) {
                this.maximizeWindow(e.target.closest('.window'));
            }
        });
        
        // Window dragging
        document.addEventListener('mousedown', (e) => {
            if (e.target.classList.contains('window__titlebar') || e.target.closest('.window__titlebar')) {
                this.startDragging(e);
            } else if (e.target.classList.contains('resize-handle')) {
                this.startResizing(e);
            }
        });
        
        document.addEventListener('mousemove', (e) => {
            if (this.isDragging) {
                this.dragWindow(e);
            } else if (this.isResizing) {
                this.resizeWindow(e);
            }
        });
        
        document.addEventListener('mouseup', () => {
            this.stopDragging();
            this.stopResizing();
        });
        
        // Window focus
        document.addEventListener('mousedown', (e) => {
            const window = e.target.closest('.window');
            if (window) {
                this.focusWindow(window);
            }
        });
    }
    
    launchApp(appId) {
        const dockApp = document.querySelector(`[data-app="${appId}"]`);
        const window = document.getElementById(`${appId}-window`);
        
        // Dock bounce animation
        dockApp.classList.add('bouncing');
        setTimeout(() => dockApp.classList.remove('bouncing'), 500);
        
        // Show and animate window
        setTimeout(() => {
            window.style.display = 'block';
            window.classList.add('opening');
            this.focusWindow(window);
            
            setTimeout(() => window.classList.remove('opening'), 300);
        }, 200);
    }
    
    closeWindow(window) {
        window.style.display = 'none';
        if (this.activeWindow === window) {
            this.activeWindow = null;
        }
    }
    
    minimizeWindow(window) {
        window.style.transform = 'scale(0.1)';
        window.style.opacity = '0';
        setTimeout(() => {
            window.style.display = 'none';
            window.style.transform = '';
            window.style.opacity = '';
        }, 300);
    }
    
    maximizeWindow(window) {
        if (window.dataset.maximized === 'true') {
            // Restore
            window.style.width = window.dataset.originalWidth;
            window.style.height = window.dataset.originalHeight;
            window.style.left = window.dataset.originalLeft;
            window.style.top = window.dataset.originalTop;
            window.dataset.maximized = 'false';
        } else {
            // Maximize
            window.dataset.originalWidth = window.style.width || window.offsetWidth + 'px';
            window.dataset.originalHeight = window.style.height || window.offsetHeight + 'px';
            window.dataset.originalLeft = window.style.left || window.offsetLeft + 'px';
            window.dataset.originalTop = window.style.top || window.offsetTop + 'px';
            
            window.style.width = 'calc(100vw - 32px)';
            window.style.height = 'calc(100vh - 140px)';
            window.style.left = '16px';
            window.style.top = '44px';
            window.dataset.maximized = 'true';
        }
    }
    
    focusWindow(window) {
        if (this.activeWindow) {
            this.activeWindow.classList.remove('active');
        }
        this.activeWindow = window;
        window.classList.add('active');
        window.style.zIndex = ++this.zIndex;
    }
    
    startDragging(e) {
        const window = e.target.closest('.window');
        if (!window) return;
        
        this.isDragging = true;
        this.activeWindow = window;
        this.focusWindow(window);
        
        const rect = window.getBoundingClientRect();
        this.dragOffset.x = e.clientX - rect.left;
        this.dragOffset.y = e.clientY - rect.top;
        
        window.style.cursor = 'move';
        document.body.style.userSelect = 'none';
    }
    
    dragWindow(e) {
        if (!this.isDragging || !this.activeWindow) return;
        
        const x = e.clientX - this.dragOffset.x;
        const y = Math.max(28, e.clientY - this.dragOffset.y); // Prevent dragging above menu bar
        
        this.activeWindow.style.left = x + 'px';
        this.activeWindow.style.top = y + 'px';
    }
    
    stopDragging() {
        if (this.isDragging) {
            this.isDragging = false;
            if (this.activeWindow) {
                this.activeWindow.style.cursor = '';
            }
            document.body.style.userSelect = '';
        }
    }
    
    startResizing(e) {
        const window = e.target.closest('.window');
        if (!window) return;
        
        this.isResizing = true;
        this.activeWindow = window;
        this.focusWindow(window);
        
        const rect = window.getBoundingClientRect();
        this.resizeData = {
            window,
            startX: e.clientX,
            startY: e.clientY,
            startWidth: rect.width,
            startHeight: rect.height,
            startLeft: rect.left,
            startTop: rect.top,
            handle: e.target.className.split('resize-handle--')[1]
        };
        
        document.body.style.userSelect = 'none';
    }
    
    resizeWindow(e) {
        if (!this.isResizing || !this.resizeData.window) return;
        
        const { window, startX, startY, startWidth, startHeight, startLeft, startTop, handle } = this.resizeData;
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        let newWidth = startWidth;
        let newHeight = startHeight;
        let newLeft = startLeft;
        let newTop = startTop;
        
        switch (handle) {
            case 'se':
                newWidth = Math.max(300, startWidth + deltaX);
                newHeight = Math.max(200, startHeight + deltaY);
                break;
            case 'sw':
                newWidth = Math.max(300, startWidth - deltaX);
                newHeight = Math.max(200, startHeight + deltaY);
                newLeft = startLeft + deltaX;
                break;
            case 'ne':
                newWidth = Math.max(300, startWidth + deltaX);
                newHeight = Math.max(200, startHeight - deltaY);
                newTop = startTop + deltaY;
                break;
            case 'nw':
                newWidth = Math.max(300, startWidth - deltaX);
                newHeight = Math.max(200, startHeight - deltaY);
                newLeft = startLeft + deltaX;
                newTop = startTop + deltaY;
                break;
            case 'n':
                newHeight = Math.max(200, startHeight - deltaY);
                newTop = startTop + deltaY;
                break;
            case 's':
                newHeight = Math.max(200, startHeight + deltaY);
                break;
            case 'e':
                newWidth = Math.max(300, startWidth + deltaX);
                break;
            case 'w':
                newWidth = Math.max(300, startWidth - deltaX);
                newLeft = startLeft + deltaX;
                break;
        }
        
        window.style.width = newWidth + 'px';
        window.style.height = newHeight + 'px';
        window.style.left = newLeft + 'px';
        window.style.top = Math.max(28, newTop) + 'px';
    }
    
    stopResizing() {
        if (this.isResizing) {
            this.isResizing = false;
            this.resizeData = {};
            document.body.style.userSelect = '';
        }
    }
    
    initializeApps() {
        this.initCalculator();
        this.initNotes();
        this.initSketch();
        this.initMusicPlayer();
        this.initTerminal();
        this.initFinder();
    }
    
    initCalculator() {
        const display = document.getElementById('calc-display');
        const buttons = document.querySelectorAll('.calculator__btn');
        
        buttons.forEach(button => {
            button.addEventListener('click', () => {
                if (button.dataset.number) {
                    this.calculatorInputNumber(button.dataset.number);
                } else if (button.dataset.action) {
                    this.calculatorInputAction(button.dataset.action);
                }
                display.value = this.calculatorState.display;
            });
        });
    }
    
    calculatorInputNumber(num) {
        const { display, waitingForOperand } = this.calculatorState;
        
        if (waitingForOperand) {
            this.calculatorState.display = num;
            this.calculatorState.waitingForOperand = false;
        } else {
            this.calculatorState.display = display === '0' ? num : display + num;
        }
    }
    
    calculatorInputAction(action) {
        const { display, previousValue, operation } = this.calculatorState;
        const inputValue = parseFloat(display);
        
        switch (action) {
            case 'clear':
                this.calculatorState = {
                    display: '0',
                    previousValue: null,
                    operation: null,
                    waitingForOperand: false
                };
                break;
            case 'equals':
                if (previousValue !== null && operation) {
                    const result = this.calculatorCalculate(previousValue, inputValue, operation);
                    this.calculatorState.display = String(result);
                    this.calculatorState.previousValue = null;
                    this.calculatorState.operation = null;
                    this.calculatorState.waitingForOperand = true;
                }
                break;
            case 'decimal':
                if (display.indexOf('.') === -1) {
                    this.calculatorState.display = display + '.';
                }
                break;
            default:
                if (previousValue === null) {
                    this.calculatorState.previousValue = inputValue;
                } else if (operation) {
                    const result = this.calculatorCalculate(previousValue, inputValue, operation);
                    this.calculatorState.display = String(result);
                    this.calculatorState.previousValue = result;
                }
                this.calculatorState.waitingForOperand = true;
                this.calculatorState.operation = action;
        }
    }
    
    calculatorCalculate(firstValue, secondValue, operation) {
        switch (operation) {
            case 'add': return firstValue + secondValue;
            case 'subtract': return firstValue - secondValue;
            case 'multiply': return firstValue * secondValue;
            case 'divide': return firstValue / secondValue;
            case 'percent': return firstValue / 100;
            default: return secondValue;
        }
    }
    
    initNotes() {
        const newBtn = document.getElementById('notes-new');
        const saveBtn = document.getElementById('notes-save');
        const textarea = document.getElementById('notes-content');
        
        newBtn.addEventListener('click', () => {
            textarea.value = '';
            textarea.focus();
        });
        
        saveBtn.addEventListener('click', () => {
            const content = textarea.value;
            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'note.txt';
            a.click();
            URL.revokeObjectURL(url);
        });
    }
    
    initSketch() {
        const canvas = document.getElementById('sketch-canvas');
        const ctx = canvas.getContext('2d');
        const brushSizeSlider = document.getElementById('brush-size');
        const brushSizeDisplay = document.getElementById('brush-size-display');
        const brushColorPicker = document.getElementById('brush-color');
        const clearBtn = document.getElementById('clear-canvas');
        
        brushSizeSlider.addEventListener('input', () => {
            this.brushSize = brushSizeSlider.value;
            brushSizeDisplay.textContent = this.brushSize + 'px';
        });
        
        brushColorPicker.addEventListener('change', () => {
            this.brushColor = brushColorPicker.value;
        });
        
        clearBtn.addEventListener('click', () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        });
        
        canvas.addEventListener('mousedown', (e) => {
            this.isDrawing = true;
            this.draw(e, ctx, canvas);
        });
        
        canvas.addEventListener('mousemove', (e) => {
            if (this.isDrawing) {
                this.draw(e, ctx, canvas);
            }
        });
        
        canvas.addEventListener('mouseup', () => {
            this.isDrawing = false;
            ctx.beginPath();
        });
    }
    
    draw(e, ctx, canvas) {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        ctx.lineWidth = this.brushSize;
        ctx.lineCap = 'round';
        ctx.strokeStyle = this.brushColor;
        
        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);
    }
    
    initMusicPlayer() {
        const loadBtn = document.getElementById('load-audio-btn');
        const fileInput = document.getElementById('audio-file-input');
        const playBtn = document.getElementById('play-btn');
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const progressBar = document.getElementById('progress-bar');
        const volumeBar = document.getElementById('volume-bar');
        const audio = document.getElementById('audio-player');
        const trackName = document.getElementById('track-name');
        const trackMeta = document.getElementById('track-meta');
        const currentTime = document.getElementById('current-time');
        const totalTime = document.getElementById('total-time');
        const playlist = document.getElementById('playlist');
        
        loadBtn.addEventListener('click', () => fileInput.click());
        
        fileInput.addEventListener('change', (e) => {
            const files = Array.from(e.target.files);
            files.forEach(file => {
                this.audioFiles.push({
                    file,
                    url: URL.createObjectURL(file),
                    name: file.name,
                    size: (file.size / 1024 / 1024).toFixed(2) + ' MB'
                });
            });
            this.updatePlaylist();
            if (this.audioFiles.length === 1) {
                this.loadTrack(0);
            }
        });
        
        playBtn.addEventListener('click', () => {
            if (this.isPlaying) {
                audio.pause();
                this.isPlaying = false;
                playBtn.textContent = '▶️';
            } else {
                audio.play();
                this.isPlaying = true;
                playBtn.textContent = '⏸️';
            }
        });
        
        prevBtn.addEventListener('click', () => {
            if (this.currentTrackIndex > 0) {
                this.loadTrack(this.currentTrackIndex - 1);
            }
        });
        
        nextBtn.addEventListener('click', () => {
            if (this.currentTrackIndex < this.audioFiles.length - 1) {
                this.loadTrack(this.currentTrackIndex + 1);
            }
        });
        
        progressBar.addEventListener('input', () => {
            if (audio.duration) {
                audio.currentTime = (progressBar.value / 100) * audio.duration;
            }
        });
        
        volumeBar.addEventListener('input', () => {
            audio.volume = volumeBar.value / 100;
        });
        
        audio.addEventListener('timeupdate', () => {
            if (audio.duration) {
                const progress = (audio.currentTime / audio.duration) * 100;
                progressBar.value = progress;
                currentTime.textContent = this.formatTime(audio.currentTime);
                totalTime.textContent = this.formatTime(audio.duration);
            }
        });
        
        audio.addEventListener('ended', () => {
            this.isPlaying = false;
            playBtn.textContent = '▶️';
            if (this.currentTrackIndex < this.audioFiles.length - 1) {
                this.loadTrack(this.currentTrackIndex + 1);
            }
        });
        
        audio.volume = 0.5;
    }
    
    loadTrack(index) {
        if (index >= 0 && index < this.audioFiles.length) {
            this.currentTrackIndex = index;
            const track = this.audioFiles[index];
            const audio = document.getElementById('audio-player');
            
            audio.src = track.url;
            document.getElementById('track-name').textContent = track.name;
            document.getElementById('track-meta').textContent = `Size: ${track.size}`;
            
            this.updatePlaylist();
        }
    }
    
    updatePlaylist() {
        const playlist = document.getElementById('playlist');
        playlist.innerHTML = '';
        
        this.audioFiles.forEach((track, index) => {
            const item = document.createElement('div');
            item.className = 'playlist-item';
            if (index === this.currentTrackIndex) {
                item.classList.add('active');
            }
            item.textContent = track.name;
            item.addEventListener('click', () => this.loadTrack(index));
            playlist.appendChild(item);
        });
    }
    
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
    
    initTerminal() {
        const input = document.getElementById('terminal-input');
        const output = document.getElementById('terminal-output');
        
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const command = input.value.trim();
                this.executeTerminalCommand(command, output);
                input.value = '';
            }
        });
        
        input.focus();
    }
    
    executeTerminalCommand(command, output) {
        // Add command to history
        const commandLine = document.createElement('div');
        commandLine.className = 'terminal__line';
        commandLine.innerHTML = `user@macbook:~$ ${command}`;
        output.appendChild(commandLine);
        
        // Execute command
        let result = '';
        if (command === 'clear') {
            output.innerHTML = '<div class="terminal__line">user@macbook:~$ <span class="terminal__cursor"></span></div>';
            return;
        } else if (command.startsWith('echo ')) {
            result = command.substring(5);
        } else if (this.terminalCommands[command]) {
            result = this.terminalCommands[command];
        } else if (command) {
            result = `Command not found: ${command}. Type 'help' for available commands.`;
        }
        
        if (result) {
            const resultLine = document.createElement('div');
            resultLine.className = 'terminal__line';
            resultLine.textContent = result;
            output.appendChild(resultLine);
        }
        
        // Add new prompt
        const newPrompt = document.createElement('div');
        newPrompt.className = 'terminal__line';
        newPrompt.innerHTML = 'user@macbook:~$ <span class="terminal__cursor"></span>';
        output.appendChild(newPrompt);
        
        // Scroll to bottom
        output.scrollTop = output.scrollHeight;
    }
    
    initFinder() {
        const sidebarItems = document.querySelectorAll('.finder__item');
        const files = document.querySelectorAll('.finder__file');
        
        sidebarItems.forEach(item => {
            item.addEventListener('click', () => {
                sidebarItems.forEach(i => i.classList.remove('active'));
                item.classList.add('active');
            });
        });
        
        files.forEach(file => {
            file.addEventListener('dblclick', () => {
                console.log('Opening file:', file.textContent);
            });
        });
    }
}

// Initialize the simulator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new MacOSSimulator();
});