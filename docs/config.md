# 配置

公共配置、多环境覆盖和模块配置统一加载、校验后注入。

配置位于项目根 `config/`，文件命名为 `app.toml` 或 `app.<环境>.toml`，例如 `app.dev.toml`、`app.test.toml`、`app.prod.toml`。环境通过二级后缀识别。

- 始终读取 `config/app.toml` 作为公共配置。
- 指定环境时，再读取 `config/app.<环境>.toml`；同名字段覆盖公共配置，未提供的字段保留公共值。
- 未指定环境时只读公共配置，不额外加载环境文件。
- 公共文件或指定环境的文件缺失均报错，不静默跳过或改用其他环境。
- 所有配置通过统一加载入口读取；环境配置只需声明相对公共配置的差异。

## 任务默认环境

- `pnpm dev` 默认环境 `dev`，读取公共配置与 `app.dev.toml`。
- 构建不选择应用运行环境，不设置默认环境，不读取、复制或嵌入应用运行配置文件；`--mode` 只控制单二进制或分离形式。
- 启动服务时未指定环境则只读取公共配置；直接运行根命令只显示帮助，不加载应用配置。
- 应用运行时从外部加载配置，运行环境在启动时确定，与构建产物独立。

配置 schema 是生成产物，位于 `.redberry/config/app.schema.json`，编辑提示和配置检查使用同一份约束。

运行子命令共用 `--env` / `-e`、`--config` / `-c`，其中 `--config` 指配置目录。参数和调用示例见[CLI 约定](cli.md#业务项目可执行文件)。

## 配置处理顺序

统一流程：确定环境 → 加载并合并公共与指定环境配置 → 按 Schema 补齐缺省值 → 校验结构 → 严格解码 → 校验语义 → 注入模块。模块默认值作为最低优先级，不覆盖显式提供的值。

字段优先级由低到高为：模块默认值 < 公共配置 < 指定环境配置。显式提供的 `false`、`0` 和空字符串也覆盖低优先级的值；未提供的字段保留低优先级值。校验在最终合并后执行。

必填项缺失、枚举不合法或出现未知配置项时，启动直接报错，并指出完整配置路径，例如 `redberry.user.allow_signup`。校验通过后才向模块注入配置。

## 配置生效时机

首版只在应用启动时加载配置，经过默认值处理和校验后注入模块。应用生命周期内配置保持稳定；修改配置文件后需要重启应用才会生效，不提供配置热更新。

## 模块配置

项目配置按“组织名 → 模块短名”分组，组织名取模块 ID 中域名后的组织部分，例如：

```toml
[redberry.user]
allow_signup = false

[redberry.rbac]
default_role = "member"
```

模块在 `backend/config.go` 中定义自身的配置类型、默认值和约束；没有配置项的模块无需创建该文件。项目根据已安装模块生成统一 schema，提供字段、枚举及说明，模块不各自加载配置文件。

Schema、时长与语义校验遵循下文[Schema 与校验](#schema-与校验)。

配置组名冲突直接报错，不自动改名，不引入额外别名配置。组织名与模块短名用于配置分组，不改变完整模块 ID 的唯一标识职责。

替代模块沿用目标模块的组织名、配置组名和配置契约。例如替代 `github.com/redberry/user` 后仍使用 `[redberry.user]`，不会因替代实现的组织或自身名称改变配置组名。替代实现新增的专属配置也放在该组内。统一 schema 根据实际选中的实现生成，不要求原模块与替代模块同时参与装配。

## Schema 与校验

Huma 从模块 `backend/config.go` 中的 Go 类型、默认值与约束生成统一配置 Schema，输出到 `.redberry/config/app.schema.json`。编辑器提示与运行配置结构校验共用这份 Schema。

普通字段使用 Huma 原生的 `default`、`enum`、`minimum` 等标签。配置使用独立的 Huma Registry，将 `time.Duration` 映射为字符串；时长默认值通过官方 `SchemaTransformer` 设置。业务字段保留原生 `time.Duration`，TOML 使用 `5s`、`1m30s` 等 Go 时长写法。

Huma 校验配置数据的结构与约束；将配置 map 解码为 Go 结构体由 Koanf 的 `UnmarshalWithConf` 承担，底层使用 `go-viper/mapstructure/v2`。配置加载实现直接引用其 `DecoderConfig` 和官方 hook，以关闭弱类型转换并解析 `time.Duration`，因此需要显式声明依赖；业务模块不自行调用解码器。

统一加载器使用 Koanf 合并配置，按 Schema 填充缺省值并校验结构；默认值处理覆盖嵌套对象、数组与映射中的对象，保留显式零值。默认值填充由配置适配层负责。随后通过 mapstructure 的官方时长解码 hook 严格解码，关闭弱类型转换，再执行模块的 Go 语义校验，全部通过后才注入。

Schema 提供类型、枚举、默认值、说明与结构约束提示；Go 时长语法及跨字段业务关系由应用配置检查验证。Go 时长不使用 JSON Schema 的 ISO duration 格式。配置 Registry 与 HTTP 接口 Registry 相互独立。

HTTP 与配置统一使用 Huma 校验体系。优先通过 Schema 表达类型、枚举、范围及可表达的组合约束；跨字段大小关系、业务条件等使用共享的 Go 语义函数，返回 Huma 的结构化 `ErrorDetail`。

HTTP 通过 `ResolverWithPath` 调用语义函数，配置入口在结构校验与严格解码后显式调用同一函数。独立的 `ModelValidator` 只执行 Schema 校验，不承担 Resolver 调用。配置语义函数不依赖 HTTP 请求上下文；可变的 `ModelValidator` 实例不在并发调用间共享。

错误位置由 `PathBuffer` 组合，HTTP 使用请求位置前缀，配置使用模块分组前缀；叶字段按 JSON 字段名显式指定，如 `prefix.With("min")`。这类字符串路径由生成、配置与接口测试核对，不属于 Go 编译期字段绑定。
