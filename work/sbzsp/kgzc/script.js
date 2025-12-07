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

/* =========================================
   校园地图交互逻辑
   ========================================= */

// 1. 定义地标数据 (模拟数据库)
const locationData = {
    1: {
        title: "旗山校区图书馆",
        desc: "福州大学旗山校区图书馆是校园的地标性建筑，外观呈正方形，宏伟大气。馆藏资源丰富，是学子们求知探索的殿堂。每当夜幕降临，灯火通明，成为校园最美的风景线。",
        img: "https://images.unsplash.com/photo-1562774053-701939374585?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" // 建议替换为 images/library.jpg
    },
    2: {
        title: "东大门",
        desc: "福州大学旗山校区的主校门，气势恢宏。校门设计融合了传统与现代元素，见证了无数新生的到来和毕业生的离去，是福大人的精神图腾。",
        img: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" // 建议替换为 images/gate.jpg
    },
    3: {
        title: "综合体育馆",
        desc: "拥有高标准的比赛场地和训练设施，承办过多次省市级大型体育赛事。这里也是开学典礼和毕业典礼的举办地，记录了同学们的青春与汗水。",
        img: "https://images.unsplash.com/photo-1577269182347-660c1d177301?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" // 建议替换为 images/gym.jpg
    },
    4: {
        title: "福友阁",
        desc: "位于校园中心湖畔，风景秀丽。福友阁是校友捐建的标志性建筑，古色古香，常有师生在此晨读或休憩，是校园文化的重要组成部分。",
        img: "https://images.unsplash.com/photo-1519451241324-20b4ea2c4220?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" // 建议替换为 images/pavilion.jpg
    }
};

// 2. 获取 DOM 元素
const pins = document.querySelectorAll('.map-pin');
const modal = document.getElementById('locationModal');
const closeBtn = document.querySelector('.close-btn');

// 模态框内部元素
const modalTitle = document.getElementById('modalTitle');
const modalDesc = document.getElementById('modalDesc');
const modalImg = document.getElementById('modalImg');

// 3. 点击图钉 -> 打开弹窗
pins.forEach(pin => {
    pin.addEventListener('click', function() {
        // 获取当前图钉的 ID
        const id = this.getAttribute('data-id');
        // 从数据中取出对应的内容
        const data = locationData[id];
        
        if(data) {
            modalTitle.innerText = data.title;
            modalDesc.innerText = data.desc;
            modalImg.src = data.img;
            
            // 显示模态框 (使用 flex 居中)
            modal.style.display = 'flex';
        }
    });
});

// 4. 点击关闭按钮 -> 关闭弹窗
if(closeBtn) {
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
}

// 5. 点击窗口空白处 -> 关闭弹窗
window.addEventListener('click', (e) => {
    if (e.target == modal) {
        modal.style.display = 'none';
    }
});