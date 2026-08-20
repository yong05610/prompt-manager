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

def ensure_favorite_field(prompts):
    """모든 프롬프트에 favorite 필드가 없으면 False로 채워준다"""
    changed = False
    for p in prompts:
        if "favorite" not in p:      # favorite 키가 없는 경우
            p["favorite"] = False    # 기본값 False로 추가
            changed = True
    if changed:                      # 하나라도 바뀌었으면
        save_prompts(prompts)        # 파일에 저장     

def add_prompt(prompts):
    print("\n=== 프롬프트 추가 ===")
    title = input("제목: ").strip()
    content = input("내용: ").strip()
    category = input("카테고리: ").strip()

    if not title or not content:
        print("❌ 제목과 내용은 필수입니다!")
        return
    new_id = max([p["id"] for p in prompts], default=0) + 1
    prompt = {
        "id": new_id,
        "title": title,
        "content": content,
        "category": category,
        "favorite" : False,
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


def toggle_favorite(prompts):
    ensure_favorite_field(prompts)

    if not prompts:
        print("\n등록된 프롬프트가 없습니다.")
        return

    print("\n=== 즐겨찾기 추가/해제 ===")

    for i, prompt in enumerate(prompts, start=1):
        star = "★" if prompt.get("favorite") else "☆"
        title = prompt.get("title", "제목 없음")
        category = prompt.get("category", "미분류")

        print(f"{i}. {star} [{category}] {title}")

    try:
        choice = int(input("\n즐겨찾기 추가/해제할 번호를 입력하세요: "))

        if choice < 1 or choice > len(prompts):
            print("잘못된 번호입니다.")
            return

        selected_prompt = prompts[choice - 1]
        selected_prompt["favorite"] = not selected_prompt.get("favorite", False)

        if selected_prompt["favorite"]:
            print(f"'{selected_prompt.get('title', '제목 없음')}' 프롬프트가 즐겨찾기에 추가되었습니다.")
        else:
            print(f"'{selected_prompt.get('title', '제목 없음')}' 프롬프트가 즐겨찾기에서 해제되었습니다.")

    except ValueError:
        print("숫자를 입력해주세요.")


def show_favorite_prompts(prompts):
    ensure_favorite_field(prompts)

    favorite_prompts = [
        prompt for prompt in prompts
        if prompt.get("favorite") == True
    ]

    print("\n=== 즐겨찾기 목록 ===")

    if not favorite_prompts:
        print("즐겨찾기한 프롬프트가 없습니다.")
        return

    for i, prompt in enumerate(favorite_prompts, start=1):
        title = prompt.get("title", "제목 없음")
        content = prompt.get("content", "내용 없음")
        category = prompt.get("category", "미분류")

        print(f"\n{i}. ★ [{category}] {title}")
        print(f"내용: {content}")        

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
        print("7. 즐겨찾기 추가/해제")
        print("8. 즐겨찾기 목록")
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
        elif choice == "7":
             toggle_favorite(prompts)
        elif choice == "8":
            show_favorite_prompts(prompts)            
        elif choice == "0":
            print("👋 프로그램을 종료합니다.")
            break
        else:
            print("❌ 잘못된 입력입니다.")

if __name__ == "__main__":
    main()