// === 1. 导航与页面切换逻辑 ===
function switchTab(tabId) {
    // 隐藏所有 section
    document.querySelectorAll('.page-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // 显示目标 section
    const target = document.getElementById(tabId);
    if(target) {
        target.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

}


// === 2. 校友寄语逻辑 (模拟) ===
function addMessage() {
    const nameInput = document.getElementById('guest-name');
    const msgInput = document.getElementById('guest-msg');
    const board = document.getElementById('message-board');

    if(nameInput.value.trim() === '' || msgInput.value.trim() === '') {
        alert('请填写姓名和祝福语哦！');
        return;
    }

    // 创建新留言卡片
    const div = document.createElement('div');
    div.className = 'bg-white p-4 rounded shadow border-l-4 border-fzuRed animate-fade-in';
    div.innerHTML = `
        <p class="text-gray-800">${msgInput.value}</p>
        <p class="text-right text-sm text-gray-500 mt-2">- ${nameInput.value}</p>
    `;
    
    // 插入到最前面
    board.insertBefore(div, board.firstChild);

    // 清空输入框
    nameInput.value = '';
    msgInput.value = '';
}