import json
import os
from datetime import datetime

SAVE_FILE = "prompts.json"

def load_prompts():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_prompts(prompts):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)

def add_prompt(prompts):
    print("\n=== 프롬프트 추가 ===")
    title = input("제목: ").strip()
    content = input("내용: ").strip()
    category = input("카테고리: ").strip()

    if not title or not content:
        print("❌ 제목과 내용은 필수입니다!")
        return

    prompt = {
        "id": len(prompts) + 1,
        "title": title,
        "content": content,
        "category": category,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    prompts.append(prompt)
    save_prompts(prompts)
    print("✅ 프롬프트가 추가되었습니다!")

def list_prompts(prompts):
    print("\n=== 프롬프트 목록 ===")

    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return

    for p in prompts:
        print(f"[{p['id']}] {p['title']} | {p['category']} | {p['created_at']}")

def search_prompt(prompts):
    print("\n=== 프롬프트 검색 ===")
    keyword = input("검색어: ").strip()

    results = [
        p for p in prompts
        if keyword in p['title'] or keyword in p['content'] or keyword in p['category']
    ]

    if not results:
        print("❌ 검색 결과가 없습니다.")
        return

    for p in results:
        print(f"[{p['id']}] {p['title']} | {p['category']}")
        print(f"    내용: {p['content']}")

def view_prompt(prompts):
    list_prompts(prompts)

    try:
        pid = int(input("\n상세 볼 ID: "))
        target = next((p for p in prompts if p['id'] == pid), None)

        if not target:
            print("❌ 해당 ID가 없습니다.")
            return

        print("\n=== 상세 보기 ===")
        print(f"ID       : {target['id']}")
        print(f"제목     : {target['title']}")
        print(f"카테고리 : {target['category']}")
        print(f"내용     : {target['content']}")
        print(f"생성일   : {target['created_at']}")

    except ValueError:
        print("❌ 숫자를 입력하세요.")

def list_by_category(prompts):
    print("\n=== 📂 카테고리별 보기 ===")

    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return

    categories = list(set(p['category'] for p in prompts))

    print("카테고리 목록:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")

    keyword = input("\n카테고리 입력: ").strip()

    results = [p for p in prompts if p['category'] == keyword]

    if not results:
        print("❌ 해당 카테고리가 없습니다.")
        return

    for p in results:
        print(f"[{p['id']}] {p['title']} | {p['created_at']}")

def delete_prompt(prompts):
    list_prompts(prompts)

    try:
        pid = int(input("\n삭제할 ID: "))
        target = next((p for p in prompts if p['id'] == pid), None)

        if not target:
            print("❌ 해당 ID가 없습니다.")
            return

        prompts.remove(target)
        save_prompts(prompts)
        print("✅ 삭제되었습니다!")

    except ValueError:
        print("❌ 숫자를 입력하세요.")

def main():
    prompts = load_prompts()

    while True:
        print("\n==============================")
        print("  🟨  프롬프트 관리 프로그램")
        print("==============================")
        print("1. 프롬프트 추가")
        print("2. 프롬프트 목록 보기")
        print("3. 카테고리별 보기")
        print("4. 프롬프트 검색")
        print("5. 프롬프트 상세보기")
        print("6. 프롬프트 삭제")
        print("0. 종료")
        print("------------------------------")

        choice = input("선택: ").strip()

        if choice == "1":
            add_prompt(prompts)
        elif choice == "2":
            list_prompts(prompts)
        elif choice == "3":
            list_by_category(prompts)
        elif choice == "4":
            search_prompt(prompts)
        elif choice == "5":
            view_prompt(prompts)
        elif choice == "6":
            delete_prompt(prompts)
        elif choice == "0":
            print("👋 프로그램을 종료합니다.")
            break
        else:
            print("❌ 잘못된 입력입니다.")

if __name__ == "__main__":
    main()