# -*- coding: utf-8 -*-
"""
ncg.py - 节点压缩图谱（Node-Compressed Graph, NCG）

每章由 Settler 提取 ≤200 字事实节点，差分存入图谱；远章聚为超节点。
支持三种视图投影：timeline（时间线流）/ character（角色视角流）/ causal（因果伏笔流）。
也是量子审计(Auditor)的事实来源。

用法:
  python ncg.py settle <书名> <章节> --text '章摘要' --tags '位移,关系变更,伏笔' [--edges 'n-0003:因果']
  python ncg.py view   <书名> <timeline|character|causal>
  python ncg.py super  <书名> [--window 10]     # 聚合超节点
  python ncg.py dump   <书名>                    # 导出原始图谱 JSON
"""
import os, sys, json
from pathlib import Path

ROOT = Path.home() / ".qclaw" / "workspace" / "novels"

def _ncg_file(book):
    return ROOT / book / "tracker" / "ncg.json"

def _load(book):
    f = _ncg_file(book)
    if not f.exists():
        return {"nodes": [], "super_nodes": []}
    return json.loads(f.read_text(encoding="utf-8"))

def _save(book, data):
    _ncg_file(book).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def cmd_settle(book, chapter, text, tags, edges):
    data = _load(book)
    nid = f"n-{len(data['nodes'])+1:04d}"
    node = {"id": nid, "chapter": int(chapter), "text": text,
            "tags": [t.strip() for t in tags.split(",") if t.strip()] if tags else [],
            "edges": []}
    if edges:
        for e in edges.split(","):
            e = e.strip()
            if ":" in e:
                to, rel = e.split(":", 1)
                node["edges"].append({"to": to.strip(), "rel": rel.strip()})
    data["nodes"].append(node)
    _save(book, data)
    print(f"OK: 节点 {nid} 已落库 (第{chapter}章, {len(node['text'])}字, tags={node['tags']})")

def cmd_view(book, kind):
    data = _load(book)
    nodes = data["nodes"]
    if kind == "timeline":
        print(f"=== 时间线流 (共{len(nodes)}节点) ===")
        for n in sorted(nodes, key=lambda x: x["chapter"]):
            print(f"  第{n['chapter']}章 [{n['id']}] {n['text']}")
    elif kind == "character":
        print(f"=== 角色视角流 ===")
        char = {}
        for n in nodes:
            for t in n["tags"]:
                pass
            # 从 text 粗略抽取涉及角色（含「男主/女主/」等）
            for who in ("男主", "女主", "师父", "反派"):
                if who in n["text"]:
                    char.setdefault(who, []).append(n)
        for who, ns in char.items():
            print(f"\n● {who} 的轨迹 ({len(ns)}节点):")
            for n in ns:
                print(f"    第{n['chapter']}章: {n['text']}")
    elif kind == "causal":
        print(f"=== 因果伏笔流 ===")
        for n in nodes:
            if any(t in ("伏笔", "因果") for t in n["tags"]):
                edge_s = ", ".join(f"{e['rel']}->{e['to']}" for e in n.get("edges", []))
                print(f"  [{n['id']}] 第{n['chapter']}章: {n['text']}" + (f"  ({edge_s})" if edge_s else ""))
    else:
        print("未知视图，可选 timeline|character|causal")

def cmd_super(book, window=10):
    data = _load(book)
    nodes = data["nodes"]
    # 简单聚合：按 window 切片，取首尾章号
    supers = []
    for i in range(0, len(nodes), window):
        chunk = nodes[i:i+window]
        if not chunk:
            continue
        c0, c1 = chunk[0]["chapter"], chunk[-1]["chapter"]
        summary = chunk[-1]["text"]
        supers.append({"id": f"s-{len(supers)+1:02d}", "cover": f"第{c0}-{c1}章",
                       "summary": summary, "edges": []})
    data["super_nodes"] = supers
    _save(book, data)
    print(f"OK: 已聚合 {len(supers)} 个超节点 (window={window})")

def cmd_dump(book):
    data = _load(book)
    print(json.dumps(data, ensure_ascii=False, indent=2))

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    cmd, book = sys.argv[1], sys.argv[2]
    if cmd == "settle":
        chapter = sys.argv[sys.argv.index("--chapter")+1] if "--chapter" in sys.argv else sys.argv[3]
        text = sys.argv[sys.argv.index("--text")+1]
        tags = sys.argv[sys.argv.index("--tags")+1] if "--tags" in sys.argv else ""
        edges = sys.argv[sys.argv.index("--edges")+1] if "--edges" in sys.argv else ""
        cmd_settle(book, chapter, text, tags, edges)
    elif cmd == "view":
        kind = sys.argv[3] if len(sys.argv) > 3 else "timeline"
        cmd_view(book, kind)
    elif cmd == "super":
        w = 10
        if "--window" in sys.argv:
            w = int(sys.argv[sys.argv.index("--window")+1])
        cmd_super(book, w)
    elif cmd == "dump":
        cmd_dump(book)
    else:
        print("未知命令"); print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()
