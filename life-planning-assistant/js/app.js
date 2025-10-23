// 人生规划助手 - Life Planning Assistant
// Powered by DeepSeek AI

class LifePlanningAssistant {
    constructor() {
        this.apiKey = localStorage.getItem('deepseek_api_key') || '';
        this.conversationHistory = [];
        this.systemPrompt = `你是一位专业的人生规划助手，致力于帮助用户规划和实现他们的人生目标。你的职责包括：

1. **目标设定与规划**：帮助用户明确短期、中期和长期目标，制定可行的实现路径。

2. **职业发展指导**：提供职业规划建议，包括技能提升、职业转型、晋升策略等。

3. **学习成长计划**：根据用户需求，制定个性化的学习计划和成长路线图。

4. **时间管理**：指导用户优化时间分配，提高工作和生活效率。

5. **工作生活平衡**：帮助用户在事业、家庭、健康、兴趣等方面找到平衡点。

6. **财务规划建议**：提供基础的理财思路和建议（非专业投资建议）。

7. **心态调整与激励**：在用户遇到困难时给予支持和鼓励，帮助调整心态。

8. **目标追踪与反思**：帮助用户定期回顾进展，调整计划。

**指导原则**：
- 以用户为中心，充分了解他们的背景、需求和限制
- 提供具体、可操作的建议，而非空泛的理论
- 鼓励用户思考和自我探索，而非简单地给出答案
- 保持积极、支持性的态度，同时客观理性
- 尊重用户的选择和价值观
- 根据用户反馈灵活调整建议

请用友好、专业的语气与用户交流，使用中文回复。在给出建议时，可以使用清晰的结构化格式（如编号列表、步骤等），便于用户理解和执行。`;

        this.init();
    }

    init() {
        this.cacheDOMElements();
        this.attachEventListeners();
        this.loadConversation();

        if (!this.apiKey) {
            this.showSettings();
        }
    }

    cacheDOMElements() {
        this.elements = {
            chatMessages: document.getElementById('chatMessages'),
            userInput: document.getElementById('userInput'),
            sendButton: document.getElementById('sendButton'),
            settingsButton: document.getElementById('settingsButton'),
            settingsPanel: document.getElementById('settingsPanel'),
            closeSettings: document.getElementById('closeSettings'),
            apiKeyInput: document.getElementById('apiKey'),
            saveSettings: document.getElementById('saveSettings'),
            clearChat: document.getElementById('clearChat'),
            welcomeMessage: document.getElementById('welcomeMessage'),
            quickButtons: document.querySelectorAll('.quick-btn')
        };

        if (this.apiKey) {
            this.elements.apiKeyInput.value = this.apiKey;
        }
    }

    attachEventListeners() {
        this.elements.sendButton.addEventListener('click', () => this.sendMessage());
        this.elements.userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        this.elements.settingsButton.addEventListener('click', () => this.showSettings());
        this.elements.closeSettings.addEventListener('click', () => this.hideSettings());
        this.elements.saveSettings.addEventListener('click', () => this.saveSettings());

        this.elements.clearChat.addEventListener('click', () => this.clearConversation());

        this.elements.quickButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const prompt = btn.getAttribute('data-prompt');
                this.elements.userInput.value = prompt;
                this.sendMessage();
            });
        });

        // Auto-resize textarea
        this.elements.userInput.addEventListener('input', () => {
            this.elements.userInput.style.height = 'auto';
            this.elements.userInput.style.height = this.elements.userInput.scrollHeight + 'px';
        });
    }

    showSettings() {
        this.elements.settingsPanel.classList.add('active');
    }

    hideSettings() {
        this.elements.settingsPanel.classList.remove('active');
    }

    saveSettings() {
        const apiKey = this.elements.apiKeyInput.value.trim();

        if (!apiKey) {
            alert('请输入有效的 API Key');
            return;
        }

        this.apiKey = apiKey;
        localStorage.setItem('deepseek_api_key', apiKey);
        this.hideSettings();

        this.showNotification('设置已保存！', 'success');
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 24px;
            background: ${type === 'success' ? '#10b981' : '#4f46e5'};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            animation: slideInRight 0.3s ease;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    async sendMessage() {
        const message = this.elements.userInput.value.trim();

        if (!message) return;

        if (!this.apiKey) {
            this.showNotification('请先配置 API Key', 'error');
            this.showSettings();
            return;
        }

        // Hide welcome message
        this.elements.welcomeMessage.classList.add('hidden');

        // Add user message to chat
        this.addMessage(message, 'user');
        this.conversationHistory.push({
            role: 'user',
            content: message
        });

        // Clear input
        this.elements.userInput.value = '';
        this.elements.userInput.style.height = 'auto';

        // Disable input while processing
        this.setInputState(false);

        // Show typing indicator
        const typingId = this.showTypingIndicator();

        try {
            const response = await this.callDeepSeekAPI(message);
            this.removeTypingIndicator(typingId);

            this.addMessage(response, 'assistant');
            this.conversationHistory.push({
                role: 'assistant',
                content: response
            });

            this.saveConversation();
        } catch (error) {
            this.removeTypingIndicator(typingId);
            this.addMessage('抱歉，发生了错误：' + error.message, 'assistant');
            console.error('API调用错误：', error);
        }

        this.setInputState(true);
    }

    async callDeepSeekAPI(userMessage) {
        const messages = [
            {
                role: 'system',
                content: this.systemPrompt
            },
            ...this.conversationHistory.slice(-10), // Keep last 10 messages for context
            {
                role: 'user',
                content: userMessage
            }
        ];

        const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify({
                model: 'deepseek-chat',
                messages: messages,
                temperature: 0.7,
                max_tokens: 2000,
                top_p: 0.95,
                frequency_penalty: 0.0,
                presence_penalty: 0.0
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error?.message || `API请求失败: ${response.status}`);
        }

        const data = await response.json();
        return data.choices[0].message.content;
    }

    addMessage(content, role) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content;

        messageDiv.appendChild(contentDiv);
        this.elements.chatMessages.appendChild(messageDiv);

        this.scrollToBottom();
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant';
        typingDiv.id = 'typing-indicator';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator';
        typingIndicator.innerHTML = '<span></span><span></span><span></span>';

        contentDiv.appendChild(typingIndicator);
        typingDiv.appendChild(contentDiv);
        this.elements.chatMessages.appendChild(typingDiv);

        this.scrollToBottom();
        return 'typing-indicator';
    }

    removeTypingIndicator(id) {
        const typingElement = document.getElementById(id);
        if (typingElement) {
            typingElement.remove();
        }
    }

    setInputState(enabled) {
        this.elements.userInput.disabled = !enabled;
        this.elements.sendButton.disabled = !enabled;

        if (enabled) {
            this.elements.userInput.focus();
        }
    }

    scrollToBottom() {
        this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
    }

    saveConversation() {
        localStorage.setItem('conversation_history', JSON.stringify(this.conversationHistory));
    }

    loadConversation() {
        const saved = localStorage.getItem('conversation_history');
        if (saved) {
            try {
                this.conversationHistory = JSON.parse(saved);

                // Display conversation history
                this.conversationHistory.forEach(msg => {
                    this.addMessage(msg.content, msg.role);
                });

                if (this.conversationHistory.length > 0) {
                    this.elements.welcomeMessage.classList.add('hidden');
                }
            } catch (e) {
                console.error('加载对话历史失败：', e);
            }
        }
    }

    clearConversation() {
        if (confirm('确定要清空所有对话记录吗？此操作无法撤销。')) {
            this.conversationHistory = [];
            this.elements.chatMessages.innerHTML = '';
            this.elements.welcomeMessage.classList.remove('hidden');
            localStorage.removeItem('conversation_history');
            this.showNotification('对话已清空', 'success');
        }
    }
}

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new LifePlanningAssistant();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
