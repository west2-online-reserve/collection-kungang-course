/* =========================================
   1. 时间轴滚动渐显动画 (仅在 timeline 存在时运行)
   ========================================= */
const timelineContainer = document.querySelector('.timeline');

if (timelineContainer) {
    const cards = document.querySelectorAll('.card');

    // 监听滚动事件
    window.addEventListener('scroll', checkBoxes);

    // 初始化运行一次
    checkBoxes();

    function checkBoxes() {
        const triggerBottom = window.innerHeight / 5 * 4;

        cards.forEach(card => {
            const cardTop = card.getBoundingClientRect().top;
            if(cardTop < triggerBottom) {
                card.classList.add('show');
            } else {
                card.classList.remove('show');
            }
        });
    }
}

/* =========================================
   2. 回到顶部按钮逻辑 (通用)
   ========================================= */
const backBtn = document.getElementById("backBtn");

if (backBtn) {
    window.onscroll = function() { scrollFunction() };

    function scrollFunction() {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
            backBtn.style.display = "block";
        } else {
            backBtn.style.display = "none";
        }
    }

    backBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/* =========================================
   3. 校园地图交互逻辑 (仅在地图页运行)
   ========================================= */
// 检测页面上是否有地图图钉，如果有才运行这部分代码
if (document.querySelector('.map-pin')) {
    
    // 定义地标数据
    const locationData = {
        1: {
            title: "旗山校区图书馆",
            desc: "福州大学旗山校区图书馆是校园的地标性建筑，外观呈正方形，宏伟大气。馆藏资源丰富，是学子们求知探索的殿堂。每当夜幕降临，灯火通明，成为校园最美的风景线。",
            img: "image/image_lib.jpg" 
        },
        2: {
            title: "东门",
            desc: "福州大学旗山校区的主校门，气势恢宏。校门设计融合了传统与现代元素，见证了无数新生的到来和毕业生的离去，是福大人的精神图腾。",
            img: "image/image_Eastgate.jpg"
        },
        3: {
            title: "第一田径场",
            desc: "第一田径场是福大校园活力的中心，这里不仅是每年校运会的主战场，也是师生们日常锻炼、夜跑和举办各类大型户外活动的首选之地。",
            img: "image/image_playground.jpg" 
        },
        4: {
            title: "福友阁",
            desc: "位于校园中心湖畔，风景秀丽。福友阁是校友捐建的标志性建筑，古色古香，常有师生在此晨读或休憩，是校园文化的重要组成部分。",
            img: "image/image_fuyouge.jpg" 
        },
        5: {
            title: "计算机与大数据学院楼",
            desc: "计算机与大数据学院楼内设有国家级实验教学示范中心与高性能计算平台，日夜闪烁的代码光影见证了无数IT学子“键盘敲击未来”的梦想，是校园里科技感与创新氛围最浓郁的地标之一。",
            img: "image/image_CSbuilding.jpg" 
        },
        6: {
            title: "晋江楼",
            desc: "晋江楼是福州大学旗山校区体量宏大、气势恢宏的标志性建筑群之一，由晋江市政府捐资兴建。它融合了闽南红砖古厝元素与现代建筑美学，不仅是理工科思维碰撞的殿堂，更象征着校地合作、产教融合的深厚情谊",
            img: "image/image_jinliangbuilding.jpg"
        }
    };

    const pins = document.querySelectorAll('.map-pin');
    const modal = document.getElementById('locationModal');
    const closeBtn = document.querySelector('.close-btn');
    const modalTitle = document.getElementById('modalTitle');
    const modalDesc = document.getElementById('modalDesc');
    const modalImg = document.getElementById('modalImg');

    // 点击图钉 -> 打开弹窗
    pins.forEach(pin => {
        pin.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const data = locationData[id];
            
            if(data && modal) {
                modalTitle.innerText = data.title;
                modalDesc.innerText = data.desc;
                // 自动修复路径分隔符，防止反斜杠在某些浏览器报错
                modalImg.src = data.img.replace(/\\/g, '/');
                modal.style.display = 'flex';
            }
        });
    });

    // 点击关闭按钮
    if(closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    // 点击空白处关闭
    window.addEventListener('click', (e) => {
        if (e.target == modal) {
            modal.style.display = 'none';
        }
    });
}

/* =========================================
   4. 夜间模式切换逻辑 (增强版)
   ========================================= */
document.addEventListener('DOMContentLoaded', () => {
    
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    // 如果找不到按钮，直接退出，防止报错
    if (!themeToggle) return;

    const icon = themeToggle.querySelector('i');

    // 1. 检查本地存储
    if (localStorage.getItem('theme') === 'dark') {
        enableDarkMode();
    }

    // 2. 绑定点击事件
    themeToggle.addEventListener('click', () => {
        if (body.classList.contains('dark-mode')) {
            disableDarkMode();
        } else {
            enableDarkMode();
        }
    });

    function enableDarkMode() {
        body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
        if(icon) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }

    function disableDarkMode() {
        body.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
        if(icon) {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    }
});