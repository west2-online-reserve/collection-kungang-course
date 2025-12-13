/* -----------------------------
   福州大学校史馆 - 交互脚本
--------------------------------*/

// 平滑滚动锚点导航
document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

// 滚动时改变导航栏背景
window.addEventListener('scroll', () => {
  const header = document.querySelector('header');
  header.classList.toggle('scrolled', window.scrollY > 50);

  // 返回顶部按钮显示
  const btn = document.getElementById('backToTop');
  if (btn) btn.classList.toggle('show', window.scrollY > 200);
});

// 返回顶部
const backToTop = document.getElementById('backToTop');
if (backToTop) {
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// 夜间模式切换
const toggleBtn = document.getElementById('darkToggle');
if (toggleBtn) {
toggleBtn.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  if (document.body.classList.contains('dark')) {
    toggleBtn.innerHTML = '&#9728;'; // ?? Unicode: U+2600
    toggleBtn.title = '切换为日间模式';
  } else {
    toggleBtn.innerHTML = '&#127769;'; // ? Unicode: U+1F311
    toggleBtn.title = '切换为夜间模式';
  }
});


}

// 图片轮播逻辑
const slides = document.querySelector('.slides');
if (slides) {
  const imgs = slides.querySelectorAll('img');
  let index = 0;
  const showSlide = i => slides.style.transform = `translateX(-${i * 100}%)`;
  document.querySelector('.next').addEventListener('click', () => {
    index = (index + 1) % imgs.length;
    showSlide(index);
  });
  document.querySelector('.prev').addEventListener('click', () => {
    index = (index - 1 + imgs.length) % imgs.length;
    showSlide(index);
  });
  setInterval(() => { index = (index + 1) % imgs.length; showSlide(index); }, 5000);
}

// 留言板功能
const msgBtn = document.getElementById('msgSend');
const msgInput = document.getElementById('msgInput');
const msgList = document.getElementById('msgList');
if (msgBtn && msgList) {
  const loadMessages = () => {
    const msgs = JSON.parse(localStorage.getItem('messages') || '[]');
    msgList.innerHTML = msgs.map(m => `<p>?? ${m}</p>`).join('');
  };
  msgBtn.addEventListener('click', () => {
    const val = msgInput.value.trim();
    if (val) {
      const msgs = JSON.parse(localStorage.getItem('messages') || '[]');
      msgs.push(val);
      localStorage.setItem('messages', JSON.stringify(msgs));
      msgInput.value = '';
      loadMessages();
    }
  });
  loadMessages();
}

// 图片点击放大（灯箱效果）
document.querySelectorAll('.gallery img').forEach(img => {
  img.addEventListener('click', () => {
    const overlay = document.createElement('div');
    overlay.className = 'lightbox';
    overlay.innerHTML = `<img src="${img.src}" class="zoomed">`;
    document.body.appendChild(overlay);
    overlay.addEventListener('click', () => overlay.remove());
  });
});

// 动态淡入动画
const fadeEls = document.querySelectorAll('.fade-in');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
});
fadeEls.forEach(el => observer.observe(el));
