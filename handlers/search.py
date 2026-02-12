from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.search_state import SearchState

from services.marketplaces import search_all_marketplaces
from services.history import save_query, get_user_history

from utils.limits import can_make_request, requests_left

async def show_history(call: CallbackQuery, state: FSMContext):
    history = get_user_history(call.from_user.id)
    
    if not history:
        await call.answer("История пуста 📭", show_alert=True)
        return

    text = "<b>📜 Последние запросы:</b>\n\n" + "\n".join([f"{i+1}. {q}" for i, q in enumerate(history)])
    
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Закрыть", callback_data="close_history")
    
    await call.message.answer(text, reply_markup=builder.as_markup())
    await call.answer()

async def search_start(call: CallbackQuery, state: FSMContext):
    prompt_msg = await call.message.answer("Введите название товара для поиска 🔎")
    
    await state.update_data(prompt_msg_id=prompt_msg.message_id)
    await state.set_state(SearchState.query)

async def search_process(message: Message, state: FSMContext):
    user_id = message.from_user.id 

    if not can_make_request(user_id):
        await message.answer(
            "⛔ Лимит запросов на сегодня исчерпан\n\n"
            "📅 Новый лимит будет доступен завтра"
        )
        return

    query = message.text.strip()
    save_query(user_id, query)

    try:
        await message.delete()
    except Exception:
        pass

    user_data = await state.get_data()
    history = user_data.get("history", [])

    if query not in history:
        history.append(query)

    await state.update_data(history=history[-10:])

    prompt_msg_id = user_data.get("prompt_msg_id")
    wait_msg = await message.answer(f"Ищу «{query}» на маркетплейсах... ⏳")

    try:
        if prompt_msg_id:
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=prompt_msg_id
                )
            except Exception:
                pass

        results = await search_all_marketplaces(query)

        try:
            await wait_msg.delete()
        except Exception:
            pass

        if not results:
            await message.answer(
                f"К сожалению, по запросу «{query}» ничего не нашлось 😔"
            )
            await state.clear()
            return

        response_text = f"<b>🔍 Результаты по запросу: {query}</b>\n\n"
        for r in results:
            item_name = r['item'][:60] + "..." if len(r['item']) > 60 else r['item']
            response_text += (
                f"📦 <b>{item_name}</b>\n"
                f"💰 Цена: <code>{r['price']}</code>\n"
                f"🏪 {r['marketplace']}: "
                f"<a href='{r['url']}'>🔗 Ссылка на товар</a>\n"
                f"{'—' * 20}\n"
            )

        await message.answer(
            response_text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    except Exception as e:
        print(f"Ошибка в поиске: {e}")
        try:
            await wait_msg.delete()
        except Exception:
            pass
        await message.answer(
            "Произошла ошибка при поиске. Попробуйте позже ❌"
        )

    left = requests_left(user_id)
    await message.answer(f"⏱ Осталось запросов на сегодня: {left}")

    await state.clear()



async def close_history(call: CallbackQuery):
    try:
        await call.message.delete()
    except Exception:
        await call.answer("Сообщение уже удалено или устарело")
    await call.answer()