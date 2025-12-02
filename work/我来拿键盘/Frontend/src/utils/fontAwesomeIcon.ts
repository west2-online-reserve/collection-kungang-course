/**
 * Font Awesome Icon Utility Functions
 * 使用真实的Font Awesome SVG库实现
 */

import { library } from '@fortawesome/fontawesome-svg-core';
import { findIconDefinition } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';

// 导入所有solid图标到库中
library.add(fas);

/**
 * 创建一个Font Awesome图标
 * @param iconName 图标名称
 * @param id 图标元素ID
 * @param color 图标颜色
 * @param size 图标大小
 * @returns 创建的图标元素
 */
export function createFAIcon(iconName: string, id: string, color: string, size: number): HTMLElement {
  // 创建一个容器元素
  const container = document.createElement('div');
  container.id = id;
  container.style.color = color;
  container.style.fontSize = `${size}px`;
  container.style.display = 'inline-flex';
  container.style.alignItems = 'center';
  container.style.justifyContent = 'center';
  container.style.width = `${size}px`;
  container.style.height = `${size}px`;

  // 检查图标是否存在
  // 使用类型断言处理iconName
  const iconDefinition = findIconDefinition({ prefix: 'fas', iconName } as any);

  if (iconDefinition) {
    // 如果找到图标定义，创建SVG元素
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svg.setAttribute('width', size.toString());
    svg.setAttribute('height', size.toString());
    svg.setAttribute('viewBox', '0 0 512 512');
    svg.setAttribute('fill', 'currentColor');

    // 创建路径元素
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    if (iconDefinition.icon[4]) {
      // 对于带有多个路径的图标，创建一个use元素
      svg.innerHTML = `<use xlink:href="#${iconName}"></use>`;
    } else {
      // 设置路径数据
      path.setAttribute('d', iconDefinition.icon[4]);
      svg.appendChild(path);
    }

    container.appendChild(svg);
  } else {
    // 图标不存在时显示占位符
    container.style.backgroundColor = color + '20';
    container.style.borderRadius = '4px';
    container.textContent = iconName[0]?.toUpperCase() || '?';
  }

  return container;
}

/**
 * 将图标挂载到指定的DOM元素
 * @param icon 图标元素
 * @param targetSelector 目标DOM元素选择器
 */
export function mountFAIcon(icon: HTMLElement, targetSelector: string): void {
  const targetElement = document.querySelector(targetSelector);
  if (targetElement) {
    targetElement.appendChild(icon);
  }
}
