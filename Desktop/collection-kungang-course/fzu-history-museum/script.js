// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    
    // 时间轴数据 - 福州大学历史沿革
    const timelineData = [
        {
            year: "1958年",
            title: "福州大学创立",
            content: "福州大学创建于1958年，是国家'双一流'建设高校、国家'211工程'重点建设大学。建校初期，学校就确立了为福建经济社会发展培养高级专门人才的办学宗旨。"
        },
        {
            year: "1960年代",
            title: "艰苦创业时期",
            content: "学校在困难条件下坚持办学，初步形成了以工为主、理工结合的办学格局，为后续发展奠定了基础。这一时期，福大人展现了艰苦奋斗的创业精神。"
        },
        {
            year: "1978年",
            title: "改革开放新发展",
            content: "随着改革开放，福州大学进入快速发展期，学科建设不断完善，研究生教育开始起步，对外交流合作逐步展开。"
        },
        {
            year: "1990年代",
            title: "'211工程'建设",
            content: "1997年，福州大学被确定为国家'211工程'重点建设高校，学校迎来了新的发展机遇，办学实力显著增强。"
        },
        {
            year: "2005年",
            title: "旗山校区启用",
            content: "旗山校区正式启用，极大拓展了学校的办学空间，为学校的长远发展提供了坚实保障，校园建设进入新阶段。"
        },
        {
            year: "2017年",
            title: "入选'双一流'",
            content: "福州大学入选国家'双一流'建设高校，化学学科入选世界一流学科建设名单，标志着学校发展进入新的历史阶段。"
        },
        {
            year: "2021年至今",
            title: "红色文化育人创新",
            content: "学校深入开展红色资源育人改革创新，与古田会议纪念馆等合作打造'行走的思政课'，推动红色文化与专业教育深度融合。"
        }
    ];
    
    // 图片数据 - 红色文化与校园建设
    const galleryData = [
        {
            title: "古田会议精神进校园",
            description: "古田会议纪念馆馆长在福大讲授思政课，让红色历史从书本走向现实。",
            alt: "古田会议纪念馆馆长在福州大学讲授思政课",
            images: "https://news.fzu.edu.cn/__local/3/6B/2E/BAFE3AD55B5EEE9D12F58E5DFC5_A532426D_12600D.png"
        },
        {
            title: "红色建筑模型展",
            description: "建筑学院学生制作的红色历史建筑模型，让党史学习教育既'有形'又'有声'。",
            alt: "福州大学学生制作的红色建筑模型",
            images: "https://jz.fdzcxy.edu.cn/_upload/article/images/98/30/d6e0285a4955962eba96d06f4cb4/153e76b4-830f-4cff-88bc-3f5fa24f9135.jpg"
        },
        {
            title: "行走的思政课堂",
            description: "师生实地调研福建红色建筑，上了一堂沉浸式实景党课和专业课。",
            alt: "福州大学师生实地调研红色建筑",
            images: "https://mmbiz.qpic.cn/mmbiz_png/cich0ic8vnyKWaC1aOSR7NW1WwciaoFLufgFAVTVasPwIvnagRCJsrJ2KK7maBN0Z8SPzPy0jmdwfuAWU1viaPTJ6w/640?wx_fmt=png&from=appmsg&watermark=1&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=1"
        },
        {
            title: "红色主题艺术展演",
            description: "红色故事、歌曲、快板等多种艺术形式，让思政教育'活'起来。",
            alt: "福州大学红色主题艺术展演活动"
        },
        {
            title: "旗山校区图书馆",
            description: "福州大学旗山校区地标性建筑，是学子求知的殿堂。",
            alt: "福州大学旗山校区图书馆"
        },
        {
            title: "福大校园文化景观",
            description: "美丽的校园环境与浓厚的学术氛围相得益彰。",
            alt: "福州大学校园文化景观"
        }
    ];
    
    // 生成时间轴内容
    function renderTimeline() {
        const timelineContainer = document.querySelector('.timeline');
        
        timelineData.forEach((item, index) => {
            const timelineItem = document.createElement('div');
            timelineItem.className = 'timeline-item';
            
            // 添加动画延迟
            timelineItem.style.animationDelay = `${index * 0.1}s`;
            
            timelineItem.innerHTML = `
                <div class="timeline-year">${item.year}</div>
                <div class="timeline-title">${item.title}</div>
                <div class="timeline-content">${item.content}</div>
            `;
            
            timelineContainer.appendChild(timelineItem);
        });
    }
    
    // 生成图片展示内容
    function renderGallery() {
        const galleryContainer = document.querySelector('.gallery-container');
        
        galleryData.forEach(item => {
            const galleryItem = document.createElement('div');
            galleryItem.className = 'gallery-item';
            
            galleryItem.innerHTML = `
                <figure>
                    <img src="${item.image}" 
                         alt="${item.alt}">
                    <figcaption>
                        <h3>${item.title}</h3>
                        <p>${item.description}</p>
                    </figcaption>
                </figure>
            `;
            
            galleryContainer.appendChild(galleryItem);
        });
    }
    
    // 平滑滚动导航
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    // 初始化页面
    renderTimeline();
    renderGallery();
    initSmoothScroll();
    
    // 添加活动时间轴交互效果
    const timelineItems = document.querySelectorAll('.timeline-item');
    timelineItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(10px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
    
    // 控制台欢迎信息
    console.log('%c🏛️ 福州大学校史馆展示页面已加载', 'color: #8B0000; font-size: 16px; font-weight: bold;');
    console.log('%c传承红色基因，培育时代新人 | 福州大学红色文化育人实践', 'color: #333;');
});