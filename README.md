# Agent系统设计

先判断需不需要多 Agent，再设计它们如何协作。

这是一份用来设计和评审的 Skill。它把需求写成可评审的方案，或按清单检查已有方案。它不运行 Agent，不是编排框架，也不负责业务代码、部署或发布。

英文完整版：<https://github.com/geniusjia666/agent-system-design>

本仓库：<https://github.com/geniusjia666/agent-system-design-cn>

两个仓库是同一方法的两种完整语言版本。中文版不是英文版的节选，英文版也不是中文版的节选。约定的初始方法版本都是 0.1.0，本仓库记在 VERSION。两边靠手动同步对齐，不是自动同步，说明见 [SYNC.md](SYNC.md)。英文仓库尚未合并的改动不作为本仓库的依据。

## 原文里实际有的内容

下列范围按收录的 Skill 原文核对，不是本仓库另加的能力、基准或兼容承诺。

- **7 步**：需求澄清、架构选型、单 Agent 设计、编排与协作、介入与加固、评测、交付与自检。普通代码已经够用时，在第 2 步停止。
- **4 档**：提示词、工作流、单 Agent、多 Agent。能用更简单的档位就不上更复杂的档位。多 Agent 要有上下文、工具或权限上的隔离理由。
- **21 种模式**：沿用旧设计建议 Skill 的检索分类，不是官方统一标准。按需要选用，不要求一次用全，模式数量也不代表效果。
- **21 维审查**：自检清单维度 1 到 21。先按类型选择适用维度，不适用的不打分。分数只评设计文档，不是任务成功率，也不是发布许可。
- **交接契约**：`dispatch` 有七个要素：identity、objective、scope、constraints、context、output_format、stop_condition。另外定义 `handoff` 和 `gate`。这是字段和校验责任，由宿主执行，文件本身不会运行。

模式编号和自检维度编号顺序不同。入口分别是 [设计模式索引](skills/agent-system-design-cn/references/10-设计模式索引.md) 和 [设计自检清单](skills/agent-system-design-cn/assets/设计自检清单.md)。

## 目录

Skill 入口是 [SKILL.md](skills/agent-system-design-cn/SKILL.md)，frontmatter 的 `name` 为 `agent-system-design-cn`。

| 参考 | 内容 |
|---|---|
| [01 架构选型](skills/agent-system-design-cn/references/01-架构选型.md) | 是否需要模型，以及四档怎么选 |
| [02 单 Agent 设计](skills/agent-system-design-cn/references/02-单Agent设计.md) | 角色、任务契约、停止条件 |
| [03 工具设计](skills/agent-system-design-cn/references/03-工具设计.md) | 工具、权限、MCP 与 Skill 的分工 |
| [04 上下文与记忆](skills/agent-system-design-cn/references/04-上下文与记忆.md) | 上下文预算、笔记、长期记忆 |
| [05 编排模式](skills/agent-system-design-cn/references/05-编排模式.md) | 主模式与组合 |
| [06 多 Agent 协作](skills/agent-system-design-cn/references/06-多Agent协作.md) | 角色隔离、派发与交接 |
| [07 人类介入与可靠性安全](skills/agent-system-design-cn/references/07-人类介入与可靠性安全.md) | 介入、失败、预算、安全 |
| [08 评测与迭代](skills/agent-system-design-cn/references/08-评测与迭代.md) | 适用性、用例、门禁 |
| [09 框架落地映射](skills/agent-system-design-cn/references/09-框架落地映射.md) | 同一契约在若干框架上的笔记 |
| [10 设计模式索引](skills/agent-system-design-cn/references/10-设计模式索引.md) | 21 种模式与自检编号 |

资产：

- [交接契约模板](skills/agent-system-design-cn/assets/交接契约模板.json)
- [设计文档模板](skills/agent-system-design-cn/assets/设计文档模板.md)
- [设计自检清单](skills/agent-system-design-cn/assets/设计自检清单.md)

原始 Skill 共 14 个文件、298664 字节，收录后未改内容，也没有改内部引用。哈希由 [scripts/validate_publication.py](scripts/validate_publication.py) 核对。

## 安装与使用

安装单元是整个目录 `skills/agent-system-design-cn/`。宿主若按「一个目录加一份带 YAML frontmatter 的 SKILL.md」加载技能，就把这个目录放到该宿主自己文档所写的位置。`references/` 和 `assets/` 要一起在，因为入口用相对路径引用它们。

这里不写具体产品的目录。发布时没有核对各宿主的现行安装文档，也没有做加载测试，所以不能写成已验证。宿主是否认出 `agent-system-design-cn`，以该宿主当时的行为为准。

使用时从 `SKILL.md` 进入，只打开当前步骤需要的参考。本 Skill 只交付设计或评审。

示例提示词在 [examples/提示词.md](examples/提示词.md)。可以直接这样开头：

> 请按 Agent 系统设计 Skill 处理这个需求。先判断需不需要多 Agent，再设计它们如何协作。信息不够时最多问 3 个问题。只交付设计，不要部署。

## 示例

[word_counts 示例](examples/word-counts-workflow.md) 是一条固定的「代码生成 → 审查 → 修复」。档位是工作流：步骤事先写明，由宿主按顺序调用和校验。它不使用多 Agent，因为这个函数没有必须分开的上下文、工具或权限。文中的输入输出是手写推演，分数留空，不代表质量、时延或费用。

## 框架映射

[框架落地映射](skills/agent-system-design-cn/references/09-框架落地映射.md) 把同一交接契约对照到 Google ADK、LangGraph、CrewAI 和 AutoGen Core 的构建骨架。原文写明：官方材料归档于 2026-10-30，补读日期是 2026-11-01；文中的包版本是当时的候选，并未安装和测试。本仓库发布时也没有安装这些包，没有运行其中的脚手架，也没有重新调查上游现状。该文只作为原资料中的映射笔记，不是兼容性认证，也不是当前版本声明。

## 版本与许可证

方法版本写在 [VERSION](VERSION)，当前是 `0.1.0`。它不是 Git tag，也不是 GitHub Release。

署名 geniusjia666。许可证使用仓库中现有的 [MIT License](LICENSE)，文件保持原样。贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。
