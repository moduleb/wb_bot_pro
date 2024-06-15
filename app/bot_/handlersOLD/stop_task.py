# from aiogram import F, Router
# from aiogram.fsm.context import FSMContext
# from aiogram.types import CallbackQuery
#
# from app.bot_ import kb
# from app.bot_.states import StateClass
#
# from app.utils.sheduler import Scheduler
#
# router = Router()
#
#
# @router.callback_query(F.data == "choose_task_to_stop")
# async def choose_task_to_stop(clbck: CallbackQuery, state: FSMContext):
#     all_tasks = Scheduler.get_all_tasks()
#     kb_info = {}
#     i = 1
#     for taskname in all_tasks:
#         kb_info[i] = taskname
#         i += 1
#     await state.update_data(kb_info=kb_info)
#     await clbck.message.answer("Выберите товар, для остановки", reply_markup=kb.all_tasks(kb_info))
#     await state.set_state(StateClass.wait_for_choose_task_to_stop)
#
#
# @router.callback_query(lambda c: c.data and c.data.startswith("confirm_stop_task_"))
# # @router.callback_query(F.data == "stop_task_confirm")
# async def stop_task_confirm(clbck: CallbackQuery, state: FSMContext):
#     task_id = clbck.data.split("_")[-1]  # Извлекаем task_id из callback_data
#     data = await state.get_data()
#     taskname = data.get("kb_info").get(int(task_id))
#     await state.set_state(StateClass.wait_for_stop_confirm)
#     await clbck.message.answer(f"Вы действительно хотите остановить задачу\n{taskname}?",
#                                reply_markup=kb.iexit_kb_stop(task_id))
#
#
# @router.callback_query(lambda c: c.data and c.data.startswith("stop_task"))
# # @router.callback_query(F.data == "stop_task")
# async def stop_task(clbck: CallbackQuery, state: FSMContext):
#     task_id = clbck.data.split("_")[-1]  # Извлекаем task_id из callback_data
#     data = await state.get_data()
#     taskname = data.get("kb_info").get(int(task_id))
#     await Scheduler.stop_task(taskname)
#     await clbck.message.answer("ok")
#     await state.clear()
