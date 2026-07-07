# 📖 novel-master

> **出版级中文长篇小说 · 全流程 AI 创作技能包**
>
> 专为 OpenClaw 设计的端到端小说创作助手，覆盖从灵感到终稿的完整出版链路。
> **v2 全新架构：分布式角色子进程 + 节点压缩图谱，让百万字级创作不烂尾、配角不 OOC。**
>
> 📦 **v2.0.0 完整源码（含 v2 脚本与参考文档）已发布在 GitHub：**[`bbroot/novel-master`](https://github.com/bbroot/novel-master)。ClawHub 市场页为 v1 入口，v2 内容请从 GitHub 获取与安装。

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img src="assets/banner-light.svg" alt="novel-master banner" width="800">
  </picture>
</p>

<p align="center">
  <a href="#english">English</a> · <a href="#中文">中文</a>
</p>

<p align="center">
  <a href="https://clawhub.ai/bbroot/skills/novel-master"><img src="https://img.shields.io/badge/ClawHub-marketplace-7b2ff7?style=flat-square" alt="ClawHub"></a>
  <a href="https://github.com/bbroot/novel-master"><img src="https://img.shields.io/badge/GitHub-v2.0.0-2ea44f?style=flat-square" alt="GitHub"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT"></a>
  <a href="#v2-分布式创作架构"><img src="https://img.shields.io/badge/架构-分布式-Purple?style=flat-square" alt="PpC"></a>
</p>

---

<h2 id="中文">🌟 为什么选择 novel-master？</h2>

| 维度 | 普通 AI 写作 | **novel-master v2** |
|------|------------|--------------------|
| 🎯 写作标准 | 随机产出，质量难控 | **出版级标准**：文字精炼、情感内敛、主题深刻 |
| 🧩 长线一致 | 写到 30 万字就忘设定 | **分布式角色子进程**：每个角色独立状态机，配角不崩 |
| 🧠 记忆机制 | 把整本书塞进上下文→溢出崩坏 | **节点压缩图谱（NCG）**：百万字压缩为可检索图 |
| 🔗 伏笔管理 | 全凭记忆，易遗漏 | **结构化追踪 + 因果伏笔流**：埋/收/预警一条龙 |
| 🛡️ 读者信任 | Bug 自己都看不见 | **量子审计门禁**：每章四维检查，未过即阻塞 |
| 🎭 人物声线 | 全员同一套模板 | **认知偏差包**：让每个角色用自己的感官说话 |
| 📚 理论支撑 | 碎片化 | **系统化理论**：麦基、菲尔德、金圣叹、希区柯克 |

---

## ✨ 核心特性

### 🏛️ v2 分布式创作架构（原创机制）

舍弃「单体 AI 记忆」，以 **进程隔离 + 图谱压缩** 从底层消灭 bug，支撑百万字级不烂尾。

- **🧬 角色即子进程（PpC）** — 每个重要角色独占一个轻量子进程，只维护自己的状态机（位置/已知信息边界/情绪值/关系网版本号），通过全局「情节总线（Plot Bus）」收发事件，互不污染。
- **🕸️ 节点压缩图谱（NCG）** — 每章结束提取 ≤200 字事实节点，差分存入图谱；远章自动聚为超节点；三级压缩管线 + 三视图投影（时间线流 / 角色视角流 / 因果伏笔流）。
- **🔬 量子审计门禁** — 每章提交前对照 NCG 做四维检查（名字/时间/地理/伏笔），未过则 Chapter Daemon 阻塞；角色状态版本只进不退。
- **🎨 认知偏差包** — 每个角色加载「感官映射 + 决策偏差」，消灭 AI 同质化，让机器在约束中迸发非套路意象。

> 工作流：`Planner 出章标 → Chapter Daemon 写章 → 角色子进程更新 → 广播 Plot Bus → Settler 入 NCG → Auditor 量检 → 总线前进`
> 任意子进程崩溃 → 从 NCG 快照 + Plot Bus 重放还原，**不重头跑全书**。

### 📋 v1 经典流程（短篇 / 轻量创作）

- **标准化创作流程**：开书立项 → 创作策划书 → 分卷大纲 → 章节细纲 → 分章撰写 → 伏笔管理 → 质量控制
- **🔗 伏笔追踪系统**：浅/中/重三层伏笔体系，自动登记、回收提醒、未回收率预警
- **🎭 人物声线卡**：矛盾性、缺陷、行动即性格，确保角色不崩
- **🧠 经典创作理论内置**：麦基《故事》、悉德·菲尔德三幕、金圣叹草蛇灰线

### 📖 参考文档与脚本

| 文档 / 脚本 | 用途 |
|------|------|
| `references/process-per-character.md` | **v2**：角色子进程 + Plot Bus 协议 |
| `references/node-compressed-graph.md` | **v2**：节点压缩图谱 + 三视图 |
| `references/quantum-auditor.md` | **v2**：四维门禁 + 版本锁 |
| `references/cognitive-bias.md` | **v2**：认知偏差包，去 AI 味 |
| `references/scene-writing.md` | 7 种场景类型 + 转换技巧 |
| `references/dramaturgy.md` | 三幕 / 救猫咪 / 英雄之旅 |
| `references/character-design.md` | 人物塑造七原则 |
| `references/style-guide.md` | 出版级文风标准 |
| `references/foreshadowing.md` | 伏笔三层体系 |
| `references/plot-structure.md` | 结构详解 + 变体 |
| `references/classic-writing-books.md` | 经典文论精华 |
| `references/genres.md` | 类型小说专项 |
| `references/banned-words.md` | 质量自检表 |
| `scripts/char_state.py` | **v2**：角色子进程 init/update/pull/recover |
| `scripts/ncg.py` | **v2**：图谱落库 / 三视图 / 超节点 |
| `scripts/auditor.py` | **v2**：量子门禁 gate + 版本校验 |
| `scripts/init_book.py` | 一键初始化项目结构 |
| `scripts/track_foreshadowing.py` | 伏笔登记/查询/回收 |
| `scripts/update_state.py` | 写作进度追踪 |

---

## 🚀 快速开始

### 安装

```bash
# OpenClaw 用户
openclaw skills install novel-master

# 或通过 ClawHub CLI
clawhub install novel-master
```

### 开始创作

告诉 AI：**「我要写一本悬疑小说」**

AI 将自动完成：阅读类型参考 → 输出《创作策划书》→ 生成分卷大纲 → 分章撰写 → 伏笔追踪 → 质量自检。

### v2 长篇模式（百万字级）

1. `python scripts/char_state.py init <书名> <角色名> --bias <偏差包id>` — 创建角色子进程
2. 每章写完后：`python scripts/char_state.py update ...` 更新状态 + `python scripts/ncg.py settle ...` 落库节点
3. 提交前：`python scripts/auditor.py gate <书名> <章>` — 量子门禁把关
4. `python scripts/ncg.py view <书名> causal` — 查看因果伏笔流，确认伏笔不丢

### 项目目录结构

```
~/.qclaw/workspace/novels/<书名>/
├── settings/
│   ├── world.md          # 世界观总览
│   ├── characters/       # 人物声线卡 + 状态机 + 偏差包
│   ├── geography.md      # 地理与势力
│   └── rules.md          # 世界运行规则
├── outline/              # 分卷 / 章节大纲
├── chapters/             # 章节正文
├── tracker/
│   ├── foreshadowing.json # 伏笔追踪
│   ├── conflicts.json     # 冲突记录
│   ├── plot_bus.json      # v2 情节总线（章节事实事件流）
│   ├── ncg.json           # v2 节点压缩图谱
│   └── style-log.md       # 文风日志
└── state.json            # 当前写作状态
```

---

## 📖 使用场景

- ✅ **长篇网络小说**：玄幻/都市/悬疑/言情 — v2 架构保持百万字级质量与一致性
- ✅ **出版级文学小说**：现实/历史/成长 — 达到出版社收稿标准
- ✅ **世界观构建**：从零搭建小说世界，确保逻辑自洽
- ✅ **群像小说**：多主角管理，配角不 OOC、不忘设定
- ✅ **经典写作理论学习**：系统掌握麦基/菲尔德/金圣叹等理论

---

## 🤝 贡献

欢迎提交 Issue 和 PR！本项目遵循 [MIT 许可证](LICENSE)，可自由使用、修改和分发。

---

## 📦 技术栈

- **运行环境**：OpenClaw AI Agent
- **辅助脚本**：Python 3
- **格式**：Markdown + JSON
- **许可证**：MIT

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/bbroot">bbroot</a><br>
  <sub>为每一个认真对待文字的人</sub>
</p>
