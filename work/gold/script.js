// 1. 时间轴点击高亮效果
const timelineItems = document.querySelectorAll('.timeline-item');
timelineItems.forEach(item => {
    item.addEventListener('click', () => {
        // 移除所有节点的高亮样式
        timelineItems.forEach(i => i.classList.remove('active'));
        // 给当前点击的节点添加高亮样式
        item.classList.add('active');
    });
});

// 2. 平滑滚动（点击导航跳转时更流畅）
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault(); // 阻止默认跳转行为
        const targetId = this.getAttribute('href'); // 获取目标区域ID
        const targetElement = document.querySelector(targetId);
        // 滚动到目标区域
        targetElement.scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// 3. 给高亮的时间轴节点添加样式（在CSS中补充）
// 这里用JS动态添加CSS，避免单独写在CSS里遗漏
const style = document.createElement('style');
style.textContent = `
    .timeline-item.active .timeline-year {
        font-size: 1.4rem;
        color: #005bac; /* 福大蓝色 */
    }
    .timeline-item.active .timeline-content {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
    }
`;
document.head.appendChild(style);