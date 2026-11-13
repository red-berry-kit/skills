# 技术选型

选依赖、配置工具或执行工程检查时，使用本页的工具、版本和命令。模块及状态职责按[设计与架构](design.md)划分，具体场景的接入模式按[开发约定](conventions.md#依赖现有能力优先)核对。

## 后端

| 用途 | 固定选择 |
| --- | --- |
| 业务语言 | Go |
| HTTP 路由 | chi |
| 依赖注入 | Uber Fx |
| ORM | Bun ORM（不是 JavaScript 运行时） |
| 默认数据库 | SQLite |
| OpenAPI、HTTP 参数校验、配置 Schema | Huma |
| CLI | github.com/urfave/cli/v3 |
| 配置加载、合并与解码 | Koanf、mapstructure/v2 |
| 日志 | Go 标准库 slog |

## 前端

| 用途 | 固定选择 |
| --- | --- |
| 运行时与包管理 | Node、pnpm |
| UI 与类型 | React、TypeScript、TSX |
| 构建 | Vite |
| 路由 | TanStack Router |
| 服务端状态与缓存 | TanStack Query |
| 表单状态 | TanStack Form |
| 表单业务校验 | Zod |
| 表格状态 | TanStack Table v9 |
| 基础 UI | Mantine |
| 日期时间控件 | Mantine dates |
| 日期格式与时间转换 | Day.js |
| 样式 | Mantine 主题；ui 模块内部按需使用 CSS Modules，不引入 Tailwind CSS |

组件接法读取 ui 模块的 `README.LLMS.md`；[前端状态与公开入口](design.md#前端状态与公开入口)规定库之间的职责边界。

## API 客户端

- **生成工具**：Huma 生成 OpenAPI，Orval 生成类型、原生 Fetch 调用与 TanStack Query 接入。
- **调用方式**：业务按操作标识与类型化参数调用生成入口，所有部署形式统一使用 `/api` 同源相对路径，不手写请求层。
- **运行依赖**：生成代码直接引用的依赖由项目显式声明；源码与生成边界按[装配约定](design.md#装配与工具职责)，校验边界按[接口与校验职责](design.md#接口与校验职责)执行。

## TypeScript

- **版本统一**：根 pnpm catalog 精确固定下表 TypeScript 版本，工作区声明使用 `catalog:`；根 `pnpm-workspace.yaml` 用 `overrides` 覆盖整个依赖树，包含生成器传递依赖。校验 peer 与真实依赖树仅有同一版本。
- **编译器 API**：使用该版本提供的同步与语法树接口；语法树及类型查询来自同一项目快照，结束时关闭 API 进程，不并行维护第二份解析器或旧版兼容分支。

## 静态检查与格式

| 工具 | 检查对象 |
| --- | --- |
| 独立 tsc | 完整类型；启用 strict、exactOptionalPropertyTypes、noUncheckedIndexedAccess |
| Oxlint／类型感知规则 | 常见错误、异步使用、组件规则与可配置边界 |
| Oxfmt | 格式与导入等格式化规则 |
| 统一边界检查 | 模块真实路径归属、依赖方向、公开入口、生成边界、UI 使用范围及静态可见的样式对象展开 |

- **覆盖范围**：统一检查覆盖业务模块与生成代码；配置集中维护，业务不能自行关闭既定规则。
- **独立执行**：Vite 构建和测试不能替代 tsc；边界静态检查统一接入 `redberry check`，检查不自动修复。
- **人工判断**：名称语义、职责划分、抽象及设计取舍按对应规范评审；工具可检查的部分接入统一检查，调研、POC 与覆盖结论仍须有来源和实际验证证据。

## 自动测试

| 测试层 | 工具与执行要求 |
| --- | --- |
| 纯逻辑 | Vitest Node |
| TSX 组件 | Vitest Browser Mode + Playwright provider + vitest-browser-react |
| 真实前后端 | Playwright Test |
| 页面视觉 | Playwright 截图断言，标记 `@visual`；默认任务跳过，在目标环境单独执行并更新基线 |

- **配置与生命周期**：统一管理测试配置与资源生命周期，默认零重试。
- **执行完整性**：拒绝未批准的 skip/todo、only 与空测试集合；统一入口核对必需测试层、退出码及结构化报告。
- **失败判定**：框架异常、报告缺失或损坏均判为失败，不以测试数量或单一退出码覆盖报告异常。

## 项目任务

通过项目根 `package.json` 的以下脚本执行任务；具体定义以目标项目为准。命令使用子命令在前、参数在后的写法。

| 入口 | 用途与边界 |
| --- | --- |
| `dev` | 默认 dev 环境；后端手动重启，前端 Vite HMR |
| `gen` | 执行项目生成入口 |
| `check` | 执行统一检查 |
| `test` | 执行统一测试 |
| `build`、`build:split` | 按目标项目定义选择发布构建形式 |

- **发布配置**：构建产物不携带运行配置，按上述构建入口选择发布形式。
- **CI 顺序**：先恢复依赖和必要产物，再执行 `check` → `test` → `build`。
- **任务归属**：脚本与 CLI 的分工按[装配与工具职责](design.md#装配与工具职责)执行。

## 工具版本

项目统一维护以下版本，通过依赖清单与锁文件固定；业务模块声明自身依赖并共用根锁文件。

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
