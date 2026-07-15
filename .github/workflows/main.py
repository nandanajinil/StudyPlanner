import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class StudyPlannerApp(App):

    def on_start(self):
        self.load_tasks()

    def load_tasks(self):

        self.root.ids.task_list.clear_widgets()

        if not os.path.exists("tasks.json"):
            self.update_dashboard()
            return

        try:

            with open("tasks.json", "r") as file:
                tasks = json.load(file)

            for item in tasks:

                self.create_task_widget(
                    item["task"],
                    item["subject"],
                    item.get("priority", "Medium"),
                    item.get("due_date", ""),
                    item.get("completed", False)
                )

            self.update_dashboard()

        except Exception as e:
            print(e)

    def create_task_widget(
            self,
            task,
            subject,
            priority,
            due_date,
            completed
    ):

        row = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint_y=None,
            height=50
        )

        status = "✓" if completed else "☐"

        task_label = Label(
            text=f"{status} [{priority}] {task}\n{subject} | Due: {due_date}",
            halign="left",
            valign="middle",
            color=(0,0,0,1)
        )

        task_label.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        complete_btn = Button(
            text="Done",
            size_hint_x=0.16,
            height=40,
            background_normal="",
            background_color=(0.18, 0.72, 0.32, 1),
            color=(1,1,1,81)
        )

        delete_btn = Button(
            text="Delete",
            size_hint_x=0.25,
            background_normal="",
            height=40,
            background_color=(1,0.25,0.25,1),
            color=(1,1,1,1)
        )

        complete_btn.bind(
            on_press=lambda x:
            self.complete_task(
                task,
                subject
            )
        )

        delete_btn.bind(
            on_press=lambda x:
            self.delete_task(
                row,
                task,
                subject
            )
        )

        row.add_widget(task_label)
        row.add_widget(complete_btn)
        row.add_widget(delete_btn)

        self.root.ids.task_list.add_widget(row)

    def update_dashboard(self):

        total = len(self.root.ids.task_list.children)
        completed = 0

        for row in self.root.ids.task_list.children:

            label = row.children[2]

            if "✓" in label.text:
                completed += 1

        pending = total - completed

        self.root.ids.total_tasks.text = (
            f"Total:{total}"
        )

        self.root.ids.completed_tasks.text = (
            f"Completed:{completed}"
        )

        self.root.ids.pending_tasks.text = (
            f"Pending:{pending}"
        )

    def add_task(self):

        task = self.root.ids.task_name.text.strip()
        subject = self.root.ids.subject_name.text.strip()
        priority = self.root.ids.priority.text
        due_date = self.root.ids.due_date.text.strip()

        if (
            task == "" or
            subject == "" or
            priority == "Select Priority" or
            due_date == ""
        ):

            Popup(
                title="Error",
                content=Label(
                    text="Please fill all fields."
                ),
                size_hint=(0.6, 0.3),
                
            ).open()

            return

        new_task = {
            "task": task,
            "subject": subject,
            "priority": priority,
            "due_date": due_date,
            "completed": False
        }

        tasks = []

        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r") as file:
                    tasks = json.load(file)
            except:
                tasks = []

        tasks.append(new_task)

        with open("tasks.json", "w") as file:
            json.dump(tasks, file, indent=4)

        self.create_task_widget(
            task,
            subject,
            priority,
            due_date,
            False
        )

        self.update_dashboard()

        self.root.ids.task_name.text = ""
        self.root.ids.subject_name.text = ""
        self.root.ids.priority.text = "Select Priority"
        self.root.ids.due_date.text = ""

        Popup(
            title="Success",
            content=Label(
                text="Task Added Successfully!"
            ),
            size_hint=(0.6, 0.3)
        ).open()


    def delete_task(self, row, task, subject):

        self.root.ids.task_list.remove_widget(row)

        if os.path.exists("tasks.json"):

            with open("tasks.json", "r") as file:
                tasks = json.load(file)

            tasks = [
                t for t in tasks
                if not (
                    t["task"] == task and
                    t["subject"] == subject
                )
            ]

            with open("tasks.json", "w") as file:
                json.dump(tasks, file, indent=4)

        self.update_dashboard()


    def complete_task(self, task, subject):

        if os.path.exists("tasks.json"):

            with open("tasks.json", "r") as file:
                tasks = json.load(file)

            for item in tasks:

                if (
                    item["task"] == task and
                    item["subject"] == subject
                ):
                    item["completed"] = True

            with open("tasks.json", "w") as file:
                json.dump(tasks, file, indent=4)

        self.load_tasks()


    def show_statistics(self):

        if not os.path.exists("tasks.json"):
            return

        with open("tasks.json", "r") as file:
            tasks = json.load(file)

        total = len(tasks)
        completed = len(
            [t for t in tasks if t.get("completed", False)]
        )
        pending = total - completed

        print("\n----- STUDY PLANNER -----")
        print("Total Tasks     :", total)
        print("Completed Tasks :", completed)
        print("Pending Tasks   :", pending)
        print("-------------------------\n")


StudyPlannerApp().run()