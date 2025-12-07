/**
 * common.js - 福大项目通用工具库
 * 包含：懒加载、导航高亮、返回顶部、背景效果复用、交互动画等
 */
const Common = (function() {
  // 私有工具方法
  const privateMethods = {
    // 检查元素是否在视口中
    isInViewport: function(el) {
      const rect = el.getBoundingClientRect();
      return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.bottom >= 0
      );
    },

    // 创建水波纹效果（复用打卡页交互）
    createRipple: function(event) {
      const button = event.currentTarget;
      if (!button) return;
      
      const ripple = document.createElement('span');
      const rect = button.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = event.clientX - rect.left - size / 2;
      const y = event.clientY - rect.top - size / 2;

      ripple.style.width = ripple.style.height = `${size}px`;
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      ripple.className = 'ripple';

      button.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    },

    // 创建粒子背景（复用打卡页效果）
    createParticles: function() {
      const particlesContainer = document.getElementById('particlesContainer');
      if (!particlesContainer) return;

      const colors = [
        `rgba(${200}, 16, 46, 0.3)`,    // 福大红
        `rgba(${0}, 85, 164, 0.3)`,     // 福大蓝
        `rgba(${40}, 167, 69, 0.3)`,    // 绿色
        `rgba(${255}, 193, 7, 0.3)`,    // 黄色
        `rgba(${111}, 66, 193, 0.3)`    // 紫色
      ];

      // 生成50个粒子
      for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';

        // 随机属性
        const size = Math.random() * 10 + 5;
        const color = colors[Math.floor(Math.random() * colors.length)];
        const left = Math.random() * 100;
        const animationDuration = Math.random() * 20 + 10;
        const animationDelay = Math.random() * 10;

        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.background = color;
        particle.style.left = `${left}%`;
        particle.style.animationDuration = `${animationDuration}s`;
        particle.style.animationDelay = `${animationDelay}s`;

        particlesContainer.appendChild(particle);
      }
    },

    // 初始化浮动背景元素（复用打卡页）
    initFloatingElements: function() {
      // 检查是否已创建浮动元素，避免重复
      if (document.querySelector('.floating-element')) return;
      
      // 创建3个浮动元素
      const floatingElements = [
        { className: 'red', style: 'top: -150px; left: -150px;' },
        { className: 'blue', style: 'bottom: -100px; right: -100px;' },
        { className: 'yellow', style: 'top: 50%; right: -75px;' }
      ];

      floatingElements.forEach(item => {
        const el = document.createElement('div');
        el.className = `floating-element ${item.className}`;
        el.style = item.style;
        document.body.appendChild(el);
      });
    }
  };

  return {
    /**
     * 初始化页面通用功能
     * 包括：懒加载、导航高亮、返回顶部、背景效果等
     */
    init: function(options = {}) {
      // 基础功能
      this.initLazyLoad();
      this.initNavbarScroll();
      this.initNavHighlight();
      this.initBackToTop();
      this.initSmoothScroll();
      this.initPageLoadAnimation();

      // 可选：背景效果（默认开启，可通过options关闭）
      if (options.enableBackground !== false) {
        privateMethods.initFloatingElements(); // 浮动色块
        privateMethods.createParticles();      // 粒子效果
      }

      // 可选：水波纹交互（默认开启）
      if (options.enableRipple !== false) {
        this.initRippleEffect();
      }
    },

    /**
     * 图片懒加载功能
     * 适配所有带有data-src属性的图片
     */
    initLazyLoad: function() {
      if (!('IntersectionObserver' in window)) {
        // 降级处理：直接加载所有图片
        document.querySelectorAll('[data-src]').forEach(img => {
          img.src = img.dataset.src;
        });
        return;
      }

      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            // 处理图片加载
            if (img.dataset.src) {
              img.src = img.dataset.src;
              // 移除观察
              observer.unobserve(img);
              // 添加加载完成动画
              img.style.opacity = '0';
              img.style.transition = 'opacity 0.3s ease';
              img.onload = () => {
                img.style.opacity = '1';
              };
            }
          }
        });
      });

      // 观察所有带data-src的图片
      document.querySelectorAll('[data-src]').forEach(img => {
        imageObserver.observe(img);
      });
    },

    /**
     * 导航栏高亮当前页面
     * 根据当前URL匹配导航链接
     */
    initNavHighlight: function() {
      const currentPath = window.location.pathname.split('/').pop() || 'homepage.html';
      const navLinks = document.querySelectorAll('.nav-link');
      
      navLinks.forEach(link => {
        const linkPath = link.getAttribute('href').split('/').pop() || 'homepage.html';
        if (linkPath === currentPath) {
          link.classList.add('active');
        }
      });
    },

    /**
     * 返回顶部按钮功能
     */
    initBackToTop: function() {
      // 检查是否已有返回顶部按钮，避免重复创建
      if (document.querySelector('.back-to-top')) return;

      const btn = document.createElement('button');
      btn.className = 'btn btn-red back-to-top';
      btn.textContent = '返回顶部';
      btn.style.position = 'fixed';
      btn.style.bottom = '30px';
      btn.style.right = '30px';
      btn.style.zIndex = '999';
      btn.style.display = 'none';
      
      document.body.appendChild(btn);

      // 点击返回顶部
      btn.addEventListener('click', () => {
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });

      // 滚动显示/隐藏按钮
      window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
          btn.style.display = 'block';
        } else {
          btn.style.display = 'none';
        }
      });
    },

    /**
     * 导航栏滚动样式变化
     */
    initNavbarScroll: function() {
      // 获取导航栏元素
      const navbar = document.querySelector('.navbar');
      // 未找到导航栏则终止执行
      if (!navbar) return;

      // 定义滚动处理函数
      const handleScroll = () => {
        if (window.scrollY > 50) {
          // 滚动距离超过50px：增强背景透明度+加深阴影
          navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
          navbar.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
        } else {
          // 滚动距离≤50px（顶部）：默认白色背景+浅阴影
          navbar.style.backgroundColor = '#fff';
          navbar.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
        }
      };

      // 初始执行一次确保样式正确
      handleScroll();

      // 添加滚动监听
      window.addEventListener('scroll', handleScroll);
    },

    /**
     * 平滑滚动锚点
     */
    initSmoothScroll: function() {
      // 获取所有以#开头的锚点链接
      const anchors = document.querySelectorAll('a[href^="#"]');
      
      // 遍历每个锚点链接并绑定点击事件
      anchors.forEach(anchor => {
        anchor.addEventListener('click', function (e) {
          // 阻止默认锚点跳转行为
          e.preventDefault();
          
          // 获取目标锚点ID
          const targetId = this.getAttribute('href');
          
          // 排除空锚点（href="#"）
          if (targetId !== '#') {
            // 查找目标元素并实现平滑滚动
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
              targetElement.scrollIntoView({
                behavior: 'smooth' // 平滑滚动
              });
            }
          }
        });
      });
    },

    /**
     * 页面加载动画
     */
    initPageLoadAnimation: function() {
      // 页面加载完成后执行动画逻辑
      window.addEventListener('load', function() {
        // 给body添加加载完成类名
        document.body.classList.add('page-loaded');
        
        // 时间轴元素动画（间接兼容导航栏布局）
        const timelineItems = document.querySelectorAll('.timeline-item');
        
        // 遍历时间轴元素，逐帧触发动画
        timelineItems.forEach((item, index) => {
          setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
          }, 200 * index);
        });
      });
    },

    /**
     * 初始化水波纹交互效果
     * 绑定到所有按钮/可点击元素
     */
    initRippleEffect: function() {
      // 绑定到所有按钮、导航链接、可点击元素
      const clickableElements = document.querySelectorAll('button, .btn, .nav-link, .checkin-item, .map-point');
      clickableElements.forEach(el => {
        el.addEventListener('click', privateMethods.createRipple);
      });
    },

    /**
     * 显示提示消息
     * @param {string} message - 消息内容
     * @param {string} type - 消息类型：success/error/info
     * @param {number} duration - 显示时长(ms)，默认3000
     */
    showToast: function(message, type = 'info', duration = 3000) {
      // 移除已存在的toast
      const existingToast = document.querySelector('.toast');
      if (existingToast) {
        existingToast.remove();
      }

      const toast = document.createElement('div');
      toast.className = `toast toast-${type}`;
      toast.textContent = message;
      
      // 样式设置
      toast.style.position = 'fixed';
      toast.style.top = '20px';
      toast.style.left = '50%';
      toast.style.transform = 'translateX(-50%)';
      toast.style.padding = '10px 20px';
      toast.style.borderRadius = '4px';
      toast.style.color = '#fff';
      toast.style.zIndex = '9999';
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s ease';

      // 类型样式
      switch(type) {
        case 'success':
          toast.style.backgroundColor = '#4CAF50';
          break;
        case 'error':
          toast.style.backgroundColor = '#f44336';
          break;
        default:
          toast.style.backgroundColor = 'var(--fd-blue)';
      }

      document.body.appendChild(toast);
      
      // 显示动画
      setTimeout(() => {
        toast.style.opacity = '1';
      }, 10);

      // 自动关闭
      setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
          toast.remove();
        }, 300);
      }, duration);
    },

    // 暴露私有方法（可选，方便特殊页面调用）
    createRipple: privateMethods.createRipple,
    createParticles: privateMethods.createParticles
  };
})();

// 页面加载完成后初始化通用功能
// 可传参控制是否启用背景效果：Common.init({ enableBackground: false })
document.addEventListener('DOMContentLoaded', () => {
  Common.init();
});