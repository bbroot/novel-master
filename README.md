# 📖 novel-master

> **出版级中文长篇小说 · 全流程 AI 创作技能包**
>
> 专为 OpenClaw 设计的端到端小说创作助手，覆盖从灵感到终稿的完整出版链路。

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img src="assets/banner-light.svg" alt="novel-master banner" width="800">
  </picture>
</p>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="README.md">中文</a>
</p>

<p align="center">
  <a href="https://clawhub.ai/USER/skills/novel-master"><img src="https://img.shields.io/badge/ClawHub-v1.0.0-7b2ff7?style=flat-square" alt="ClawHub"></a>
  <a href="https://github.com/USER/novel-master"><img src="https://img.shields.io/badge/GitHub-open-2ea44f?style=flat-square" alt="GitHub"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT"></a>
</p>

---

## 🌟 为什么选择 novel-master？

| 维度 | traditional AI prompting | **novel-master** |
|------|------------------------|-----------------|
| 🎯 写作标准 | 随机产出，质量难控 | **出版级标准**：文字精炼、情感内敛、主题深刻 |
| 📋 创作流程 | 即兴发挥，无章可循 | **标准化流程**：开书→策划→大纲→撰写→质控 |
| 🔗 伏笔管理 | 全凭记忆，易遗漏 | **结构化追踪**：伏笔登记/回收/预警系统 |
| 🧠 理论支撑 | 碎片化 | **系统化理论**：麦基、菲尔德、金圣叹、希区柯克 |
| 🎭 人物塑造 | 脸谱化 | **声线卡系统**：矛盾性、缺陷、行动即性格 |
| 📚 参考资料 | 需要自行搜索 | **10个内置文档**：场景/结构/文风/对话/类型专项 |

---

## ✨ 核心特性

- **📋 标准化创作流程**
  开书立项 → 创作策划书 → 分卷大纲 → 章节细纲 → 分章撰写 → 伏笔管理 → 质量控制

- **🔗 伏笔追踪系统**
  浅/中/重三层伏笔体系，自动登记、回收提醒、未回收率预警，告别「挖坑不填」

- **🎭 人物声线卡**
  每个角色建立独立声线卡，说话方式、思维特征、内心秘密、人物弧光，确保角色不崩

- **🧠 经典创作理论内置**
  麦基《故事》、悉德·菲尔德三幕、《救猫咪》15节拍、金圣叹草蛇灰线、希区柯克悬念公式

- **📖 10 个参考文档**
  | 文档 | 用途 |
  |------|------|
  | `references/scene-writing.md` | 7种场景类型 + 转换技巧 |
  | `references/dramaturgy.md` | 三幕/救猫咪/英雄之旅 |
  | `references/character-design.md` | 人物塑造七原则 |
  | `references/style-guide.md` | 出版级文风标准 |
  | `references/foreshadowing.md` | 伏笔三层体系 |
  | `references/plot-structure.md` | 结构详解 + 变体 |
  | `references/classic-writing-books.md` | 经典文论精华 |
  | `references/genres.md` | 类型小说专项 |
  | `references/banned-words.md` | 质量自检表 |
  | `references/term-mappings.md` | 术语映射（预留） |

- **🔧 辅助脚本**
  `scripts/init_book.py` — 一键初始化项目结构
  `scripts/track_foreshadowing.py` — 伏笔登记/查询/回收
  `scripts/update_state.py` — 写作进度追踪

---

## 🚀 快速开始

### 安装技能

```bash
# OpenClaw 用户
openclaw skills install novel-master

# 或通过 ClawHub CLI
clawhub install novel-master
```

### 开始创作

告诉 AI：**「我要写一本悬疑小说」**

AI 将自动完成：
1. 阅读类型参考 → 2. 输出《创作策划书》→ 3. 生成分卷大纲 → 4. 分章撰写 → 5. 伏笔追踪 → 6. 质量自检

### 项目目录结构

```
~/.qclaw/workspace/novels/<书名>/
├── settings/
│   ├── world.md          # 世界观总览
│   ├── characters/       # 人物声线卡
│   ├── geography.md      # 地理与势力
│   └── rules.md          # 世界运行规则
├── outline/
│   ├── arc-outline.md    # 分卷大纲
│   └── chapter-outline.md # 章节细纲
├── chapters/             # 章节正文
├── tracker/
│   ├── foreshadowing.json # 伏笔追踪
│   ├── conflicts.json     # 冲突记录
│   └── style-log.md       # 文风日志
└── state.json            # 当前写作状态
```

---

## 📖 使用场景

- ✅ **长篇网络小说**：玄幻/都市/悬疑/言情 — 保持长期连载的质量和一致性
- ✅ **出版级文学小说**：现实/历史/成长 — 达到出版社收稿标准
- ✅ **世界观构建**：从零搭建小说世界，确保逻辑自洽
- ✅ **人物体系设计**：多主角/群像小说的角色管理
- ✅ **经典写作理论学习**：系统掌握麦基/菲尔德/金圣叹等理论

---

## 🤝 贡献

欢迎提交 Issue 和 PR！  
本项目遵循 [MIT 许可证](LICENSE)，可自由使用、修改和分发。

---

## 📦 技术栈

- **运行环境**：OpenClaw AI Agent
- **辅助脚本**：Python 3
- **格式**：Markdown + JSON
- **许可证**：MIT

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/USER">USER</a><br>
  <sub>为每一个认真对待文字的人</sub>
</p>
