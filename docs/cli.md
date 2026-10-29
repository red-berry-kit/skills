# CLI 与开发流程

本文是 CLI 命令与流程在整体需求中的原始表述。CLI 的权威需求条目、命令契约与实现都在独立仓库
`red-berry-kit/cli`（`docs/requirements.md`、`docs/commands.md`），两侧不一致时以该仓库为准。

## 依赖维护：redberry

外部模块源码放 `.redberry/modules/`，自有模块放项目内的模块目录。

| 命令 | 职责 |
| --- | --- |
| `redberry create app <名称>` | 使用项目模板创建项目，并生成项目根 `AGENTS.md` |
| `redberry create mod <模块ID>` | 使用模块模板创建模块并加入当前项目 |
| `redberry add <模块ID>[@版本约束]` | 添加依赖或更新已有约束 |
| `redberry install [--locked]` | 安装清单声明的全部模块 |
| `redberry rm <模块ID>` | 移除直接依赖 |
| `redberry up [模块ID]` | 在现有约束内升级指定或全部模块 |
| `redberry outdated` | 查询落后版本 |
| `redberry list` | 查看实际模块、版本、依赖关系与替代实现 |
| `redberry gen` | 生成装配、路由、API 客户端等产物 |
| `redberry check` | 检查代码合规、模块规范与安装及生成状态 |

项目与模块都从对应模板创建；CLI 将名称或模块 ID 填入模板，并完成项目依赖接入。

官方默认模板随 CLI 同版本发布。创建项目或模块时可以显式指定外部模板仓库，使用该仓库的模板替代本次创建所用的默认模板。

每个模板仓库根目录承载一种模板，分别遵循[项目结构或独立模块结构](structure.md)。`create app` 使用项目模板，`create mod` 使用模块模板。

两个创建命令共用 `--template` 参数，短别名为 `-t`，参数位于名称或模块 ID 之后；省略时使用官方默认模板。

```sh
redberry create app shop -m github.com/acme/shop -t <仓库地址>
redberry create mod github.com/acme/shop/modules/order -t <仓库地址>
```

`create app` 必须通过 `--module` / `-m` 指定项目的 Go module 路径。`--scope` / `-s` 指定前端包组织名；省略时按模块路径推导。创建只准备模板与模块装配，随后在项目根运行 `redberry install` 安装依赖并生成完整产物。

```sh
redberry create app shop -m github.com/acme/shop -s acme
cd shop
redberry install
```

外部模板可通过 `--ref` / `-r` 固定分支、标签或提交；省略时使用仓库默认分支。模板只做文件渲染，不执行仓库脚本。外部模板创建成功后，在标准错误输出仓库、请求 ref 和解析得到的完整提交，默认分支同样保留来源诊断。

`create mod` 接收完整模块 ID，采用 Go module path 格式。项目内模块 ID 必须以项目根 `go.mod` 的 module 路径为前缀，其余路径与项目根下的相对目录一致；模块目录不要求位于 `modules/` 下，但不能占用 `cmd/`、`backend/`、`frontend/`、`config/`、`migrations/`、`scripts/`、`tests/` 等工程目录与隐藏目录。例如项目根路径为 `github.com/acme/shop` 时，`redberry create mod github.com/acme/shop/modules/order` 在 `modules/order/` 创建本地模块，`github.com/acme/shop/order` 则在 `order/` 创建，两种写法都加入项目依赖。默认模块模板包含完整前后端基础文件：`redberry.yaml`、`go.mod`、`backend/redberry_module.go`、`backend/order.go`、`frontend/package.json`、`frontend/index.ts` 和 `frontend/order.tsx`；`order` 替换为模块目录名。初始模块版本为 `0.1.0`，项目依赖清单写入 `^0.1.0`。配置定义与 `migrations/` 按需添加。

项目根 `AGENTS.md` 在项目创建时生成，包含项目结构、常用 CLI 与项目任务命令、用户模块与 `.redberry/` 生成目录边界，以及项目特有规则区。文件归业务项目维护，依赖管理、安装、生成、检查和升级操作均不覆盖它。Skill 与配套规范由用户独立安装和更新，CLI 不管理。

### 版本与添加

```sh
redberry add github.com/redberry/user@^1.2.0
redberry add github.com/redberry/user@1.2.0
redberry add github.com/redberry/user
```

版本使用 SemVer，支持精确版本与标准 `^` 范围，不带 `v`。省略版本时选择最新稳定版，以该版本起始的 `^` 范围写入清单，锁文件固定实际版本。

`up` 只升级到当前约束允许的最新稳定版，不修改约束；省略模块 ID 时升级全部模块。修改约束或跨大版本使用 `add <模块ID>@<新约束>`。所有变更均须满足完整依赖图、替代关系与唯一实现约束。

### 安装与移除

- 有锁时按锁安装，不主动升级；无锁时解析清单并生成锁文件。
- 普通安装保留仍有效的锁定项，仅重新解析清单变更影响的依赖。
- `--locked` 在锁缺失或与清单不一致时报错，不修改锁文件；缺失源码仍可按锁定来源下载。
- `add`、`rm`、`up` 同步清单、锁文件、受管理源码、工作区与生成装配，清理不再需要的受管理依赖。
- `rm` 只移除项目直接声明；仍被间接依赖的模块继续保留。目标没有直接声明时明确提示，不改写其他模块的依赖。
- 依赖维护命令不删除项目内的用户模块源码。

### 查询与结构化输出

`outdated` 只读查询，不修改项目文件：

| 字段 | 含义 |
| --- | --- |
| `current` | 当前锁定版本 |
| `wanted` | 当前约束内最新稳定版 |
| `latest` | 最新稳定版，可能超出当前约束 |

`list`、`outdated`、`check` 支持 `--json`。标准输出仅包含一个 JSON 结果，诊断写标准错误。

### 生成与检查

`gen` 使用当前安装结果生成产物，不隐式升级或安装依赖；源码缺失、安装状态不完整时提示先运行 `redberry install`。

`check` 由 `pnpm check` 调用，检查类型、格式、静态规则、模块边界、迁移约定、受管理源码、锁文件与生成产物一致性。仅检查，不自动修复。

## 业务项目可执行文件

以下以项目命令名 `shop` 为例：

| 命令 | 职责 |
| --- | --- |
| `shop` | 显示帮助，不加载配置或启动服务 |
| `shop serve` | 加载、合并、校验配置，执行必要迁移后启动 HTTP |
| `shop check` | 仅加载、合并、校验配置 |
| `shop migrate` | 执行统一迁移流程后退出，不启动 HTTP |

需要配置的子命令共用参数，参数位于子命令之后：

| 参数 | 短别名 | 含义 |
| --- | --- | --- |
| `--env` | `-e` | 指定环境；省略时只读取公共配置 |
| `--config` | `-c` | 配置目录，默认当前工作目录的 `./config` |

```sh
./shop serve -e prod -c /etc/shop
./shop check -e prod -c /etc/shop
./shop migrate -e prod -c /etc/shop
```

成功返回 `0`，配置、迁移或启动失败返回非零并报告错误。`shop check` 检查运行配置；`redberry check` 检查开发阶段代码与项目状态。

`check` 复用服务的配置加载与校验，不需要先获取数据库连接或监听端口，失败时报告完整配置路径。`migrate` 成功或没有待执行迁移均返回 `0`，配置、锁等待或迁移失败返回非零，结束后释放资源；提前运行 `migrate` 不会让 `serve` 绕过迁移检查，后者按版本账本跳过已完成步骤。详细加载规则见[配置](config.md)，事务、锁与失败处理见[数据迁移](migrations.md)。

## 项目任务

项目根 `package.json` 提供统一入口，脚本只转发到 Red Berry CLI：

| 脚本 | 行为 |
| --- | --- |
| `pnpm dev` | 检查依赖并生成产物，启动后端与 Vite；默认环境 `dev` |
| `pnpm gen` | 调用统一生成入口 |
| `pnpm check` | 检查代码、模块边界与生成一致性 |
| `pnpm test` | 运行必需测试层并校验报告 |
| `pnpm build` | 生成、检查并构建单二进制产物 |
| `pnpm build:split` | 生成、检查并构建前后端分离产物 |

`redberry app dev --env test` 覆盖开发运行环境；后端代码修改后手动重启。构建不选择运行环境，不携带运行配置。
前端专用脚本另有 `dev:web`、`build:web`、`check:web`、`test:web`、`gen:api`，只覆盖前端一层。

CI 恢复锁定依赖与必要生成产物后，依次执行 `check` → `test` → `build`。脚本负责转发，依赖维护、生成与任务编排集中在 Red Berry CLI，脚本不重复实现这些领域逻辑。

`check` 采用检查模式，不格式化或自动修复，也不能通过覆盖旧产物来掩盖生成不一致。冷启动 CI 先恢复锁定依赖和必要产物，再执行检查；`build` 自身保留检查前置条件。

## 开发运行

`pnpm dev` 负责统一启动开发环境：

1. 检查依赖，生成必要的模块装配与其他启动输入。
2. 同时启动 Go 后端和 Vite。
3. 后端代码修改后由开发者手动重启，不提供自动热重载；前端由 Vite 提供 HMR。
4. 用户按 `Ctrl+C` 时统一关闭两个进程；任一进程异常退出时停止另一进程，向任务入口报告失败。

开发模式不嵌入前端资源，Vite 通过 `/api` 代理到开发后端。不引入后端热重载工具。

### 开发地址与端口

| 服务 | 默认开发地址 |
| --- | --- |
| Go 后端 | `127.0.0.1:8080` |
| Vite | `127.0.0.1:5173` |

端口被占用时直接报错，不自动选择其他端口，避免代理目标错位。

后端监听地址从所选应用配置读取；开发启动入口使用同一地址设置 Vite 的 `/api` 代理，不另行维护一份后端地址。

发布形式与资源路径见[构建与发布产物](structure.md#构建与发布产物)。
