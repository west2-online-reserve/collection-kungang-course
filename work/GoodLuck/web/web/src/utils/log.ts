export function showSuccessMessage(message:string, delay = 1500) {
  // 创建提示框元素
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 20px 30px;
    border-radius: 10px;
    z-index: 9999;
    font-size: 16px;
    animation: fadeIn 0.3s ease-in;
  `;
  
  // 添加动画样式
  const style = document.createElement('style');
  style.textContent = `
    @keyframes fadeIn {
      from { opacity: 0; transform: translate(-50%, -60%); }
      to { opacity: 1; transform: translate(-50%, -50%); }
    }
  `;
  document.head.appendChild(style);
  
  toast.textContent = message;
  document.body.appendChild(toast);
  
  // 延时后移除提示框并执行后续操作
  setTimeout(() => {
    toast.remove();
    style.remove();
  }, delay);
}