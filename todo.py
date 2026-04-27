import json
import os
import heapq

FILE_NAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)


def build_heap(tasks):
    heap = []
    for task in tasks:
        if not task["done"]:
            # (优先级, id, task)
            heapq.heappush(heap, (task["priority"], task["id"], task))
    return heap


def add_task(tasks):
    title = input("输入任务内容: ")
    priority = int(input("输入优先级(1最高,5最低): "))

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,
        "done": False
    }

    tasks.append(task)
    save_tasks(tasks)
    print("✅ 任务已添加")


def list_tasks(tasks):
    if not tasks:
        print("📭 当前没有任务")
        return

    print("\n📋 任务列表（按优先级排序）:")

    heap = build_heap(tasks)

    while heap:
        _, _, task = heapq.heappop(heap)
        print(f"[{task['id']}] {task['title']} (优先级:{task['priority']})")

    print("\n已完成任务:")
    for task in tasks:
        if task["done"]:
            print(f"[{task['id']}] {task['title']}")


def complete_task(tasks):
    heap = build_heap(tasks)

    if not heap:
        print("没有未完成任务")
        return

    _, _, task = heapq.heappop(heap)
    task["done"] = True

    save_tasks(tasks)
    print(f"已完成最高优先级任务: {task['title']}")


def delete_task(tasks):
    task_id = int(input("输入要删除的任务ID: "))

    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(new_tasks) == len(tasks):
        print("未找到任务")
        return

    # 重新编号
    for i, task in enumerate(new_tasks):
        task["id"] = i + 1

    save_tasks(new_tasks)
    print("任务已删除")


def main():
    tasks = load_tasks()

    while True:
        print("\n==== Todo Priority CLI ====")
        print("1. 查看任务（按优先级）")
        print("2. 添加任务")
        print("3. 完成最高优先级任务")
        print("4. 删除任务")
        print("0. 退出")

        choice = input("选择操作: ")

        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
            tasks = load_tasks()
        elif choice == "3":
            complete_task(tasks)
            tasks = load_tasks()
        elif choice == "4":
            delete_task(tasks)
            tasks = load_tasks()
        elif choice == "0":
            print("再见")
            break
        else:
            print("无效输入")


if __name__ == "__main__":
    main()