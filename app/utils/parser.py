from app import text
from app.send_msg import send_msg

class Parser:
    @staticmethod
    async def check_price(item):
        await send_msg(item.user_id, "checking...")
        if new_price := item.check_price():
            msg = text.price_changed.format(
                title=item.title,
                old_price=item.price,
                new_price=new_price
            )
            await send_msg(item.user_id, msg)
            item.price = new_price
