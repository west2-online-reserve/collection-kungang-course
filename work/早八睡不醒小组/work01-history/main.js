// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// 导航栏滚动效果
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.backgroundColor = '#003A70';
        navbar.style.padding = '0.8rem 0';
    } else {
        navbar.style.backgroundColor = '#c8102e';
        navbar.style.padding = '1rem 0';
    }
});

// 图片加载失败兜底
document.querySelectorAll('img').forEach(img => {
    img.addEventListener('error', function() {
        this.src = '"image/图片1.png"'; // 可添加默认图片
        this.alt = '图片加载失败';
    });
});

// 滚动渐入效果
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, { threshold: 0.1 });

// 导航栏当前页面高亮
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.navbar a');

    sections.forEach(section => {
        const top = section.offsetTop - 100;
        const height = section.offsetHeight;
        const id = section.getAttribute('id');

        if (window.scrollY >= top && window.scrollY < top + height) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${id}`) {
                    link.classList.add('active');
                }
            });
        }
    });
});

// 页面加载完成后隐藏加载动画
window.addEventListener('load', () => {
    document.querySelector('.loader').classList.add('hidden');
});

// 红色校史问答交互
const qaItems = document.querySelectorAll('.qa-item');
qaItems.forEach(item => {
    const question = item.querySelector('.qa-question');
    question.addEventListener('click', () => {
        // 关闭其他问答
        qaItems.forEach(i => {
            if (i !== item) i.classList.remove('active');
        });
        // 切换当前问答
        item.classList.toggle('active');
    });
});

// 回到顶部按钮
const backToTopBtn = document.querySelector('.back-to-top');
window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
        backToTopBtn.classList.add('show');
    } else {
        backToTopBtn.classList.remove('show');
    }
});
backToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // 平滑滚动
    });
});

// 给所有板块添加观察
document.querySelectorAll('section').forEach(section => {
    section.classList.add('fade-in-hidden'); // 初始隐藏
    observer.observe(section);
});