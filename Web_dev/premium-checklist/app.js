// Premium Purchase Checklist Application
class PremiumChecklist {
    constructor() {
        this.correctPin = '0000';
        this.currentPin = '';
        this.isAuthenticated = false;
        this.isDarkMode = false;
        this.editingItemId = null;
        
        // Initialize data with sample items
        this.items = [
            {
                id: 1,
                name: "MacBook Pro 16-inch",
                price: 2499,
                category: "Electronics",
                priority: "High",
                completed: false,
                notes: "M3 Max chip, 32GB RAM, 1TB SSD",
                dateAdded: "2025-06-09"
            },
            {
                id: 2,
                name: "Designer Office Chair",
                price: 899,
                category: "Home",
                priority: "Medium",
                completed: true,
                notes: "Ergonomic, premium leather",
                dateAdded: "2025-06-08"
            },
            {
                id: 3,
                name: "Premium Headphones",
                price: 549,
                category: "Electronics",
                priority: "Low",
                completed: false,
                notes: "Noise cancelling, wireless",
                dateAdded: "2025-06-07"
            }
        ];
        
        this.categories = [
            "Electronics", "Fashion", "Home", "Sports", "Books", 
            "Travel", "Health", "Food", "Other"
        ];
        
        this.smartSuggestions = [
            "iPhone 15 Pro Max", "iPad Pro", "AirPods Pro", "Tesla Model S",
            "Rolex Submariner", "MacBook Air", "PlayStation 5", "Nintendo Switch",
            "Camera Lens", "Standing Desk"
        ];
        
        this.nextId = Math.max(...this.items.map(item => item.id)) + 1;
        this.filteredItems = [...this.items];
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.populateCategories();
        this.updateStats();
        this.renderItems();
        this.initializeTheme();
    }
    
    setupEventListeners() {
        // PIN Screen Events
        document.addEventListener('keydown', (e) => {
            if (!this.isAuthenticated) {
                this.handlePinKeypress(e);
            }
        });
        
        // Keypad Events
        document.querySelectorAll('.keypad-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const digit = e.target.dataset.digit;
                const action = e.target.dataset.action;
                
                if (digit) {
                    this.addPinDigit(digit);
                } else if (action === 'delete') {
                    this.deletePinDigit();
                }
                
                this.animateButton(e.target);
            });
        });
        
        // Main App Events
        document.getElementById('addItemBtn').addEventListener('click', () => this.openModal());
        document.getElementById('addFirstItemBtn').addEventListener('click', () => this.openModal());
        document.getElementById('darkModeToggle').addEventListener('click', () => this.toggleDarkMode());
        
        // Modal Events
        document.getElementById('modalClose').addEventListener('click', () => this.closeModal());
        document.getElementById('cancelBtn').addEventListener('click', () => this.closeModal());
        document.getElementById('itemForm').addEventListener('submit', (e) => this.handleFormSubmit(e));
        
        // Search and Filter Events
        document.getElementById('searchInput').addEventListener('input', (e) => this.handleSearch(e.target.value));
        document.getElementById('categoryFilter').addEventListener('change', (e) => this.handleFilter());
        document.getElementById('priorityFilter').addEventListener('change', (e) => this.handleFilter());
        document.getElementById('sortBy').addEventListener('change', (e) => this.handleSort(e.target.value));
        
        // Item name input for suggestions
        document.getElementById('itemName').addEventListener('input', (e) => this.handleNameInput(e.target.value));
        document.getElementById('itemName').addEventListener('focus', () => this.showSuggestions());
        document.getElementById('itemName').addEventListener('blur', () => {
            setTimeout(() => this.hideSuggestions(), 200);
        });
        
        // Modal backdrop click
        document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
            backdrop.addEventListener('click', () => this.closeModal());
        });
        
        // Confirmation modal events
        document.getElementById('confirmCancel').addEventListener('click', () => this.closeConfirmModal());
        document.getElementById('confirmOk').addEventListener('click', () => this.executeConfirmAction());
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (this.isAuthenticated && !this.isModalOpen()) {
                if (e.ctrlKey || e.metaKey) {
                    switch (e.key) {
                        case 'n':
                            e.preventDefault();
                            this.openModal();
                            break;
                        case 'f':
                            e.preventDefault();
                            document.getElementById('searchInput').focus();
                            break;
                    }
                }
                if (e.key === 'Escape') {
                    this.closeModal();
                }
            }
        });
    }
    
    // PIN Authentication Methods
    handlePinKeypress(e) {
        if (e.key >= '0' && e.key <= '9') {
            this.addPinDigit(e.key);
        } else if (e.key === 'Backspace') {
            this.deletePinDigit();
        }
    }
    
    addPinDigit(digit) {
        if (this.currentPin.length < 4) {
            this.currentPin += digit;
            this.updatePinDots();
            
            if (this.currentPin.length === 4) {
                setTimeout(() => this.checkPin(), 300);
            }
        }
    }
    
    deletePinDigit() {
        if (this.currentPin.length > 0) {
            this.currentPin = this.currentPin.slice(0, -1);
            this.updatePinDots();
        }
    }
    
    updatePinDots() {
        const dots = document.querySelectorAll('.pin-dot');
        dots.forEach((dot, index) => {
            if (index < this.currentPin.length) {
                dot.classList.add('filled');
            } else {
                dot.classList.remove('filled');
            }
        });
    }
    
    checkPin() {
        if (this.currentPin === this.correctPin) {
            this.authenticate();
        } else {
            this.showPinError();
        }
    }
    
    authenticate() {
        this.isAuthenticated = true;
        const pinScreen = document.getElementById('pinScreen');
        const mainApp = document.getElementById('mainApp');
        
        pinScreen.style.transform = 'translateY(-100%)';
        pinScreen.style.opacity = '0';
        
        setTimeout(() => {
            pinScreen.classList.add('hidden');
            mainApp.classList.remove('hidden');
            mainApp.style.animation = 'slideInUp 0.8s ease-out';
        }, 500);
    }
    
    showPinError() {
        const pinScreen = document.getElementById('pinScreen');
        const pinError = document.getElementById('pinError');
        
        pinScreen.classList.add('shake');
        pinError.classList.add('show');
        
        setTimeout(() => {
            pinScreen.classList.remove('shake');
            pinError.classList.remove('show');
            this.currentPin = '';
            this.updatePinDots();
        }, 1500);
    }
    
    animateButton(button) {
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 100);
    }
    
    // Theme Management
    initializeTheme() {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        this.isDarkMode = prefersDark;
        this.updateThemeIcon();
    }
    
    toggleDarkMode() {
        this.isDarkMode = !this.isDarkMode;
        document.documentElement.setAttribute('data-color-scheme', this.isDarkMode ? 'dark' : 'light');
        this.updateThemeIcon();
        this.animateThemeTransition();
    }
    
    updateThemeIcon() {
        const icon = document.querySelector('#darkModeToggle svg');
        if (this.isDarkMode) {
            icon.innerHTML = '<path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>';
        } else {
            icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';
        }
    }
    
    animateThemeTransition() {
        document.body.style.transition = 'all 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }
    
    // Data Management
    addItem(itemData) {
        const newItem = {
            id: this.nextId++,
            ...itemData,
            completed: false,
            dateAdded: new Date().toISOString().split('T')[0]
        };
        
        this.items.unshift(newItem);
        this.applyFiltersAndSort();
        this.updateStats();
        this.renderItems();
        this.animateItemAdd();
    }
    
    updateItem(id, itemData) {
        const index = this.items.findIndex(item => item.id === id);
        if (index !== -1) {
            this.items[index] = { ...this.items[index], ...itemData };
            this.applyFiltersAndSort();
            this.updateStats();
            this.renderItems();
        }
    }
    
    deleteItem(id) {
        const itemElement = document.querySelector(`[data-item-id="${id}"]`);
        if (itemElement) {
            itemElement.style.animation = 'slideInUp 0.3s ease-out reverse';
            setTimeout(() => {
                this.items = this.items.filter(item => item.id !== id);
                this.applyFiltersAndSort();
                this.updateStats();
                this.renderItems();
            }, 300);
        }
    }
    
    toggleItemCompletion(id) {
        const item = this.items.find(item => item.id === id);
        if (item) {
            item.completed = !item.completed;
            this.updateStats();
            this.renderItems();
            this.animateItemToggle(id, item.completed);
        }
    }
    
    // UI Rendering Methods
    renderItems() {
        const itemsList = document.getElementById('itemsList');
        const emptyState = document.getElementById('emptyState');
        
        if (this.filteredItems.length === 0) {
            itemsList.innerHTML = '';
            emptyState.classList.remove('hidden');
        } else {
            emptyState.classList.add('hidden');
            itemsList.innerHTML = this.filteredItems.map((item, index) => 
                this.createItemHTML(item, index)
            ).join('');
            
            // Add event listeners to new items
            this.attachItemEventListeners();
        }
    }
    
    createItemHTML(item, index) {
        return `
            <div class="item-card ${item.completed ? 'completed' : ''}" 
                 data-item-id="${item.id}" 
                 style="animation-delay: ${index * 0.1}s">
                <div class="item-header">
                    <div class="item-checkbox ${item.completed ? 'checked' : ''}" 
                         onclick="app.toggleItemCompletion(${item.id})">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                            <polyline points="20,6 9,17 4,12"></polyline>
                        </svg>
                    </div>
                    <div class="item-content">
                        <h3 class="item-name">${item.name}</h3>
                        <div class="item-meta">
                            <span class="item-price">$${item.price.toLocaleString()}</span>
                            <span class="item-category">${item.category}</span>
                            <span class="item-priority item-priority--${item.priority.toLowerCase()}">${item.priority}</span>
                        </div>
                        ${item.notes ? `<p class="item-notes">${item.notes}</p>` : ''}
                    </div>
                    <div class="item-actions">
                        <button class="item-action-btn" onclick="app.editItem(${item.id})" title="Edit">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                                <path d="m18.5 2.5 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                            </svg>
                        </button>
                        <button class="item-action-btn item-action-btn--delete" onclick="app.confirmDelete(${item.id})" title="Delete">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="3,6 5,6 21,6"></polyline>
                                <path d="m19,6v14a2,2,0,0,1-2,2H7a2,2,0,0,1-2-2V6m3,0V4a2,2,0,0,1,2-2h4a2,2,0,0,1,2,2v2"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    attachItemEventListeners() {
        // Event listeners are handled via onclick attributes for simplicity
        // This is acceptable for this premium application
    }
    
    updateStats() {
        const totalItems = this.items.length;
        const completedItems = this.items.filter(item => item.completed).length;
        const totalValue = this.items.reduce((sum, item) => sum + item.price, 0);
        
        document.getElementById('totalItems').textContent = totalItems;
        document.getElementById('completedItems').textContent = completedItems;
        document.getElementById('totalValue').textContent = `$${totalValue.toLocaleString()}`;
        
        this.animateStats();
    }
    
    animateStats() {
        document.querySelectorAll('.stat-value').forEach(stat => {
            stat.style.animation = 'pulse 0.5s ease-out';
            setTimeout(() => {
                stat.style.animation = '';
            }, 500);
        });
    }
    
    // Modal Management
    openModal(item = null) {
        const modal = document.getElementById('itemModal');
        const modalTitle = document.getElementById('modalTitle');
        const form = document.getElementById('itemForm');
        
        this.editingItemId = item ? item.id : null;
        modalTitle.textContent = item ? 'Edit Item' : 'Add New Item';
        
        if (item) {
            this.populateForm(item);
        } else {
            form.reset();
            document.getElementById('itemPriority').value = 'Medium';
            document.getElementById('itemCategory').value = this.categories[0];
        }
        
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        setTimeout(() => {
            document.getElementById('itemName').focus();
        }, 300);
    }
    
    closeModal() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.classList.remove('show');
        });
        document.body.style.overflow = '';
        this.hideSuggestions();
        this.editingItemId = null;
    }
    
    populateForm(item) {
        document.getElementById('itemName').value = item.name;
        document.getElementById('itemPrice').value = item.price;
        document.getElementById('itemCategory').value = item.category;
        document.getElementById('itemPriority').value = item.priority;
        document.getElementById('itemNotes').value = item.notes || '';
    }
    
    handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('itemName').value.trim(),
            price: parseFloat(document.getElementById('itemPrice').value),
            category: document.getElementById('itemCategory').value,
            priority: document.getElementById('itemPriority').value,
            notes: document.getElementById('itemNotes').value.trim()
        };
        
        if (this.validateForm(formData)) {
            if (this.editingItemId) {
                this.updateItem(this.editingItemId, formData);
            } else {
                this.addItem(formData);
            }
            this.closeModal();
        }
    }
    
    validateForm(data) {
        if (!data.name || data.name.length < 2) {
            this.showFormError('Item name must be at least 2 characters long');
            return false;
        }
        
        if (!data.price || data.price <= 0) {
            this.showFormError('Price must be greater than 0');
            return false;
        }
        
        return true;
    }
    
    showFormError(message) {
        // Simple error handling - could be enhanced with toast notifications
        alert(message);
    }
    
    // Search and Filter Methods
    handleSearch(query) {
        this.searchQuery = query.toLowerCase();
        this.applyFiltersAndSort();
        this.renderItems();
    }
    
    handleFilter() {
        this.applyFiltersAndSort();
        this.renderItems();
    }
    
    handleSort(sortBy) {
        this.sortBy = sortBy;
        this.applyFiltersAndSort();
        this.renderItems();
    }
    
    applyFiltersAndSort() {
        let filtered = [...this.items];
        
        // Apply search filter
        if (this.searchQuery) {
            filtered = filtered.filter(item => 
                item.name.toLowerCase().includes(this.searchQuery) ||
                item.category.toLowerCase().includes(this.searchQuery) ||
                item.notes.toLowerCase().includes(this.searchQuery)
            );
        }
        
        // Apply category filter
        const categoryFilter = document.getElementById('categoryFilter').value;
        if (categoryFilter) {
            filtered = filtered.filter(item => item.category === categoryFilter);
        }
        
        // Apply priority filter
        const priorityFilter = document.getElementById('priorityFilter').value;
        if (priorityFilter) {
            filtered = filtered.filter(item => item.priority === priorityFilter);
        }
        
        // Apply sorting
        const sortBy = document.getElementById('sortBy').value;
        filtered.sort((a, b) => {
            switch (sortBy) {
                case 'name':
                    return a.name.localeCompare(b.name);
                case 'price':
                    return b.price - a.price;
                case 'priority':
                    const priorityOrder = { 'High': 3, 'Medium': 2, 'Low': 1 };
                    return priorityOrder[b.priority] - priorityOrder[a.priority];
                case 'dateAdded':
                default:
                    return new Date(b.dateAdded) - new Date(a.dateAdded);
            }
        });
        
        this.filteredItems = filtered;
    }
    
    // Smart Suggestions
    handleNameInput(value) {
        if (value.length > 1) {
            this.showSuggestions(value);
        } else {
            this.hideSuggestions();
        }
    }
    
    showSuggestions(query = '') {
        const suggestions = document.getElementById('suggestions');
        let filteredSuggestions = this.smartSuggestions;
        
        if (query) {
            filteredSuggestions = this.smartSuggestions.filter(suggestion =>
                suggestion.toLowerCase().includes(query.toLowerCase())
            );
        }
        
        if (filteredSuggestions.length > 0) {
            suggestions.innerHTML = filteredSuggestions.slice(0, 5).map(suggestion =>
                `<div class="suggestion-item" onclick="app.selectSuggestion('${suggestion}')">${suggestion}</div>`
            ).join('');
            suggestions.classList.add('show');
        } else {
            this.hideSuggestions();
        }
    }
    
    hideSuggestions() {
        const suggestions = document.getElementById('suggestions');
        suggestions.classList.remove('show');
    }
    
    selectSuggestion(suggestion) {
        document.getElementById('itemName').value = suggestion;
        this.hideSuggestions();
        document.getElementById('itemPrice').focus();
    }
    
    // Item Actions
    editItem(id) {
        const item = this.items.find(item => item.id === id);
        if (item) {
            this.openModal(item);
        }
    }
    
    confirmDelete(id) {
        const item = this.items.find(item => item.id === id);
        if (item) {
            this.showConfirmDialog(
                'Delete Item',
                `Are you sure you want to delete "${item.name}"?`,
                () => this.deleteItem(id)
            );
        }
    }
    
    showConfirmDialog(title, message, onConfirm) {
        const modal = document.getElementById('confirmModal');
        document.getElementById('confirmTitle').textContent = title;
        document.getElementById('confirmMessage').textContent = message;
        
        this.confirmAction = onConfirm;
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
    
    closeConfirmModal() {
        const modal = document.getElementById('confirmModal');
        modal.classList.remove('show');
        document.body.style.overflow = '';
        this.confirmAction = null;
    }
    
    executeConfirmAction() {
        if (this.confirmAction) {
            this.confirmAction();
            this.confirmAction = null;
        }
        this.closeConfirmModal();
    }
    
    // Animation Methods
    animateItemAdd() {
        const firstItem = document.querySelector('.item-card');
        if (firstItem) {
            firstItem.style.animation = 'slideInUp 0.5s ease-out';
        }
    }
    
    animateItemToggle(id, completed) {
        const itemElement = document.querySelector(`[data-item-id="${id}"]`);
        if (itemElement) {
            itemElement.style.transition = 'all 0.3s ease';
            if (completed) {
                itemElement.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    itemElement.style.transform = 'scale(1)';
                }, 200);
            }
        }
    }
    
    // Utility Methods
    populateCategories() {
        const categorySelect = document.getElementById('itemCategory');
        const categoryFilter = document.getElementById('categoryFilter');
        
        // Populate form select
        categorySelect.innerHTML = this.categories.map(category =>
            `<option value="${category}">${category}</option>`
        ).join('');
        
        // Populate filter select
        categoryFilter.innerHTML = '<option value="">All Categories</option>' +
            this.categories.map(category =>
                `<option value="${category}">${category}</option>`
            ).join('');
    }
    
    isModalOpen() {
        return document.querySelector('.modal.show') !== null;
    }
}

// Initialize the application
const app = new PremiumChecklist();

// Export for global access
window.app = app;