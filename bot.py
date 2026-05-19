from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
import asyncio
import random
import datetime
import uuid
import os

TOKEN = os.environ.get("TOKEN", "8200641951:AAGRGbyzc4x2Xz4BLvdtJfCfiD_1DYP-6Lo")
BOSS_LINK = "https://t.me/HOANGTUNGS8"
BOSS_ID = int(os.environ.get("BOSS_ID", "7616985896"))
MA_KICH_HOAT = os.environ.get("MA_KICH_HOAT", "GPT666888")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()

users_vip = set()
user_tables = {}
pending_orders = {}
blink_tasks = {}

def get_banner():
    if os.path.exists("banner.jpg"):
        return FSInputFile("banner.jpg")
    return None
def man_hinh_khoa():
    return f"""
<b>👑💎 CHÀO MỮNG BẠN ĐÃ ĐẾN VỚI 💎👑</b>
<b>🤖 AI GPT BACCARAT VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>🔐 TÀI KHOẢN CHƯA ĐƯỢC KÍCH HOẠT</b>

<b>🐠 BẠN CẦN MÃ VIP ĐỂ MỜ KHÓA HỆ THỐNG</b>
<b>🚀 LIÊN HỆ TELEGRAM ĐỂ NHẪN MÃ KÍCH HOẠT</b>

<b>👑 TELEGRAM BOSS:</b>
<b><a href="{BOSS_LINK}">@HOANGTUNGS8</a></b>

<b>━━━━━━━━━━━━━━━━━━━━</b>
<b>💎 NHẪP MÃ KÍCH HOẠT VÀO KHUNG CHAT</b>
"""
def menu_chon_sanh():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏛️ CHẬN SẢNH", callback_data="show_rooms")],
            [InlineKeyboardButton(text="👑 LIÊN HỆ TELEGRAM", url=BOSS_LINK)]
        ]
    )

def menu_bat_dau():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 BắT ĐẦU", callback_data="start_ai")],
            [InlineKeyboardButton(text="🎲 ĐỔI BÀN", callback_data="show_rooms")]
        ]
    )

def menu_sau_khi_vao_lenh():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 LỆNH KẾP TIẾP", callback_data="start_ai"),
                InlineKeyboardButton(text="🎲 ĐỔI BÀN", callback_data="show_rooms")
            ],
            [InlineKeyboardButton(text="👑 LIÊN HỆ TELEGRAM", url=BOSS_LINK)]
        ]
    )

def room_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔥 SẢNH SEXY", callback_data="room_sexy")],
            [InlineKeyboardButton(text="💎 SẢNH DG", callback_data="room_dg")],
            [InlineKeyboardButton(text="⚡ SẢNH MT", callback_data="room_mt")]
        ]
    )
def sexy_table_menu():
    buttons = []
    row = []

    for i in range(1, 16):
        row.append(
            InlineKeyboardButton(
                text=f"🎲 C{i:02}",
                callback_data=f"table_C{i:02}"
            )
        )

        if len(row) == 3:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def boss_confirm_menu(request_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟦 CON", callback_data=f"boss_result:{request_id}:CON"),
                InlineKeyboardButton(text="🟥 CÁI", callback_data=f"boss_result:{request_id}:CAI"),
                InlineKeyboardButton(text="🟨 HÒA", callback_data=f"boss_result:{request_id}:HOA")
            ]
        ]
    )
def ket_qua_xac_nhan(user_id, ket_qua):
    now = datetime.datetime.now().strftime("%H:%M:%S")

    ban_text = ""
    if user_id in user_tables:
        ban_text = f"<b>🎲 BÀN HIỆN TẠI: {user_tables[user_id]}</b>\n"

    if ket_qua == "CON":
        hoa = random.randint(3, 15)
        con = random.randint(75, 92)
        cai = random.randint(10, 30)
        icon = "🟦"
    elif ket_qua == "CAI":
        hoa = random.randint(3, 15)
        con = random.randint(10, 30)
        cai = random.randint(75, 92)
        icon = "🟥"
    else:
        hoa = random.randint(35, 55)
        con = random.randint(25, 45)
        cai = random.randint(25, 45)
        icon = "🟨"

    return f"""
<b>✅ KẾT QUẢ ĐÃ ĐƯỢC XÁC NHẪN</b>
<b>━━━━━━━━━━━━━━━━━━</b>

{ban_text}<b>📈 KẾT QUẢ DỰ ĐOÁN</b>
<b>━━━━━━━━━━━━━━━━━━</b>

<b>🟨 HÒA: {hoa}%</b>
<b>🟦 CON: {con}%</b>
<b>🟥 CÁI: {cai}%</b>

<b>{icon} LỆNH CHÍNH: {ket_qua}</b>

<b>🔥 ĐỘ TIN CẪy: CAO</b>
<b>⏰ THỚI GIAN: {now}</b>

<b>━━━━━━━━━━━━━━━━━━</b>
<b>👑 LIÊN HỆ TELEGRAM:</b>
<b><a href="{BOSS_LINK}">@HOANGTUNGS8</a></b>
"""
async def gui_man_hinh_khoa(msg):
    await msg.answer(man_hinh_khoa(), disable_web_page_preview=True)

async def gui_man_hinh_vip(msg):
    banner = get_banner()

    text = """
<b>✅ KÍCH HOẠT THÀNH CÔNG VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>👑 TÀI KHOẢN ĐÃ ĐƯỢC MỜ KHÓA</b>
<b>🎯 HỆ THỐNG AI VIP ĐÃ SẴN SÀNG</b>
<b>🔥 GIAO DIỆN PHÂN TÍCH CAO CẤP</b>

<b>💎 VUI LÒNG CHẬN SẢNH ĐỂ BắT ĐẦU</b>
"""

    if banner:
        await msg.answer_photo(photo=banner, caption=text, reply_markup=menu_chon_sanh())
    else:
        await msg.answer(text, reply_markup=menu_chon_sanh())

async def blink_waiting_message(request_id):
    dots = ["", ".", "..", "..."]

    while request_id in pending_orders:
        info = pending_orders[request_id]

        for dot in dots:
            if request_id not in pending_orders:
                return

            text = f"""
<b>✅ ĐÃ XÁC NHẪN LỆNH</b>
<b>━━━━━━━━━━━━━━━━━━</b>

<b>🤖 CHAT GPT ĐANG TÍNH TOÁN KẾT QUẢ{dot}</b>
<b>🎲 BÀN: {info["table"]}</b>

<b>⏳ VUI LÒNG CHẨ BOSS XÁC NHẪN KẾT QUẢ</b>
"""

            try:
                await bot.edit_message_text(
                    chat_id=info["chat_id"],
                    message_id=info["message_id"],
                    text=text
                )
            except Exception:
                pass

            await asyncio.sleep(1.2)
@dp.message()
async def start(msg: types.Message):
    user_id = msg.from_user.id
    text = msg.text.strip().upper() if msg.text else ""

    if user_id not in users_vip:
        if text == MA_KICH_HOAT:
            users_vip.add(user_id)
            await gui_man_hinh_vip(msg)
            return

        await gui_man_hinh_khoa(msg)
        return

    await msg.answer(
        """
<b>👑 AI GPT BACCARAT VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>💎 VUI LÒNG CHẬN SẢNH ĐỂ BắT ĐẦU</b>
""",
        reply_markup=menu_chon_sanh()
    )
@dp.callback_query()
async def callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    data = call.data

    if data.startswith("boss_result:"):
        if user_id != BOSS_ID:
            await call.answer("Bạn không có quyền xác nhận lệnh này.")
            return

        _, request_id, ket_qua = data.split(":")

        if request_id not in pending_orders:
            await call.answer("Lệnh này đã xử lý rồi.")
            return

        info = pending_orders.pop(request_id)

        if request_id in blink_tasks:
            blink_tasks[request_id].cancel()
            del blink_tasks[request_id]

        await bot.edit_message_text(
            chat_id=info["chat_id"],
            message_id=info["message_id"],
            text=ket_qua_xac_nhan(info["user_id"], ket_qua),
            reply_markup=menu_sau_khi_vao_lenh(),
            disable_web_page_preview=True
        )

        await call.message.edit_text(
            f"""
<b>✅ BOSS ĐÃ XÁC NHẪN KẾT QUẢ</b>

<b>🎲 BÀN: {info["table"]}</b>
<b>📌 KẾT QUẢ: {ket_qua}</b>
"""
        )

        await call.answer("Đã gửi kết quả về nhóm.")
        return

    if user_id not in users_vip:
        await call.answer("🔐 VUI LÒNG KÍCH HOẠT VIP TRƯỚC")
        await call.message.answer(
            man_hinh_khoa(),
            disable_web_page_preview=True
        )
        return
    if data == "show_rooms":
        await call.answer("🏛️ ĐANG MỜ DANH SÁCH SẢNH...")

        await call.message.answer(
            """
<b>🏛️ HỆ THỐNG SẢNH AI VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>✨ VUI LÒNG CHẬN SẢNH ĐỂ TIẾP TỤC</b>
<b>🎯 AI ĐANG ĐỒNG BỘ DỬ LIỆU...</b>
""",
            reply_markup=room_menu()
        )
        return

    if data == "room_sexy":
        await call.answer("🔥 ĐÃ CHẬN SẢNH SEXY")

        await call.message.answer(
            """
<b>🔥 SẢNH SEXY VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>🎯 VUI LÒNG CHẬN BÀN</b>
""",
            reply_markup=sexy_table_menu()
        )
        return

    if data == "room_dg":
        await call.answer("💎 ĐÃ CHẬN SẢNH DG")

        await call.message.answer(
            """
<b>💎 SẢNH DG VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>⚠️ SẢNH NÀY ĐANG ĐƯỢC CẬP NHẬT</b>
<b>🔥 VUI LÒNG CHẬN SẢNH SEXY ĐỂ SỦ DỤNG TRƯỚC</b>
""",
            reply_markup=menu_chon_sanh()
        )
        return

    if data == "room_mt":
        await call.answer("⚡ ĐÃ CHẬN SẢNH MT")

        await call.message.answer(
            """
<b>⚡ SẢNH MT VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>⚠️ SẢNH NÀY ĐANG ĐƯỢC CẬP NHẬT</b>
<b>🔥 VUI LÒNG CHẬN SẢNH SEXY ĐỂ SỦ DỤNG TRƯỚC</b>
""",
            reply_markup=menu_chon_sanh()
        )
        return
    if data.startswith("table_"):
        ten_ban = data.replace("table_", "")
        user_tables[user_id] = f"SẢNH SEXY BÀN {ten_ban}"

        await call.answer("✅ CHẬN BÀN THÀNH CÔNG")

        await call.message.edit_reply_markup(
            reply_markup=menu_bat_dau()
        )
        return

    if data == "start_ai":
        if user_id not in user_tables:
            await call.answer("🎲 VUI LÒNG CHẬN BÀN TRƯỚC")
            await call.message.answer(
                """
<b>⚠️ BẠN CHƯA CHẬN BÀN</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>🎲 VUI LÒNG CHẬN SẢNH VÀ CHẬN BÀN TRƯỚC KHI BắT ĐẦU</b>
""",
                reply_markup=menu_chon_sanh()
            )
            return

        request_id = uuid.uuid4().hex[:8]
        table_name = user_tables[user_id]

        wait_msg = await call.message.answer(
            f"""
<b>✅ ĐÃ XÁC NHẪN LỆNH</b>
<b>━━━━━━━━━━━━━━━━━━</b>

<b>🤖 CHAT GPT ĐANG TÍNH TOÁN KẾT QUẢ...</b>
<b>🎲 BÀN: {table_name}</b>

<b>⏳ VUI LÒNG CHẨ BOSS XÁC NHẪN KẾT QUẢ</b>
"""
        )

        pending_orders[request_id] = {
            "chat_id": call.message.chat.id,
            "message_id": wait_msg.message_id,
            "user_id": user_id,
            "table": table_name
        }

        blink_tasks[request_id] = asyncio.create_task(
            blink_waiting_message(request_id)
        )

        try:
            await bot.send_message(
                chat_id=BOSS_ID,
                text=f"""
<b>📩 CÓ LỆNH MỚI CẦN XÁC NHẪN</b>
<b>━━━━━━━━━━━━━━━━━━</b>

<b>🎲 BÀN: {table_name}</b>
<b>👤 USER ID: {user_id}</b>

<b>Boss xem web rồi chọn kết quả bên dưới:</b>
""",
                reply_markup=boss_confirm_menu(request_id)
            )
        except Exception:
            await call.message.answer(
                """
<b>⚠️ CHƯA GỦI ĐƯỢC TIN NHắN CHO BOSS</b>

<b>Boss cần nhắn /start riêng với bot trước.</b>
"""
            )

        await call.answer("✅ ĐÃ GỦI LỆNH CHẨ BOSS XÁC NHẪN")
        return


async def main():
    print("BOT DANG CHAY...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
