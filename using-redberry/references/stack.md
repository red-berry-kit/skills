# 技术选型

本文汇总技术栈、版本和检查工具。接口约定见[API 契约](api.md)，模块装配见[模块与依赖](modules.md)，配置校验见[配置](config.md)，组件接入见[前端开发](frontend.md)。

## 后端

| 职责 | 选择 |
| --- | --- |
| HTTP 路由 | chi |
| 依赖注入与装配 | Uber Fx |
| ORM | Bun ORM |
| 默认数据库 | SQLite |
| Go 接口生成 OpenAPI、HTTP 参数校验 | Huma |
| 终端 CLI | github.com/urfave/cli/v3 |
| 配置加载、合并与解码 | Koanf（底层使用 mapstructure/v2 解码） |
| 配置 Schema 生成与结构校验 | Huma |
| 日志 | Go 标准库 slog |

Bun 指 Go ORM。前端使用 Node 与 pnpm。

## 前端

| 职责 | 选择 |
| --- | --- |
| UI 与类型 | React、TypeScript、TSX |
| 构建 | Vite |
| 包管理 | pnpm |
| 路由 | TanStack Router |
| 服务端状态与缓存 | TanStack Query |
| 表单状态 | TanStack Form |
| 表单业务校验 | Zod |
| 表格状态 | TanStack Table v9 |
| 基础 UI | Mantine |
| 日期与时间控件 | Mantine dates |
| 日期控件格式与时间转换 | Day.js |
| 内部样式 | CSS Modules |

基础 UI 集中维护主题和有限组件入口，业务使用 TSX 组合界面。表单与表格使用各自统一的状态来源。 样式采用 Mantine 主题与 CSS Modules，不引入 Tailwind CSS。

## 项目任务

项目根 `package.json` 的脚本提供 `dev`、`gen`、`check`、`test`、`build`、`build:split`。脚本只做转发，模块解析、安装、生成与任务编排由 Red Berry CLI 承担。

## TypeScript

统一使用 TypeScript 7.0.2，由根 pnpm catalog 精确固定，工作区声明使用 `catalog:`。严格校验 peer 与真实依赖树的单版本状态；编译器 API 检查器采用 TypeScript 7 原生 `typescript/unstable/sync` 与 `typescript/unstable/ast`；语法树和类型查询来自同一原生项目快照，结束时关闭 API 进程。根 `pnpm-workspace.yaml` 通过 `overrides` 将整个依赖树统一到 7.0.2，包括生成器的传递依赖，不保留另一份 TypeScript。

## 静态检查与格式

| 工具 | 职责 |
| --- | --- |
| 独立 tsc | 完整类型检查，启用 strict、exactOptionalPropertyTypes、noUncheckedIndexedAccess |
| Oxlint / 类型感知规则 | 常见错误、异步使用、组件规则与可配置边界 |
| Oxfmt | 统一代码格式 |
| 统一边界检查 | 模块真实路径归属、静态可见的样式对象展开 |

类型检查覆盖业务模块与生成代码。检查配置集中维护，业务不能自行关闭既定规则。Vite 构建和测试执行不代替 tsc。

## 自动测试

| 层次 | 选择 |
| --- | --- |
| 纯逻辑 | Vitest Node |
| TSX 组件 | Vitest Browser Mode + Playwright provider + vitest-browser-react |
| 真实前后端 | Playwright Test |
| 页面视觉 | Playwright 截图断言 |

统一管理配置与生命周期，默认零重试。拒绝未批准的 skip/todo、only 与空测试集合。统一入口同时校验退出码和结构化报告，确保必需测试层均已执行，框架异常、报告缺失或损坏均判为失败。

## 工具版本

项目采用以下版本，正式实现通过依赖清单与锁文件固定。

| 依赖 | 版本 |
| --- | --- |
| Go | 1.27.3 |
| chi / Fx / Huma | 5.5.0 / 1.24.0 / 2.40.0 |
| Bun / sqliteshim | 1.3.0 / 1.3.0 |
| Koanf / mapstructure | 2.4.1 / 2.5.0 |
| Node / pnpm | 26.12.1 / 12.15.0 |
| TypeScript / React | 7.0.2 / 19.3.1 |
| Vite / Mantine | 8.3.5 / 9.7.4 |
| Mantine dates / Day.js | 9.7.4 / 1.11.23 |
| Router / Query | 1.170.46 / 5.105.0 |
| Form / Table / Zod | 1.33.5 / 9.3.1 / 4.6.7 |
| Orval | 8.45.0 |
| Oxlint / Oxfmt | 1.89.0 / 0.74.0 |
| Vitest / Playwright Test | 5.0.5 / 1.64.1 |
| vitest-browser-react | 2.3.0 |

版本由项目统一维护，业务模块声明自身依赖并共用根锁文件。
