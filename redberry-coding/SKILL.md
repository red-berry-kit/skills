---
name: redberry-coding
description: Use when implementing or refactoring an agreed Red Berry change, integrating generated clients, or applying an authorized bug fix.
---

# 红莓编码

按已明确需求、方案和实施安排编码。缺少关键行为或任务映射时分别交 `redberry-requirements`、`redberry-design` 或 `redberry-planning` 补齐；局部变更可直接引用已有约定。

## 执行

1. 以目标项目规则为准，按[设计与架构](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/design.md)核对源码归属、公开入口、装配与校验边界；实现方法按[开发约定](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md)执行。
   - 命名按[命名判据](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#命名判据)自查；公开名称变更同步调用方、配置、生成来源与文档。
   - 多个应用的路由、资源或交付按[独立应用边界](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/design.md#独立应用边界)装配。
   - 使用或调整模块能力时，读取实际安装版本的 `README.LLMS.md`，执行全部适用使用契约；按已确认的设计与选型实施，核对实际接入与决定一致。
   - 用户界面、用户可见 API 消息及语言格式按[国际化契约](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/i18n.md)落实前后端规范。
   - 邻近风格与语言惯例优先，跨模块只通过公开入口协作。
2. 按依赖现有能力实现：
   - 按[依赖现有能力优先](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#依赖现有能力优先)查当前版本推荐用法、完整示例与已有机制，确认接入模式后再安排实现；依赖提供的方案缺口明确后才自行补充。
   - 按[行为过程与生命周期](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/conventions.md#行为过程与生命周期)推演触发到收尾的行为链，再安排状态与更新顺序。
   - 按计划小步实现完整行为，保留验收对应；实施后核对接入与决定一致。
   - 故障修复先确认失败判据再改根因；新行为按风险建立可观察的回归验证。
   - 共享逻辑改动追踪调用方；超出既定接口或状态方案时返回设计。
   - 用户操作、失败处理或后端执行按[错误反馈与诊断](https://raw.githubusercontent.com/red-berry-kit/skills/main/standards/diagnostics.md)分别落实纠错反馈与开发诊断，按对应完成条件自查。
3. 按模块契约实现默认装配：
   - 模块专属接线留在模块内，由生成装配提供；消费应用不复制它来弥补生成能力缺失。
   - 生成产物的问题改在源码、生成输入或官方配置，再从项目现有生成入口重跑并核对差异。
   - 同步验证副本按项目机制处理，只作查阅。
   - 接口、迁移、配置与版本变化同步所属模块说明、调用方及相关测试。
4. 从目标项目的依赖声明、锁文件、实际脚本及工具帮助核对工具、版本和命令，执行项目必需检查：
   - 格式、静态、编译与独立类型检查；构建和测试不能替代独立类型检查。
   - 本次行为与边界的相关测试。
   - 已有有效证据可复用。
5. 记录改动、实际检查结果、失败与未执行项，核对需求未被实现细节缩小：
   - 受影响文档写最终规则。
   - 实验与过程证据留在已有过程资料区。

## 出口与交接

实现与生成产物一致、局部检查已有证据后：

- 更新任务记录，按 `redberry-verification` 选择验收方式，验收与复查完成前仅标记编码完成。
- 小改动由当前 agent 针对性验证和复查；需要独立验收时交接源码与原始证据，再交审查，不替验收者预填结论。
- 遇到失败进入 `redberry-debugging`，修复后按原验收条件验证；验收或审查问题按 `using-redberry` 处理。
- 必需检查受阻时明确阻断并继续独立工作。

低风险文案或等价局部修改核对实际差异及适当现有检查，无需新增镜像实现的测试。只交付计划、代码草案或未执行的验证安排时，按实际状态说明交付范围。
