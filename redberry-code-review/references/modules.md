# 模块与依赖

用户业务与基础功能都作为独立模块维护。`redberry create mod` 使用模块模板创建完整的前后端基础文件；配置定义与迁移按需添加。自有源码放项目内的模块目录，外部源码由 CLI 管理于 `.redberry/modules/`。

## 公开入口

| 部分 | 文件 | 导出约定 |
| --- | --- | --- |
| 后端 | `backend/redberry_module.go` | 导出 `Module`，统一提供 Fx 装配 |
| 配置检查 | `backend/redberry_check.go` | 按需导出 `CheckModule`，仅提供纯声明和检查 |
| 迁移扩展 | `backend/redberry_migration.go` | 按需导出 `MigrationModule`，提供独立迁移所需连接或扩展 |
| 前端 | `frontend/index.ts` | 使用具名导出，公开允许外部使用的内容 |

CLI 同时识别旧的 `module.go`、`config.go`、`migration.go`、`check.go` 入口；同类新旧入口同时存在时拒绝生成，须保留一个。新模块采用 `redberry_` 前缀。

跨模块调用通过后端的 `backend` 包或前端的 `frontend/index.ts`，不直接引用内部实现。Go 的包导出规则仍然适用；`redberry_module.go` 是装配入口文件，不意味着 Go 可以限制其他包只访问这一文件。

描述文件不重复声明入口。CLI 根据约定路径生成装配代码。

跨模块引用包含类型引用，模块内部可引用自身实现。私有子目录的 `index.ts` 不自动获得模块级入口地位；提供方不能通过公开入口转出其他模块的私有实现。

边界检查按真实文件归属判断，覆盖相对路径、tsconfig 别名、软链接与再导出。动态导入使用固定字面量。模块根由依赖管理器持有的模块图提供，业务不另维护边界清单。

## 添加即用的交付契约

可复用模块必须在干净应用中通过 CLI 添加并填写必要配置后，直接使用其默认能力。必要配置包括外部地址、部署秘密和明确的业务策略；不包括让使用者复制示例中的 API 映射、Provider、路由注册或基础设施接线。

设计时分清模块默认装配、应用配置和可选扩展。模块通过公开入口声明默认装配；生成器连接应用能力，模块不得反向引用应用私有文件或其生成目录。扩展接口不能成为默认路径必须手写的步骤。缺少通用装配能力时，修复生成器／模板的契约，不在每个消费应用重复补胶水代码。

验收至少有一条独立消费链：新建应用 → 真实 CLI 添加模块 → 必要配置 → 启动 → 模块核心操作；检查生成客户端、路由、配置、迁移及适用的卸载／恢复行为。记录所有人工改动，出现模块专属接线即判定默认接入未完成。已有 examples 的业务测试只能补充这条证据。未发布模块可使用 CLI 支持的本地来源或隔离的版本仓库夹具，注明所覆盖的安装路径，不能以复制源码或手改生成产物替代安装。

前端模块可在 `frontend/index.ts` 具名导出 `createProvider(context)`，返回 Provider 组件。CLI 生成 `.redberry/frontend/providers.tsx`，按依赖在外、消费方在内组合；应用入口在 render 外调用 `createModuleProviders(queryClient)`，在 UI 与 Query Provider 内统一挂载返回的 `ModuleProviders`。上下文提供生成 `api`、有限 `ui`、应用 `scope` 、`queryClient` 和可卸载请求扩展 `http`；模块用最小结构类型声明所需能力，生成调用负责静态兼容检查。无工厂的模块直接透传 children。工厂只定义组件，不获取资源；组件挂载／卸载管理资源，不在 render 中创建订阅或会话。应用主题可通过有限 UI 入口定制，旧应用升级需一次接入通用容器，不为每个模块增加专属装配。

前端页面在路由 `staticData` 中声明 `layout`（省略时为 `workspace`，全屏需显式设为 `fullscreen`）及可选 `menu`（必填标题 `title`、可选顺序 `order`，省略顺序为 0，同序沿用路由装配顺序）。模块模板为普通页面生成菜单声明；未声明 `menu` 的页面不进入菜单，全屏页面也不进入工作台菜单。登录等全屏页不嵌套工作台。布局、菜单可见性与访问控制分别设计和验收，不把全屏或隐藏菜单当成权限声明。

模块专有 npm 依赖自行声明可解析的版本；只有平台已经提供的共同依赖才引用统一 catalog，不要求每个消费应用补模块私有 catalog 条目。

## 装配与生命周期

使用 Uber Fx 组合模块，通过构造函数参数表达依赖。容器操作集中在 `backend/redberry_module.go` 与项目装配层，业务代码通过显式参数获取依赖。

统一检查入口执行 `fx.ValidateApp`，在不执行构造器的情况下检查依赖缺失、重复提供与循环依赖。图检查使用类型化提供者，不要求加载部署配置；它属于检查阶段的图验证，不是 Go 编译期验证。

构造阶段只创建对象和注册生命周期。数据库连接、端口监听等资源在 `OnStart` 获取，通过 `OnStop` 逆序释放；某个启动步骤失败时，该步骤负责清理自身获取的资源，Fx 回退已成功启动的步骤。构造器业务错误与实际启动行为通过测试验证。

持续后台任务及其专用资源通过 `app.ProvideBackground` 声明，宿主仅在 `serve` 构造并管理其生命周期；维护命令、迁移、检查与导出不构造后台服务。多个后台服务的启动次序不固定，有次序依赖的工作由同一服务组织。共享连接等命令所需资源继续使用普通 Fx 生命周期。

跨模块配置检查在 `backend/redberry_check.go` 的 `CheckModule` 初始化表达式中直接注册 `app.ProvideConfigCheck`，或经 `fx.Options` 组合；检查及依赖不得获取运行资源。CLI 自动生成检查装配并拒绝未接入 `CheckModule` 的直接注册。数据库扩展同时在 `CheckModule` 中声明所需纯驱动信息，独立迁移所需连接或扩展在 `backend/redberry_migration.go` 的 `MigrationModule` 中声明。CLI 收集所有声明及其依赖闭包，不按模块 ID 特判；依赖有 `MigrationModule` 时使用该入口，否则使用普通 `Module`。因此普通入口含不应在迁移时启动的服务时，模块须提供精简迁移入口。`migrations/` 保存迁移脚本，`backend/redberry_migration.go` 负责运行所需装配。存在脚本但没有数据库连接时，检查和迁移失败；升级 CLI 的现有应用须升级数据库模块以提供迁移入口，并重新生成装配。

## 模块描述

`redberry.yaml` 只负责模块 ID、版本、依赖和替代声明。入口及迁移资源按约定路径发现，不增加对应配置字段。依赖字段使用 `deps`，替代声明使用 `replaces`。

身份字段写法：

```yaml
id: github.com/redberry/user
version: 1.2.0
```

- `id` 是模块唯一标识，采用 Go 模块路径风格；包含 Go 代码时，与模块根目录 `go.mod` 的 module 路径一致。
- `version` 使用 SemVer，YAML 中统一不带 `v`，对应 Git 标签使用 `v1.2.0`；新模块模板初始版本为 `0.1.0`。
- 纯前端模块使用相同格式的 ID，不需要为了标识创建 `go.mod`。
- 项目内自有模块的 ID 由项目根 `go.mod` 的 module 路径和项目根下的相对目录组成，ID 后缀与项目内目录保持一致；模块目录不要求位于 `modules/` 下，但不能占用工程目录与隐藏目录。例如根路径为 `github.com/acme/shop`、目录为 `modules/order/` 时 ID 为 `github.com/acme/shop/modules/order`，目录为 `order/` 时 ID 为 `github.com/acme/shop/order`。

### 模块依赖

```yaml
id: github.com/redberry/rbac
version: 1.0.0

deps:
  github.com/redberry/user: ^1.2.0
```

`deps` 按“模块 ID → 版本约束”声明 Red Berry 模块依赖，支持精确版本与标准 `^` 写法，版本统一不带 `v`。`^1.2.0` 表示 `>=1.2.0 <2.0.0`；零主版本按兼容范围收窄，`^0.2.3` 表示 `>=0.2.3 <0.3.0`，`^0.0.3` 表示 `>=0.0.3 <0.0.4`。Go 依赖由各自模块根层的 `go.mod` 管理，前端包依赖由 `frontend/package.json` 管理，不重复放入 `deps`。

锁文件固定实际选中的实现及源码提交，以便重现解析结果。

### 替代声明

```yaml
id: github.com/acme/user
version: 2.0.0

replaces:
  github.com/redberry/user: 1
```

`replaces` 按“目标模块 ID → 大版本”声明替代关系，不填写目标的次版本、补丁版本或 `^` 范围。上例声明可以替代目标模块的 `1.x` 版本线；替代模块自身版本独立维护，不要求与目标版本一致。

消费方继续通过 `deps` 声明原目标及其版本约束，不改写成替代实现的 ID。替代维护者负责遵守该目标大版本的约定。

### 实现唯一性

同一目标模块在项目中只允许一个实现，不支持原模块与替代模块共存，也不支持同一目标的多版本或多个替代实现共存。

项目选择替代模块后，所有依赖统一使用该实现。依赖约束无法同时满足时直接报冲突，不通过隔离或并存解决。锁文件保存最终选择。

### 项目选择替代实现

项目直接在 `deps` 中引入替代模块，不增加单独的实现选择字段：

```yaml
deps:
  github.com/redberry/rbac: ^1.0.0
  github.com/acme/user: ^2.0.0
```

如果 `github.com/acme/user` 声明 `replaces: {github.com/redberry/user: 1}`，解析器就用该实现满足 RBAC 对原用户模块的大版本 1 的依赖，不再安装原实现。替代模块自身版本通过其 `deps` 约束选择；替代目标按 `replaces` 中的大版本匹配。

发现多个候选实现则报冲突，不按声明顺序或版本高低自动挑选。锁文件记录最终解析结果。

## 源码与版本锁定

依赖源码与生成目录由 Git 忽略；项目提交依赖清单和锁文件。锁文件固定实际选中的实现、版本与源码提交，CLI 维护安装结果、工作区和装配输入。

有锁按锁恢复，无锁解析并生成；`--locked` 拒绝缺锁或与清单不一致，不等同于离线。添加、安装、移除、升级和状态查询的完整行为见[CLI 约定](cli.md#依赖维护redberry)。

外部依赖目录不保存业务自定义；需要特殊行为时通过模块公开扩展接口，或选择声明替代关系的独立实现。

## 配置与迁移归属

模块在 `backend/redberry_config.go` 定义配置类型，使用统一加载入口。替代模块沿用目标的组织、配置组名和配置契约，新增专属配置也放同组，见[模块配置](config.md#模块配置)。

迁移放模块根 `migrations/`。替代实现按自身模块 ID 记录迁移，不继承或映射原模块历史；原模块遗留数据与记录不自动清理，见[数据迁移](migrations.md)。

模块可具名导出 `RouteGuard`，CLI 生成 `ModuleRouteBoundary` 并在 Router 内的模板根统一组合，Provider 仍在 Router 外；门禁不阻止 RouterProvider 自身挂载。生成客户端通过受管理的通用 HTTP mutator 支持模块请求中间件，模块在 effect 中注册并卸载，不覆盖全局 fetch。认证模块可默认保护所有业务并通过配置声明匿名页面/API；页面与API例外相互独立，前端跳转不能代替后端权限边界。运行库通过通用HTTP中间件组支持模块默认策略，不由CLI特判模块ID。
