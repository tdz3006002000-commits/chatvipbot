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
current_password = "PGT666888"

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


async def check_user_click_limit(call: types.CallbackQuery) -> bool:
    uid = call.from_user.id
    if uid not in users_vip:
        return False

    user_click_counters[uid] = user_click_counters.get(uid, 0) + 1

    if user_click_counters[uid] > 10:
        users_vip.discard(uid)
        user_click_counters.pop(uid, None)

        try:
            await call.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass

        await call.message.answer(
            f"❌ <b>HỬT LƯỢT SọNG CÔNG NGHỆ!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ Tài khoản của bạn đã hết 10 lượt bấm lệnh trải nghiệm.\n"
            f"🚀 Vui lòng liên hệ Telegram Boss để được cấp lại mật khẩu mới:\n"
            f"👑 TELEGRAM BOSS: <a href='{BOSS_LINK}'>@HOANGTUNGS8</a>",
            disable_web_page_preview=True
        )
        return False
    return True

def man_hinh_khoa():
    return (
        "<b>👑💎 CHÀO MẬNG BẠN ĐÃ ĐẾN VỚI 💎👑</b>\n"
        "<b>🤖 AI GPT BACCARAT VIP</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>🔐 TÀI KHOẢN CHƯA ĐƯỢC KÍCH HOẠT</b>\n"
        "<b>💠 BẠN CẦN MÃ VIP ĐỂ MỞ KHÓA HỆ THỐNG</b>\n"
        "<b>🚀 LIÊN HỆ TELEGRAM ĐỂ NHẬN MÃ KÍCH HOẠT</b>\n"
        "<b>👑 TELEGRAM BOSS:</b>\n"
        f"<b><a href=\"{BOSS_LINK}\">@HOANGTUNGS8</a></b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>💎 NHẬP MÃ KÍCH HOẠT VÀO KHUNG CHAT</b>"
    )


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
                InlineKeyboardButton(text="🔄 LỆNH KẼ TIẾP", callback_data="start_ai"),
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
    for i in range(1, 21):
        row.append(InlineKeyboardButton(text=f"Bàn {i}", callback_data=f"table_{i}"))
        if len(row) == 4:
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
    now = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
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

    return (
        "<b>✅ KẾT QUẢ ĐÃ ĐƯỢC XÁC NHẬN</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"{ban_text}"
        "<b>📈 KẾT QUẢ DỰ ĐOÁN</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"<b>🟨 HÒA: {hoa}%</b>\n"
        f"<b>🟦 CON: {con}%</b>\n"
        f"<b>🟥 CÁI: {cai}%</b>\n\n"
        f"<b>{icon} LỆNH CHÍNH: {ket_qua}</b>\n\n"
        "<b>🔥 ĐỘ TIN CẬY: CAO</b>\n"
        f"<b>⏰ THỚI GIAN: {now}</b>\n\n"
        "<b>━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>👑 LIÊN HỆ TELEGRAM:</b>\n"
        f"<b><a href=\"{BOSS_LINK}\">@HOANGTUNGS8</a></b>"
    )


# ANH 1: chuakichhoat.png
async def gui_man_hinh_khoa(msg):
    img_path = "chuakichhoat.png"
    if os.path.exists(img_path):
        await msg.answer_photo(
            photo=FSInputFile(img_path),
            caption=man_hinh_khoa(),
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await msg.answer(man_hinh_khoa(), disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())


# ANH 2: chonsanh.png
async def gui_man_hinh_vip(msg):
    text = (
        "<b>✅ KÍCH HOẠT THÀNH CÔNG VIP</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        "<b>👑 TÀI KHOẢN ĐÃ ĐƯỢC MỞ KHÓA</b>\n"
        "<b>🎯 HỆ THỐNG AI VIP ĐÃ SẴN SÀNG</b>\n"
        "<b>🔥 GIAO DIỆN PHÂN TÍCH CAO CẤP</b>\n\n"
        "<b>💎 VUI LÒNG CHỌN SẢNH ĐỂ BẮT ĐẦU</b>"
    )
    img_path = "chonsanh.png"
    logging.info(f"[DEBUG] cwd={os.getcwd()}, files={os.listdir('.')}, chonsanh exists={os.path.exists(img_path)}")
    if os.path.exists(img_path):
        try:
            await msg.answer_photo(
                photo=FSInputFile(img_path),
                caption=text,
                reply_markup=menu_chon_sanh()
            )
            logging.info("[DEBUG] chonsanh photo sent OK")
        except Exception as e:
            logging.error(f"[DEBUG] chonsanh photo FAILED: {e}")
            await msg.answer(text, reply_markup=menu_chon_sanh())
    else:
        await msg.answer(text, reply_markup=menu_chon_sanh())


async def blink_waiting_message(request_id):
    dots = ["", ".", "..", "..."]
    while request_id in pending_orders:
        info = pending_orders[request_id]
        for dot in dots:
            if request_id not in pending_orders:
                return
            try:
                blink_text = (
                    "<b>✅ ĐÃ XÁC NHẬN LỆNH</b>\n"
                    "<b>━━━━━━━━━━━━━━━━━━</b>\n\n"
                    f"<b>🤖 CHAT GPT ĐANG TÍNH TOÁN KẾT QUẢ{dot}</b>\n"
                    f"<b>🎲 BÀN: {info['table']}</b>\n\n"
                    "<b>⏳ VUI LÒNG CHỜ BOSS XÁC NHẬN KẾT QUẢ</b>"
                )
                if info.get("is_photo"):
                    await bot.edit_message_caption(
                        chat_id=info["chat_id"],
                        message_id=info["message_id"],
                        caption=blink_text
                    )
                else:
                    await bot.edit_message_text(
                        chat_id=info["chat_id"],
                        message_id=info["message_id"],
                        text=blink_text
                    )
            except Exception:
                pass
            await asyncio.sleep(0.8)


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    if user_id in users_vip:
        await message.answer(
            "<b>👑 AI GPT BACCARAT VIP</b>\n"
            "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
            "<b>💎 VUI LÒNG CHỌN SẢNH ĐỂ BẮT ĐẦU</b>",
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
        if text == current_password:
            users_vip.add(user_id)
            user_click_counters[user_id] = 0

            await gui_man_hinh_vip(msg)

            current_password = generate_random_password()
            try:
                await bot.send_message(
                    chat_id=BOSS_ID,
                    text=(
                        f"🔑 Khách vừa kích hoạt thành công!\n"
                        f"🆔 User ID: <b>{user_id}</b>\n"
                        f"🔐 Mã VIP ngẫu nhiên mới: <b>{current_password}</b>\n"
                        f"👉 Hãy lưu lại mã mới này để cấp cho khách tiếp theo!"
                    )
                )
            except Exception as e:
                logging.error(f"Lỗi gửi tin nhắn mật khẩu về cho Boss: {e}")
            return

        await gui_man_hinh_khoa(msg)
        return

    await msg.answer(
        "<b>👑 AI GPT BACCARAT VIP</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        "<b>💎 VUI LÒNG CHỌN SẢNH ĐỂ BẮT ĐẦU</b>",
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

        # ANH 5: ketqua.png
        ket_qua_text = ket_qua_xac_nhan(info["user_id"], ket_qua)
        img_path_ketqua = "ketqua.png"
        if os.path.exists(img_path_ketqua):
            try:
                await bot.delete_message(
                    chat_id=info["chat_id"],
                    message_id=info["message_id"]
                )
            except Exception:
                pass
            await bot.send_photo(
                chat_id=info["chat_id"],
                photo=FSInputFile(img_path_ketqua),
                caption=ket_qua_text,
                reply_markup=menu_sau_khi_vao_lenh()
            )
        else:
            if info.get("is_photo"):
                await bot.edit_message_caption(
                    chat_id=info["chat_id"],
                    message_id=info["message_id"],
                    caption=ket_qua_text,
                    reply_markup=menu_sau_khi_vao_lenh()
                )
            else:
                await bot.edit_message_text(
                    chat_id=info["chat_id"],
                    message_id=info["message_id"],
                    text=ket_qua_text,
                    reply_markup=menu_sau_khi_vao_lenh(),
                    disable_web_page_preview=True
                )

        await call.message.edit_text(
            f"<b>✅ BOSS ĐÃ XÁC NHẬN KẾT QUẢ</b>\n\n"
            f"<b>🎲 BÀN: {info['table']}</b>\n"
            f"<b>📌 KẾT QUẢ: {ket_qua}</b>"
        )
        await call.answer("Đã gửi kết quả về nhóm.")
        return

    if user_id not in users_vip:
        await call.answer("🔐 VUI LÒNG KÍCH HOẠT VIP TRƯỚC")
        banner = get_banner()
        if banner:
            await call.message.answer_photo(photo=banner, caption=man_hinh_khoa(), reply_markup=ReplyKeyboardRemove())
        else:
            await call.message.answer(man_hinh_khoa(), disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
        return

    if not await check_user_click_limit(call):
        return

    if data == "show_rooms":
        await call.answer("🏛️ CHỌN SẢNH")
        await call.message.answer(
            "<b>🏛️ CHỌN SẢNH VIP</b>\n"
            "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
            "<b>🎯 VUI LÒNG CHỌN SẢNH BÊN DƯỚI</b>",
            reply_markup=room_menu()
        )
        return

    if data == "room_sexy":
        await call.answer("🔥 ĐÃ CHỌN SẢNH SEXY")
        await call.message.answer(
            "<b>🔥 SẢNH SEXY VIP</b>\n"
            "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
            "<b>🎯 VUI LÒNG CHỌN BÀN</b>",
            reply_markup=sexy_table_menu()
        )
        return

    if data == "room_dg":
        await call.answer("💎 ĐÃ CHỌN SẢNH DG")
        await call.message.answer(
            "<b>💎 SẢNH DG VIP</b>\n"
            "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
            "<b>⚠️ SẢNH NÀY ĐANG ĐƯỢC CẬP NHẬT</b>\n"
            "<b>🔥 VUI LÒNG CHỌN SẢNH SEXY ĐỂ SọNG TRƯỚC</b>",
            reply_markup=menu_chon_sanh()
        )
        return

    if data == "room_mt":
        await call.answer("⚡ ĐÃ CHỌN SẢNH MT")
        await call.message.answer(
            "<b>⚡ SẢNH MT VIP</b>\n"
            "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
            "<b>⚠️ SẢNH NÀY ĐANG ĐƯỢC CẬP NHẬT</b>\n"
            "<b>🔥 VUI LÒNG CHỌN SẢNH SEXY ĐỂ SọNG TRƯỚC</b>",
            reply_markup=menu_chon_sanh()
        )
        return

    if data.startswith("table_"):
        ten_ban = data.replace("table_", "")
        user_tables[user_id] = f"SẢNH SEXY BÀN {ten_ban}"
        await call.answer("✅ CHỌN BÀN THÀNH CÔNG")

        # ANH 3: chonban.png
        img_path_chonban = "chonban.png"
        ten_ban_caption = (
            f"<b>✅ ĐÃ CHỌN SẢNH SEXY BÀN {ten_ban}</b>\n"
            "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
            "<b>🚀 BẤM NÚT BẮT ĐẦU ĐỂ PHÂN TÍCH</b>"
        )
        if os.path.exists(img_path_chonban):
            try:
                await call.message.answer_photo(
                    photo=FSInputFile(img_path_chonban),
                    caption=ten_ban_caption,
                    reply_markup=menu_bat_dau()
                )
                logging.info("[DEBUG] chonban photo sent OK")
            except Exception as e:
                logging.error(f"[DEBUG] chonban photo FAILED: {e}")
                await call.message.answer(ten_ban_caption, reply_markup=menu_bat_dau())
        else:
            await call.message.edit_reply_markup(reply_markup=menu_bat_dau())
        return

    if data == "start_ai":
        if user_id not in user_tables:
            await call.answer("🎲 VUI LÒNG CHỌN BÀN TRƯỚC")
            await call.message.answer(
                "<b>⚠️ BẠN CHƯA CHỌN BÀN</b>\n"
                "<b>━━━━━━━━━━━━━━━━━━━━</b>\n\n"
                "<b>🎲 VUI LÒNG CHỌN SẢNH VÀ CHỌN BÀN TRƯỚC KHI BẮT ĐẦU</b>",
                reply_markup=menu_chon_sanh()
            )
            return

        request_id = uuid.uuid4().hex[:8]
        table_name = user_tables[user_id]

        # ANH 4: dangtinhtoan.png
        img_path_dang = "dangtinhtoan.png"
        dang_xu_ly_text = (
            "<b>✅ ĐÃ XÁC NHẬN LỆNH</b>\n"
            "<b>━━━━━━━━━━━━━━━━━━</b>\n\n"
            "<b>🤖 CHAT GPT ĐANG TÍNH TOÁN KẾT QUẢ...</b>\n"
            f"<b>🎲 BÀN: {table_name}</b>\n\n"
            "<b>⏳ VUI LÒNG CHỜ BOSS XÁC NHẬN KẾT QUẢ</b>"
        )
        if os.path.exists(img_path_dang):
            wait_msg = await call.message.answer_photo(
                photo=FSInputFile(img_path_dang),
                caption=dang_xu_ly_text
            )
            is_photo_msg = True
        else:
            wait_msg = await call.message.answer(dang_xu_ly_text)
            is_photo_msg = False

        pending_orders[request_id] = {
            "chat_id": call.message.chat.id,
            "message_id": wait_msg.message_id,
            "user_id": user_id,
            "table": table_name,
            "is_photo": is_photo_msg
        }

        blink_tasks[request_id] = asyncio.create_task(blink_waiting_message(request_id))

        try:
            await bot.send_message(
                chat_id=BOSS_ID,
                text=(
                    "<b>📩 CÓ LỆNH MỚI CẦN XÁC NHẬN</b>\n"
                    "<b>━━━━━━━━━━━━━━━━━━</b>\n\n"
                    f"<b>🎲 BÀN: {table_name}</b>\n"
                    f"<b>👤 USER ID: {user_id}</b>\n\n"
                    "<b>Boss xem web rồi chọn kết quả bên dưới:</b>"
                ),
                reply_markup=boss_confirm_menu(request_id)
            )
        except Exception:
            await call.message.answer(
                "<b>⚠️ CHƯA Gửi ĐƯỢC TIN NHẬN CHO BOSS</b>\n\n"
                "<b>Boss cần nhắn /start riêng với bot trước.</b>"
            )

        await call.answer("✅ ĐÃ Gửi LỆNH CHỜ BOSS XÁC NHẬN")
        return


async def main():
    print("BOT AI GPT BACCARAT VIP ĐANG CHẠY TRÊN RAILWAY...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
