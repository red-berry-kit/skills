---
name: redberry-coding
description: Use when implementing or refactoring an agreed Red Berry change, integrating generated clients, or applying an authorized bug fix.
---

# 红莓编码

输入为已明确需求、方案和实施安排。缺少关键行为或任务映射时分别交 `redberry-requirements`、`redberry-design` 或 `redberry-planning` 补齐；局部变更可直接引用已有约定。流程由 `using-redberry` 组织。

## 执行

1. 确认源码归属与生成边界。新增或修改名称按[命名判据](references/conventions.md#命名判据)自查；公开名称的变更同步调用方、配置、生成来源与文档。以目标项目规则为准；涉及多个应用的路由、资源或交付时，落实[独立应用边界](references/conventions.md#独立应用边界)。按范围读取[开发约定](references/conventions.md)、[模块与依赖](references/modules.md)、[API 契约](references/api.md)或[前端开发](references/frontend.md)。选择或替换 UI 组件时，必须按[Mantine 与统一主题](references/frontend.md#ui-与样式)、[能力复用与 Hooks](references/frontend.md#能力复用与-hooks)、[组件选型](references/frontend.md#组件选型)及[按钮图标](references/frontend.md#按钮图标)落实适用专用组件；使用通用组件时须有可核验的不适配依据。新增或修改用户界面、用户可见的 API 消息及语言格式时，落实[国际化契约](references/i18n.md)及对应前后端规范。邻近风格与语言惯例优先，跨模块通过公开入口协作。
2. 先按[依赖原生模式优先](references/conventions.md#依赖原生模式优先)查当前版本推荐用法、完整示例与已有机制，确认接入模式后，按[行为过程与生命周期](references/conventions.md#行为过程与生命周期)推演从触发到收尾的行为链，再安排状态和更新顺序；原生方案缺口明确后才自行补充。新增表单、调整布局或向已有页面增加字段／操作时，编码前先按[表单整体设计](references/frontend.md#表单整体设计)完成任务设计与布局决定，再核对[组件选型](references/frontend.md#组件选型)；复用依据与本次任务匹配后实施，缺失部分先补齐。实施后核对实际接入与决定一致。按计划小步实现完整行为，保留验收对应。故障修复先确认失败判据，再修改根因；新行为按风险建立可观察的回归验证。共享逻辑修改追踪调用方，超出既定接口或状态方案时返回设计。涉及用户操作、失败处理或后端执行时，读取[错误反馈与诊断](references/diagnostics.md)，分别落实用户纠错反馈与开发诊断，按对应完成条件自查。
3. 可复用模块实现[默认装配](references/modules.md#添加即用的交付契约)，不向消费应用复制模块专属接线来掩盖生成能力缺失。生成产物的修复落在源码、生成输入或官方配置，再执行项目现有生成入口并核对差异。同步验证副本遵循项目机制，不把副本当源码修改。新增或调整数据库表时，读取[数据迁移的表与字段备注](references/migrations.md#表与字段备注)，补齐表、字段与关键约束的中文备注，并同步实际建表入口和 CLI 模板。新增或调整账户 ID、乐观锁或安全版本时，读取[业务资源标识](references/api.md#业务资源标识)，核对生成、数据库条件写及接口表示。迁移、配置与版本变化按项目规则处理。
4. 从实际脚本或工具帮助中选择命令，执行项目必需的格式、静态、编译及独立类型检查，运行本次行为与边界的相关测试。构建与测试不能替代独立类型检查；已有有效证据可复用。
5. 记录改动、实际检查结果、失败和未执行项，核对需求未被实现细节缩小。修改受影响文档的最终规则；实验与过程证据留在已有过程资料区。

## 出口与交接

实现与生成产物一致、局部检查已有证据后，更新任务记录，按 `redberry-verification` 选择验收方式：小改动由当前 agent 完成针对性验证和复查；需要独立验收时交接源码与原始证据，再交审查，不替验收者预填结论。编码完成不等于整体任务完成。遇到失败进入 `redberry-debugging`，修复后回到原验收条件；来自验收或审查的问题按 `using-redberry` 闭环处理。必需检查受阻时明确阻断并继续独立工作。

低风险文案或等价局部修改核对实际差异及适当现有检查，无需新增镜像实现的测试。只交付计划、代码草案或未执行的验证安排时，按实际状态说明，不报告为已运行通过。
