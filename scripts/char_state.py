# -*- coding: utf-8 -*-
"""
char_state.py - 角色即子进程（Process-per-Character, PpC）状态机

每个重要角色 = 一个轻量子进程，只维护自己的状态机，通过情节总线(Plot Bus)收发事件。
不依赖「把整本书塞进上下文」，崩溃时可从快照 + 总线重放恢复。

用法:
  python char_state.py init   <书名> <角色名> [--bias <偏差包id>]
  python char_state.py update <书名> <角色名> --json '<patch JSON>'
  python char_state.py pull   <书名> <角色名>
  python char_state.py show   <书名> <角色名>
  python char_state.py recover <书名> <角色名>

patch JSON 示例（update 用）:
  {"location":"城西","emotion_value":0.6,
   "relationships":{"女主":{"type":"敌对","strength":0.7}},
   "known_info_boundary":["得知身世真相"]}
"""
import os, sys, json
from pathlib import Path
from datetime import datetime

ROOT = Path.home() / ".qclaw" / "workspace" / "novels"

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

def cmd_update(book, name, patch):
    st = _load_state(book, name)
    # 冻结旧版本快照（只进不退）
    snap = {k: st[k] for k in st if k != "snapshots"}
    st["snapshots"].append({"version": st["version"], "state": snap,
                            "frozen_at": datetime.now().strftime("%Y-%m-%d %H:%M")})
    st["version"] += 1
    # 应用 patch
    for k, v in patch.items():
        if k == "known_info_boundary" and isinstance(v, list):
            for item in v:
                if item not in st["known_info_boundary"]:
                    st["known_info_boundary"].append(item)
        elif k == "relationships" and isinstance(v, dict):
            for other, rel in v.items():
                st["relationships"][other] = rel
            st["relationship_net_version"] += 1
        else:
            st[k] = v
    if "updated_chapter" not in patch:
        pass
    _state_file(book, name).write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {name} 状态已更新 -> version={st['version']}")

def cmd_pull(book, name):
    bf = _bus_file(book)
    if not bf.exists():
        print("情节总线为空"); return
    bus = json.loads(bf.read_text(encoding="utf-8"))
    print(f"=== {name} 相关的情节总线事件 ===")
    n = 0
    for entry in bus:
        for f in entry.get("facts", []):
            hit = (f.get("who") == name
                   or (f.get("a") == name or f.get("b") == name)
                   or (f.get("type") == "info_reveal" and f.get("who") == name))
            if hit:
                print(f"  第{entry.get('chapter')}章: {f}")
                n += 1
    if n == 0:
        print("  (暂无相关事件)")

def cmd_show(book, name):
    st = _load_state(book, name)
    print(json.dumps(st, ensure_ascii=False, indent=2))

def cmd_recover(book, name):
    st = _load_state(book, name)
    # 版本异常检测
    if not st["snapshots"]:
        print(f"{name} 无快照，状态正常(version={st['version']})"); return
    last = st["snapshots"][-1]
    print(f"检测到快照 v{last['version']}，最近更新章={st.get('updated_chapter')}")
    print("执行 Plot Bus 重放...")
    cmd_pull(book, name)
    print(f"✓ 恢复完成：当前 version={st['version']}，可从快照回滚至 v{last['version']}")

def main():
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    cmd, book, name = sys.argv[1], sys.argv[2], sys.argv[3]
    if cmd == "init":
        bias = None
        if "--bias" in sys.argv:
            bias = sys.argv[sys.argv.index("--bias") + 1]
        cmd_init(book, name, bias)
    elif cmd == "update":
        js = sys.argv[sys.argv.index("--json") + 1]
        cmd_update(book, name, json.loads(js))
    elif cmd == "pull":
        cmd_pull(book, name)
    elif cmd == "show":
        cmd_show(book, name)
    elif cmd == "recover":
        cmd_recover(book, name)
    else:
        print("未知命令"); print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()
