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