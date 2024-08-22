msg = text.price_changed.format(
    old_price=item.price,
    new_price=new_price,
    title=item.title
)

# bot.send_message(chat_id=item.user_id, text=msg)