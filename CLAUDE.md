# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概览

这是一个基于 React 构建的医院管理系统（HospitalRun），使用 Create React App 创建。该应用提供多语言支持（中文、英语、日语），用于管理医院环境中的患者、医生和预约。

## 开发命令

### 启动开发服务器
```bash
npm start
```
在开发模式下运行应用，地址为 http://localhost:3000

### 运行测试
```bash
npm test
```
以交互式监视模式启动测试运行器

### 构建生产版本
```bash
npm run build
```
在 `build` 文件夹中创建优化的生产版本

## 架构

### 应用结构

应用使用标准的 React SPA 架构，包含以下关键层次：

1. **路由层** (`src/App.js`)：React Router v7 路由，包裹在 `LanguageProvider` 和 Material-UI `ThemeProvider` 中
2. **上下文层** (`src/contexts/`)：通过 React Context API 进行全局状态管理
3. **页面层** (`src/pages/`)：顶层路由组件（Dashboard、Patients、Doctors、Appointments）
4. **组件层** (`src/components/`)：可复用的 UI 组件（表单、Header、Sidebar）

### 核心架构模式

#### 多语言支持
- **上下文**：`LanguageContext` 管理翻译和语言切换
- **翻译加载**：组件挂载时从 `/public/locales/{lang}/translation.json` 获取 JSON 文件
- **回退策略**：如果翻译文件加载失败，回退到内联默认值；如果缺少键，回退到中文(zh)，然后是键本身
- **使用方式**：组件使用 `const { t } = useLanguage()` 钩子，调用 `t('key')` 获取翻译字符串
- **支持的语言**：中文(zh)、英语(en)、日语(ja)

#### 状态管理
- **本地状态**：所有数据（患者、医生、预约）当前使用页面组件中的 `useState` 管理
- **无后端**：数据仅存储在内存中；页面刷新后重置
- **表单模式**：使用受控组件的模态对话框进行添加/编辑操作

#### UI 框架
- **Material-UI v7**：主要组件库 (`@mui/material`)
- **主题**：浅色模式，蓝色主色调 (#1976d2)，定义在 `App.js:13`
- **布局**：响应式布局，包含 Header、可折叠的 Sidebar 和主内容区域
- **图标**：使用 Material-UI Icons 包提供所有图标

### 组件模式

#### 表单组件
所有表单组件（PatientForm、DoctorForm、AppointmentForm）遵循以下模式：
- 接受 `open`、`onClose`、`onSave` 和可选的 entity 属性用于编辑
- 使用 Material-UI Dialog 和受控输入
- 通过 `useEffect` 依赖 `[entity, open]` 在对话框打开时重置表单状态
- 根据是否提供 entity 属性处理创建和编辑模式
- 提交时调用 `onSave(formData)` 然后 `onClose()`

#### 页面组件
所有页面组件遵循以下模式：
- 使用 `useState` 管理实体数组和表单对话框状态
- 渲染 Material-UI Table 展示数据
- 包含浮动操作按钮 (Fab) 用于添加新实体
- 通过设置 `editingEntity` 状态并打开表单对话框处理编辑
- 使用 `Math.max(...entities.map(e => e.id)) + 1` 生成新 ID

### 翻译键命名约定
- 组件标签：小写驼峰式（例如：`patientName`、`appointmentDate`）
- 导航/分区：小写（例如：`patients`、`doctors`、`dashboard`）
- 操作：小写（例如：`add`、`edit`、`save`、`cancel`）
- 在翻译调用中为缺失的键提供回退默认值：`t('key', 'default value')`

### 数据验证
- AppointmentForm 验证新预约的日期不能是过去时间（第 76-86 行）
- DoctorForm 使用 alert 验证必填字段（姓名、专业、工作年限）
- 表单在 TextField 组件上使用 HTML5 `required` 属性

## 重要依赖

- `react-router-dom` (v7)：客户端路由
- `@mui/material` (v7)：UI 组件库
- `@mui/x-date-pickers` (v8)：日期选择器组件（在 AppointmentForm 中与 date-fns 适配器一起使用）
- `axios` (v1.13)：HTTP 客户端（已安装但当前未使用）
- `date-fns` (v4)：日期操作工具

## 测试

测试配置使用 React Testing Library 和 Jest（通过 react-scripts）。测试文件应命名为 `*.test.js` 并与组件放在一起。
