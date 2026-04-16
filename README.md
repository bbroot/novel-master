# novel-master

> 出版级中文长篇小说全流程创作技能包。适用于网络连载与实体出版双标准。

---

## 功能特性

- 🎯 **出版级标准**：文字精炼、情感内敛、主题深刻、留白艺术
- 🔄 **完整工作流**：开书立项 → 策划书 → 大纲 → 分章撰写 → 伏笔管理 → 质量控制
- 🧠 **理论深度**：麦基《故事》、悉德·菲尔德三幕、金圣叹草蛇灰线、希区柯克悬念
- 📖 **场景专项**：7种核心场景类型 + 经典转换技巧
- 🤖 **工具支持**：伏笔追踪脚本、状态管理脚本、项目初始化脚本
- 📚 **10个参考文档**：涵盖结构/人物/文风/伏笔/类型专项/经典文论

---

## 目录结构

```
novel-master/
├── SKILL.md                              # 技能主入口
├── assets/                               # 资源目录（预留）
├── references/
│   ├── banned-words.md                   # 质量自检表 / 禁忌词表
│   ├── character-design.md               # 人物设计七原则 / 声线卡模板
│   ├── classic-writing-books.md           # 经典写作书籍核心摘要
│   │                                    #   麦基《故事》· 斯蒂芬·金 · 刘勰 · 李渔 · 金圣叹 · 王国维
│   ├── dramaturgy.md                    # 经典剧作理论
│   │                                    #   三幕结构 / 救猫咪节拍表 / 英雄之旅 / 悬念公式
│   ├── foreshadowing.md                  # 伏笔三层体系 / 回收技巧 / 管理规则
│   ├── genres.md                         # 类型小说专项（悬疑/言情/科幻/历史/现实）
│   ├── plot-structure.md                 # 三幕结构详解 / 非线性结构变体 / 章节节奏
│   ├── scene-writing.md                  # 7种场景类型 / 转换技巧 / 高潮设计
│   └── style-guide.md                    # 出版级文风标准 / 禁忌词表 / 章节收尾
└── scripts/
    ├── init_book.py                      # 新项目初始化（创建完整目录结构）
    ├── track_foreshadowing.py            # 伏笔登记 / 查询 / 回收管理
    └── update_state.py                   # 写作状态更新
```

---

## 快速开始

### 安装

将整个 `novel-master` 文件夹复制到 OpenClaw 的用户技能目录：

```bash
# Windows
cp -r C:\novel-master %USERPROFILE%\.qclaw\skills\novel-master

# 或手动复制到
# ~/.qclaw/skills/novel-master/
```

> OpenClaw 会自动扫描 `~/.qclaw/skills/` 目录，技能无需额外配置即可生效。

### 初始化新小说项目

```bash
python scripts/init_book.py "书名" "作者名"
```

这将在 `~/.qclaw/workspace/novels/书名/` 下创建完整项目结构。

### 伏笔管理

```bash
# 添加伏笔
python scripts/track_foreshadowing.py "书名" add 3 事件 中 "男主左手腕有旧伤" 18

# 查看所有伏笔
python scripts/track_foreshadowing.py "书名" list

# 检查章节伏笔状态
python scripts/track_foreshadowing.py "书名" check 15

# 标记伏笔已回收
python scripts/track_foreshadowing.py "书名" resolve fp-001 18 "揭示真正原因"
```

### 更新写作状态

```bash
python scripts/update_state.py "书名" 5 6200 2
# 参数：书名 章节号 本章字数 未回收伏笔数
```

---

## 创作工作流

```
① 告诉AI："我要写一本[类型]小说"
       ↓
② AI生成《创作策划书》
   （世界观 / 人物 / 三幕结构 / 伏笔系统）
       ↓
③ 确认或修改策划书
       ↓
④ AI生成分卷大纲 + 章节细纲
       ↓
⑤ 分章撰写（每批5-10章）
   过程中自动：
   - 加载人物声线卡
   - 更新伏笔追踪
   - 质量自检
       ↓
⑥ 全书中段审查（伏笔命中率检查）
       ↓
⑦ 全书收尾 + 伏笔全部回收
       ↓
⑧ 终稿整合
```

---

## 参考文档速查

| 文档 | 什么时候读 |
|------|-----------|
| `dramaturgy.md` | 规划大纲、理解叙事理论时 |
| `plot-structure.md` | 开书立项、规划三幕时 |
| `scene-writing.md` | 写具体场景时（最常用）|
| `character-design.md` | 设计人物声线卡时 |
| `style-guide.md` | 每次动笔前 |
| `foreshadowing.md` | 设计/回收伏笔时 |
| `classic-writing-books.md` | 建立写作知识体系时 |
| `banned-words.md` | 章节完成后自检时 |
| `genres.md` | 特定类型创作时 |

---

## 三个核心写作原则

### 1. 展示而非告知（Show, Don't Tell）
```markdown
# ❌ 告知
他很紧张。

# ✅ 展示
他把烟一根根捻灭。烟灰落了一地。
```

### 2. 草蛇灰线（金圣叹）
> 伏笔不是大喊大叫，是走路时留下的脚印。
> 伏笔：前文轻描淡写 → 回收：揭示全部意义

### 3. 炸弹悬念（希区柯克）
> 让观众知道桌下有炸弹，主角不知道 → 这才是悬念。
> 不是"坏人来了"，而是"危险正在逼近但他们不知道"。

---

## 适用场景

- ✅ 写长篇网络小说（玄幻/都市/悬疑/言情）
- ✅ 写出版级文学小说（现实/历史/成长）
- ✅ 建立小说世界观与人物体系
- ✅ 系统化管理伏笔与前后一致
- ✅ 学习麦基/悉德·菲尔德/金圣叹等经典写作理论

---

## License

MIT / 可自由使用、修改、分发
