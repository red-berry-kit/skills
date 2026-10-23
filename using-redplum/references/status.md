# 规范与实现归属

本仓库维护十个 Red Plum Skills、配套技术规范及流程行为测试。`docs/` 是规范唯一源；七个需要参考资料的 Skill 通过同步脚本获得 `references/` 副本，需求、计划、验收三个 Skill 自包含。Skills 由开发者独立安装与更新，CLI 不管理。

## 工程边界

- `red-plum-kit/skills`：阶段入口、交接与验收闭环、随包技术规范。
- `red-plum-kit/cli`：CLI、应用及模块模板、工作区与生成装配、工程任务编排。
- `go-admin-template`：公共运行时 `app`、`config`、`migrate` 与运行库自身检查。
- 消费项目：业务、配置、模块接入、部署和实际验收证据。

规范描述约定，不代表所有旧版本已经具备这些能力。执行任务前核对目标项目实际源码、CLI／模板版本及任务入口；模块默认装配的缺口按[模块交付契约](modules.md#添加即用的交付契约)处理。

## 检查与证据

Skills 仓库使用 `python3 scripts/check-skills.py` 检查元数据、名称引用与包内链接，使用 `python3 scripts/sync-references.py --check` 检查规范副本；变更规范后先执行不带 `--check` 的同步命令。行为场景与报告在 `tests/workflow/`，静态检查不能证明流程行为或业务模块可用。

其他工程的 `check/test/build` 等任务以各自 AGENTS、脚本或实际工具帮助为准，不把运行库的 Taskfile 当成 Skills 仓库入口。软件交付是否完成，以对应当前源码、环境和完整判据、与变更风险匹配的验证及审查证据为准；实验、模拟和已有示例不能代替实际安装验收。远程 CI、正式版本发布和目标部署没有执行时必须保留缺项。
