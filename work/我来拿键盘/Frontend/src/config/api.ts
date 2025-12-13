/**
 * API 配置文件
 * 统一管理后端API基础路径
 */

// 获取API基础URL
// 开发环境通过vite代理，使用相对路径
// 生产环境使用完整URL
const getApiBaseUrl = (): string => {
  return ''
}

export const API_BASE_URL = getApiBaseUrl()

/**
 * 生成完整的API URL
 * @param path API路径，如 '/api/user/info'
 * @returns 完整的API URL
 */
export const getApiUrl = (path: string): string => {
  // 如果已经是完整URL，直接返回
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  return `${API_BASE_URL}${path}`
}

/**
 * 生成完整的静态资源URL
 * @param path 资源路径，如 'avatar/default1.png' 或 '/static/avatar/default1.png'
 * @returns 完整的资源URL
 */
export const getStaticUrl = (path: string): string => {
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }

  // 确保路径以/static/开头，避免相对路径问题
  const cleanPath = path.startsWith('/') ? path.slice(1) : path

  if (import.meta.env.VITE_STATIC_BASE_URL) {
    return `${import.meta.env.VITE_STATIC_BASE_URL}/${cleanPath}`
  }

  // 始终生成完整的/static/前缀路径
  return `/static/${cleanPath}`
}

// API 端点常量
export const API_ENDPOINTS = {
  // 认证
  LOGIN: '/api/login',
  REGISTER: '/api/register',

  // 用户
  USER_INFO: '/api/user/info',
  USER_PASSWORD_CHANGE: '/api/user/password/change',
  USER_NAME_CHANGE: '/api/user/name/change',
  USER_AVATAR_UPLOAD: '/api/user/avatar/upload',

  // 学院
  COLLEGE_COMMENTS: (collegeId: number | string) => `/api/college/comments/${collegeId}`,
  COLLEGE_COMMENT: '/api/college/comment',
  COLLEGE_COMMENT_LIKE: (commentId: number | string) => `/api/college/comment/${commentId}/like`,
  COLLEGE_COMMENT_DELETE: (commentId: number | string) => `/api/college/comment/${commentId}`,

  // 签到
  CHECKIN_SUBMIT: '/api/checkin/submit',
  CHECKIN_COMMENTS: (locationId: number | string) => `/api/checkin/comments/${locationId}`,
  CHECKIN_DANMAKU: (locationId: number | string) => `/api/checkin/danmaku/${locationId}`,

  // 游戏
  GAME_WATERMELON_LEADERBOARD: '/api/game/watermelon/leaderboard',
  GAME_WATERMELON_PERSONAL: '/api/game/watermelon/personal',
  GAME_WATERMELON_SCORE: '/api/game/watermelon/score',
}

// 静态资源端点
export const STATIC_ENDPOINTS = {
  AVATAR_DEFAULT: '/static/avatar/default1.png',
}
