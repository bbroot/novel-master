---
name: novel-master
description: 出版级中文长篇小说全流程创作技能包。当用户要求写小说、创作故事、分章节写作、连续剧情、章节悬念、长篇小说时触发。覆盖从世界观设定、人物塑造、大纲规划、分章撰写到伏笔管理、质量控制的全链路。
---

# novel-master

出版级中文小说创作技能包，适用于网络连载与实体出版双标准。

> **v2 重大升级（分布式架构）**：在 v1 经典流程之上，叠加「角色即子进程（PpC）+ 节点压缩图谱（NCG）+ 量子审计」原创机制，
> 可支撑百万字级不烂尾、配角不 OOC。详见下方「v2 分布式创作架构」。
>
> - 短篇 / 轻量创作 → 用 **v1 经典流程**（直接写，轻量追踪）。
> - 中长篇 / 长篇 / 百万字级 → 用 **v2 分布式架构**（PpC + NCG + Auditor）。

## 核心原则

**出版级 vs 网文级核心差异：**
- 出版级：文字精炼、情感内敛、主题深刻、留白艺术
- 网文级：节奏快爽、情绪外放、更新驱动、字数为王

本技能默认目标：**出版级**，即可以投递出版社或文学期刊的质量标准。

**理论框架（可按需深入）：**
- 叙事学基础 → `references/dramaturgy.md`（悉德·菲尔德三幕 / 麦基《故事》/ 英雄之旅）
- 经典文论 → `references/classic-writing-books.md`（麦基 / 斯蒂芬·金 / 刘勰《文心雕龙》/ 李渔《闲情偶寄》/ 金圣叹 / 王国维）
- 场景专项 → `references/scene-writing.md`（7种场景类型 + 转换技巧 + 高潮设计）

## 项目结构

每个小说项目按以下目录组织：

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

## 工作流程

### 第一阶段：开书立项

**输入：** 用户提供以下任一组合：
- 小说类型（悬疑/言情/科幻/历史/现实/奇幻）
- 核心主题（1句话）
- 主角基本信息（可选）
- 篇幅目标（短篇3-5万/中篇8-15万/长篇20-40万）

**执行步骤：**

1. 阅读 `references/plot-structure.md` 确认结构框架
2. 阅读 `references/character-design.md` 确认人物设计原则
3. 创建项目目录结构
4. 生成《创作策划书》

**《创作策划书》模板（强制输出）：**
```markdown
# 《书名》创作策划书

## 一、作品定位
- 类型：
- 受众：
- 体裁：长篇小说 / 中篇小说 / 短篇集
- 字数目标：
- 出版/连载定位：

## 二、核心主题
- 主线主题：
- 副线主题：
- 情感基调：
- 核心意象（贯穿全文的象征物）：

## 三、世界观设定
[依据类型加载 references 中对应内容]

## 四、人物设定
### 4.1 主角
- 姓名/年龄/职业：
- 核心矛盾：
- 人物弧光（起点→转折→终点）：
- 声线特征：

### 4.2 核心配角（每个配角需回答：他/她为何存在？）

## 五、结构规划
### 三幕结构
- 第一幕（铺陈，约占全文15%）：
- 第二幕（对抗，约占全文70%）：
- 第三幕（解决，约占全文15%）：

### 分卷规划（长篇必做）
卷一：
卷二：
卷三：

## 六、伏笔系统
列出全书3-5个核心伏笔，标注埋入章节和预期回收章节。

## 七、出版级写作标准
- 叙述语气：
- 句式节奏：
- 对话准则：
- 禁止项：
```

### 第二阶段：大纲规划

**分卷大纲（长篇必须）：**
每个分卷输出一份《分卷大纲》，包含：
- 本卷核心事件（3-5个）
- 本卷人物命运走向
- 与前后卷的衔接点
- 伏笔埋入计划

**章节细纲（按需生成）：**
一次生成5-10章细纲，每章细纲格式：
```markdown
## 第X章 《章题》
- 核心事件：
- 视角人物：
- 情感走向（开端→发展→转折）：
- 场景数（建议2-4个）：
- 关键对话片段：
- 伏笔/回收记录：
```

### 第三阶段：分章撰写

**写作参数（每次撰写时确定）：**
- 章号与章题
- 视角人物（严格单章单视角）
- 字数目标（短篇3000-5000字/长篇6000-8000字）
- 本章核心任务（推进/揭示/转折/铺垫）

**写作流程（强制执行）：**
1. 加载本章细纲
2. 加载涉及人物声线卡（references/character-design.md）
3. 加载文风标准（references/style-guide.md）
4. 加载伏笔追踪状态（tracker/foreshadowing.json）
5. 动笔撰写
6. 自检：对照伏笔计划检查本章
7. 更新 tracker/foreshadowing.json

**章节质量自检表（完成后必查）：**
- [ ] 无语病、错字
- [ ] 视角统一（无跳视角）
- [ ] "展示而非告知"原则
- [ ] 对话推进剧情（非闲聊填充）
- [ ] 场景转换有节奏感
- [ ] 章节结尾有钩子（悬念/情感高点/信息差）
- [ ] 字数在目标±10%以内

### 第四阶段：伏笔管理

伏笔登记格式（写入 tracker/foreshadowing.json）：
```json
{
  "id": "fp-001",
  "埋入章节": 3,
  "内容": "男主左手腕有一道旧伤疤",
  "暗示层次": "轻（只提了一次）",
  "预期回收章节": 18,
  "回收状态": "未回收",
  "备注": ""
}
```

伏笔回收检查：
- 轻伏笔：全文至少暗示2次，回收1次
- 重伏笔：全文至少暗示3次，回收1次
- 伏笔未回收率 > 5% 须预警

### 第五阶段：质量控制

**冲突检测：**
- 地理/时间冲突（"明明在北京"→实际在上海）
- 人物设定冲突（性格突变无充分动机）
- 前后矛盾（已死角色突然出现）

**文风一致性：**
- 每5章做一次文风回顾（朗读法：出声朗读前3段）
- 声线卡一致性检查

## 文风标准（出版级）

详见 `references/style-guide.md`，核心摘要：

- **叙述**：第三人称限知视角为主，第一人称慎用
- **句式**：长短交错，短句制造节奏，长句制造氛围
- **对话**：口语化但有角色特征，禁止"是的"/"我知道了"式废话
- **描写**：五感描写，拒绝堆砌形容词，以动代静
- **禁忌词**：绝对/永远/莫名/突然（除非情节需要）

## v2 分布式创作架构（原创机制）

> 参考设计理念：「分布式角色子进程 + 情节节点压缩图谱」。舍弃单体 AI 记忆，以进程隔离 + 图谱压缩从底层消灭 bug。

### 四大支柱

1. **角色即子进程（PpC）** — 每个重要角色独立状态机，只通过情节总线（Plot Bus）收发事件，互不污染。
   详见 `references/process-per-character.md`，脚本 `scripts/char_state.py`。
2. **节点压缩图谱（NCG）** — 每章 ≤200 字事实节点，差分存储，远章聚超节点；三级压缩管线 + 三视图投影。
   详见 `references/node-compressed-graph.md`，脚本 `scripts/ncg.py`。
3. **量子审计门禁** — 每章提交前四维（名字/时间/地理/伏笔）检查，未过则阻塞；状态只进不退。
   详见 `references/quantum-auditor.md`，脚本 `scripts/auditor.py`。
4. **认知偏差包** — 每个角色加载特有「感官映射 + 决策偏差」，消灭 AI 同质化，让机器在约束中迸发非套路意象。
   详见 `references/cognitive-bias.md`。

### v2 工作流（loop）

```
Planner 出章标
  → Chapter Daemon 写章（动笔前 pull 该章视角角色的偏差包）
  → 角色子进程更新状态（char_state.py update，旧版本冻结快照）
  → Chapter Daemon 向 Plot Bus 广播章节事实 JSON（tracker/plot_bus.json）
  → Settler 提取 ≤200 字节点入 NCG（ncg.py settle）
  → Auditor 量子量检（auditor.py gate，未过则 BLOCK 回修）
  → 总线前进，进入下一章
```

### recover（崩溃恢复）
任意角色子进程上下文丢失 → `char_state.py recover <书名> <角色名>`，
从 NCG 快照 + Plot Bus 重放还原，**不重头跑全书**。

### v2 命令速查

| 操作 | 命令 |
|------|------|
| 创建角色子进程 | `python scripts/char_state.py init <书名> <角色名> [--bias <id>]` |
| 更新角色状态 | `python scripts/char_state.py update <书名> <角色名> --json '{...}'` |
| 拉取相关剧情 | `python scripts/char_state.py pull <书名> <角色名>` |
| 落库章节节点 | `python scripts/ncg.py settle <书名> <章> --text '...' --tags '位移,伏笔'` |
| 三视图投影 | `python scripts/ncg.py view <书名> <timeline|character|causal>` |
| 聚合超节点 | `python scripts/ncg.py super <书名> --window 10` |
| 量子门禁 | `python scripts/auditor.py gate <书名> <章>` |
| 版本一致性 | `python scripts/auditor.py check-version <书名>` |

## 参考文档

| 文件 | 何时阅读 |
|------|---------|
| references/plot-structure.md | 开书立项、规划大纲时 |
| references/dramaturgy.md | 规划大纲、理解叙事理论时 |
| references/classic-writing-books.md | 建立写作知识体系、精研大师理论时 |
| references/character-design.md | 设计人物、写作人物对话时 |
| references/style-guide.md | 写作全程，每次动笔前 |
| references/scene-writing.md | 写具体场景时（最常用实操参考）|
| references/foreshadowing.md | 规划伏笔、回收伏笔时 |
| references/genres.md | 特定类型创作时（悬疑/言情等） |
| references/banned-words.md | 章节完成后质量自检时 |
| **references/process-per-character.md** | **v2：设计角色子进程、情节总线时** |
| **references/node-compressed-graph.md** | **v2：设计图谱、做三视图、长线压缩时** |
| **references/quantum-auditor.md** | **v2：设置门禁、做四维检查、recover 时** |
| **references/cognitive-bias.md** | **v2：给角色锻造个性、去 AI 味时** |

## 状态文件

`state.json` 格式：
```json
{
  "book": "书名",
  "current_arc": 1,
  "current_chapter": 5,
  "total_words": 28000,
  "unresolved_foreshadowing": 3,
  "last_updated": "2026-04-16"
}
```

每次完成章节后更新。
