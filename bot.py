import os
import json
import random
import string
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN", "8877176302:AAETTH8e3LWY0BL3pHsOpUo4huAQjzOq2bg")
CHAT_LINK = "-1003617964607"
DATA_FILE = "storage.json"

# ==================== CẤU HÌNH THÔNG TIN ADMIN (BẠN CẦN ĐIỀN VÀO ĐÂY) ====================
MY_TELEGRAM_ID = 123456789  # SỬA THÀNH: ID Telegram cá nhân của bạn để nhận mật khẩu random
URL_ANH_NEN = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe" # Link ảnh nền công nghệ lúc /start
# =======================================================================================

WAITING = 1
WAITING_PASS = 99
pending = {}

# Hệ thống lưu trạng thái bộ đếm 10 lượt bấm và danh sách đã xác thực
authenticated_users = set()
user_click_counters = {} 

# Mật khẩu ban đầu của bạn (Viết hoa hoàn bộ)
if "current_password" not in globals():
    current_password = "HARRY2005TDZ"

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Hàm sinh mật khẩu ngẫu nhiên gồm 8 ký tự viết hoa và số
def generate_random_password():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

# Thanh menu thiết kế tinh gọn theo yêu cầu (Không chứa /nap, có thêm /all)
def bieu_dien_menu():
    boc_cut_nut = [
        ['/gui1', '/gui2', '/gui3', '/gui4', '/gui5'],
        ['/gui6', '/gui7', '/gui8', '/gui9', '/gui10'],
        ['/doi1', '/doi2', '/doi3', '/doi4', '/doi5'],
        ['/doi6', '/doi7', '/doi8', '/doi9', '/doi10'],
        ['/all']
    ]
    return ReplyKeyboardMarkup(boc_cut_nut, resize_keyboard=True, one_time_keyboard=False)

# Kiểm tra bộ đếm 10 lượt bấm của người dùng
async def check_user_limit(u: Update, c: ContextTypes.DEFAULT_TYPE) -> bool:
    uid = u.effective_user.id
    if uid not in authenticated_users:
        return False
        
    # Mỗi lần bấm nút lệnh bất kỳ, tăng bộ đếm lên 1
    user_click_counters[uid] = user_click_counters.get(uid, 0) + 1
    
    # Nếu vượt quá 10 lượt bấm
    if user_click_counters[uid] > 10:
        # Khóa tài khoản
        authenticated_users.discard(uid)
        user_click_counters.pop(uid, None)
        
        # Thông báo khóa và ẩn thanh menu đi
        await u.message.reply_text(
            "❌ Hết lượt sử dụng VIP công nghệ!\n"
            "Vui lòng liên hệ Admin để được cấp lại mật khẩu mới mới có thể tiếp tục sử dụng.",
            reply_markup=ReplyKeyboardRemove()
        )
        return False
    return True

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    uid = u.effective_user.id
    if uid in authenticated_users:
        await u.message.reply_text(
            "👋 Hệ thống điều khiển BOT LENH VIP đã mở khóa sẵn sàng!\n\n"
            "📥 Lưu dữ liệu: Gõ tay lệnh /nap1 đến /nap10 (Chỉ làm 1 lần)\n"
            "📤 Gửi nhanh, đổi nội dung ảnh và gửi trực tiếp: Dùng thanh menu bên dưới.",
            reply_markup=bieu_dien_menu()
        )
        return ConversationHandler.END

    pending[uid] = ("login", None, None)
    
    # Gửi TẤM ẢNH NỀN kèm nội dung chữ chuẩn chính tả yêu cầu nhập pass
    caption_text = (
        "🔒 <b>HỆ THỐNG ĐÃ ĐƯỢC BẢO MẬT VIP</b>\n\n"
        "Vui lòng nhập chính xác mật khẩu để xác thực quyền truy cập và kích hoạt hệ thống điều khiển:"
    )
    try:
        await c.bot.send_photo(
            chat_id=u.effective_chat.id,
            photo=URL_ANH_NEN,
            caption=caption_text,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception:
        # Fallback gửi tin nhắn chữ nếu link ảnh lỗi
        await u.message.reply_text(caption_text, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        
    return WAITING_PASS

async def handle_password(u: Update, c: ContextTypes.DEFAULT_TYPE):
    global current_password
    uid = u.effective_user.id
    user_pass = u.message.text.strip()
    
    if user_pass == current_password:
        # 1. Kích hoạt quyền sử dụng cho khách hiện tại và reset bộ đếm về 0
        authenticated_users.add(uid)
        user_click_counters[uid] = 0
        pending.pop(uid, None)
        
        # 2. Tạo giao diện Inline giống hệt bản cũ của bạn
        inline_keyboard = [
            [InlineKeyboardButton("🏛️ CHẬN SẢNH", callback_mode="sanh_main"),
             InlineKeyboardButton("👑 LIÊN HỆ TELEGRAM", url="https://t.me/HARRY2005TDZ")] # Đã chèn link tele của bạn vào nút
        ]
        reply_markup_inline = InlineKeyboardMarkup(inline_keyboard)
        
        # Gửi ảnh báo kích hoạt thành công kèm nút Inline dính dưới ảnh
        try:
            await c.bot.send_photo(
                chat_id=u.effective_chat.id,
                photo=URL_ANH_NEN,
                caption="🎉 <b>KÍCH HOẠT THÀNH CÔNG VIP!</b>\nHệ thống phân tích sảnh đã được mở khóa hoàn tất.",
                parse_mode="HTML",
                reply_markup=reply_markup_inline
            )
        except Exception:
            await u.message.reply_text("🎉 KÍCH HOẠT THÀNH CÔNG VIP!", reply_markup=reply_markup_inline)
            
        # 3. Tự động cấp luôn thanh menu điều khiển 10 ô lệnh cho khách bấm
        await u.message.reply_text(
            "📥 Gõ tay lệnh /nap1 đến /nap10 để cấu hình dữ liệu ban đầu.\n"
            "📤 Sử dụng các nút bấm dưới đây để thực hiện gửi lệnh nhanh (Tối đa 10 lượt bấm):",
            reply_markup=bieu_dien_menu()
        )
        
        # 4. Tạo mật khẩu random mới đè lên để khách sau không dùng lại pass cũ được nữa
        old_pass = current_password
        current_password = generate_random_password()
        
        # 5. Ngay lập tức bắn thông báo mật khẩu mới về Telegram cá nhân của bạn
        try:
            await c.bot.send_message(
                chat_id=MY_TELEGRAM_ID,
                text=f"🔔 <b>THÔNG BÁO HỆ THỐNG BOT</b>\n\n"
                     f"👤 Khách hàng ID <code>{uid}</code> vừa nhập đúng pass: <b>{old_pass}</b>\n"
                     f"🔄 Hệ thống đã tự động đổi mật khẩu random mới: <b>{current_password}</b>\n"
                     f"👉 Vui lòng lưu lại để cấp cho khách tiếp theo!" ,
                parse_mode="HTML"
            )
        except Exception as e:
            logging.error(f"Không thể gửi mật khẩu về cho Admin: {e}")
            
        return ConversationHandler.END
    else:
        await u.message.reply_text("❌ Mật khẩu sai rồi! Vui lòng kiểm tra và nhập lại mật khẩu:")
        return WAITING_PASS

# Xử lý các sự kiện bấm nút Inline (Sảnh) cũ của bạn
async def inline_button_click(u: Update, c: ContextTypes.DEFAULT_TYPE):
    query = u.callback_query
    await query.answer()
    # Chức năng nhấp nhả chuyển đổi sảnh cũ của bạn giữ nguyên cấu trúc
    if query.data == "sanh_main":
        sanh_keyboard = [
            [InlineKeyboardButton("🔥 SẢNH SEXY", callback_data="sexy"),
             InlineKeyboardButton("💎 SẢNH DG", callback_data="dg"),
             InlineKeyboardButton("⚡ SẢNH MT", callback_data="mt")]
        ]
        await query.edit_message_caption(
            caption="🔮 Vui lòng chọn sảnh bạn muốn phân tích dữ liệu bên dưới:",
            reply_markup=InlineKeyboardMarkup(sanh_keyboard)
        )
    elif query.data in ["sexy", "dg", "mt"]:
        bat_dau_keyboard = [[InlineKeyboardButton("🚀 Bắt Đầu Phân Tích", callback_data="start_analysis")]]
        await query.edit_message_caption(
            caption=f"✅ Đã chọn sảnh thành công! Hãy bấm nút bắt đầu để chạy thuật toán.",
            reply_markup=InlineKeyboardMarkup(bat_dau_keyboard)
        )

async def nap_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    uid = u.effective_user.id
    if uid not in authenticated_users:
        await u.message.reply_text("🔒 Bạn cần gõ /start và nhập mật khẩu trước khi dùng lệnh!")
        return ConversationHandler.END
        
    cmd = u.message.text.split()[0][1:]
    slot = cmd.replace("nap", "")
    pending[uid] = ("nap", slot, None)
    await u.message.reply_text(f"📥 Gửi nội dung cho ô {slot}:")
    return WAITING

async def doi_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if not await check_user_limit(u, c): return ConversationHandler.END
        
    uid = u.effective_user.id
    cmd = u.message.text.split()[0][1:]
    if "gui" in cmd:
        parts = cmd.split("gui")
        slot_doi = parts[0].replace("doi", "")
        slot_gui = parts[1]
        pending[uid] = ("doigui", slot_doi, slot_gui)
        await u.message.reply_text(f"🔄 Gửi nội dung mới cho ô {slot_doi} (sẽ gửi ô {slot_gui} lên nhóm):")
    else:
        slot = cmd.replace("doi", "")
        pending[uid] = ("doi", slot, None)
        await u.message.reply_text(f"🔄 Gửi HÌNH ẢNH MỚI cho ô {slot} (Bot sẽ giữ văn bản cũ và tự gửi lên nhóm):")
    return WAITING

async def all_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if not await check_user_limit(u, c): return ConversationHandler.END
        
    uid = u.effective_user.id
    pending[uid] = ("all", None, None)
    await u.message.reply_text("⚡ Gửi tin nhắn bất kỳ (Chữ/Ảnh/Video), Bot sẽ bắn thẳng lên nhóm ngay lập tức:")
    return WAITING

async def handle_content(u: Update, c: ContextTypes.DEFAULT_TYPE):
    uid = u.effective_user.id
    info = pending.get(uid)
    if not info:
        return ConversationHandler.END
        
    action, slot1, slot2 = info
    msg = u.message
    
    if action == "all":
        try:
            if msg.text:
                await c.bot.send_message(CHAT_LINK, msg.text_html, parse_mode="HTML")
            elif msg.photo:
                await c.bot.send_photo(CHAT_LINK, msg.photo[-1].file_id, caption=msg.caption_html or "", parse_mode="HTML")
            elif msg.video:
                await c.bot.send_video(CHAT_LINK, msg.video.file_id, caption=msg.caption_html or "", parse_mode="HTML")
            elif msg.animation:
                await c.bot.send_animation(CHAT_LINK, msg.animation.file_id, caption=msg.caption_html or "", parse_mode="HTML")
            elif msg.document:
                await c.bot.send_document(CHAT_LINK, msg.document.file_id, caption=msg.caption_html or "", parse_mode="HTML")
            else:
                await u.message.reply_text("❌ Không hỗ trợ định dạng này!", reply_markup=bieu_dien_menu())
                return ConversationHandler.END
            await u.message.reply_text("✅ Đã bắn thẳng nội dung lên nhóm thành công!", reply_markup=bieu_dien_menu())
        except Exception as e:
            await u.message.reply_text(f"❌ Lỗi gửi thẳng: {e}", reply_markup=bieu_dien_menu())
        pending.pop(uid, None)
        return ConversationHandler.END

    data = load()
    
    if action == "doi":
        item_cu = data.get(slot1)
        van_ban_cu = ""
        if item_cu:
            if item_cu["type"] == "text":
                van_ban_cu = item_cu["content"]
            else:
                van_ban_cu = item_cu.get("caption", "")
                
        if msg.photo:
            data[slot1] = {"type": "photo", "file_id": msg.photo[-1].file_id, "caption": van_ban_cu}
        elif msg.video:
            data[slot1] = {"type": "video", "file_id": msg.video.file_id, "caption": van_ban_cu}
        elif msg.animation:
            data[slot1] = {"type": "animation", "file_id": msg.animation.file_id, "caption": van_ban_cu}
        elif msg.document:
            data[slot1] = {"type": "document", "file_id": msg.document.file_id, "caption": van_ban_cu}
        elif msg.text:
            data[slot1] = {"type": "text", "content": msg.text_html}
        else:
            await u.message.reply_text("❌ Định dạng không hợp lệ!", reply_markup=bieu_dien_menu())
            return ConversationHandler.END
            
        save(data)
        await u.message.reply_text(f"✅ Đã đổi ảnh và giữ nguyên văn bản cũ cho ô {slot1}!", reply_markup=bieu_dien_menu())
        
        try:
            item = data[slot1]
            t = item["type"]
            if t == "text":
                await c.bot.send_message(CHAT_LINK, item["content"], parse_mode="HTML")
            elif t == "photo":
                await c.bot.send_photo(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
            elif t == "video":
                await c.bot.send_video(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
            elif t == "animation":
                await c.bot.send_animation(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
            elif t == "document":
                await c.bot.send_document(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
            await u.message.reply_text(f"🚀 Tự động gửi ô {slot1} kèm ảnh mới lên nhóm thành công!", reply_markup=bieu_dien_menu())
        except Exception as e:
            await u.message.reply_text(f"❌ Lỗi tự động gửi lên nhóm: {e}", reply_markup=bieu_dien_menu())
            
        pending.pop(uid, None)
        return ConversationHandler.END

    if msg.text:
        data[slot1] = {"type": "text", "content": msg.text_html}
    elif msg.photo:
        data[slot1] = {"type": "photo", "file_id": msg.photo[-1].file_id, "caption": msg.caption_html or ""}
    elif msg.video:
        data[slot1] = {"type": "video", "file_id": msg.video.file_id, "caption": msg.caption_html or ""}
    elif msg.animation:
        data[slot1] = {"type": "animation", "file_id": msg.animation.file_id, "caption": msg.caption_html or ""}
    elif msg.document:
        data[slot1] = {"type": "document", "file_id": msg.document.file_id, "caption": msg.caption_html or ""}
    else:
        await u.message.reply_text("❌ Không hỗ trợ định dạng này!", reply_markup=bieu_dien_menu())
        return ConversationHandler.END
        
    save(data)
    await u.message.reply_text(f"✅ Đã lưu/cập nhật dữ liệu ô {slot1}!", reply_markup=bieu_dien_menu())
    
    if action == "doigui":
        item = data.get(slot2)
        if item:
            try:
                t = item["type"]
                if t == "text":
                    await c.bot.send_message(CHAT_LINK, item["content"], parse_mode="HTML")
                elif t == "photo":
                    await c.bot.send_photo(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
                elif t == "video":
                    await c.bot.send_video(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
                elif t == "animation":
                    await c.bot.send_animation(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
                elif t == "document":
                    await c.bot.send_document(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
                await u.message.reply_text(f"✅ Đã gửi ô {slot2} vào nhóm!", reply_markup=bieu_dien_menu())
            except Exception as e:
                await u.message.reply_text(f"❌ Lỗi gửi: {e}", reply_markup=bieu_dien_menu())
        else:
            await u.message.reply_text(f"❌ Ô {slot2} chưa có nội dung!", reply_markup=bieu_dien_menu())
            
    pending.pop(uid, None)
    return ConversationHandler.END

async def gui_cmd(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if not await check_user_limit(u, c): return
        
    cmd = u.message.text.split()[0][1:]
    slot = cmd.replace("gui", "")
    data = load()
    item = data.get(slot)
    if not item:
        await u.message.reply_text(f"❌ Ô {slot} chưa có nội dung!", reply_markup=bieu_dien_menu())
        return
    try:
        t = item["type"]
        if t == "text":
            await c.bot.send_message(CHAT_LINK, item["content"], parse_mode="HTML")
        elif t == "photo":
            await c.bot.send_photo(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
        elif t == "video":
            await c.bot.send_video(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
        elif t == "animation":
            await c.bot.send_animation(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
        elif t == "document":
            await c.bot.send_document(CHAT_LINK, item["file_id"], caption=item["caption"], parse_mode="HTML")
        await u.message.reply_text(f"✅ Đã gửi ô {slot} vào nhóm!", reply_markup=bieu_dien_menu())
    except Exception as e:
        await u.message.reply_text(f"❌ Lỗi: {e}", reply_markup=bieu_dien_menu())

async def cancel(u: Update, c: ContextTypes.DEFAULT_TYPE):
    pending.pop(u.effective_user.id, None)
    await u.message.reply_text("❌ Đã hủy lệnh hiện tại!", reply_markup=bieu_dien_menu())
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Quản lý luồng đăng nhập bằng mật khẩu khi gõ /start
    login_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={WAITING_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(login_handler)
    
    # Handler tiếp nhận tương tác nút bấm Inline của sảnh
    app.add_handler(CallbackQueryHandler(inline_button_click))

    # Đăng ký xử lý lệnh gửi trực tiếp /all độc lập trong menu
    conv_all = ConversationHandler(
        entry_points=[CommandHandler("all", all_cmd)],
        states={WAITING: [MessageHandler(filters.ALL & ~filters.COMMAND, handle_content)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(conv_all)

    for i in range(1, 11):
        # /napX (Lệnh gõ tay cấu hình ban đầu)
        conv_nap = ConversationHandler(
            entry_points=[CommandHandler(f"nap{i}", nap_cmd)],
            states={WAITING: [MessageHandler(filters.ALL & ~filters.COMMAND, handle_content)]},
            fallbacks=[CommandHandler("cancel", cancel)],
        )
        app.add_handler(conv_nap)

        # /guiX
        app.add_handler(CommandHandler(f"gui{i}", gui_cmd))

        # /doiX
        conv_doi = ConversationHandler(
            entry_points=[CommandHandler(f"doi{i}", doi_cmd)],
            states={WAITING: [MessageHandler(filters.ALL & ~filters.COMMAND, handle_content)]},
            fallbacks=[CommandHandler("cancel", cancel)],
        )
        app.add_handler(conv_doi)

        # /doiXguiY
        for j in range(1, 11):
            conv_doigui = ConversationHandler(
                entry_points=[CommandHandler(f"doi{i}gui{j}", doi_cmd)],
                states={WAITING: [MessageHandler(filters.ALL & ~filters.COMMAND, handle_content)]},
                fallbacks=[CommandHandler("cancel", cancel)],
            )
            app.add_handler(conv_doigui)

    print("Bot đang hoạt động ổn định với hệ thống đếm lượt thông minh!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
