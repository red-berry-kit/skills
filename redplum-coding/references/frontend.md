# 前端开发

前端采用 React、Vite、TypeScript / TSX 与 pnpm。技术及版本见[技术选型](stack.md)，目录与依赖归属见[主入口与工作区](structure.md#主入口与工作区)。

## UI 与样式

采用 Mantine + CSS Modules，不引入 Tailwind CSS。

使用 Mantine 作为统一基础 UI。基础 UI 模块集中维护主题、颜色、字体、间距、密度和常见页面结构，业务通过有限组件入口组合界面。

业务入口暴露操作意图、密度等语义参数，避免直接透传完整底层样式能力。基础 UI 内部按需使用 CSS Modules；CSS Modules 负责隔离内部样式，不负责自动保证设计一致。

Mantine 默认主题可以被覆盖，因此“使用同一 UI 库”不等于“已强制全部页面风格一致”，仍需入口规则和实际页面检查。

业务 UI 使用 TSX 标签语法。业务目录限制底层 UI/CSS 直接导入、createElement/cloneElement 等元素创建入口；正常命名 hooks 与合法属性展开保留。样式展开补充检查只处理静态可见类型，不是一套新的 CSS 语言或运行时安全机制。

## API 客户端

采用 Orval + 原生 Fetch + TanStack Query。Huma 导出统一 OpenAPI，Orval 生成 `.redplum/frontend/api.ts`，包含类型、调用函数、query key、Query options 与 hooks。

业务基于 operationId 和类型化参数调用，统一使用 `/api` 同源路径。生成代码直接引用的 React 与 Query 运行依赖由根 `package.json` 显式声明。生成文件不手工修改。

强校验覆盖代码、类型、规范与模块边界；客户端请求和响应不增加重复的 schema 校验。服务端输入校验、表单业务校验和 HTTP 错误处理各自承担职责。

## 列表状态

Router URL 是列表条件的状态来源，页码、每页数量、筛选与排序全部进入 Query 查询键。前端只传递条件，不对当前页再次排序或筛选。

Table 使用服务端模式，开启 `manualPagination`、`manualSorting`，在边界接入[列表响应](api.md#列表查询)：

| 接口字段 | Table 接入 |
| --- | --- |
| `page` | `pageIndex = page - 1`；请求时反向转换 |
| `size` | `pageSize` |
| `items` | `data` |
| `total` | `rowCount` |

修改筛选、排序或每页数量时回到第一页。当前请求对应的服务端响应 `page`、`size` 是最终分页状态，并用于替换 URL；删除后的越界调整交给服务端，前端不根据总数另算页码。

使用 `keepPreviousData` 时，占位数据不参与分页同步，加载期间禁用依赖旧行的操作。

## 表单状态与提交

TanStack Form 是可编辑表单状态的来源，Zod 承担表单业务校验。使用生成类型提交[完整更新](api.md#更新接口)声明的全部可编辑字段，保留 `null`、零值与空字符串的区别。

保存操作放在 TanStack Form 的 `onSubmit`，调用生成请求函数；validator 只负责校验，不执行写入。服务端字段错误通过原生 `setErrorMap({onSubmit: {form, fields}})` 回填，Mantine 从 Field 的错误状态显示错误。

接口层使用 Huma `errors.location` 定位字段，例如 `body.title`。每个表单对已注册字段维护显式、受类型检查的映射；不将任意服务端字符串强断言为字段路径。相同字段的多条错误合并，未映射位置、无字段详情的业务错误与网络失败显示为表单级提示，不丢弃未知位置的错误。

字段通过 `onChange`、`onBlur` 与 Form 校验连接，修正后由原生提交错误生命周期清除该字段的过期错误，不因修改其他字段而清空仍未修正的字段错误。服务端字段错误收到后立即显示，不依赖用户是否先触碰字段。

提交失败回填后继续保持失败语义，不能将 `isSubmitSuccessful` 标记为成功；提交入口消费已显示的失败，避免未处理的 Promise 拒绝。只有成功分支刷新查询或执行成功操作。提交期间锁定本表单输入和保存按钮，避免重复写入及旧响应覆盖新输入。

## 日期控件

日期与时间输入使用同版本的 `@mantine/dates`，由统一 UI 入口提供 `DatePickerInput` 和 `DateTimePicker`，复用 Mantine 主题与 TanStack Form。项目显式声明其 peer 依赖 Day.js，不额外引入表单体系。统一样式入口先加载 core 样式，再加载 dates 样式；日期 locale 等公共设置由 `DatesProvider` 集中维护。

纯日期控件使用字符串或 null，与接口声明的可空性一致，不转换为 Date。时间控件的值为不带时区的日历时间；字段须明确编辑时区，在控件边界转换为带时区的 RFC 3339 字符串。UTC 编辑场景使用 Day.js 官方 UTC 插件；不将控件原值直接当作时间点。

默认 popover 模式以 `onDropdownClose` 标记弹层交互结束；触发器 `onBlur` 仅在未展开时调用字段 `handleBlur`，覆盖直接 Tab 离开的路径。打开日历后的内部焦点移动不提前标记 blur，也不因此显示必填错误。

必填日期清空后暂存为表单空值，提交前由表单校验阻止请求；可空日期保持 `null` 并按接口契约提交。日期与时间字段的服务端错误通过相同的 Form 提交错误槽显示，纠错后按原生生命周期清理。

普通时间编辑开启秒输入。未编辑的时间保留原始接口字符串；编辑后按控件秒精度提交，毫秒为零。必须手工录入毫秒或处理其他业务时区的字段单独明确交互与转换规则。
