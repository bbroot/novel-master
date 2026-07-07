# 角色即子进程（Process-per-Character, PpC）

> 本机制为 v2 分布式架构的核心。解决的问题：单体 AI 通写全体角色时，
> 配角记忆随上下文溢出而丢失，导致 OOC（Out Of Character）与设定崩坏。

## 一、核心思想

- **每个重要角色独占一个「轻量子进程」**（本地即一个 `settings/characters/<name>/state.json` 状态机文件 + 认知偏差包）。
- 子进程**只维护该角色自己的状态**：当前位置、已知信息边界、情绪值、关系网版本号。
- 子进程之间**不直接通信**，全部通过全局「情节总线（Plot Bus）」收发事件包，避免上下文互相污染。
- 主写作进程（Chapter Daemon）每章向总线广播「章节事实 JSON」，各角色子进程只拉取**与自己相关的字段**并在本地更新 —— 实现「章节发生即记录并前进」。

## 二、角色状态机 Schema

`settings/characters/<name>/state.json`：

```json
{
  "name": "角色名",
  "version": 1,
  "snapshots": [],
  "location": "当前位置",
  "known_info_boundary": ["已知信息A", "已知信息B"],
  "emotion_value": 0.3,
  "relationship_net_version": 1,
  "relationships": {
    "他人名": { "type": "同盟|敌对|中立|暧昧", "strength": 0.5 }
  },
  "cognitive_bias_pack": "bias_pack_id",
  "updated_chapter": 5
}
```

字段说明：

| 字段 | 类型 | 含义 |
|------|------|------|
| `version` | int | 状态版本号，**单调递增**，重写章节时不回退 |
| `snapshots` | array | 旧版本冻结快照，用于 recover |
| `location` | string | 当前物理/场景位置 |
| `known_info_boundary` | list | 该角色**此刻应当已掌握**的信息清单（边界） |
| `emotion_value` | float | 情绪值，区间 -1（绝望）~ +1（亢奋），0 为基线 |
| `relationship_net_version` | int | 关系网版本，关系变更时 +1 |
| `relationships` | map | 与其他角色的当前关系与强度 |
| `cognitive_bias_pack` | string | 引用认知偏差包 id（见 `cognitive-bias.md`） |
| `updated_chapter` | int | 最近一次更新的章号 |

## 三、情节总线（Plot Bus）协议

广播载体：`tracker/plot_bus.json`（追加式事件日志）。

**章节事实 JSON（Chapter Daemon 每章广播）**：

```json
{
  "chapter": 5,
  "facts": [
    { "type": "character_move", "who": "男主", "to": "城西" },
    { "type": "foreshadow_trigger", "id": "fp-003", "desc": "灯下旧信" },
    { "type": "relationship_change", "a": "男主", "b": "女主", "new": "敌对", "strength": 0.7 },
    { "type": "info_reveal", "who": "男主", "info": "得知身世真相" },
    { "type": "event", "desc": "城门失火" }
  ]
}
```

**事实类型（fact type）**：

- `character_move`：位移（更新对应角色 `location`）
- `foreshadow_trigger`：触发/埋入伏笔（写入 NCG + 伏笔台账）
- `relationship_change`：关系变更（更新对应双方 `relationships`，双方 `relationship_net_version` +1）
- `info_reveal`：信息揭示（把 `info` 加入对应角色 `known_info_boundary`）
- `event`：其他客观事件（进入 NCG 节点）

**子进程拉取规则**：每个角色子进程只接收 `who` 命中自己、或 `relationship_change` 涉及自己、或 `info_reveal.who` 为自己的事实，其余丢弃。

## 四、更新与版本锁

- 每次角色状态更新前，**先把当前 state 推入 `snapshots` 冻结**（旧版本不覆盖）。
- `version` +1。此举实现「状态只进不退」——重写第 5 章时，第 5 章前的角色快照仍可还原。
- 参考实现：`scripts/char_state.py update`。

## 五、崩溃恢复（recover）

任意角色子进程「上下文丢失」（即 AI 忘记配角设定）时：

1. 读取该角色 `state.json` 最新 `version` 与 `known_info_boundary`。
2. 若版本异常（如回退、缺失关键字段），从最近 `snapshots` 还原。
3. 重新 `pull` Plot Bus 中该角色相关事实，本地重放至最新章。
4. 不依赖重读全文 —— 这是 PpC 相比「单体 AI 记忆」的根本优势。
