import asyncio


class Scheduler:
    @staticmethod
    async def _loop(func, *args):
        while True:
            await func(*args)
            await asyncio.sleep(2)
    
    @staticmethod
    async def start_task(func, item, taskname):
        await asyncio.create_task(Scheduler._loop(func, item), name=taskname)
    
    @staticmethod
    def get_all_tasks():
        return [task.get_name() for task in asyncio.all_tasks() if not task.get_name().startswith("Task")]
    
    @staticmethod
    async def stop_task(taskname):
        for task in asyncio.all_tasks():
            if task.get_name() == taskname:
                task.cancel()
                print(f"Задача: {task.get_name()}, остановлена.")
                return