import json

class Task:
    def __init__(self,description,task_id,priority_level):
        if len(description.strip()) == 0:
            raise ValueError("Description cannot be empty.")
        if not isinstance(task_id, int):
            raise TypeError("Task_ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task_ID must be greater than zero.")
        
        self.description = description.strip()
        self.task_id = task_id
        self.priority_level = priority_level
        self.is_completed = False

    def mark_as_completed(self):
        if not self.is_completed:
            self.is_completed = True
            print(f"Task '{self.description}' (Priority: {self.priority_level}) has been marked as complete.")
        else:
            print(f"Task '{self.description}' (Priority: {self.priority_level}) was already completed.")

    def to_dict(self):
        return {"task_id":self.task_id,"description":self.description,"is_completed":self.is_completed,"priority_level":self.priority_level}
    
    def __str__(self):
        return f"{self.task_id}. {self.priority_level} - {"[X]" if self.is_completed else "[ ]"} {self.description}"
    
class TodoList:
    def __init__(self,file_name='tasks.json'):
        self.tasks = []
        self.file_name = file_name
        self.next_id = 1
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.file_name,'r',encoding='utf-8') as f:
                data_tasks = json.load(f)
        except FileNotFoundError:
           with open(self.file_name,'x') as f:
               json.dump([],f,indent=5,ensure_ascii=False)
               data_tasks = []
        except json.decoder.JSONDecodeError:
            data_tasks = []
        
        if len(data_tasks) > 0:
            for task in data_tasks:
                task_loading = Task(task["description"],task["task_id"],task["priority_level"])
                task_loading.is_completed = task["is_completed"]
                self.tasks.append(task_loading)
                self.next_id += 1

    def save_tasks(self):
        try:
            data_to_save = [task.to_dict() for task in self.tasks]
            with open(self.file_name,'w',encoding='utf-8') as f:
                json.dump(data_to_save,f,indent=5,ensure_ascii=False)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def update_id(self):
        current_id = 1
        for task in self.tasks:
            task.task_id = current_id
            current_id += 1
        self.next_id = current_id
                
    def add_task(self,description,priority_level):
        try:
            new_task = Task(description,self.next_id,priority_level)
        except (ValueError, TypeError) as e:
            print(e)
        else:
            self.tasks.append(new_task)
            self.next_id += 1
            print(f"Task '{description}' (Priority: {priority_level}) added successfully.")

    def get_task_by_id(self,task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def mark_task_completed(self,task_id):
        task_mark = self.get_task_by_id(task_id)
        if task_mark is not None:
            task_mark.mark_as_completed()
        else:
            print(f"Task with ID {task_id} not found.")

    def delete_task(self,task_id,all_completed=False):
        if not all_completed:
            task_del = self.get_task_by_id(task_id)
            if task_del is not None:
                self.tasks.remove(task_del)
                self.update_id()
                print(f"Task '{task_del.description}' (Priority: {task_del.priority_level}) has been removed.")
            else:
                print(f"Task with ID {task_id} not found.")
        else:
            tasks = [task for task in self.tasks if task.is_completed]
            if len(tasks) > 0:
                self.tasks = [task for task in self.tasks if task not in tasks]
                self.update_id()
                print("All completed tasks deleted.")
            else:
                print("No completed tasks to delete. Get some tasks done!")

    def display_tasks(self,status):
        tasks = [task for task in self.tasks if task.is_completed == status] if status is not None else self.tasks
        if len(tasks) > 0:
            for task in tasks:
                print(task)
        else:
            if status:
                print("No completed tasks found. Get some tasks done!")
            elif status is False:
                print("No incomplete tasks found. Add some new tasks!")
            elif status is None:
                print("Your task list is empty. Add a few tasks to get started!")

def check_action_input(action):
    action_list = ["view","add","complete","delete","exit"]
    if not action.isalpha() or action not in action_list:
        raise ValueError("Invalid action. Please choose from (View/Add/Complete/Delete/Exit).")
    return action

def check_status_input(status):
    status_list = ["all","completed","incomplete"]
    if not status.isalpha() or status not in status_list:
        raise ValueError("Invalid status. Please choose from (All/Completed/Incomplete).")
    return status

def main():
    todo_list = TodoList()
    while True:
        print("How can I help you with your to-do list?")
        daft_action = input("(View/Add/Complete/Delete/Exit): ").strip().lower()
        try:
            action = check_action_input(daft_action)
        except ValueError as v:
            print(f"{v}\nPlease try again.")
            continue
        
        if action == "exit":
            todo_list.save_tasks()
            print("Have a nice day and enjoy your work!")
            break

        if action == "view":
            while True:
                draft_status = input("View tasks: (All/Completed/Incomplete)? ").strip().lower()
                try:
                    status_str = check_status_input(draft_status)
                except ValueError as v:
                    print(f"{v}\nPlease try again.")
                    continue
                break

            if status_str == "all":
                status = None
            elif status_str == "completed":
                status = True
            elif status_str == "incomplete":
                status = False

            todo_list.display_tasks(status)

        elif action == "add":
            description = input("Describe your task please: ")
            priority_levels = ["high","medium","low"]
            while True:
                priority_level = input("What is the priority level for this task? (High/Medium/Low): ").strip().lower()
                if priority_level in priority_levels:
                    break
                else:
                    print("Priority must be High, Medium, or Low.")
            
            priority_level = priority_level.capitalize()
            todo_list.add_task(description,priority_level)

        elif action == "delete":
            while True:
                print("Delete: all completed tasks or a specific task?")
                delete_type = input("(All/Single): ").strip().lower()
                if delete_type in ["all","single"]:
                    break
                else:
                    print("Please choose 'All' or 'Single'.")

            if delete_type == "all":
                todo_list.delete_task(all_completed=True)
            else:
                while True:
                    task_id_str = input("Please enter the id task: ")
                    try:
                        task_id = int(task_id_str)
                        if task_id <= 0:
                            print("ID must be greater than zero")
                            continue
                        break
                    except ValueError:
                        print("ID must be an integer.\nPlease try again.")
                
                todo_list.delete_task(task_id)
                
            
        elif action == "complete":
            while True:
                task_id_str = input("Please enter the id task: ")
                try:
                    task_id = int(task_id_str)
                    if task_id <= 0:
                        print("ID must be greater than zero")
                        continue
                    break
                except ValueError:
                    print("ID must be an integer.\nPlease try again.")
                    
            todo_list.mark_task_completed(task_id)

main()