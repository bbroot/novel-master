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

# 跨 Agent 数据根目录：优先环境变量，回退当前工作目录下的 novels/
# 支持 WorkBuddy / 豆包工作 / Claude Code / Cursor / CodeBuddy / QClaw
ROOT = Path(os.environ.get("NOVELS_ROOT", Path.cwd() / "novels")).expanduser()

def _load(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

def _fp_field(f, *names, default=None):
    """兼容多种伏笔字段命名（id/编号、内容/内容摘要 等）。"""
    for n in names:
        if n in f:
            return f[n]
    return default

def _state_location(st):
    """上一章位置优先取 snapshots 末尾；没有快照才回退当前 location。"""
    snaps = st.get("snapshots") or []
    if snaps:
        last = snaps[-1]
        if isinstance(last, dict):
            s = last.get("state", last)
            return s.get("location", "")
    return st.get("location", "")

def cmd_gate(book, chapter, chapter_file=None):
    chapter = int(chapter)
    ncg = _load(ROOT / book / "tracker" / "ncg.json") or {"nodes": []}
    bus = _load(ROOT / book / "tracker" / "plot_bus.json") or []
    fp = _load(ROOT / book / "tracker" / "foreshadowing.json") or {"伏笔列表": []}
    conflicts = _load(ROOT / book / "tracker" / "conflicts.json") or {"冲突列表": []}
    chars_dir = ROOT / book / "settings" / "characters"

    issues = []
    checks = {"name": True, "time": True, "geo": True, "foreshadow": True}

    # 收集角色状态；上一章位置取快照，避免 update 后当前位置与位移目标恒等
    states = {}
    if chars_dir.exists():
        for cdir in chars_dir.iterdir():
            st = _load(cdir / "state.json")
            if st and st.get("name"):
                states[st["name"]] = st

    # 本章正文（可选），用于 name/time 维度的证据匹配
    body = ""
    if chapter_file:
        p = Path(chapter_file)
        if p.exists():
            body = p.read_text(encoding="utf-8")
    body = body or " ".join(
        str(n.get("text", "")) for n in (ncg.get("nodes") or [])
        if n.get("chapter") == chapter
    )

    # —— geo: 上一章位置（快照）vs 本章位移 ——
    for entry in bus:
        if entry.get("chapter") != chapter:
            continue
        for f in entry.get("facts", []):
            if f.get("type") == "character_move":
                who, to = f.get("who"), f.get("to")
                st = states.get(who)
                prev = _state_location(st) if st else None
                if prev and prev != to and "（过渡）" not in (f.get("note", "")):
                    issues.append({"dim": "geo", "level": "red",
                                   "msg": f"{who} 上章在『{prev}』，本章无过渡出现在『{to}』"})
                    checks["geo"] = False

    # —— name: 已死角色不得在本章正文/位移/NCG 中出现 ——
    dead = {c.get("who") for c in conflicts.get("冲突列表", [])
            if c.get("type") == "death" and c.get("who")}
    dead |= {name for name, st in states.items() if st.get("is_dead")}
    for who in dead:
        appeared = (who in body) or any(
            f.get("who") == who
            for e in bus if e.get("chapter") == chapter
            for f in e.get("facts", [])
        )
        if appeared:
            issues.append({"dim": "name", "level": "red",
                           "msg": f"已故角色『{who}』在本章出现"})
            checks["name"] = False

    # —— time: NCG 节点章号不得倒挂、冲突表标记的时间矛盾 ——
    chapters_seen = [n.get("chapter") for n in (ncg.get("nodes") or [])
                     if isinstance(n.get("chapter"), int)]
    time_conflicts = [c for c in conflicts.get("冲突列表", [])
                      if c.get("type") in ("time", "timeline", "时间线")]
    if time_conflicts:
        for c in time_conflicts:
            issues.append({"dim": "time", "level": "red",
                           "msg": f"时间线冲突未消解：{c.get('desc') or c.get('detail') or c}"})
        checks["time"] = False
    # 节点回填乱序本身只是数据组织问题，降级为提示，不阻断
    if chapters_seen and chapters_seen != sorted(chapters_seen):
        issues.append({"dim": "time", "level": "yellow",
                       "msg": "NCG 节点章号非单调（回填乱序），建议重整"})

    # —— foreshadow: 超期未回收（兼容多种字段命名，缺字段降级为 issue 而非崩溃）——
    for f in (fp.get("伏笔列表") or []):
        fid = _fp_field(f, "编号", "id", default="?")
        status = _fp_field(f, "回收状态", default="未回收")
        due = _fp_field(f, "预期回收章节", default=None)
        if status == "未回收":
            if due is None:
                issues.append({"dim": "foreshadow", "level": "yellow",
                               "msg": f"伏笔 {fid} 缺『预期回收章节』，无法判定超期"})
                checks["foreshadow"] = False
            else:
                try:
                    if chapter > int(due) + 2:
                        issues.append({"dim": "foreshadow", "level": "orange",
                                       "msg": f"伏笔 {fid} 超期未回收（预期第{due}章）"})
                        checks["foreshadow"] = False
                except (TypeError, ValueError):
                    issues.append({"dim": "foreshadow", "level": "yellow",
                                   "msg": f"伏笔 {fid} 预期回收章节非法：{due!r}"})
                    checks["foreshadow"] = False

    gate = "PASS" if all(checks.values()) else "BLOCK"
    sig = {"chapter": chapter, "gate": gate, "checks": checks, "issues": issues}
    print(json.dumps(sig, ensure_ascii=False, indent=2))
    sys.exit(0 if gate == "PASS" else 1)

def cmd_check_version(book):
    chars_dir = ROOT / book / "settings" / "characters"
    bad = []
    if not chars_dir.exists():
        print("✓ 无角色状态目录，跳过版本校验")
        return
    for cdir in chars_dir.iterdir():
        st = _load(cdir / "state.json")
        if not st:
            continue
        # 版本单调性：snapshots 末尾 version 必须 < 当前 version；快照须为列表
        snaps = st.get("snapshots", [])
        if not isinstance(snaps, list):
            bad.append(f"{st.get('name', cdir.name)}: snapshots 非列表，可能被 patch 污染")
            continue
        if snaps:
            try:
                last_v = snaps[-1]["version"]
                cur_v = st["version"]
                if last_v >= cur_v:
                    bad.append(f"{st.get('name', cdir.name)}: 快照版本{last_v} >= 当前{cur_v}")
            except (KeyError, TypeError):
                bad.append(f"{st.get('name', cdir.name)}: 版本字段缺失或类型非法")
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
