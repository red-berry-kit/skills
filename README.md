# Red Berry Skills

统一入口：[using-redberry](using-redberry/SKILL.md)。它负责选择阶段、恢复任务与组织交付；各专业 Skill 定义阶段的输入、执行、出口和下一步。阶段路径与发现问题后的修复循环只在入口维护；验收方式的选择、独立验收者的创建与复用、交接材料和证据规则由 [redberry-verification](redberry-verification/SKILL.md) 定义。

## 在项目中使用

将需要的 Skill 目录安装到客户端支持的位置。建议安装整套，以便入口串联各阶段；也可单独使用某个专业 Skill。Skill 不再携带规范副本，规范通过 `standards/` 的远程地址按需读取，离线环境需预先镜像 `standards/`；专业 Skill 的名称引用表示阶段交接，不代表下游已经安装或执行。

项目 `AGENTS.md` 保留以下入口即可，其余位置继续维护项目特有规则：

> Red Berry 的需求、调研、设计、实现、排障、验收与审查使用已安装的 `using-redberry`；按入口实际读取所需专业 Skill，并维护当前阶段、产出、证据与下一步。复用已有授权及有效结论。

通用 Skill 维护任务流程，`standards/` 维护通用开发原则；具体模块的使用说明由模块随代码维护，不在本仓库另设转述或跳转文件。

编写或修订模块 `README.LLMS.md` 时使用 [redberry-writing-readme-llms](redberry-writing-readme-llms/SKILL.md)：正文维护使用约定，公共入口附短注及代码链接，详细接法留在代码注释中。

安装方式依客户端而定，安装后核对实际文件路径与发现结果；源码更新不保证当前会话重新加载目录。Skills 由开发者安装和更新，Red Berry CLI 不管理 Skills。

## 维护

- `standards/`：通用开发原则与跨技术开发要求的维护源；不维护模块 API、CLI 参数、生成目录清单或运行库实现细节。涉及多个模块的具体用法仍由实现方维护。
- `<skill-name>/SKILL.md`：流程源文件。`description` 用英文描述触发条件，正文中文；规范通过 `standards/` 的远程地址按需读取，不随 Skill 复制。
- `tests/workflow/`：行为验收场景和本次验证结果；不作为项目开发时的必读文件。

规范变更后，在本仓库执行：

```bash
python3 scripts/check-skills.py
```

流程变更应先看实际失败或对照行为，再按风险选择静态检查、场景推演或独立执行；局部规则调整无需默认展开多 agent 对照实验。静态检查覆盖元数据、Skill 名称引用、`SKILL.md`／`standards/`／README 的包内链接与锚点，以及指向本仓库 `standards/` 远程地址的文件与锚点；它不证明执行者会持续遵守流程。每次测试区分推演、真实执行及未验证内容，记录实际限制。

本 Skills 目录的使用说明由本 README 及各 Skill 的 `SKILL.md` 提供。
