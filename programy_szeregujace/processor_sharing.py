from random import choice
from typing import Optional


class Task:

    def __init__(self, id: int, start_time: int, duration: int, progress: int = 0) -> None:
        self.id = id
        self.start = start_time
        self.duration = duration
        self.progress = progress
        self.end_cycle: Optional[int] = None

    def add_compute_time(self, time: float, cycle: int) -> int:
        self.progress += time
        delta = 0

        if self.duration < self.progress:
            delta = self.progress - self.duration
            self.progress = self.duration

        if self.progress == self.duration:
            self.end_cycle = cycle

        return delta

    @property
    def is_done(self):
        return self.duration == self.progress

    @property
    def real_duration(self):
        return self.end_cycle - self.start + 1

    def __repr__(self):
        return f"Task {self.id}: Start: {self.start} - End {self.end_cycle}"


class Node:
    def __init__(self) -> None:
        self.tasks: list[Task] = []
        self.completed_tasks: list[Task] = []

    @property
    def active_tasks(self) -> int:
        return len(self.tasks)

    def mark_completed(self) -> None:
        new_completed = [task for task in self.tasks if task.is_done]
        self.tasks = [task for task in self.tasks if task not in new_completed]
        self.completed_tasks.extend(new_completed)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


def least_busy(nodes: list[Node]) -> Node:
    assert len(nodes) > 0
    wining_nodes = [nodes[0]]
    for node in nodes[1:]:

        if node.active_tasks < wining_nodes[0].active_tasks:
            wining_nodes = [node]
        elif node.active_tasks == wining_nodes[0].active_tasks:
            wining_nodes.append(node)

    return choice(wining_nodes)
