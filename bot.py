from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
2
from telegram.ext import (
3
Application,
4
CommandHandler,
5
MessageHandler,
6
CallbackQueryHandler,
7
ContextTypes,
8
filters
9
)
10
 
11
import json
12
import os
13
 
14
TOKEN = os.getenv("BOT_TOKEN")
15
ADMIN_ID = 687844961
16
 
17
 
18
def load_users():
19
with open("users.json", "r", encoding="utf-8") as f:
20
return json.load(f)
21
 
22
 
23
def save_users(data):
24
with open("users.json", "w", encoding="utf-8") as f:
25
json.dump(data, f, ensure_ascii=False, indent=2)
26
 
27
 
28
def load_manuals():
29
with open("manuals.json", "r", encoding="utf-8") as f:
30
return json.load(f)
31
 
32
 
33
def is_allowed(user_id):
34
users = load_users()
35
return user_id in users["users"]
36
 
37
 
38
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
39
 
40
user_id = update.effective_user.id
41
 
42
if not is_allowed(user_id):
43
 
44
await update.message.reply_text(
45
f"⛔ У вас немає доступу.\n\n"
46
f"Ваш ID:\n{user_id}\n\n"
47
f"Надішліть цей ID адміністратору."
48
)
49
return
50
 
51
keyboard = [
52
[
53
InlineKeyboardButton("Mayekawa", callback_data="mayekawa"),
54
InlineKeyboardButton("JBT", callback_data="jbt")
55
],
56
[
57
InlineKeyboardButton("FoodMate", callback_data="foodmate"),
58
InlineKeyboardButton("Baader", callback_data="baader")
59
],
60
[
61
InlineKeyboardButton("Stork", callback_data="stork"),
62
InlineKeyboardButton("FHF", callback_data="fhf")
63
],
64
[
65
InlineKeyboardButton("AMF", callback_data="amf"),
66
InlineKeyboardButton("Dimaq", callback_data="dimaq")
67
],
68
[
69
InlineKeyboardButton("KFC", callback_data="kfc")
70
],
71
[
72
InlineKeyboardButton(
73
"⚠️ Типові несправності",
74
callback_data="faults"
75
)
76
]
77
]
78
 
79
await update.message.reply_text(
80
"🔧 Оберіть розділ:",
81
reply_markup=InlineKeyboardMarkup(keyboard)
82
)
83
 
84
 
85
async def allow_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
86
 
87
if update.effective_user.id != ADMIN_ID:
88
 
89
await update.message.reply_text(
90
"⛔ Тільки адміністратор."
91
)
92
return
93
 
94
try:
95
 
96
new_user_id = int(context.args[0])
97
 
98
users = load_users()
99
 
100
if new_user_id not in users["users"]:
101
users["users"].append(new_user_id)
102
 
103
save_users(users)
104
 
105
await update.message.reply_text(
106
f"✅ Користувач {new_user_id} доданий."
107
)
108
 
109
except Exception:
110
 
111
await update.message.reply_text(
112
"Приклад:\n/allow 123456789"
113
)
114
 
115
 
116
async def users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
117
 
118
if update.effective_user.id != ADMIN_ID:
119
return
120
 
121
users = load_users()
122
 
123
text = "👥 Користувачі:\n\n"
124
 
125
for user in users["users"]:
126
text += f"{user}\n"
127
 
128
await update.message.reply_text(text)
129
 
130
 
131
async def list_manuals(update: Update, context: ContextTypes.DEFAULT_TYPE):
132
 
133
if not is_allowed(update.effective_user.id):
134
return
135
 
136
manuals = load_manuals()
137
 
138
text = "📚 Список мануалів:\n\n"
139
 
140
for item in manuals.values():
141
text += f"• {item['name']}\n"
142
 
143
await update.message.reply_text(text)
144
 
145
 
146
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
147
 
148
query = update.callback_query
149
 
150
await query.answer()
151
 
152
if query.data == "faults":
153
 
154
await query.message.reply_text(
155
"⚠️ Типові несправності\n\n"
156
"Розділ у наповненні.\n\n"
157
"Сюди можна буде додати окремі мануали та інструкції."
158
)
159
return
160
 
161
manuals = load_manuals()
162
 
163
if query.data in manuals:
164
 
165
item = manuals[query.data]
166
 
167
await query.message.reply_text(
168
f"✅ {item['name']}\n\n"
169
f"🔗 {item['url']}"
170
)
171
 
172
 
173
async def search_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
174
 
175
if not is_allowed(update.effective_user.id):
176
 
177
await update.message.reply_text(
178
"⛔ Доступ заборонений."
179
)
180
return
181
 
182
query = update.message.text.lower().strip()
183
 
184
manuals = load_manuals()
185
 
186
for item in manuals.values():
187
 
188
if query in item["name"].lower():
189
 
190
await update.message.reply_text(
191
f"✅ {item['name']}\n\n"
192
f"🔗 {item['url']}"
193
)
194
return
195
 
196
for keyword in item.get("keywords", []):
197
 
198
keyword = keyword.lower()
199
 
200
if (
201
query == keyword
202
or query in keyword
203
or keyword in query
204
):
205
 
206
await update.message.reply_text(
207
f"✅ {item['name']}\n\n"
208
f"🔗 {item['url']}"
209
)
210
return
211
 
212
await update.message.reply_text(
213
"❌ Нічого не знайдено."
214
)
215
 
216
 
217
app = Application.builder().token(TOKEN).build()
218
 
219
app.add_handler(CommandHandler("start", start))
220
app.add_handler(CommandHandler("list", list_manuals))
221
app.add_handler(CommandHandler("allow", allow_user))
222
app.add_handler(CommandHandler("users", users_list))
223
 
224
app.add_handler(
225
CallbackQueryHandler(button_handler)
226
)
227
 
228
app.add_handler(
229
MessageHandler(
230
filters.TEXT & ~filters.COMMAND,
231
search_manual
232
)
233
)
234
 
235
print("Bot started")
236
 
237
app.run_polling()
