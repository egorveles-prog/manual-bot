from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

import json
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 687844961


def load_users():
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(data):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_manuals():
    with open("manuals.json", "r", encoding="utf-8") as f:
        return json.load(f)


def is_allowed(user_id):
    users = load_users()
    return user_id in users["users"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if not is_allowed(user_id):
        await update.message.reply_text(
            f"⛔ У вас немає доступу.\n\n"
            f"Ваш ID:\n{user_id}\n\n"
            f"Надішліть цей ID адміністратору."
        )
        return

    keyboard = [
        [
            InlineKeyboardButton("Mayekawa", callback_data="mayekawa"),
            InlineKeyboardButton("JBT", callback_data="jbt")
        ],
        [
            InlineKeyboardButton("FoodMate", callback_data="foodmate"),
            InlineKeyboardButton("Baader", callback_data="baader")
        ],
        [
            InlineKeyboardButton("Stork", callback_data="stork"),
            InlineKeyboardButton("FHF", callback_data="fhf")
        ],
        [
            InlineKeyboardButton("AMF", callback_data="amf"),
            InlineKeyboardButton("Dimaq", callback_data="dimaq")
        ],
        [
            InlineKeyboardButton("KFC", callback_data="kfc")
        ],
        [
            InlineKeyboardButton(
                "⚠️ Типові несправності",
                callback_data="faults"
            )
        ]
    ]

    await update.message.reply_text(
        "Оберіть розділ:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def allow_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "⛔ Тільки адміністратор."
        )
        return

    try:
        new_user_id = int(context.args[0])

        users = load_users()

        if new_user_id not in users["users"]:
            users["users"].append(new_user_id)

        save_users(users)

        await update.message.reply_text(
            f"✅ Користувач {new_user_id} доданий."
        )

    except Exception:
        await update.message.reply_text(
            "Приклад:\n/allow 123456789"
        )


async def users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    users = load_users()

    text = "👥 Користувачі:\n\n"

    for user in users["users"]:
        text += f"{user}\n"

    await update.message.reply_text(text)


async def list_manuals(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_allowed(update.effective_user.id):
        return

    manuals = load_manuals()

    text = "📚 Список мануалів:\n\n"

    for item in manuals.values():
        text += f"• {item['name']}\n"

    await update.message.reply_text(text)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
143
 
144
query = update.callback_query
145
await query.answer()
146
 
147
if query.data == "faults":
148
 
149
await query.message.reply_text(
150
"⚠️ Типові несправності\n\n"
151
"🔹 Не запускається\n"
152
"1. Перевірити аварійні кнопки\n"
153
"2. Перевірити автоматичні вимикачі\n"
154
"3. Перевірити живлення\n\n"
155
"🔹 Помилка датчика\n"
156
"1. Очистити датчик\n"
157
"2. Перевірити кабель\n"
158
"3. Перевірити кріплення\n\n"
159
"🔹 Помилка частотника\n"
160
"1. Записати код помилки\n"
161
"2. Перезапустити обладнання\n"
162
"3. Викликати електрика\n\n"
163
"🔹 Проблема філетування\n"
164
"1. Перевірити ножі\n"
165
"2. Перевірити напрямні\n"
166
"3. Перевірити налаштування\n\n"
167
"🔹 Заклинювання конвеєра\n"
168
"1. Зупинити обладнання\n"
169
"2. Перевірити ланцюг\n"
170
"3. Перевірити привід"
171
)
172
return
173
 
174
manuals = load_manuals()
175
 
176
if query.data in manuals:
177
 
178
item = manuals[query.data]
179
 
180
await query.message.reply_text(
181
f"✅ {item['name']}\n\n"
182
f"🔗 {item['url']}"
183
)
184
 
185
 
186
async def search_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
187
 
188
if not is_allowed(update.effective_user.id):
189
 
190
await update.message.reply_text(
191
"⛔ Доступ заборонений."
192
)
193
return
194
 
195
query = update.message.text.lower().strip()
196
 
197
manuals = load_manuals()
198
 
199
for item in manuals.values():
200
 
201
if query in item["name"].lower():
202
 
203
await update.message.reply_text(
204
f"✅ {item['name']}\n\n"
205
f"🔗 {item['url']}"
206
)
207
return
208
 
209
for keyword in item.get("keywords", []):
210
 
211
keyword = keyword.lower()
212
 
213
if (
214
query == keyword
215
or query in keyword
216
or keyword in query
217
):
218
await update.message.reply_text(
219
f"✅ {item['name']}\n\n"
220
f"🔗 {item['url']}"
221
)
222
return
223
 
224
await update.message.reply_text(
225
"❌ Нічого не знайдено."
226
)
227
 
228
 
229
app = Application.builder().token(TOKEN).build()
230
 
231
app.add_handler(CommandHandler("start", start))
232
app.add_handler(CommandHandler("list", list_manuals))
233
app.add_handler(CommandHandler("allow", allow_user))
234
app.add_handler(CommandHandler("users", users_list))
235
 
236
app.add_handler(
237
CallbackQueryHandler(button_handler)
238
)
239
 
240
app.add_handler(
241
MessageHandler(
242
filters.TEXT & ~filters.COMMAND,
243
search_manual
244
)
245
)
246
 
247
print("Bot started")
248
 
249
app.run_polling()
