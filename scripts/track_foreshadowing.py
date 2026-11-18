#!/usr/bin/env python3
"""
track_foreshadowing.py - 伏笔管理工具
用法:
  python track_foreshadowing.py <书名> add <章节> <类型> <层级> <内容摘要> <预期回收章节>
  python track_foreshadowing.py <书名> list
  python track_foreshadowing.py <书名> check <章节>
  python track_foreshadowing.py <书名> resolve <伏笔编号> <回收章节> <回收方式>
"""
import os
import sys
import json
from pathlib import Path

# 字段兼容：同时支持文档 schema（id/内容/埋入章节）与脚本 schema（编号/内容摘要）
def _g(fp, *keys, default=None):
    for k in keys:
        if k in fp:
            return fp[k]
    return default

def fid(fp):     return _g(fp, "编号", "id", default="?")
def summary(fp): return _g(fp, "内容摘要", "内容", default="")
def buried(fp):  return _g(fp, "埋入章节", default="?")
def due(fp):     return _g(fp, "预期回收章节", default=0) or 0
def status(fp):  return _g(fp, "回收状态", default="未回收")

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    book_name = sys.argv[1]
    action = sys.argv[2]

    novels_root = Path(os.environ.get("NOVELS_ROOT", Path.cwd() / "novels")).expanduser()
    fp_file = novels_root / book_name / "tracker" / "foreshadowing.json"

    if not fp_file.exists():
        print(f"错误: 未找到项目 {book_name} 的伏笔追踪文件")
        sys.exit(1)

    data = json.loads(fp_file.read_text(encoding="utf-8"))
    data.setdefault("伏笔列表", [])

    if action == "add":
        if len(sys.argv) < 8:
            print("用法: add <章节> <类型> <层级> <内容摘要> <预期回收章节>")
            sys.exit(1)
        chapter = int(sys.argv[3])
        ftype = sys.argv[4]
        level = sys.argv[5]
        content = sys.argv[6]
        expect_ch = int(sys.argv[7])

        fp_id = f"fp-{len(data['伏笔列表'])+1:03d}"
        new_fp = {
            "编号": fp_id, "id": fp_id,          # 双写，兼容文档 schema
            "类型": ftype, "层级": level,
            "埋入章节": chapter,
            "内容摘要": content, "内容": content,  # 双写
            "出现记录": [{"章节": chapter, "内容": "首次埋入"}],
            "预期回收章节": expect_ch,
            "回收状态": "未回收",
            "回收章节": None, "回收方式": "", "文学效果": ""
        }
        data["伏笔列表"].append(new_fp)
        fp_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"OK: 伏笔 {fp_id} 已登记 (埋于第{chapter}章, 预期回收第{expect_ch}章)")

    elif action == "list":
        fps = data["伏笔列表"]
        if not fps:
            print("当前无伏笔记录")
            return
        unresolved = sum(1 for fp in fps if status(fp) == "未回收")
        print(f"=== 伏笔总览 ===")
        print(f"总数: {len(fps)} | 未回收: {unresolved}")
        for fp in fps:
            mark = "✓" if status(fp) == "已回收" else "✗"
            print(f"[{fid(fp)}] {mark} 第{buried(fp)}章 → 第{due(fp)}章 | {summary(fp)}")

    elif action == "check":
        if len(sys.argv) < 4:
            print("用法: check <章节号>")
            sys.exit(1)
        ch = int(sys.argv[3])
        def dnum(fp):
            try:
                return int(due(fp))
            except (TypeError, ValueError):
                return 0
        unresolved = [fp for fp in data["伏笔列表"]
                      if status(fp) == "未回收" and dnum(fp) and ch > dnum(fp)]
        overdue = [fp for fp in data["伏笔列表"]
                   if status(fp) == "未回收" and dnum(fp) and dnum(fp) <= ch <= dnum(fp) + 2]

        if overdue:
            print("⚠ 临近回收期伏笔:")
            for fp in overdue:
                print(f"  [{fid(fp)}] 第{due(fp)}章应回收 | {summary(fp)}")
        if unresolved:
            print(f"⚠ 超期未回收伏笔 ({len(unresolved)}个):")
            for fp in unresolved:
                print(f"  [{fid(fp)}] 预期{due(fp)}章 | {summary(fp)}")
        if not overdue and not unresolved:
            print(f"第{ch}章无伏笔预警")

    elif action == "resolve":
        # 需要 argv[3]=编号, [4]=章节, [5]=回收方式，共 6 项
        if len(sys.argv) < 6:
            print("用法: resolve <伏笔编号> <回收章节> <回收方式>")
            sys.exit(1)
        fp_id = sys.argv[3]
        resolve_ch = int(sys.argv[4])
        method = sys.argv[5]

        for fp in data["伏笔列表"]:
            if fid(fp) == fp_id:
                fp["回收状态"] = "已回收"
                fp["回收章节"] = resolve_ch
                fp["回收方式"] = method
                fp_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"OK: 伏笔 {fp_id} 已标记为已回收（第{resolve_ch}章）")
                return
        print(f"错误: 未找到伏笔 {fp_id}")

    else:
        print("未知操作"); print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()
