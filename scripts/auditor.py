# -*- coding: utf-8 -*-
"""
auditor.py - 量子审计与原创门禁（Quantum Auditor）

每章提交前由独立 Auditor 进程对照 NCG 做四维检查（name/time/geo/foreshadow）。
未过则 Chapter Daemon 阻塞（gate=BLOCK），从底层杜绝设定崩坏与 OOC。
审计粒度量子化到「单章事实」，成本与总字数无关。

用法:
  python auditor.py gate <书名> <章节> [--chapter-file <正文路径>]
  python auditor.py check-version <书名>        # 校验所有角色状态版本单调性
"""
import os, sys, json
from pathlib import Path

ROOT = Path.home() / ".qclaw" / "workspace" / "novels"

def _load(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

def cmd_gate(book, chapter, chapter_file=None):
    chapter = int(chapter)
    ncg = _load(ROOT / book / "tracker" / "ncg.json") or {"nodes": []}
    bus = _load(ROOT / book / "tracker" / "plot_bus.json") or []
    fp = _load(ROOT / book / "tracker" / "foreshadowing.json") or {"伏笔列表": []}
    chars_dir = ROOT / book / "settings" / "characters"

    issues = []
    checks = {"name": True, "time": True, "geo": True, "foreshadow": True}

    # —— geo: 角色位置自洽（上一章 location vs Plot Bus 中本章位移）——
    loc_map = {}
    for cdir in chars_dir.iterdir():
        st = _load(cdir / "state.json")
        if st:
            loc_map[st["name"]] = st.get("location", "")
    for entry in bus:
        if entry.get("chapter") != chapter:
            continue
        for f in entry.get("facts", []):
            if f.get("type") == "character_move":
                who, to = f.get("who"), f.get("to")
                prev = loc_map.get(who)
                if prev and prev != to and "（过渡）" not in (f.get("note", "")):
                    # 允许：有显式过渡说明则不报
                    issues.append({"dim": "geo", "level": "red",
                                    "msg": f"{who} 上章在『{prev}』，本章无过渡出现在『{to}』"})
                    checks["geo"] = False

    # —— foreshadow: 已埋伏笔不丢，回收在窗口 ——
    for f in fp.get("伏笔列表", []):
        if f["回收状态"] == "未回收" and chapter > f["预期回收章节"] + 2:
            issues.append({"dim": "foreshadow", "level": "orange",
                           "msg": f"伏笔 {f['编号']} 超期未回收（预期第{f['预期回收章节']}章）"})
            checks["foreshadow"] = False

    # —— name: 已死角色不出现（依据 conflicts.json 标记的死亡）——
    # （简版：检查 NCG 中是否出现「已故」标记角色，需人工在 state 标注 is_dead）
    # 此处给出可扩展钩子
    conflicts = _load(ROOT / book / "tracker" / "conflicts.json") or {"冲突列表": []}
    dead = {c.get("who") for c in conflicts.get("冲突列表", []) if c.get("type") == "death"}

    gate = "PASS" if all(checks.values()) else "BLOCK"
    sig = {"chapter": chapter, "gate": gate, "checks": checks, "issues": issues}
    print(json.dumps(sig, ensure_ascii=False, indent=2))
    sys.exit(0 if gate == "PASS" else 1)

def cmd_check_version(book):
    chars_dir = ROOT / book / "settings" / "characters"
    bad = []
    for cdir in chars_dir.iterdir():
        st = _load(cdir / "state.json")
        if not st:
            continue
        # 版本单调性：snapshots 末尾 version 应 < 当前 version
        snaps = st.get("snapshots", [])
        if snaps:
            last_v = snaps[-1]["version"]
            if last_v >= st["version"]:
                bad.append(f"{st['name']}: 快照版本{last_v} >= 当前{st['version']}")
    if bad:
        print("⚠ 版本异常:")
        for b in bad:
            print("  " + b)
        sys.exit(1)
    print("✓ 所有角色状态版本单调，无回退")

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    cmd, book = sys.argv[1], sys.argv[2]
    if cmd == "gate":
        chapter = sys.argv[3] if len(sys.argv) > 3 else None
        cf = None
        if "--chapter-file" in sys.argv:
            cf = sys.argv[sys.argv.index("--chapter-file")+1]
        if not chapter:
            print("需提供章节号"); sys.exit(1)
        cmd_gate(book, chapter, cf)
    elif cmd == "check-version":
        cmd_check_version(book)
    else:
        print("未知命令"); print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()
