// --- 1. 时间轴滚动渐显动画 ---

// 获取所有的卡片
const cards = document.querySelectorAll('.card');

// 监听滚动事件
window.addEventListener('scroll', checkBoxes);

// 初始化运行一次
checkBoxes();

function checkBoxes() {
    // 设定触发高度：屏幕底部的 80% 处
    const triggerBottom = window.innerHeight / 5 * 4;

    cards.forEach(card => {
        // 获取元素顶部距离视口的距离
        const cardTop = card.getBoundingClientRect().top;

        if(cardTop < triggerBottom) {
            card.classList.add('show');
        } else {
            // 如果想让卡片划走时消失，保留这行；否则可以注释掉
            card.classList.remove('show');
        }
    });
}

// --- 2. 回到顶部按钮逻辑 ---

const backBtn = document.getElementById("backBtn");

// 监听滚动，控制按钮显示/隐藏
window.onscroll = function() { scrollFunction() };

function scrollFunction() {
    // 兼容不同浏览器的滚动距离判断
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        backBtn.style.display = "block";
    } else {
        backBtn.style.display = "none";
    }
}

// 点击按钮逻辑
backBtn.addEventListener('click', () => {
    // 平滑滚动回顶部
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});