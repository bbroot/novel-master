"""
init_book.py - 创建新小说项目结构
用法: python init_book.py <书名> [作者名]
"""
import os
import sys
import json
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("用法: python init_book.py <书名> [作者名]")
        sys.exit(1)
    
    book_name = sys.argv[1].strip()
    author = sys.argv[2].strip() if len(sys.argv) > 2 else ""
    
    # 创建项目根目录
    base_dir = Path.home() / ".qclaw" / "workspace" / "novels" / book_name
    dirs = [
        base_dir / "settings" / "characters",
        base_dir / "outline",
        base_dir / "chapters",
        base_dir / "tracker",
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    # 创建 state.json
    state = {
        "book": book_name,
        "author": author,
        "current_arc": 1,
        "current_chapter": 0,
        "total_words": 0,
        "unresolved_foreshadowing": 0,
        "last_updated": "",
        "status": "drafting"
    }
    
    # 创建伏笔追踪
    foreshadowing = {"伏笔列表": []}
    
    # 创建冲突记录
    conflicts = {"冲突列表": []}
    
    # 写文件
    (base_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / "tracker" / "foreshadowing.json").write_text(json.dumps(foreshadowing, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / "tracker" / "conflicts.json").write_text(json.dumps(conflicts, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / "tracker" / "style-log.md").write_text(f"# 文风日志 - {book_name}\n\n## 记录\n", encoding="utf-8")
    (base_dir / "settings" / "world.md").write_text(f"# 世界观设定 - {book_name}\n\n", encoding="utf-8")
    (base_dir / "outline" / "arc-outline.md").write_text(f"# 分卷大纲 - {book_name}\n\n", encoding="utf-8")
    
    print(f"OK: 项目已创建于 {base_dir}")
    print(f"下一步：请使用 novel-master skill 开始创作策划书")

if __name__ == "__main__":
    main()
