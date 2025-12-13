/// <reference types="vite/client" />
// src/env.d.ts
interface ImportMetaEnv {
  // 已有的类型...
  readonly VITE_APP_TITLE: string
  
  // 添加你的自定义环境变量
  readonly VITE_API_BASE_URL: string
  readonly VITE_UPLOAD_URL: string
  readonly VITE_TIMEOUT: string
  readonly VITE_APP_ENV: 'development' | 'production' | 'test'
  
  // 更多环境变量...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}