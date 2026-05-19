import os
import json
import random
import string
import logging
import asyncio
import datetime
import uuid
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, ReplyKeyboardRemove

logging.basicConfig(level=logging.INFO)

TOKEN = "8200641951:AAGRGbyzc4x2Xz4BLvdtJfCfiD_1DYP-6Lo"
BOSS_LINK = "https://t.me/HOANGTUNGS8"
BOSS_ID = 7616985896

# MẬT KHẨU KHỞI CHẠY BAN ĐẦU (Viết hoa toàn bộ)
current_password = "HARRY2005TDZ"

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()

users_vip = set()
user_tables = {}
pending_orders = {}
blink_tasks = {}

# Bộ nhớ đếm số lần bấm nút Inline của khách
user_click_counters = {}

def get_banner():
    if os.path.exists("banner.jpg"):
        return FSInputFile("banner.jpg")
    return None

def generate_random_password():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

# Hàm kiểm tra giới hạn 10 lượt bấm nút lệnh của khách
async def check_user_click_limit(call: types.CallbackQuery) -> bool:
    uid = call.from_user.id
    if uid not in users_vip:
        return False
        
    # Cứ khách bấm bất kỳ nút tương tác lệnh nào, tăng bộ đếm lên 1
    user_click_counters[uid] = user_click_counters.get(uid, 0) + 1
    
    # Nếu vượt quá 10 lượt bấm nút
    if user_click_counters[uid] > 10:
        users_vip.discard(uid)  # Khóa VIP
        user_click_counters.pop(uid, None)  # Xóa bộ đếm
        
        # Thu hồi/Xóa toàn bộ các nút bấm Inline bên dưới tin nhắn hiện tại
        try:
            await call.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass
            
        # Gửi thông báo hết hạn bắt khách liên hệ Admin cấp mã
        await call.message.answer(
            f"❌ <b>HẾT LƯỢT SỬ DỤNG VIP CÔNG NGHỆ!</b>\n"
            f"————————————————━━\n"
            f"⚠️ Tài khoản của bạn đã hết 10 lượt bấm lệnh trải nghiệm.\n"
            f"🚀 Vui lòng liên hệ Telegram Boss để được cấp lại mật khẩu mới:\n"
            f"👑 TELEGRAM BOSS: <a href='{BOSS_LINK}'>@HOANGTUNGS8</a>",
            disable_web_page_preview=True
        )
        return False
    return True

def man_hinh_khoa():
    return f"""
<b>👑💎 CHÀO MỪNG BẠN ĐÃ ĐẾN VỚI 💎👑</b>
<b>🤖 AI GPT BACCARAT VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>🔐 TÀI KHOẢN CHƯA ĐƯỢC KÍCH HOẠT</b>

<b>💠 BẠN CẦN MÃ VIP ĐỂ MỞ KHÓA HỆ THỐNG</b>
<b>🚀 LIÊN HỆ TELEGRAM ĐỂ NHẬN MÃ KÍCH HOẠT</b>

<b>👑 TELEGRAM BOSS:</b>
<b><a href="{BOSS_LINK}">@HOANGTUNGS8</a></b>

<b>━━━━━━━━━━━━━━━━━━━━</b>
<b>💎 NHẬP MÃ KÍCH HOẠT VÀO KHUNG CHAT</b>
"""

def menu_chon_sanh():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏛️ CHỌN SẢNH", callback_data="show_rooms")],
            [InlineKeyboardButton(text="👑 LIÊN HỆ TELEGRAM", url=BOSS_LINK)]
        ]
    )

def menu_bat_dau():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 BẮT ĐẦU", callback_data="start_ai")],
            [InlineKeyboardButton(text="🎲 ĐỔI BÀN", callback_data="show_rooms")]
        ]
    )

def menu_sau_khi_vao_lenh():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 LỆNH KẾ TIẾP", callback_data="start_ai"),
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
<b>✅ KẾT QUẢ ĐÃ ĐƯỢC XÁC NHẬN</b>
<b>━━━━━━━━━━━━━━━━━━</b>

{ban_text}<b>📈 KẾT QUẢ DỰ ĐOÁN</b>
<b>━━━━━━━━━━━━━━━━━━</b>

<b>🟨 HÒA: {hoa}%</b>
<b>🟦 CON: {con}%</b>
<b>🟥 CÁI: {cai}%</b>

<b>{icon} LỆNH CHÍNH: {ket_qua}</b>

<b>🔥 ĐỘ TIN CẬY: CAO</b>
<b>⏰ THỜI GIAN: {now}</b>

<b>━━━━━━━━━━━━━━━━━━</b>
<b>👑 LIÊN HỆ TELEGRAM:</b>
<b><a href="{BOSS_LINK}">@HOANGTUNGS8</a></b>
"""

async def gui_man_hinh_khoa(msg):
    banner = get_banner()
    if banner:
        await msg.answer_photo(photo=banner, caption=man_hinh_khoa(), reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer(man_hinh_khoa(), disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())

async def gui_man_hinh_vip(msg):
    banner = get_banner()
    text = """
<b>✅ KÍCH HOẠT THÀNH CÔNG VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>👑 TÀI KHOẢN ĐÃ ĐƯỢC MỞ KHÓA</b>
<b>🎯 HỆ THỐNG AI VIP ĐÃ SẴN SÀNG</b>
<b>🔥 GIAO DIỆN PHÂN TÍCH CAO CẤP</b>

<b>💎 VUI LÒNG CHỌN SẢNH ĐỂ BẮT ĐẦU</b>
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
<b>✅ ĐÃ XÁC NHẬN LỆNH</b>
<b>━━━━━━━━━━━━━━━━━━</b>

<b>🤖 CHAT GPT ĐANG TÍNH TOÁN KẾT QUẢ{dot}</b>
<b>🎲 BÀN: {info["table"]}</b>

<b>⏳ VUI LÒNG CHỜ BOSS XÁC NHẬN KẾT QUẢ</b>
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

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    if user_id in users_vip:
        await message.answer(
            """
<b>👑 AI GPT BACCARAT VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>💎 VUI LÒNG CHỌN SẢNH ĐỂ BẮT ĐẦU</b>
""",
            reply_markup=menu_chon_sanh()
        )
        return
    await gui_man_hinh_khoa(message)

@dp.message()
async def handle_text_message(msg: types.Message):
    global current_password
    user_id = msg.from_user.id
    text = msg.text.strip() if msg.text else ""

    if user_id not in users_vip:
        # Nếu khách nhập chính xác mật khẩu đang có trên hệ thống
        if text == current_password:
            users_vip.add(user_id)
            user_click_counters[user_id] = 0 # Khởi tạo bộ đếm bấm nút bằng 0
            
            # 1. Gửi màn hình kích hoạt VIP thành công kèm ảnh nền cũ
            await gui_man_hinh_vip(msg)
            
            # 2. Thực hiện đổi mã kích hoạt ngẫu nhiên ngay lập tức
            old_pass = current_password
            current_password = generate_random_password()
            
            # 3. Bắn thẳng thông báo mật khẩu mới về máy của bạn (Boss)
            try:
                await bot.send_message(
                    chat_id=BOSS_ID,
                    text=f"🔔 <b>THÔNG BÁO HỆ THỐNG AI BACCARAT</b>\n\n"
                         f"👤 Khách hàng vừa nhập đúng mã: <b>{old_pass}</b>\n"
                         f"🔑 Hệ thống đã tự động đổi mã VIP ngẫu nhiên mới: <b>{current_password}</b>\n"
                         f"👉 Hãy lưu lại mã mới này để cấp cho khách tiếp theo!"
                )
            except Exception as e:
                logging.error(f"Lỗi gửi tin nhắn mật khẩu về cho Boss: {e}")
            return

        await gui_man_hinh_khoa(msg)
        return

    await msg.answer(
        """
<b>👑 AI GPT BACCARAT VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>💎 VUI LÒNG CHỌN SẢNH ĐỂ BẮT ĐẦU</b>
""",
        reply_markup=menu_chon_sanh()
    )

@dp.callback_query()
async def callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    data = call.data

    # Xử lý nút duyệt lệnh của Boss (Không tính vào lượt bấm của khách)
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
<b>✅ BOSS ĐÃ XÁC NHẬN KẾT QUẢ</b>

<b>🎲 BÀN: {info["table"]}</b>
<b>📌 KẾT QUẢ: {ket_qua}</b>
"""
        )
        await call.answer("Đã gửi kết quả về nhóm.")
        return

    # Nếu người lạ cố tình bấm nút
    if user_id not in users_vip:
        await call.answer("🔐 VUI LÒNG KÍCH HOẠT VIP TRƯỚC")
        banner = get_banner()
        if banner:
            await call.message.answer_photo(photo=banner, caption=man_hinh_khoa(), reply_markup=ReplyKeyboardRemove())
        else:
            await call.message.answer(man_hinh_khoa(), disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
        return

    # KIỂM TRA GIỚI HẠN LƯỢT BẤM CỦA KHÁCH (Nếu bấm nút thứ 11 sẽ bị khóa ngay tại đây)
    if not await check_user_click_limit(call):
        await call.answer("❌ Đã hết lượt dùng VIP!")
        return

    # TOÀN BỘ LOGIC DI CHUYỂN ROOM/BÀN CŨ ĐƯỢC GIỮ NGUYÊN VẸN 100%
    if data == "show_rooms":
        await call.answer("🏛️ ĐANG MỞ DANH SÁCH SẢNH...")
        await call.message.answer(
            """
<b>🏛️ HỆ THỐNG SẢNH AI VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>✨ VUI LÒNG CHỌN SẢNH ĐỂ TIẾP TỤC</b>
<b>🎯 AI ĐANG ĐỒNG BỘ DỮ LIỆU...</b>
""",
            reply_markup=room_menu()
        )
        return

    if data == "room_sexy":
        await call.answer("🔥 ĐÃ CHỌN SẢNH SEXY")
        await call.message.answer(
            """
<b>🔥 SẢNH SEXY VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>🎯 VUI LÒNG CHỌN BÀN</b>
""",
            reply_markup=sexy_table_menu()
        )
        return

    if data == "room_dg":
        await call.answer("💎 ĐÃ CHỌN SẢNH DG")
        await call.message.answer(
            """
<b>💎 SẢNH DG VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>⚠️ SẢNH NÀY ĐANG ĐƯỢC CẬP NHẬT</b>
<b>🔥 VUI LÒNG CHỌN SẢNH SEXY ĐỂ SỬ DỤNG TRƯỚC</b>
""",
            reply_markup=menu_chon_sanh()
        )
        return

    if data == "room_mt":
        await call.answer("⚡ ĐÃ CHỌN SẢNH MT")
        await call.message.answer(
            """
<b>⚡ SẢNH MT VIP</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>⚠️ SẢNH NÀY ĐANG ĐƯỢC CẬP NHẬT</b>
<b>🔥 VUI LÒNG CHỌN SẢNH SEXY ĐỂ SỬ DỤNG TRƯỚC</b>
""",
            reply_markup=menu_chon_sanh()
        )
        return

    if data.startswith("table_"):
        ten_ban = data.replace("table_", "")
        user_tables[user_id] = f"SẢNH SEXY BÀN {ten_ban}"
        await call.answer("✅ CHỌN BÀN THÀNH CÔNG")
        await call.message.edit_reply_markup(reply_markup=menu_bat_dau())
        return

    if data == "start_ai":
        if user_id not in user_tables:
            await call.answer("🎲 VUI LÒNG CHỌN BÀN TRƯỚC")
            await call.message.answer(
                """
<b>⚠️ BẠN CHƯA CHỌN BÀN</b>
<b>━━━━━━━━━━━━━━━━━━━━</b>

<b>🎲 VUI LÒNG CHỌN SẢNH VÀ CHỌN BÀN TRƯỚC KHI BẮT ĐẦU</b>
""",
                reply_markup=menu_chon_sanh()
            )
            return

        request_id = uuid.uuid4().hex[:8]
        table_name = user_tables[user_id]

        wait_msg = await call.message.answer(
            f"""
<b>✅ ĐÃ XÁC NHẬN LỆNH</b>
<b>━━━━━━━━━━━━━━━━━━</b>

<b>🤖 CHAT GPT ĐANG TÍNH TOÁN KẾT QUẢ...</b>
<b>🎲 BÀN: {table_name}</b>

<b>⏳ VUI LÒNG CHỜ BOSS XÁC NHẬN KẾT QUẢ</b>
"""
        )

        pending_orders[request_id] = {
            "chat_id": call.message.chat.id,
            "message_id": wait_msg.message_id,
            "user_id": user_id,
            "table": table_name
        }

        blink_tasks[request_id] = asyncio.create_task(blink_waiting_message(request_id))

        try:
            await bot.send_message(
                chat_id=BOSS_ID,
                text=f"""
<b>📩 CÓ LỆNH MỚI CẦN XÁC NHẬN</b>
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
<b>⚠️ CHƯA GỬI ĐƯỢC TIN NHẮN CHO BOSS</b>

<b>Boss cần nhắn /start riêng với bot trước.</b>
"""
            )

        await call.answer("✅ ĐÃ GỬI LỆNH CHỜ BOSS XÁC NHẬN")
        return

async def main():
    print("BOT AI GPT BACCARAT VIP ĐANG CHẠY TRÊN RAILWAY...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
