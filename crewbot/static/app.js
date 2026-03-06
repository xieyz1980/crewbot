// CrewBot React App
const { useState, useEffect, useCallback } = React;

// API配置
const API_BASE_URL = 'http://localhost:8080/api/v1';
const WS_URL = 'ws://localhost:8080/ws';

// 状态颜色映射
const statusColors = {
    pending: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    running: 'bg-blue-100 text-blue-800 border-blue-200',
    completed: 'bg-green-100 text-green-800 border-green-200',
    failed: 'bg-red-100 text-red-800 border-red-200',
    online: 'bg-green-500',
    offline: 'bg-gray-400',
    busy: 'bg-yellow-500'
};

const statusLabels = {
    pending: '待处理',
    running: '执行中',
    completed: '已完成',
    failed: '失败',
    online: '在线',
    offline: '离线',
    busy: '忙碌'
};

// 图标组件
const Icons = {
    Bot: () => React.createElement('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 },
        React.createElement('rect', { x: 3, y: 11, width: 18, height: 10, rx: 2 }),
        React.createElement('circle', { cx: 12, cy: 5, r: 2 }),
        React.createElement('path', { d: 'M12 7v4M8 16h8' })
    ),
    TaskList: () => React.createElement('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 },
        React.createElement('rect', { x: 3, y: 5, width: 6, height: 6, rx: 1 }),
        React.createElement('path', { d: 'M3 17h18M13 7h8M13 11h8' })
    ),
    Plus: () => React.createElement('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 },
        React.createElement('path', { d: 'M12 5v14M5 12h14' })
    ),
    Activity: () => React.createElement('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 },
        React.createElement('path', { d: 'M22 12h-4l-3 9L9 3l-3 9H2' })
    ),
    Refresh: () => React.createElement('svg', { width: 16, height: 16, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 },
        React.createElement('path', { d: 'M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8M3 3v5h5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16M3 21v-5h5' })
    ),
    ChevronRight: () => React.createElement('svg', { width: 16, height: 16, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 },
        React.createElement('path', { d: 'm9 18 6-6-6-6' })
    ),
    Cpu: () => React.createElement('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 },
        React.createElement('rect', { x: 4, y: 4, width: 16, height: 16, rx: 2 }),
        React.createElement('rect', { x: 9, y: 9, width: 6, height: 6 }),
        React.createElement('path', { d: 'M15 2v2M15 20v2M9 2v2M9 20v2M20 9h2M2 9h2M20 15h2M2 15h2' })
    ),
    Clock: () => React.createElement('svg', { width: 16, height: 16, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 },
        React.createElement('circle', { cx: 12, cy: 12, r: 10 }),
        React.createElement('path', { d: 'M12 6v6l4 2' })
    ),
    Dollar: () => React.createElement('svg', { width: 16, height: 16, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 },
        React.createElement('path', { d: 'M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6' })
    ),
    X: () => React.createElement('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 },
        React.createElement('path', { d: 'M18 6 6 18M6 6l12 12' })
    ),
    Check: () => React.createElement('svg', { width: 16, height: 16, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 },
        React.createElement('path', { d: 'M20 6 9 17l-5-5' })
    ),
    Loader: () => React.createElement('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2, className: 'animate-spin' },
        React.createElement('path', { d: 'M21 12a9 9 0 1 1-6.219-8.56' })
    )
};

// API服务
const apiService = {
    async getTasks() {
        const res = await fetch(`${API_BASE_URL}/tasks`);
        if (!res.ok) throw new Error('获取任务失败');
        return await res.json();
    },
    async createTask(task) {
        const res = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(task)
        });
        if (!res.ok) throw new Error('创建任务失败');
        return await res.json();
    },
    async getAgents() {
        const res = await fetch(`${API_BASE_URL}/agents`);
        if (!res.ok) throw new Error('获取Agent失败');
        return await res.json();
    },
    async getAgentStatus() {
        const res = await fetch(`${API_BASE_URL}/agents/status`);
        if (!res.ok) throw new Error('获取Agent状态失败');
        return await res.json();
    },
    async getStats() {
        const res = await fetch(`http://localhost:8080/api/v1/stats`);
        if (!res.ok) throw new Error('获取统计失败');
        return await res.json();
    }
};

// 统计卡片组件
const StatCard = ({ title, value, icon: Icon, color, isLoading }) => (
    React.createElement('div', { className: 'bg-white rounded-xl shadow-sm p-6 border border-gray-100' },
        React.createElement('div', { className: 'flex items-center justify-between' },
            React.createElement('div', null,
                React.createElement('p', { className: 'text-gray-500 text-sm font-medium' }, title),
                React.createElement('p', { className: `text-3xl font-bold mt-2 ${color}` }, 
                    isLoading ? '-' : value
                )
            ),
            React.createElement('div', { className: `p-3 rounded-lg ${color.replace('text-', 'bg-').replace('600', '100')}` },
                React.createElement(Icon)
            )
        )
    )
);

// 任务列表页面
const TaskListPage = ({ onTaskClick }) => {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all');

    const loadTasks = useCallback(async () => {
        try {
            setLoading(true);
            const data = await apiService.getTasks();
            setTasks(data);
        } catch (error) {
            console.error('加载任务失败:', error);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadTasks();
        const interval = setInterval(loadTasks, 5000);
        return () => clearInterval(interval);
    }, [loadTasks]);

    const filteredTasks = filter === 'all' ? tasks : tasks.filter(t => t.status === filter);

    return React.createElement('div', { className: 'space-y-6 fade-in' },
        React.createElement('div', { className: 'flex items-center justify-between' },
            React.createElement('div', { className: 'flex items-center gap-4' },
                React.createElement('h2', { className: 'text-2xl font-bold text-gray-800' }, '📋 任务列表'),
                React.createElement('button', {
                    onClick: loadTasks,
                    className: 'p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors'
                }, React.createElement(Icons.Refresh))
            ),
            React.createElement('div', { className: 'flex gap-2' },
                ['all', 'pending', 'running', 'completed', 'failed'].map(status =>
                    React.createElement('button', {
                        key: status,
                        onClick: () => setFilter(status),
                        className: `px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                            filter === status 
                                ? 'bg-blue-600 text-white' 
                                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                        }`
                    }, status === 'all' ? '全部' : statusLabels[status])
                )
            )
        ),
        
        loading && tasks.length === 0
            ? React.createElement('div', { className: 'text-center py-20' },
                React.createElement(Icons.Loader),
                React.createElement('p', { className: 'text-gray-500 mt-4' }, '加载任务中...')
            )
            : filteredTasks.length === 0
                ? React.createElement('div', { className: 'bg-white rounded-xl p-12 text-center border border-gray-100' },
                    React.createElement('p', { className: 'text-gray-400 text-lg' }, '暂无任务')
                )
                : React.createElement('div', { className: 'grid gap-4' },
                    filteredTasks.map(task =>
                        React.createElement('div', {
                            key: task.id,
                            onClick: () => onTaskClick(task),
                            className: 'bg-white rounded-xl p-5 border border-gray-100 hover:shadow-md transition-all cursor-pointer group'
                        },
                            React.createElement('div', { className: 'flex items-start justify-between' },
                                React.createElement('div', { className: 'flex-1' },
                                    React.createElement('div', { className: 'flex items-center gap-3 mb-2' },
                                        React.createElement('h3', { className: 'font-semibold text-gray-800 text-lg' }, task.name),
                                        React.createElement('span', {
                                            className: `px-3 py-1 rounded-full text-xs font-medium border ${statusColors[task.status] || 'bg-gray-100'}`
                                        }, statusLabels[task.status] || task.status)
                                    ),
                                    React.createElement('p', { className: 'text-gray-500 text-sm mb-3 line-clamp-2' }, task.description),
                                    React.createElement('div', { className: 'flex items-center gap-4 text-sm text-gray-400' },
                                        task.assigned_agent && React.createElement('span', { className: 'flex items-center gap-1' },
                                            React.createElement(Icons.Bot),
                                            task.assigned_agent
                                        ),
                                        React.createElement('span', { className: 'flex items-center gap-1' },
                                            React.createElement(Icons.Clock),
                                            new Date(task.created_at).toLocaleString('zh-CN')
                                        ),
                                        React.createElement('span', { className: 'flex items-center gap-1' },
                                            React.createElement(Icons.Dollar),
                                            `$${task.budget}`
                                        ),
                                        React.createElement('span', null, `优先级: ${task.priority}`)
                                    )
                                ),
                                React.createElement('div', { className: 'text-gray-300 group-hover:text-blue-500 transition-colors' },
                                    React.createElement(Icons.ChevronRight)
                                )
                            )
                        )
                    )
                )
    );
};

// Agent状态看板
const AgentDashboardPage = () => {
    const [agents, setAgents] = useState([]);
    const [agentStatus, setAgentStatus] = useState({});
    const [loading, setLoading] = useState(true);

    const loadData = useCallback(async () => {
        try {
            setLoading(true);
            const [agentsData, statusData] = await Promise.all([
                apiService.getAgents(),
                apiService.getAgentStatus()
            ]);
            setAgents(agentsData);
            setAgentStatus(statusData);
        } catch (error) {
            console.error('加载Agent数据失败:', error);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadData();
        const interval = setInterval(loadData, 5000);
        return () => clearInterval(interval);
    }, [loadData]);

    return React.createElement('div', { className: 'space-y-6 fade-in' },
        React.createElement('div', { className: 'flex items-center justify-between' },
            React.createElement('h2', { className: 'text-2xl font-bold text-gray-800' }, '👥 Agent状态看板'),
            React.createElement('button', {
                onClick: loadData,
                className: 'p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors'
            }, React.createElement(Icons.Refresh))
        ),
        
        loading && agents.length === 0
            ? React.createElement('div', { className: 'text-center py-20' },
                React.createElement(Icons.Loader),
                React.createElement('p', { className: 'text-gray-500 mt-4' }, '加载Agent数据中...')
            )
            : React.createElement('div', { className: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' },
                agents.map(agent => {
                    const status = agentStatus[agent.name] || agent.status || 'offline';
                    return React.createElement('div', {
                        key: agent.name,
                        className: 'bg-white rounded-xl p-6 border border-gray-100 hover:shadow-lg transition-all'
                    },
                        React.createElement('div', { className: 'flex items-start justify-between mb-4' },
                            React.createElement('div', { className: 'flex items-center gap-3' },
                                React.createElement('div', { className: 'p-3 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl text-white' },
                                    React.createElement(Icons.Bot)
                                ),
                                React.createElement('div', null,
                                    React.createElement('h3', { className: 'font-semibold text-gray-800' }, agent.name),
                                    React.createElement('p', { className: 'text-sm text-gray-500' }, agent.model)
                                )
                            ),
                            React.createElement('div', { className: 'flex items-center gap-2' },
                                React.createElement('span', { className: `w-2.5 h-2.5 rounded-full pulse-dot ${statusColors[status] || 'bg-gray-400'}` }),
                                React.createElement('span', { className: 'text-sm text-gray-600' }, statusLabels[status] || status)
                            )
                        ),
                        React.createElement('p', { className: 'text-gray-600 text-sm mb-4' }, agent.description),
                        React.createElement('div', null,
                            React.createElement('p', { className: 'text-xs text-gray-400 font-medium mb-2 uppercase tracking-wider' }, '技能'),
                            React.createElement('div', { className: 'flex flex-wrap gap-2' },
                                agent.skills.map(skill =>
                                    React.createElement('span', {
                                        key: skill,
                                        className: 'px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-xs font-medium'
                                    }, skill)
                                )
                            )
                        )
                    );
                })
            )
    );
};

// 创建任务表单
const CreateTaskPage = ({ onSuccess }) => {
    const [form, setForm] = useState({
        name: '',
        description: '',
        task_type: 'general',
        priority: 1,
        budget: 1.0,
        input_data: {}
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const taskTypes = [
        { value: 'general', label: '通用任务', desc: '一般性的任务处理' },
        { value: 'research', label: '研究任务', desc: '资料搜索、分析报告' },
        { value: 'coding', label: '编程任务', desc: '代码编写、调试、审查' },
        { value: 'writing', label: '写作任务', desc: '文章、文案、报告撰写' },
        { value: 'analysis', label: '分析任务', desc: '数据分析、洞察生成' }
    ];

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        
        try {
            await apiService.createTask(form);
            setSuccess(true);
            setForm({ name: '', description: '', task_type: 'general', priority: 1, budget: 1.0, input_data: {} });
            setTimeout(() => {
                setSuccess(false);
                onSuccess();
            }, 1500);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return React.createElement('div', { className: 'max-w-2xl mx-auto fade-in' },
        React.createElement('div', { className: 'flex items-center gap-3 mb-6' },
            React.createElement('div', { className: 'p-3 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl text-white' },
                React.createElement(Icons.Plus)
            ),
            React.createElement('h2', { className: 'text-2xl font-bold text-gray-800' }, '创建新任务')
        ),
        
        React.createElement('form', { onSubmit: handleSubmit, className: 'bg-white rounded-xl p-8 border border-gray-100 shadow-sm space-y-6' },
            success && React.createElement('div', { className: 'bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center gap-2' },
                React.createElement(Icons.Check),
                '任务创建成功！'
            ),
            
            error && React.createElement('div', { className: 'bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg' }, error),
            
            React.createElement('div', null,
                React.createElement('label', { className: 'block text-sm font-medium text-gray-700 mb-2' }, '任务名称 *'),
                React.createElement('input', {
                    type: 'text',
                    required: true,
                    value: form.name,
                    onChange: e => setForm({ ...form, name: e.target.value }),
                    className: 'w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all',
                    placeholder: '例如：撰写AI行业分析报告'
                })
            ),
            
            React.createElement('div', null,
                React.createElement('label', { className: 'block text-sm font-medium text-gray-700 mb-2' }, '任务描述 *'),
                React.createElement('textarea', {
                    required: true,
                    rows: 4,
                    value: form.description,
                    onChange: e => setForm({ ...form, description: e.target.value }),
                    className: 'w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all resize-none',
                    placeholder: '详细描述任务需求...'
                })
            ),
            
            React.createElement('div', null,
                React.createElement('label', { className: 'block text-sm font-medium text-gray-700 mb-2' }, '任务类型'),
                React.createElement('div', { className: 'grid grid-cols-2 md:grid-cols-3 gap-3' },
                    taskTypes.map(type =>
                        React.createElement('button', {
                            key: type.value,
                            type: 'button',
                            onClick: () => setForm({ ...form, task_type: type.value }),
                            className: `p-3 rounded-lg border text-left transition-all ${
                                form.task_type === type.value
                                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                                    : 'border-gray-200 hover:border-blue-300 hover:bg-blue-50/50'
                            }`
                        },
                            React.createElement('div', { className: 'font-medium text-sm' }, type.label),
                            React.createElement('div', { className: 'text-xs opacity-70 mt-1' }, type.desc)
                        )
                    )
                )
            ),
            
            React.createElement('div', { className: 'grid grid-cols-2 gap-4' },
                React.createElement('div', null,
                    React.createElement('label', { className: 'block text-sm font-medium text-gray-700 mb-2' }, '优先级 (1-10)'),
                    React.createElement('input', {
                        type: 'number',
                        min: 1,
                        max: 10,
                        value: form.priority,
                        onChange: e => setForm({ ...form, priority: parseInt(e.target.value) || 1 }),
                        className: 'w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none'
                    })
                ),
                React.createElement('div', null,
                    React.createElement('label', { className: 'block text-sm font-medium text-gray-700 mb-2' }, '预算 ($)'),
                    React.createElement('input', {
                        type: 'number',
                        min: 0.1,
                        step: 0.1,
                        value: form.budget,
                        onChange: e => setForm({ ...form, budget: parseFloat(e.target.value) || 1 }),
                        className: 'w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none'
                    })
                )
            ),
            
            React.createElement('div', { className: 'flex gap-3 pt-4' },
                React.createElement('button', {
                    type: 'submit',
                    disabled: loading,
                    className: 'flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2'
                }, loading ? React.createElement(Icons.Loader) : React.createElement(Icons.Plus), '创建任务'),
                React.createElement('button', {
                    type: 'button',
                    onClick: () => onSuccess(),
                    className: 'px-6 py-3 border border-gray-200 rounded-lg font-medium text-gray-600 hover:bg-gray-50 transition-colors'
                }, '取消')
            )
        )
    );
};

// 主应用
const App = () => {
    const [activeTab, setActiveTab] = useState('tasks');
    const [stats, setStats] = useState({
        total_tasks: 0,
        pending_tasks: 0,
        completed_tasks: 0,
        agents_count: 0,
        available_models: 0
    });
    const [wsConnected, setWsConnected] = useState(false);

    // WebSocket连接
    useEffect(() => {
        const ws = new WebSocket(WS_URL);
        
        ws.onopen = () => {
            setWsConnected(true);
            console.log('WebSocket已连接');
        };
        
        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.type === 'status_update') {
                    // 可以在这里处理实时状态更新
                }
            } catch (e) {
                console.error('WebSocket消息解析失败:', e);
            }
        };
        
        ws.onclose = () => {
            setWsConnected(false);
            console.log('WebSocket已断开');
        };
        
        return () => ws.close();
    }, []);

    // 加载统计数据
    useEffect(() => {
        const loadStats = async () => {
            try {
                const data = await apiService.getStats();
                setStats(data);
            } catch (error) {
                console.error('加载统计失败:', error);
            }
        };
        loadStats();
        const interval = setInterval(loadStats, 10000);
        return () => clearInterval(interval);
    }, []);

    const tabs = [
        { id: 'tasks', label: '任务列表', icon: Icons.TaskList },
        { id: 'agents', label: 'Agent看板', icon: Icons.Bot },
        { id: 'create', label: '创建任务', icon: Icons.Plus }
    ];

    return React.createElement('div', { className: 'min-h-screen bg-gray-50' },
        // Header
        React.createElement('header', { className: 'bg-white border-b border-gray-200 sticky top-0 z-50' },
            React.createElement('div', { className: 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8' },
                React.createElement('div', { className: 'flex items-center justify-between h-16' },
                    React.createElement('div', { className: 'flex items-center gap-3' },
                        React.createElement('div', { className: 'p-2 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg text-white' },
                            React.createElement(Icons.Bot)
                        ),
                        React.createElement('div', null,
                            React.createElement('h1', { className: 'text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent' }, 'CrewBot'),
                            React.createElement('p', { className: 'text-xs text-gray-400' }, '多Agent协作平台')
                        )
                    ),
                    React.createElement('div', { className: 'flex items-center gap-4' },
                        React.createElement('div', { className: 'flex items-center gap-2 text-sm' },
                            React.createElement('span', { className: `w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}` }),
                            React.createElement('span', { className: 'text-gray-500' }, wsConnected ? '实时连接' : '离线')
                        )
                    )
                )
            )
        ),

        // Navigation
        React.createElement('nav', { className: 'bg-white border-b border-gray-200' },
            React.createElement('div', { className: 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8' },
                React.createElement('div', { className: 'flex gap-1' },
                    tabs.map(tab =>
                        React.createElement('button', {
                            key: tab.id,
                            onClick: () => setActiveTab(tab.id),
                            className: `flex items-center gap-2 px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                                activeTab === tab.id
                                    ? 'border-blue-600 text-blue-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                            }`
                        },
                            React.createElement(tab.icon),
                            tab.label
                        )
                    )
                )
            )
        ),

        // Stats Bar
        activeTab !== 'create' && React.createElement('div', { className: 'bg-gradient-to-r from-blue-600 to-purple-600 text-white' },
            React.createElement('div', { className: 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6' },
                React.createElement('div', { className: 'grid grid-cols-2 md:grid-cols-5 gap-4' },
                    [
                        { label: '总任务', value: stats.total_tasks, icon: Icons.TaskList },
                        { label: '待处理', value: stats.pending_tasks, icon: Icons.Clock },
                        { label: '已完成', value: stats.completed_tasks, icon: Icons.Check },
                        { label: 'Agent数', value: stats.agents_count, icon: Icons.Bot },
                        { label: '可用模型', value: stats.available_models, icon: Icons.Cpu }
                    ].map((stat, idx) =>
                        React.createElement('div', { key: idx, className: 'text-center' },
                            React.createElement('div', { className: 'text-3xl font-bold' }, stat.value),
                            React.createElement('div', { className: 'text-blue-100 text-sm flex items-center justify-center gap-1 mt-1' },
                                React.createElement(stat.icon),
                                stat.label
                            )
                        )
                    )
                )
            )
        ),

        // Main Content
        React.createElement('main', { className: 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8' },
            activeTab === 'tasks' && React.createElement(TaskListPage, { onTaskClick: task => console.log('Task clicked:', task) }),
            activeTab === 'agents' && React.createElement(AgentDashboardPage),
            activeTab === 'create' && React.createElement(CreateTaskPage, { onSuccess: () => setActiveTab('tasks') })
        ),

        // Footer
        React.createElement('footer', { className: 'bg-white border-t border-gray-200 mt-auto' },
            React.createElement('div', { className: 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6' },
                React.createElement('div', { className: 'flex items-center justify-between text-sm text-gray-500' },
                    React.createElement('p', null, '© 2026 CrewBot - 让AI协作像呼吸一样自然 🐾'),
                    React.createElement('p', null, 'v0.1.0')
                )
            )
        )
    );
};

// 渲染应用
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(React.createElement(App));
