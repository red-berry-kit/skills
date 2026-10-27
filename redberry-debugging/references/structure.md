# 目录结构

本页给出业务项目、独立模块与受管理目录的具体文件位置。模块身份及替代见[模块与依赖](modules.md)，运行步骤见[CLI 约定](cli.md)。

## 项目结构

```text
shop/
├── AGENTS.md                     # Agent 开发入口，项目命令与项目特有规则
├── go.mod                        # 项目根 Go 模块
├── go.sum
├── redberry.yaml                   # 项目依赖清单
├── redberry.lock                   # 实际解析版本与依赖锁定结果
├── go.work                        # CLI 维护的 Go 工作区
├── package.json                   # workspace 根、统一任务入口与生成代码运行依赖
├── pnpm-lock.yaml
├── pnpm-workspace.yaml
├── .gitignore
├── cmd/
│   └── shop/                     # 根据项目命令名生成，不固定叫 app
│       ├── main.go               # CLI 入口与退出处理
│       └── bootstrap.go          # 应用装配与启动，与 main.go 同包
├── backend/                      # 项目后端模块
│   ├── module.go                 # Fx 装配入口
│   └── config.go                 # 项目配置定义（按需）
├── frontend/                     # 项目前端应用
│   ├── package.json              # 应用依赖与前端脚本
│   ├── index.html                # HTML 入口
│   ├── main.tsx                  # React 挂载入口
│   ├── index.ts                  # 模块公开入口
│   ├── router.tsx                # 项目路由组合
│   ├── vite.config.ts
│   ├── tsconfig.json             # 类型检查配置入口
│   ├── tsconfig.app.json         # 浏览器代码
│   └── tsconfig.node.json        # Node 工具配置
├── .local/redberry/operation.lock # 依赖操作互斥锁，不属于生成事务
├── migrations/                   # 项目自身模块的迁移资源（按需）
│   ├── embed.go                  # 嵌入并导出迁移 SQL
│   └── 0.1.0.sql                 # 版本迁移示例
├── modules/                      # 用户维护的业务模块示例（ID 后缀即模块目录）
│   └── order/
│       ├── redberry.yaml
│       ├── go.mod
│       ├── go.sum
│       ├── backend/
│       │   ├── module.go          # 后端 Fx 模块入口
│       │   ├── config.go          # 模块配置定义（按需）
│       │   └── order.go
│       ├── frontend/
│       │   ├── package.json       # 模块前端依赖
│       │   ├── index.ts           # 前端公开入口
│       │   └── order.tsx
│       └── migrations/
│           ├── embed.go
│           └── 0.1.0.sql
├── config/
│   ├── app.toml                   # 始终读取的公共配置
│   ├── app.dev.toml               # 开发环境配置
│   ├── app.test.toml              # 测试环境配置
│   └── app.prod.toml              # 生产环境配置
└── .redberry/                      # CLI 管理，Git 忽略，可恢复
    ├── modules/                   # 拉取的外部依赖模块源码
    │   └── github.com/
    │       └── redberry/
    │           └── user/          # 外部用户模块源码
    ├── config/
    │   └── app.schema.json        # 配置编辑提示与检查约束
    ├── backend/
    │   ├── modules.go             # 后端模块导入与 Fx 组合
    │   └── assets/                # 单二进制模式生成
    │       ├── embed.go           # 嵌入并导出前端资源
    │       ├── admin/             # 后台前端构建输出
    │       └── <应用名>/          # 独立应用构建输出
    ├── frontend/
    │   ├── modules.ts             # 前端模块入口汇总
    │   ├── routes.ts              # 路由装配导出
    │   ├── providers.tsx          # 模块默认 Provider 装配
    │   └── api.ts                 # Orval 生成的 Fetch、类型与 Query 接入
    └── openapi.json               # 后端导出的 OpenAPI
```

`cmd/<项目命令名>/` 是后端启动层。项目根包含 `go.mod`、`go.sum`，不为命令目录单独创建 Go module。项目内的模块目录保存用户自有模块，ID 后缀与该目录一致；示例放在 `modules/` 下，也可以直接放在项目根。`.redberry/modules/` 保存受管理的外部源码，用户不在其中维护业务修改。模板只产出一套结构；没有前端的项目不生成前端文件。

`go.work` 由 CLI 更新，自有模块通过 `use` 纳入，受管理外部目标通过生成的本地映射接入；生成包共用根模块，不独立列为工作区模块。用户无需手工维护 `replace`。模块 ID 到 `.redberry/modules/` 路径的映射由 CLI 统一处理，图中的域名路径仅展示一个依赖实例。

## 模块结构

`redberry create mod` 从模块模板创建模块描述、Go module、后端 Fx 入口与业务文件，以及前端包描述、公开入口与业务组件。`backend/config.go` 和 `migrations/` 按需创建。

```text
order/
├── redberry.yaml        # 模块描述
├── go.mod             # 位于模块根目录（默认生成）
├── go.sum             # Go 依赖校验和
├── backend/
│   ├── module.go       # Fx 入口（默认生成）
│   ├── config.go       # 配置类型、默认值与约束（按需）
│   └── order.go        # 后端业务实现（默认生成）
├── frontend/
│   ├── package.json    # 模块前端依赖（默认生成）
│   ├── index.ts        # 前端公开入口（默认生成）
│   └── order.tsx       # 前端业务实现（默认生成）
└── migrations/         # 模块根层的迁移资源
    ├── embed.go        # 嵌入并导出迁移资源
    └── 0.1.0.sql       # 版本迁移示例
```

`go.mod` 位于模块根目录，使 `backend` 和 `migrations` 同属一个 Go module。`migrations/embed.go` 在资源所在目录嵌入 SQL，后端通过导入迁移包获取资源，无需跨父目录嵌入。

`frontend/package.json` 声明模块前端依赖，由项目 pnpm workspace 统一安装；`pnpm-lock.yaml` 统一位于项目根目录，模块内不另建锁文件。

模块功能可以只实现一侧；`create mod` 的默认模板同时生成前后端基础入口。纯前端模块不需要 Go 工程文件。模块描述不重复声明约定入口 `backend/module.go`、`frontend/index.ts` 及资源目录。

迁移资源由模块自己维护，项目统一发现和执行，不要求额外复制到项目根。迁移目录的“根层”指模块根层。一次迁移批次覆盖所有模块的待执行迁移，事务与中断恢复遵循[数据迁移](migrations.md#迁移事务与失败处理)中的数据库方言约定。

## 主入口与工作区

后端入口位于 `cmd/<项目命令名>/main.go`，同目录 `bootstrap.go` 负责应用装配与启动，两者属于同一个 `main` 包。创建项目时根据项目名生成命令目录；`app` 不是固定目录名。

例如项目命令名为 `shop`，从根目录执行 `go run ./cmd/shop`，构建可执行文件默认名为 `shop`。

前端以 `frontend/` 为 Vite root，`frontend/index.html` 引用 `/main.tsx`，由 `frontend/main.tsx` 挂载 React。根脚本通过切换到 `frontend/` 运行前端命令，使 Vite 自动发现同目录配置。

`frontend/index.ts` 只提供模块公开导出，不执行挂载，也不反向引用项目启动入口。浏览器代码和 Node 配置分别由 `tsconfig.app.json`、`tsconfig.node.json` 检查，`tsconfig.json` 为配置入口；检查范围须覆盖参与装配的模块和生成代码，而不只包含主入口的导入闭包。

根 `package.json` 负责统一脚本、工具版本约束，以及根层生成代码直接引用的运行依赖（当前为 React 与 TanStack Query），`frontend/package.json` 声明应用依赖，各模块仍声明自身依赖。workspace 显式纳入各模块的前端包与 `.redberry/modules/` 下的前端包，统一使用根锁文件。

前端 workspace 包名与 Go 模块 ID 分开：项目应用包使用 `@<组织>/app`，模块前端包使用 `@<组织>/<模块名>`，模块包名不附加所属项目名。应用包和模块包均设为 `private: true`。例如组织为 `acme` 时，项目应用包名为 `@acme/app`，`order` 模块包名为 `@acme/order`。根 `package.json` 是 workspace 根层工具包，不与应用或模块前端包共用身份。

`.redberry/frontend/` 生成代码引用解析后的模块公开入口静态路径；不假定它会继承 `frontend/package.json` 的包解析环境。Orval 生成的 `api.ts` 直接导入 TanStack Query，因此其运行依赖由根 `package.json` 显式声明；应用和模块仍声明自身使用的依赖，不靠 hoist 或应用目录为生成代码兜底。

自动生成文件归入 `.redberry/`，不手工修改。隐藏目录可以通过完整包路径显式导入；生成包共用根目录 `go.mod`，不额外创建生成模块。外部依赖模块保留各自的 `go.mod`。

## 受管理目录

项目内的模块目录为自有模块，`.redberry/modules/` 为 CLI 管理的外部依赖。`.redberry/` 整体由 Git 忽略，依赖按根层锁文件重新拉取，生成代码重新生成。锁文件、用户配置和迁移执行状态不放入该目录。

生成层的 `backend/`、`frontend/` 按启用部分生成。生成前准备依赖，构建和检查前确保生成结果完整，移除模块时清理旧产物。隐藏生成包须由统一检查入口显式覆盖，不能只依靠根层 `go test ./...`。

## 构建与发布产物

同一套业务代码支持两种构建模式，默认单二进制，按需选择前后端分离模式。模式由 `pnpm build` 与 `pnpm build:split` 选择，CLI 的 `--mode` 只接受 `single`、`split`，默认 `single`，其他值直接报错。

| 模式 | 发布产物（以项目命令名 `shop` 为例） | 行为 |
| --- | --- | --- |
| 单二进制（默认） | `dist/shop` | 先构建前端，再通过 `go:embed` 嵌入静态资源，由后端提供资源与 API |
| 前后端分离 | `dist/backend/shop`、`dist/admin/` | 后端提供 API，前端静态资源独立部署 |

`dist/` 用于发布产物，由 Git 忽略；`.redberry/` 继续用于受管理依赖和生成代码。两种模式共用业务实现。

### 构建模式参数

```sh
pnpm build              # 默认单二进制，等同 --mode single
pnpm build:split        # 前后端分离
```

`--mode` 是 CLI 构建参数，不是应用运行环境，不用于选择 `config/app.<环境>.toml`。非法值在执行构建步骤前报错，不静默回退。

### 前端嵌入资源

```text
.redberry/backend/assets/
├── embed.go
├── admin/           # 后台前端构建输出
└── <应用名>/        # 独立应用构建输出
```

单二进制构建时，先将各应用分别构建到 `.redberry/backend/assets/<应用名>/`，再编译 Go。`embed.go` 按应用名嵌入并提供独立资源根，宿主依应用声明交付页面与静态资源。

分离模式不引入该嵌入包，前端直接输出到 `dist/admin/`。构建流程应保证模式切换时不会误引入上次生成的嵌入资源。清理构建产物时保留 `.redberry/modules/` 中的依赖源码。

中间资源由 CLI 管理，保留在 `.redberry/`；最终发布产物仍在 `dist/`。

### API 路径与转发

前端统一使用 `/api` 相对路径调用后端，各环境共享同一套业务调用代码。

| 场景 | 请求处理 |
| --- | --- |
| 开发 | Vite 将 `/api` 请求代理到开发后端 |
| 单二进制部署 | 后端在同一来源提供前端静态资源和 `/api` 接口 |
| 前后端分离部署 | 部署侧反向代理将同一来源下的 `/api` 请求转发到后端，静态资源由前端部署提供 |

分离部署采用同源入口，不要求业务代码切换 API 域名。具体代理地址由开发或部署配置负责，不硬编码在业务模块中。

### SPA 路由回退

访问前端页面路径或直接刷新该路径时，返回 `index.html`，由前端路由处理页面匹配。`/api` 及其子路径不参与页面回退；找不到的静态资源保留真实错误，不以 HTML 页面响应掩盖资源缺失。

单二进制部署由后端处理上述规则；分离部署由静态服务器或部署侧代理处理。

配置文件及其加载规则见[配置](config.md)，迁移文件及事务规则见[数据迁移](migrations.md)。
