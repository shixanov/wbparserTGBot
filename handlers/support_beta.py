from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import GROUP_ID

router = Router()

class SendMessageState(StatesGroup):
    waiting_for_text = State()

@router.callback_query(lambda c: c.data == "support_beta")
async def support_beta_callback(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Напишите сообщение, которое хотите передать в поддержку:")
    await state.set_state(SendMessageState.waiting_for_text)

@router.message(SendMessageState.waiting_for_text)
async def send_to_group(message: types.Message, state: FSMContext):
    try:
        await message.bot.send_message(
            chat_id=GROUP_ID,
            text=f"Сообщение от пользователя @{message.from_user.username}: {message.text}"
        )
        await message.answer("Сообщение успешно отправлено в поддержку!")
    except Exception as e:
        await message.answer(f"Ошибка при отправке: {e}")
    finally:
        await state.clear()
