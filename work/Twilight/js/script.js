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


