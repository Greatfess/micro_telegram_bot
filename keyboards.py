from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_1 = InlineKeyboardButton('Большую!', callback_data='большую')
inline_btn_2 = InlineKeyboardButton('Маленькую...', callback_data='маленькую')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)

inline_btn_3 = InlineKeyboardButton('Картой!', callback_data='картой')
inline_btn_4 = InlineKeyboardButton('Наличкой...', callback_data='наличкой')
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_3, inline_btn_4)

inline_btn_5 = InlineKeyboardButton('Да!', callback_data='accept')
inline_btn_6 = InlineKeyboardButton('Отменить заказ...', callback_data='reset')
inline_kb3 = InlineKeyboardMarkup().add(inline_btn_5, inline_btn_6)
