from dataclasses import dataclass

from app.repositories import TaskRepository
from app.schemas import TaskSchema, TaskCreateSchema
from app.exceptions import TaskNotFound


@dataclass
class TaskService:
    task_repository: TaskRepository

    async def get_tasks(self) -> list[TaskSchema]:

        tasks = await self.task_repository.get_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]

        return tasks_schema

    async def create_task(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = await self.task_repository.create_task(body, user_id)
        task = await self.task_repository.get_task_by_id(task_id)
        return TaskSchema.model_validate(task)

    async def update_task_name(self, task_id: int, name: str, user_id: int) -> TaskSchema:

        task = await self.task_repository.get_user_task(user_id, task_id)
        if not task:
            raise TaskNotFound

        task = await self.task_repository.update_task_name(task_id, name, user_id)
        return TaskSchema.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:

        task = await self.task_repository.get_user_task(user_id, task_id)
        if not task:
            raise TaskNotFound

        await self.task_repository.delete_task(task_id, user_id)
