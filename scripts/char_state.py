# -*- coding: utf-8 -*-
"""
char_state.py - 角色即子进程（Process-per-Character, PpC）状态机

每个重要角色 = 一个轻量子进程，只维护自己的状态机，通过情节总线(Plot Bus)收发事件。
不依赖「把整本书塞进上下文」，崩溃时可从快照 + 总线重放恢复。

用法:
  python char_state.py init   <书名> <角色名> [--bias <偏差包id>]
  python char_state.py update <书名> <角色名> --json '<patch JSON>'
  python char_state.py pull   <书名> <角色名> [--apply]
  python char_state.py show   <书名> <角色名>
  python char_state.py recover <书名> <角色名>
  python char_state.py broadcast <书名> <章节> --json '<事实 JSON>'   # 向 Plot Bus 广播章节事实

事实 JSON 示例（broadcast 用，支持多条）:
  {"facts":[{"type":"character_move","who":"张三","to":"城西"},
            {"type":"info_reveal","who":"李四","info":"得知身世真相"}]}

patch JSON 示例（update 用）:
  {"location":"城西","emotion_value":0.6,
   "relationships":{"女主":{"type":"敌对","strength":0.7}},
   "known_info_boundary":["得知身世真相"]}
"""
import os, sys, json
from pathlib import Path
from datetime import datetime

# 跨 Agent 数据根目录：优先环境变量，回退当前工作目录下的 novels/
# 支持 WorkBuddy / 豆包工作 / Claude Code / Cursor / CodeBuddy / QClaw
ROOT = Path(os.environ.get("NOVELS_ROOT", Path.cwd() / "novels")).expanduser()

def _chars_dir(book):
    return ROOT / book / "settings" / "characters"

def _state_file(book, name):
    return _chars_dir(book) / name / "state.json"

def _bus_file(book):
    return ROOT / book / "tracker" / "plot_bus.json"

def _new_state(name, bias=None):
    return {
        "name": name, "version": 1, "snapshots": [],
        "location": "", "known_info_boundary": [],
        "emotion_value": 0.0, "relationship_net_version": 1,
        "relationships": {}, "cognitive_bias_pack": bias or "",
        "updated_chapter": 0
    }

def cmd_init(book, name, bias=None):
    d = _chars_dir(book) / name
    d.mkdir(parents=True, exist_ok=True)
    sf = d / "state.json"
    if sf.exists():
        print(f"⚠ 角色 {name} 已存在，跳过初始化")
        return
    sf.write_text(json.dumps(_new_state(name, bias), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: 角色子进程已创建 {name} (version=1)" + (f" bias={bias}" if bias else ""))

def _load_state(book, name):
    sf = _state_file(book, name)
    if not sf.exists():
        print(f"错误: 未找到角色 {name}，请先 init"); sys.exit(1)
    return json.loads(sf.read_text(encoding="utf-8"))

# 允许 patch 修改的字段白名单；version/snapshots/name 等保留字段禁止覆盖，
# 否则可绕过「版本只进不退」与 auditor.check-version 校验
MUTABLE_FIELDS = {"location", "emotion_value", "known_info_boundary",
                  "relationships", "cognitive_bias_pack", "updated_chapter"}

def cmd_update(book, name, patch):
    st = _load_state(book, name)
    unknown = [k for k in patch if k not in MUTABLE_FIELDS]
    if unknown:
        print(f"⚠ 以下字段为保留字段，已忽略（不可通过 patch 覆盖）: {unknown}")
    # 冻结旧版本快照（只进不退）
    snap = {k: st[k] for k in st if k != "snapshots"}
    st["snapshots"].append({"version": st["version"], "state": snap,
                            "frozen_at": datetime.now().strftime("%Y-%m-%d %H:%M")})
    st["version"] += 1
    # 应用 patch（仅白名单字段）
    for k, v in patch.items():
        if k not in MUTABLE_FIELDS:
            continue
        if k == "known_info_boundary" and isinstance(v, list):
            for item in v:
                if item not in st["known_info_boundary"]:
                    st["known_info_boundary"].append(item)
        elif k == "relationships" and isinstance(v, dict):
            if not v:  # 空关系不触发版本自增
                continue
            for other, rel in v.items():
                st["relationships"][other] = rel
                # 关系涉及双方：同步对方的反向关系并自增其关系网版本
                inv = _load_state_if_exists(book, other)
                if inv is not None:
                    inv.setdefault("relationships", {})[name] = rel
                    inv["relationship_net_version"] = inv.get("relationship_net_version", 1) + 1
                    _state_file(book, other).write_text(
                        json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8")
            st["relationship_net_version"] += 1
        else:
            st[k] = v
    # updated_chapter 自动维护（patch 未提供时取最大值，不回退）
    uc = patch.get("updated_chapter")
    if isinstance(uc, int) and uc > st.get("updated_chapter", 0):
        st["updated_chapter"] = uc
    _state_file(book, name).write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {name} 状态已更新 -> version={st['version']}")

def _load_state_if_exists(book, name):
    sf = _state_file(book, name)
    return json.loads(sf.read_text(encoding="utf-8")) if sf.exists() else None

def _relevant_events(bus, name):
    out = []
    for entry in bus:
        for f in entry.get("facts", []):
            hit = (f.get("who") == name
                   or (f.get("a") == name or f.get("b") == name))
            if hit:
                out.append((entry.get("chapter"), f))
    return out

def cmd_pull(book, name, apply=False):
    """读取情节总线中与该角色相关的事件。apply=True 时把 info_reveal 应用到已知信息边界。"""
    bf = _bus_file(book)
    if not bf.exists():
        print("情节总线为空"); return
    bus = json.loads(bf.read_text(encoding="utf-8"))
    events = _relevant_events(bus, name)
    print(f"=== {name} 相关的情节总线事件 ===")
    applied = 0
    for chapter, f in events:
        print(f"  第{chapter}章: {f}")
        if apply and f.get("type") == "info_reveal":
            info = f.get("info") or f.get("content")
            if info:
                st = _load_state(book, name)
                if info not in st.get("known_info_boundary", []):
                    st.setdefault("known_info_boundary", []).append(info)
                    st["version"] = st.get("version", 1) + 1
                    _state_file(book, name).write_text(
                        json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")
                    applied += 1
    if not events:
        print("  (暂无相关事件)")
    if apply:
        print(f"  · 已应用 info_reveal {applied} 条到已知信息边界")

def cmd_broadcast(book, chapter, payload):
    """向 tracker/plot_bus.json 追加一章的事实（Plot Bus 写入方）。"""
    chapter = int(chapter)
    facts = payload.get("facts")
    if facts is None:  # 兼容直接传单条事实
        facts = [payload]
    if not isinstance(facts, list):
        print("错误: 事实须为对象或含 facts 数组"); sys.exit(1)
    bf = _bus_file(book)
    bf.parent.mkdir(parents=True, exist_ok=True)
    bus = json.loads(bf.read_text(encoding="utf-8")) if bf.exists() else []
    # 同章节重复广播时合并 facts，避免重复条目
    merged = False
    for entry in bus:
        if entry.get("chapter") == chapter:
            entry.setdefault("facts", []).extend(facts)
            merged = True
            break
    if not merged:
        bus.append({"chapter": chapter, "facts": facts})
    bus.sort(key=lambda e: e.get("chapter", 0))
    bf.write_text(json.dumps(bus, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: 已向第{chapter}章 Plot Bus 广播 {len(facts)} 条事实")

def cmd_show(book, name):
    st = _load_state(book, name)
    print(json.dumps(st, ensure_ascii=False, indent=2))

def cmd_recover(book, name):
    """从最近快照回滚状态，再重放 Plot Bus 的 info_reveal 事件（真正写回 state.json）。"""
    st = _load_state(book, name)
    if not st.get("snapshots"):
        print(f"{name} 无快照，状态正常(version={st['version']})"); return
    last = st["snapshots"][-1]
    base = json.loads(json.dumps(last["state"]))  # 深拷贝快照
    print(f"回滚至快照 v{last['version']}，最近更新章={base.get('updated_chapter')}")
    # 重放：快照版本之后、按章号升序应用 info_reveal
    snap_chapter = base.get("updated_chapter", 0)
    bf = _bus_file(book)
    replayed = 0
    if bf.exists():
        bus = json.loads(bf.read_text(encoding="utf-8"))
        events = sorted(_relevant_events(bus, name), key=lambda x: (x[0] or 0))
        base.setdefault("known_info_boundary", [])
        for chapter, f in events:
            if (chapter or 0) <= snap_chapter:
                continue
            if f.get("type") == "info_reveal":
                info = f.get("info") or f.get("content")
                if info and info not in base["known_info_boundary"]:
                    base["known_info_boundary"].append(info)
                    replayed += 1
    # 恢复后的版本必须高于快照版本，保证单调
    base["version"] = max(base.get("version", 1), last["version"]) + 1
    base.setdefault("snapshots", st["snapshots"])  # 保留历史快照
    _state_file(book, name).write_text(
        json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ 恢复完成：重放 {replayed} 条情报，当前 version={base['version']}")

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    cmd, book = sys.argv[1], sys.argv[2]
    if cmd == "broadcast":
        if len(sys.argv) < 4 or "--json" not in sys.argv:
            print("用法: char_state.py broadcast <书名> <章节> --json '<事实 JSON>'"); sys.exit(1)
        chapter = sys.argv[3]
        cmd_broadcast(book, chapter, json.loads(sys.argv[sys.argv.index("--json") + 1]))
        return
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    name = sys.argv[3]
    if cmd == "init":
        bias = None
        if "--bias" in sys.argv:
            bias = sys.argv[sys.argv.index("--bias") + 1]
        cmd_init(book, name, bias)
    elif cmd == "update":
        js = sys.argv[sys.argv.index("--json") + 1]
        cmd_update(book, name, json.loads(js))
    elif cmd == "pull":
        cmd_pull(book, name, apply="--apply" in sys.argv)
    elif cmd == "show":
        cmd_show(book, name)
    elif cmd == "recover":
        cmd_recover(book, name)
    else:
        print("未知命令"); print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()
