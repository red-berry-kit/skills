# Red Berry Skills

统一入口：[using-redberry](using-redberry/SKILL.md)。它负责选择阶段、恢复任务与组织交付；各专业 Skill 定义阶段的输入、执行、出口和下一步。阶段路径与发现问题后的修复循环只在入口维护；验收方式的选择、独立验收者的创建与复用、交接材料和证据规则由 [redberry-verification](redberry-verification/SKILL.md) 定义。

## 在项目中使用

将需要的 Skill 目录安装到客户端支持的位置。建议安装整套，以便入口串联各阶段；也可单独使用某个专业 Skill。每个包内的相对资料链接可以独立解析；专业 Skill 的名称引用表示阶段交接，不代表下游已经安装或执行。

项目 `AGENTS.md` 保留以下入口即可，其余位置继续维护项目特有规则：

> Red Berry 的需求、调研、设计、实现、排障、验收与审查使用已安装的 `using-redberry`；按入口实际读取所需专业 Skill，并维护当前阶段、产出、证据与下一步。复用已有授权及有效结论。

安装方式依客户端而定，安装后核对实际文件路径与发现结果；源码更新不保证当前会话重新加载目录。Skills 由开发者安装和更新，Red Berry CLI 不管理 Skills。

## 维护

- `<skill-name>/SKILL.md`：流程源文件。`description` 用英文描述触发条件，正文中文。
- `docs/`：随包技术规范的唯一维护源，自独立仓库已有规范快照迁入。项目本身的规则优先；不要再用旧模板仓库的打包脚本覆盖本仓库。
- `<skill-name>/references/`：规范副本。带此目录的 Skill 通过同步脚本获得独立安装所需资料；`SKILL.md` 按任务触发条件引用包内资料，自包含 Skill 按自身说明使用。
- `tests/workflow/`：行为验收场景和本次验证结果；不作为项目开发时的必读文件。

规范变更后，在本仓库执行：

```bash
python3 scripts/sync-references.py
python3 scripts/sync-references.py --check
python3 scripts/check-skills.py
```

流程变更应先看实际失败或对照行为，再按风险选择静态检查、场景推演或独立执行；局部规则调整无需默认展开多 agent 对照实验。静态检查验证元数据、名称引用及包内 Markdown 链接；它不证明执行者会持续遵守流程。每次测试区分推演、真实执行及未验证内容，记录实际限制。
