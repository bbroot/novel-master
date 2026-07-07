# 量子审计与原创门禁（Quantum Auditor）

> v2 架构的「质量闸门」。每章提交前由**独立** Auditor 进程对照 NCG 做四维检查，
> 未过则 Chapter Daemon 阻塞，从底层杜绝设定崩坏与 OOC。

## 一、四维门禁检查

| 维度 | 检查项 | 数据来源 |
|------|--------|----------|
| 名字（name） | 角色名前后一致；无凭空出现的新角色；已死角色不出现 | NCG + 角色状态机 |
| 时间（time） | 章节时间线不矛盾；跨度计算合理 | NCG 节点时间戳 |
| 地理（geo） | 角色位置自洽；上一章在A地，本章不能随意出现在B地无过渡 | 角色 `location` |
| 伏笔（foreshadow） | 已埋伏笔不丢；回收在预期窗口；无「埋了不收」 | 伏笔台账 + NCG |

## 二、门禁信号

Auditor 输出 JSON 信号，Chapter Daemon 据此决定是否放行：

```json
{
  "chapter": 5,
  "gate": "PASS | BLOCK",
  "checks": { "name": true, "time": true, "geo": true, "foreshadow": true },
  "issues": [
    { "dim": "geo", "level": "red", "msg": "女主第4章在城东，第5章无过渡出现在城西" }
  ]
}
```

- `gate == "PASS"`：放行，进入 NCG 落库。
- `gate == "BLOCK"`：Chapter Daemon 阻塞，必须先修复 `issues` 再提交。

## 三、状态只进不退（角色级版本锁）

- 角色状态 `version` 单调递增（见 `process-per-character.md`）。
- 重写章节时，旧版本冻结为 `snapshots` 快照，**不覆盖**。
- Auditor 同时校验版本单调性：若发现某角色 `version` 回退，判定为 `name/time` 级异常并 BLOCK。

## 四、审计量子化

「量子化」指审计粒度最小化到**单章事实**而非整本：

- 每章只对照「上一章状态 + 本章事实 + NCG 局部」，不重读全书。
- 使得百万字级作品每次审计成本恒定，与总字数无关。
- 配合 PpC 的「子进程不互相污染」，实现天然的故障隔离。

## 五、集成命令

`scripts/auditor.py gate <书名> <章节> [--chapter-file <正文路径>]`

输出门禁信号 JSON。推荐在 `update_state.py` 提交环节之前调用。
