import os
import json
import random
import string
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN", "8200641951:AAGRByzc4x2Xz4BLvdtJfcfId_1DYP-6Lo")
BOSS_LINK = "https://t.me/HOANGTUNGS8"

# ==================== ĐIỀN ID TELEGRAM CỦA BẠN VÀO ĐÂY ====================
BOSS_ID = 7616985896  # Bot sẽ bắn mật khẩu random mới về ID này cho bạn
# =========================================================================

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

DATA_FILE = "storage.json"

# Bộ nhớ lưu trữ trạng thái người dùng
users_vip = set()
user_click_counters = {}
pending_orders = {}

# Mật khẩu ban đầu (Viết hoa hoàn toàn)
current_password = "HARRY2005TDZ"

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def generate_random_password():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

# Thanh menu thiết kế tinh gọn theo yêu cầu (Không chứa /nap, có thêm /all)
def bieu_dien_menu():
    keyboard = [
        [KeyboardButton(text='/gui1'), KeyboardButton(text='/gui2'), KeyboardButton(text='/gui3'), KeyboardButton(text='/gui4'), KeyboardButton(text='/gui5')],
        [KeyboardButton(text='/gui6'), KeyboardButton(text='/gui7'), KeyboardButton(text='/gui8'), KeyboardButton(text='/gui9'), KeyboardButton(text='/gui10')],
        [KeyboardButton(text='/doi1'), KeyboardButton(text='/doi2'), KeyboardButton(text='/doi3'), KeyboardButton(text='/doi4'), KeyboardButton(text='/doi5')],
        [KeyboardButton(text='/doi6'), KeyboardButton(text='/doi7'), KeyboardButton(text='/doi8'), KeyboardButton(text='/doi9'), KeyboardButton(text='/doi10')],
        [KeyboardButton(text='/all')]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)

# Hàm kiểm tra và tăng bộ đếm 10 lượt bấm của khách
async def check_user_limit(message: types.Message) -> bool:
    uid = message.from_user.id
    if uid not in users_vip:
        return False
        
    user_click_counters[uid] = user_click_counters.get(uid, 0) + 1
    
    if user_click_counters[uid] > 10:
        users_vip.discard(uid)
        user_click_counters.pop(uid, None)
        await message.reply(
            "❌ <b>Hết lượt sử dụng VIP công nghệ!</b>\n"
            "Vui lòng liên hệ Admin để được cấp lại mật khẩu mới mới có thể tiếp tục sử dụng.",
            reply_markup=ReplyKeyboardRemove()
        )
        return False
    return True

def get_banner():
    if os.path.exists("banner.jpg"):
        return FSInputFile("banner.jpg")
    return None

def man_hinh_khoa():
    return f"""<b>👑💎 CHÀO MỪNG BẠN ĐÃ ĐẾN VỚI 💎👑
🤖 AI GPT BACCARAT VIP</b>
——————————————————
🔒 <b>TÀI KHOẢN CHƯA ĐƯỢC KÍCH HOẠT</b>

🐋 BẠN CẦN MÃ VIP ĐỂ MỞ KHÓA HỆ THỐNG
🚀 LIÊN HỆ TELEGRAM ĐỂ NHẬN MÃ KÍCH HOẠT

👑 TELEGRAM BOSS:
<a href="{BOSS_LINK}">@HOANGTUNGS8</a>
——————————————————
💎 <b>NHẬP MÃ KÍCH HOẠT VÀO KHUNG CHAT</b>"""

def menu_chon_sanh():
    inline_keyboard = [
        [InlineKeyboardButton(text="🏛️ CHỌN SẢNH", callback_data="show_rooms")],
        [InlineKeyboardButton(text="👑 LIÊN HỆ TELEGRAM", url=BOSS_LINK)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    uid = message.from_user.id
    if uid in users_vip:
        await message.reply(
            "👋 Hệ thống điều khiển BOT LENH VIP đã sẵn sàng!\n"
            "📤 Sử dụng các nút bấm dưới đây để thực hiện gửi lệnh nhanh (Tối đa 10 lượt bấm):",
            reply_markup=bieu_dien_menu()
        )
        return

    pending_orders[uid] = "waiting_password"
    banner = get_banner()
    if banner:
        await message.answer_photo(photo=banner, caption=man_hinh_khoa(), reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text=man_hinh_khoa(), reply_markup=ReplyKeyboardRemove())

@dp.message(lambda msg: pending_orders.get(msg.from_user.id) == "waiting_password")
async def handle_password(message: types.Message):
    global current_password
    uid = message.from_user.id
    user_pass = message.text.strip()

    if user_pass == current_password:
        users_vip.add(uid)
        user_click_counters[uid] = 0
        pending_orders.pop(uid, None)

        caption_success = """✅ <b>KÍCH HOẠT THÀNH CÔNG VIP</b>
——————————————————
👑 TÀI KHỎAN ĐÃ ĐƯỢC MỞ KHÓA
🎯 HỆ THỐNG AI VIP ĐÃ SẴN SÀNG
🔥 GIAO DIỆN PHÂN TÍCH CAO CẤP

💎 VUI LÒNG CHỌN SẢNH ĐỂ BẮT ĐẦU"""

        banner = get_banner()
        if banner:
            await message.answer_photo(photo=banner, caption=caption_success, reply_markup=menu_chon_sanh())
        else:
            await message.answer(text=caption_success, reply_markup=menu_chon_sanh())

        await message.answer(
            "📥 Gõ tay lệnh /nap1 đến /nap10 để cấu hình dữ liệu ban đầu.\n"
            "📤 Sử dụng menu điều khiển bên dưới để gửi lệnh nhanh lên nhóm (Tối đa 10 lượt bấm):",
            reply_markup=bieu_dien_menu()
        )

        old_pass = current_password
        current_password = generate_random_password()

        try:
            await bot.send_message(
                chat_id=BOSS_ID,
                text=f"🔔 <b>THÔNG BÁO HỆ THỐNG BOT</b>\n\n"
                     f"👤 Khách hàng ID <code>{uid}</code> vừa nhập đúng pass: <b>{old_pass}</b>\n"
                     f"🔄 Hệ thống đã tự động đổi mật khẩu random mới: <b>{current_password}</b>\n"
                     f"👉 Vui lòng lưu lại để cấp cho khách tiếp theo!"
            )
        except Exception as e:
            logging.error(f"Lỗi gửi tin nhắn cho Boss: {e}")
    else:
        await message.reply("❌ Mật khẩu sai rồi! Vui lòng kiểm tra và nhập lại mật khẩu:")

@dp.callback_query(lambda c: c.data == "show_rooms")
async def process_show_rooms(callback_query: types.CallbackQuery):
    inline_keyboard = [
        [InlineKeyboardButton(text="🔥 SẢNH SEXY", callback_data="room_sexy"),
         InlineKeyboardButton(text="💎 SẢNH DG", callback_data="room_dg"),
         InlineKeyboardButton(text="⚡ SẢNH MT", callback_data="room_mt")]
    ]
    await callback_query.message.edit_caption(
        caption="🏛️ <b>HỆ THỐNG SẢNH AI VIP</b>\n\n✨ VUI LÒNG CHỌN SẢNH ĐỂ TIẾP TỤC\n🎯 AI ĐANG ĐỒNG BỘ DỮ LIỆU...",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    )
    await callback_query.answer()

@dp.callback_query(lambda c: c.data.startswith("room_"))
async def process_room_select(callback_query: types.CallbackQuery):
    room_name = callback_query.data.replace("room_", "").upper()
    inline_keyboard = [[InlineKeyboardButton(text="🚀 Bắt Đầu", callback_data="start_analysis")]]
    await callback_query.message.edit_caption(
        caption=f"🔥 <b>SẢNH {room_name} VIP</b>\n——————————————————\n🎯 VUI LÒNG CHỌN BÀN",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    )
    await callback_query.answer()

@dp.message(Command("all"))
async def all_cmd(message: types.Message):
    if not await check_user_limit(message): return
    uid = message.from_user.id
    pending_orders[uid] = "waiting_all_content"
    await message.reply("⚡ Gửi tin nhắn bất kỳ (Chữ/Ảnh/Video), Bot sẽ bắn thẳng lên nhóm ngay lập tức:")

@dp.message(lambda msg: msg.text and msg.text.startswith("/nap"))
async def nap_cmd(message: types.Message):
    uid = message.from_user.id
    if uid not in users_vip:
        await message.reply("🔒 Bạn cần gõ /start và nhập mật khẩu trước khi dùng lệnh!")
        return
    slot = message.text.split()[0].replace("/nap", "")
    pending_orders[uid] = f"waiting_nap_{slot}"
    await message.reply(f"📥 Gửi nội dung cho ô {slot}:")

@dp.message(lambda msg: msg.text and msg.text.startswith("/doi"))
async def doi_cmd(message: types.Message):
    if not await check_user_limit(message): return
    uid = message.from_user.id
    cmd = message.text.split()[0].replace("/doi", "")
    if "gui" in cmd:
        parts = cmd.split("gui")
        slot_doi = parts[0]
        slot_gui = parts[1]
        pending_orders[uid] = f"waiting_doigui_{slot_doi}_{slot_gui}"
        await message.reply(f"🔄 Gửi nội dung mới cho ô {slot_doi} (sẽ gửi ô {slot_gui} lên nhóm):")
    else:
        pending_orders[uid] = f"waiting_doi_{cmd}"
        await message.reply(f"🔄 Gửi HÌNH ẢNH MỚI cho ô {cmd} (Bot sẽ giữ văn bản cũ và tự gửi lên nhóm):")

@dp.message(lambda msg: msg.text and msg.text.startswith("/gui"))
async def gui_cmd(message: types.Message):
    if not await check_user_limit(message): return
    slot = message.text.split()[0].replace("/gui", "")
    data = load()
    item = data.get(slot)
    if not item:
        await message.reply(f"❌ Ô {slot} chưa có nội dung!")
        return
    try:
        t = item["type"]
        if t == "text":
            await bot.send_message(CHAT_LINK, item["content"])
        elif t == "photo":
            await bot.send_photo(CHAT_LINK, item["file_id"], caption=item["caption"])
        elif t == "video":
            await bot.send_video(CHAT_LINK, item["file_id"], caption=item["caption"])
        elif t == "animation":
            await bot.send_animation(CHAT_LINK, item["file_id"], caption=item["caption"])
        elif t == "document":
            await bot.send_document(CHAT_LINK, item["file_id"], caption=item["caption"])
        await message.reply(f"✅ Đã gửi ô {slot} vào nhóm!")
    except Exception as e:
        await message.reply(f"❌ Lỗi: {e}")

@dp.message()
async def handle_universal_content(message: types.Message):
    uid = message.from_user.id
    state = pending_orders.get(uid, "")
    
    if not state:
        return

    # Luồng xử lý gửi thẳng /all
    if state == "waiting_all_content":
        try:
            if message.text:
                await bot.send_message(CHAT_LINK, message.html_text)
            elif message.photo:
                await bot.send_photo(CHAT_LINK, message.photo[-1].file_id, caption=message.html_text or "")
            elif message.video:
                await bot.send_video(CHAT_LINK, message.video.file_id, caption=message.html_text or "")
            elif message.animation:
                await bot.send_animation(CHAT_LINK, message.animation.file_id, caption=message.html_text or "")
            elif message.document:
                await bot.send_document(CHAT_LINK, message.document.file_id, caption=message.html_text or "")
            await message.reply("✅ Đã bắn thẳng nội dung lên nhóm thành công!", reply_markup=bieu_dien_menu())
        except Exception as e:
            await message.reply(f"❌ Lỗi gửi thẳng: {e}", reply_markup=bieu_dien_menu())
        pending_orders.pop(uid, None)
        return

    data = load()

    # Luồng xử lý /doiX đổi ảnh giữ nguyên văn bản cũ
    if state.startswith("waiting_doi_"):
        slot = state.replace("waiting_doi_", "")
        item_cu = data.get(slot)
        van_ban_cu = ""
        if item_cu:
            van_ban_cu = item_cu["content"] if item_cu["type"] == "text" else item_cu.get("caption", "")

        if message.photo:
            data[slot] = {"type": "photo", "file_id": message.photo[-1].file_id, "caption": van_ban_cu}
        elif message.video:
            data[slot] = {"type": "video", "file_id": message.video.file_id, "caption": van_ban_cu}
        elif message.animation:
            data[slot] = {"type": "animation", "file_id": message.animation.file_id, "caption": van_ban_cu}
        elif message.document:
            data[slot] = {"type": "document", "file_id": message.document.file_id, "caption": van_ban_cu}
        elif message.text:
            data[slot] = {"type": "text", "content": message.html_text}
            
        save(data)
        await message.reply(f"✅ Đã đổi ảnh và giữ nguyên văn bản cũ cho ô {slot}!")

        try:
            item = data[slot]
            t = item["type"]
            if t == "text":
                await bot.send_message(CHAT_LINK, item["content"])
            elif t == "photo":
                await bot.send_photo(CHAT_LINK, item["file_id"], caption=item["caption"])
            elif t == "video":
                await bot.send_video(CHAT_LINK, item["file_id"], caption=item["caption"])
            elif t == "animation":
                await bot.send_animation(CHAT_LINK, item["file_id"], caption=item["caption"])
            elif t == "document":
                await bot.send_document(CHAT_LINK, item["file_id"], caption=item["caption"])
            await message.reply(f"🚀 Tự động gửi ô {slot} kèm ảnh mới lên nhóm thành công!", reply_markup=bieu_dien_menu())
        except Exception as e:
            await message.reply(f"❌ Lỗi tự động gửi: {e}", reply_markup=bieu_dien_menu())
            
        pending_orders.pop(uid, None)
        return

    # Luồng xử lý nạp dữ liệu /napX ban đầu
    if state.startswith("waiting_nap_"):
        slot = state.replace("waiting_nap_", "")
        if message.text:
            data[slot] = {"type": "text", "content": message.html_text}
        elif message.photo:
            data[slot] = {"type": "photo", "file_id": message.photo[-1].file_id, "caption": message.html_text or ""}
        elif message.video:
            data[slot] = {"type": "video", "file_id": message.video.file_id, "caption": message.html_text or ""}
        elif message.animation:
            data[slot] = {"type": "animation", "file_id": message.animation.file_id, "caption": message.html_text or ""}
        elif message.document:
            data[slot] = {"type": "document", "file_id": message.document.file_id, "caption": message.html_text or ""}
            
        save(data)
        await message.reply(f"✅ Đã lưu dữ liệu ô {slot}!", reply_markup=bieu_dien_menu())
        pending_orders.pop(uid, None)
        return

    # Luồng xử lý /doiXguiY cũ của bạn
    if state.startswith("waiting_doigui_"):
        parts = state.replace("waiting_doigui_", "").split("_")
        slot_doi = parts[0]
        slot_gui = parts[1]
        
        if message.text:
            data[slot_doi] = {"type": "text", "content": message.html_text}
        elif message.photo:
            data[slot_doi] = {"type": "photo", "file_id": message.photo[-1].file_id, "caption": message.html_text or ""}
            
        save(data)
        await message.reply(f"✅ Đã cập nhật ô {slot_doi}!")

        item = data.get(slot_gui)
        if item:
            try:
                t = item["type"]
                if t == "text":
                    await bot.send_message(CHAT_LINK, item["content"])
                elif t == "photo":
                    await bot.send_photo(CHAT_LINK, item["file_id"], caption=item["caption"])
                await message.reply(f"✅ Đã gửi ô {slot_gui} vào nhóm!", reply_markup=bieu_dien_menu())
            except Exception as e:
                await message.reply(f"❌ Lỗi gửi: {e}", reply_markup=bieu_dien_menu())
        pending_orders.pop(uid, None)

async def main():
    print("Bot đang khởi chạy bằng AIOGRAM...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
