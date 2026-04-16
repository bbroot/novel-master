"""
update_state.py - 更新写作状态
用法: python update_state.py <书名> <章节号> <字数> [伏笔数]
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

def main():
    if len(sys.argv) < 4:
        print("用法: python update_state.py <书名> <章节号> <字数> [伏笔数]")
        sys.exit(1)
    
    book_name = sys.argv[1]
    chapter = int(sys.argv[2])
    words = int(sys.argv[3])
    unresolved_fp = int(sys.argv[4]) if len(sys.argv) > 4 else None
    
    state_file = Path.home() / ".qclaw" / "workspace" / "novels" / book_name / "state.json"
    
    if not state_file.exists():
        print(f"错误: 未找到项目 {book_name}，请先运行 init_book.py")
        sys.exit(1)
    
    state = json.loads(state_file.read_text(encoding="utf-8"))
    
    state["current_chapter"] = chapter
    state["total_words"] += words
    state["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    if unresolved_fp is not None:
        state["unresolved_foreshadowing"] = unresolved_fp
    
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: 状态已更新 (第{chapter}章, 总字数:{state['total_words']})")

if __name__ == "__main__":
    main()
