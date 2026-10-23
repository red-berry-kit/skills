# i18n 规范独立验收

结论：本轮规范验收通过，未发现必修问题。验收者 `/root/skills_i18n_full_acceptance`，干净独立上下文，未参与实施、不递归派发，未读取前轮结论。范围为当前 Skills 规范；没有执行真实应用 i18n、浏览器、HTTP 并发或 CLI 安装测试，也不据此声称应用已实现国际化。

环境：Linux/bash、Python 3；工作目录 `/home/mapleafgo/Projects/OpenProject/red-plum-kit/skills`。使用 `using-redplum`、`redplum-verification`、`writing-for-agents`（含 Skill mechanics）核对流程、证据与渐进披露。保留原工作区改动，仅新增本报告，不提交发布。

| 验收条件 | 实际入口与核对方式 | 结果与证据 |
| --- | --- | --- |
| 流程可发现且可执行 | 入口 → conventions 前后端触发 → i18n → frontend/api；requirements、design、coding、verification、code-review 分别检查要求、职责、落地与覆盖 | 通过；各阶段存在具体动作及出口，references 与源文档一致 |
| 前后端分工及稳定错误语义 | docs/i18n.md 职责与装配；docs/api.md 错误响应国际化 | 通过；每条消息约定一层翻译，业务错误语言无关，HTTP 状态/身份/位置稳定，原生 ErrorModel 与 OpenAPI 兼容；未知错误安全回退 |
| 自动校验与内部错误 | docs/api.md 错误响应国际化 | 通过；明确涵盖自动请求校验及 title/detail/errors[].message，敏感诊断不进入用户消息 |
| 隔离与回退 | docs/i18n.md 验收；docs/api.md 错误响应国际化 | 通过；支持/无效/不支持/默认语言、请求级 locale、并发隔离及缓存语言变体均有要求 |
| 模块添加即用 | docs/i18n.md 职责与装配及验收；docs/modules.md 添加即用；阶段入口 | 通过；命名空间资源随包、公开契约与 CLI 自动装配，不要求消费者写模块接线，真实干净应用验收仍是应用实施时必需项 |
| Mantine 原生外观及状态/格式 | docs/frontend.md 国际化；docs/i18n.md 验收 | 通过；公开 locale/label 接口保持原生样式，时区独立，API 格式不变；菜单、既有错误、标题更新并保留会话/表单；覆盖长文案和可访问名称 |
| 范围约束与库接口 | 逐段静态核对当前 i18n 新规则 | 通过；复用既有语言/库，无固定新增语言或框架；未引入臆造翻译库接口，资源契约留给项目设计 |

## 最小规范场景推演

以下是文本路径推演，未执行应用代码。

1. **已有语言体系的登录页 + 后端 422**：requirements 复用语言范围及翻译分工 → design 读取统一契约，覆盖全屏页/模块资源及错误映射 → coding 复用项目翻译库；覆盖自动 422 的概要与字段消息，保持状态、身份、位置 → verification 检查登录文案、已有字段错误切换、会话及表单保留、控件原生外观和 CLI 装配 → code-review 核对遗漏。该路径不要求新增库或重复翻译。
2. **无 i18n 约定的单语言 API 模块错误**：requirements 先明确该单语言、默认/回退和后端消息分工；尚未确认时记决策缺口，不擅定双语。design 保持普通 Go 错误及原生问题响应，coding 覆盖业务/自动校验/未知错误安全消息，verification 按确认的单语言核对一致性及干净应用添加链路。纯后端场景不强加 UI；缺少约定时验收返回需求，不能默认通过。
3. **服务端按请求翻译、并发不同语言**：design 明确请求语言来源、响应标识、支持/默认/回退和缓存变体 → coding 采用请求级语言状态 → verification 安排并发不同支持语言及无效/不支持/缺省请求，比较消息语言、错误身份、HTTP 状态、字段位置、业务结果。契约可导出隔离及回退的可观察断言，不允许全局 locale 混串。

## 实际命令与限制

- `python3 scripts/check-skills.py`：退出码 0；`检查 10 个 Skills，0 个问题`。
- `python3 scripts/sync-references.py --check`：退出码 0；`发现漂移：0 个文件`。
- 上述只证明元数据、包内链接/锚点、名称引用及副本同步；不证明应用 i18n 行为。
- 未复用历史验收证据；应用 i18n 属于另行实施范围，真实前后端链路、CLI 添加和并发测试在本次规范任务中不适用。

## 固定源码基准

以下为本轮审查文件 SHA-256；正文和五类专题的全部 references 副本，以及执行脚本均纳入，报告本身除外。规范在验收期间由主 agent 冻结；清单同时覆盖未跟踪源文件，不依赖 Git 提交内容。

```text
0628acd986bd5d43c3455efde282b6602d22e43664ac4692886b282c327d11a1  docs/api.md
1736cb064f9ebbc7690b573ef8cef7efbe79ecae5e373da15b48b24341fc98d5  docs/conventions.md
355c69408f5d98189fc5772fb699f790f050d61fbeab459629e9b844cf1d8e6d  docs/frontend.md
592e0bb3551a76b850abeb50b8b654139650d705c54f2f622ed892499e95bc6b  docs/i18n.md
160465af16a62f931ee7350783be14acd43eaba1ebd8db056714ac5341bb19e5  docs/modules.md
ce351ec1fb9816730b4a657466f4ea30342ba46ae813e26eb45a66ce26e05d59  redplum-code-review/SKILL.md
0628acd986bd5d43c3455efde282b6602d22e43664ac4692886b282c327d11a1  redplum-code-review/references/api.md
1736cb064f9ebbc7690b573ef8cef7efbe79ecae5e373da15b48b24341fc98d5  redplum-code-review/references/conventions.md
355c69408f5d98189fc5772fb699f790f050d61fbeab459629e9b844cf1d8e6d  redplum-code-review/references/frontend.md
592e0bb3551a76b850abeb50b8b654139650d705c54f2f622ed892499e95bc6b  redplum-code-review/references/i18n.md
160465af16a62f931ee7350783be14acd43eaba1ebd8db056714ac5341bb19e5  redplum-code-review/references/modules.md
a1ce578f20142ee93f7ccff3809bdbd2b51922ecd8242b3d80d903293b3fb3dd  redplum-coding/SKILL.md
0628acd986bd5d43c3455efde282b6602d22e43664ac4692886b282c327d11a1  redplum-coding/references/api.md
1736cb064f9ebbc7690b573ef8cef7efbe79ecae5e373da15b48b24341fc98d5  redplum-coding/references/conventions.md
355c69408f5d98189fc5772fb699f790f050d61fbeab459629e9b844cf1d8e6d  redplum-coding/references/frontend.md
592e0bb3551a76b850abeb50b8b654139650d705c54f2f622ed892499e95bc6b  redplum-coding/references/i18n.md
160465af16a62f931ee7350783be14acd43eaba1ebd8db056714ac5341bb19e5  redplum-coding/references/modules.md
0628acd986bd5d43c3455efde282b6602d22e43664ac4692886b282c327d11a1  redplum-debugging/references/api.md
1736cb064f9ebbc7690b573ef8cef7efbe79ecae5e373da15b48b24341fc98d5  redplum-debugging/references/conventions.md
355c69408f5d98189fc5772fb699f790f050d61fbeab459629e9b844cf1d8e6d  redplum-debugging/references/frontend.md
592e0bb3551a76b850abeb50b8b654139650d705c54f2f622ed892499e95bc6b  redplum-debugging/references/i18n.md
160465af16a62f931ee7350783be14acd43eaba1ebd8db056714ac5341bb19e5  redplum-debugging/references/modules.md
8b9d2edc80f5a299d022bd5cdf1f7302696488613f8beb179b256e45e1a68502  redplum-design/SKILL.md
0628acd986bd5d43c3455efde282b6602d22e43664ac4692886b282c327d11a1  redplum-design/references/api.md
1736cb064f9ebbc7690b573ef8cef7efbe79ecae5e373da15b48b24341fc98d5  redplum-design/references/conventions.md
355c69408f5d98189fc5772fb699f790f050d61fbeab459629e9b844cf1d8e6d  redplum-design/references/frontend.md
592e0bb3551a76b850abeb50b8b654139650d705c54f2f622ed892499e95bc6b  redplum-design/references/i18n.md
160465af16a62f931ee7350783be14acd43eaba1ebd8db056714ac5341bb19e5  redplum-design/references/modules.md
0628acd986bd5d43c3455efde282b6602d22e43664ac4692886b282c327d11a1  redplum-proof-of-concept/references/api.md
1736cb064f9ebbc7690b573ef8cef7efbe79ecae5e373da15b48b24341fc98d5  redplum-proof-of-concept/references/conventions.md
355c69408f5d98189fc5772fb699f790f050d61fbeab459629e9b844cf1d8e6d  redplum-proof-of-concept/references/frontend.md
592e0bb3551a76b850abeb50b8b654139650d705c54f2f622ed892499e95bc6b  redplum-proof-of-concept/references/i18n.md
160465af16a62f931ee7350783be14acd43eaba1ebd8db056714ac5341bb19e5  redplum-proof-of-concept/references/modules.md
df14ffe758938a5349a679c08be1bfa6695bdfcb68b048ca4db93fba9a8aa719  redplum-requirements/SKILL.md
0628acd986bd5d43c3455efde282b6602d22e43664ac4692886b282c327d11a1  redplum-research/references/api.md
1736cb064f9ebbc7690b573ef8cef7efbe79ecae5e373da15b48b24341fc98d5  redplum-research/references/conventions.md
355c69408f5d98189fc5772fb699f790f050d61fbeab459629e9b844cf1d8e6d  redplum-research/references/frontend.md
592e0bb3551a76b850abeb50b8b654139650d705c54f2f622ed892499e95bc6b  redplum-research/references/i18n.md
160465af16a62f931ee7350783be14acd43eaba1ebd8db056714ac5341bb19e5  redplum-research/references/modules.md
c2819fb532a6d38279b3413c221920bc8cdab27d58f1c1e064b9a000582dfa86  redplum-verification/SKILL.md
e8a6a71b3f924e86450abcc56fe2a37130bb9b5420e9ee1b06f07782fdee1337  scripts/check-skills.py
d1c0019befa1a6e33c6d99d4263bee8f1bf9f855c674862fe9f2d2c24f706928  scripts/sync-references.py
a542d0864efe30c993cc4e0235c71507c65964183dae7f719f15a28fd7a552d3  using-redplum/SKILL.md
0628acd986bd5d43c3455efde282b6602d22e43664ac4692886b282c327d11a1  using-redplum/references/api.md
1736cb064f9ebbc7690b573ef8cef7efbe79ecae5e373da15b48b24341fc98d5  using-redplum/references/conventions.md
355c69408f5d98189fc5772fb699f790f050d61fbeab459629e9b844cf1d8e6d  using-redplum/references/frontend.md
592e0bb3551a76b850abeb50b8b654139650d705c54f2f622ed892499e95bc6b  using-redplum/references/i18n.md
160465af16a62f931ee7350783be14acd43eaba1ebd8db056714ac5341bb19e5  using-redplum/references/modules.md
```
