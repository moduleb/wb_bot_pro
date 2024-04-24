import asyncio

from app.utils.parser import Parser

class Scheduler:
    @staticmethod
    async def _loop(item):
        while True:
            await Parser.check_price(item)
            await asyncio.sleep(2)
    
    @staticmethod
    async def start_task(item):
        await asyncio.create_task(Scheduler._loop(item), name=item._id)
    
    @staticmethod
    async def get_all_tasks():
        return [task.get_name() for task in asyncio.all_tasks()]
    
    @staticmethod
    async def stop_task(task_name):
        for task in asyncio.all_tasks():
            if task.get_name() == str(task_name):
                task.cancel()
                return