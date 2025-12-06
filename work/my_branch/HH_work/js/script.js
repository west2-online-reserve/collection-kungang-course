// 动态导航栏高亮
document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll("nav a");
  const current = window.location.pathname.split("/").pop();

  navLinks.forEach(link => {
    if (link.getAttribute("href") === current) {
      link.classList.add("active");
    }
  });

  // 时间轴滚动出现动画
  const items = document.querySelectorAll(".timeline .content");
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  }, { threshold: 0.2 });

  items.forEach(item => observer.observe(item));
});
