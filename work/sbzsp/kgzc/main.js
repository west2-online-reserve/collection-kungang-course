// --- 顶部导航切换 ---
const navBtns = document.querySelectorAll('.menu-item');
const sections = document.querySelectorAll('.page-section');
navBtns.forEach(btn=>{
  btn.onclick = ()=>{
    navBtns.forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    sections.forEach(sec=>sec.classList.remove('showing'));
    document.getElementById(btn.dataset.page).classList.add('showing');
    window.scrollTo({top:0,behavior:"smooth"});
  }
});

// --- 校史时间轴切换 ---
const historyEvents = {
  "1958": {
    img: "img/1958.jpg",
    title: "1958年 创校",
    desc: "1958年，福州大学正式创建，成为新中国背景下福建省最重要的高校之一，红色精神在此埋下火种。"
  },
  "1978": {
    img: "img/1978.jpg",
    title: "1978年 新校区建设",
    desc: "1978年，福大扩建新校区，设施更新，迎来快速发展期。"
  },
  "2000": {
    img: "img/2000.jpg",
    title: "2000年 211工程",
    desc: "2000年福大进入国家'211工程'重点支持行列，学科建设与科研迈上新台阶。"
  },
  "2021": {
    img: "img/2021.jpg",
    title: "2021年 双一流高校",
    desc: "2021年入选“双一流”建设高校，学校发展进入新阶段，着力一流学科建设。"
  }
};
document.querySelectorAll('.timeline-list .evt').forEach(evt=>{
  evt.onclick=function(){
    document.querySelectorAll('.timeline-list .evt').forEach(e=>e.classList.remove('active'));
    evt.classList.add('active');
    const key = evt.getAttribute('data-evt');
    document.getElementById('history-img').src = historyEvents[key].img;
    document.getElementById('history-img').alt = historyEvents[key].title;
    document.getElementById('history-title').innerText = historyEvents[key].title;
    document.getElementById('history-desc').innerText = historyEvents[key].desc;
  }
});

// --- 校园打卡点 ---
const locations = {
  "lib": {
    name: "图书馆", 
    img: "img/bookhall.jpg",
    desc: "福大图书馆，藏书浩瀚，是校园自习、学术交流与灵感汇聚的经典地标。"
  },
  "lake": {
    name: "知明湖",
    img: "img/lake.jpg",
    desc: "校园中央湖泊，碧波荡漾。学子们流连于美景，留下青春回忆。"
  },
  "gym": {
    name: "综合体育馆",
    img: "img/gym.jpg",
    desc: "福大体育馆，运动健儿的舞台，是大型赛事和学生活动的热门打卡点。"
  }
};
document.querySelectorAll('.point').forEach(pt=>{
  pt.onclick=()=>{
    const data = locations[pt.dataset.id];
    document.getElementById('location-info').innerHTML = `
      <img src="${data.img}" alt="${data.name}">
      <h2>${data.name}</h2>
      <p>${data.desc}</p>
    `;
  };
});

// --- 学院简介的tab切换 ---
const tabBtns = document.querySelectorAll('.college-tab-btn');
tabBtns.forEach(btn=>{
  btn.onclick = ()=>{
    tabBtns.forEach(b=>b.classList.remove('active'));
    document.querySelectorAll('.college-tab-content').forEach(div=>div.style.display='none')
    btn.classList.add('active');
    document.getElementById(btn.dataset.tab).style.display = 'block';
  }
});