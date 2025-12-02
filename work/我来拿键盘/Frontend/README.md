# 前端 (Frontend)

该模板旨在帮助您开始使用 Vite 进行 Vue 3 开发。

## 项目结构

前端应用程序使用 Vue 3 构建，并遵循标准的基于组件的架构。

- **`src/pages`**: 包含应用程序的主要视图（例如，登录、主页、学院详情）。
- **`src/components`**: 可复用的 UI 组件。
- **`src/router`**: Vue Router 配置。
- **`src/stores`**: 状态管理 (Pinia/Vuex)。
- **`src/assets`**: 静态资源，如图片和样式。

## 推荐 IDE 设置

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (并禁用 Vetur)。

## 推荐浏览器设置

- 基于 Chromium 的浏览器 (Chrome, Edge, Brave 等):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) 
  - [在 Chrome DevTools 中开启自定义对象格式化程序](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [在 Firefox DevTools 中开启自定义对象格式化程序](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## TS 中 `.vue` 导入的类型支持

TypeScript 默认无法处理 `.vue` 导入的类型信息，因此我们使用 `vue-tsc` 替换 `tsc` CLI 进行类型检查。在编辑器中，我们需要 [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) 使 TypeScript 语言服务能够感知 `.vue` 类型。

## 自定义配置

请参阅 [Vite 配置参考](https://vite.dev/config/)。

## 项目设置

```sh
pnpm install
```

### 开发环境编译和热重载

```sh
pnpm dev
```

### 生产环境类型检查、编译和压缩

```sh
pnpm build
```

### 运行单元测试 [Vitest](https://vitest.dev/)

```sh
pnpm test:unit
```

### 运行端到端测试 [Playwright](https://playwright.dev)

```sh
# 首次运行安装浏览器
npx playwright install

# 在 CI 上测试时，必须先构建项目
pnpm build

# 运行端到端测试
pnpm test:e2e
# 仅在 Chromium 上运行测试
pnpm test:e2e --project=chromium
# 运行特定文件的测试
pnpm test:e2e tests/example.spec.ts
# 在调试模式下运行测试
pnpm test:e2e --debug
```

### 使用 [ESLint](https://eslint.org/) 进行代码检查

```sh
pnpm lint
```
