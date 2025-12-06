// === 1. 导航与页面切换逻辑 ===
function switchTab(tabId) {
    // 隐藏所有 section
    document.querySelectorAll('.page-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // 显示目标 section
    const target = document.getElementById(tabId);
    if(target) {
        target.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

}


// 校友寄语逻辑 
function addMessage() {
    const nameInput = document.getElementById('guest-name');
    const msgInput = document.getElementById('guest-msg');
    const board = document.getElementById('message-board');

    if(nameInput.value.trim() === '' || msgInput.value.trim() === '') {
        alert('请填写姓名和祝福语哦！');
        return;
    }

    // 创建新留言卡片
    const div = document.createElement('div');
    div.className = 'bg-white p-4 rounded shadow border-l-4 border-fzuRed animate-fade-in';
    div.innerHTML = `
        <p class="text-gray-800">${msgInput.value}</p>
        <p class="text-right text-sm text-gray-500 mt-2">- ${nameInput.value}</p>
    `;
    
    // 插入到最前面
    board.insertBefore(div, board.firstChild);

    // 清空输入框
    nameInput.value = '';
    msgInput.value = '';
}

//校史问答逻辑
const quizData = [
    {
        question: "福州大学创建于哪一年？",
        options: ["1958年", "1960年", "1978年", "1921年"],
        correct: 0
    },
    {
        question: "福州大学的校训是？",
        options: ["自强不息，厚德载物", "明德至诚，博学远志", "实事求是", "爱国 进步 民主 科学"],
        correct: 1
    },
    {
        question: "福州大学入选了国家哪项建设工程？",
        options: ["985工程", "211工程", "珠峰计划", "卓越工程师"],
        correct: 1
    },
    {
        question: "福州大学“三种精神”不包括以下哪项？",
        options: ["艰苦奋斗的创业精神", "严谨求实的治学精神", "勇于拼搏的奉献精神", "兼容并包的自由精神"],
        correct: 3
    },
    {
        question: "福州大学目前主要校区位于？",
        options: ["鼓浪屿", "怡山", "旗山", "马尾"],
        correct: 2
    }
];

let currentQuestionIndex = 0;
let score = 0;
let hasAnswered = false;

function loadQuestion() {
    hasAnswered = false;
    const q = quizData[currentQuestionIndex];
    document.getElementById('question-number').innerText = `Question ${currentQuestionIndex + 1}/${quizData.length}`;
    document.getElementById('question-text').innerText = q.question;
    document.getElementById('next-btn').classList.add('hidden');

    const optionsHtml = q.options.map((opt, index) => `
        <div onclick="checkAnswer(${index}, this)" class="option-card p-4 border-2 border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition flex items-center">
            <div class="w-8 h-8 rounded-full border-2 border-gray-300 mr-4 flex items-center justify-center font-bold text-gray-500 option-letter">${String.fromCharCode(65 + index)}</div>
            <span>${opt}</span>
        </div>
    `).join('');
    
    document.getElementById('options-area').innerHTML = optionsHtml;
}

function checkAnswer(selectedIndex, element) {
    if (hasAnswered) return; // 防止重复点击
    hasAnswered = true;

    const correctIndex = quizData[currentQuestionIndex].correct;
    const options = document.querySelectorAll('.option-card');

    if (selectedIndex === correctIndex) {
        element.classList.remove('border-gray-200');
        element.classList.add('border-green-500', 'bg-green-50');
        element.querySelector('.option-letter').classList.add('bg-green-500', 'text-white', 'border-green-500');
        score += 20;
    } else {
        element.classList.remove('border-gray-200');
        element.classList.add('border-red-500', 'bg-red-50');
        element.querySelector('.option-letter').classList.add('bg-red-500', 'text-white', 'border-red-500');
        
        // 显示正确答案
        options[correctIndex].classList.add('border-green-500', 'bg-green-50');
        options[correctIndex].querySelector('.option-letter').classList.add('bg-green-500', 'text-white', 'border-green-500');
    }

    document.getElementById('current-score').innerText = `Score: ${score}`;
    document.getElementById('next-btn').classList.remove('hidden');
}

function nextQuestion() {
    currentQuestionIndex++;
    if (currentQuestionIndex < quizData.length) {
        loadQuestion();
    } else {
        showResult();
    }
}

function showResult() {
    document.getElementById('question-area').classList.add('hidden');
    document.getElementById('result-area').classList.remove('hidden');
    document.getElementById('final-score').innerText = score;
    
    let comment = "";
    if(score === 100) comment = "太棒了！您是如假包换的福大人！";
    else if(score >= 80) comment = "成绩优秀！看来您对校史很了解。";
    else if(score >= 60) comment = "及格啦！继续了解更多福大故事吧。";
    else comment = "还需努力哦，建议多逛逛校史馆！";
    
    document.getElementById('result-comment').innerText = comment;
}

function restartQuiz() {
    currentQuestionIndex = 0;
    score = 0;
    document.getElementById('current-score').innerText = `Score: 0`;
    document.getElementById('result-area').classList.add('hidden');
    document.getElementById('question-area').classList.remove('hidden');
    loadQuestion();
}
