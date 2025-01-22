from aiogram.utils.markdown import hide_link

from .texts_pics import pictures

# Add other languages and their corresponding codes as needed.
SUPPORTED_LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}

TEXT_BUTTONS = {
    "ru": {
        "add": "﹢ Добавить",
        "back": "‹ Назад",
        "main": "≡ Главная",
        "retry": "↻ Повторить",
        "delete": "× Удалить",
        "confirm": "✓ Подтвердить",

        "connect_wallet": "Подключить {wallet_name}",
        "open_wallet": "Перейти в {wallet_name}",
        "disconnect_wallet": "× Отключиться",

        "change_language": "↻ Изменить язык",
        "get_access": "🔍 Проверить наличие доступа",

        "newsletter": "📰 Новостная рассылка",
        "admins_menu": "👥 Администраторы",
        "chats_menu": "💬 Чаты",
        "tokens_menu": "💎 Токены",
        "edit_min_amount": "✎ Изменить минимальную сумму",
    },
    "en": {
        "add": "﹢ Add",
        "back": "‹ Back",
        "main": "≡ Main",
        "retry": "↻ Retry",
        "delete": "× Delete",
        "confirm": "✓ Confirm",

        "connect_wallet": "Connect {wallet_name}",
        "open_wallet": "Go to {wallet_name}",
        "disconnect_wallet": "× Disconnect",

        "change_language": "↻ Change Language",
        "get_access": "🔍 Check access availability",

        "newsletter": "📰 Newsletter",
        "admins_menu": "👥 Admins",
        "chats_menu": "💬 Chats",
        "tokens_menu": "💎 Tokens",
        "edit_min_amount": "✎ Edit minimum amount",
    }
}

TEXT_MESSAGES = {
    "ru": {
        "loader_text": "⏳",
        "outdated_text": "...",

        "main_menu": (
            f"{hide_link(pictures['Welcome'])}"
            "🤖 <b>Добро пожаловать!</b>\n\n"
            "Я - твой личный проводник в мире приватных чатов. "
            "Моя главная задача - предоставить тебе доступ к нашим приватным чатам, "
            "опираясь на наличие у тебя соответствующих токенов.\n\n"
            "<blockquote><b>Приватные чаты:</b>\n{chats}\n"
            "<b>Необходимые токены:</b>\n{tokens}</blockquote>\n\n"
            "Жми на <b>Проверить наличие доступа</b>, чтобы узнать, будешь ли ты допущен!\n\n"
            "<b>Подключен к:</b> {wallet}"
        ),
        "select_language": (
            f"{hide_link(pictures['Main'])}"
            "👋 <b>Привет!</b>\n\n"
            "Выбери язык:"
        ),
        "change_language": (
            f"{hide_link(pictures['Main'])}"
            "<b>Выбери язык:</b>"
        ),
        "deny_access": (
            f"{hide_link(pictures['Access denied'])}"
            "🚫 <b>Доступ запрещен</b>\n\n"
            "К сожалению, не обнаружены необходимые токены в твоем кошельке.\n\n"
            "Не расстраивайся, ты можешь <b>приобрести токены, перейдя по кнопкам</b> ниже и повторить попытку."
        ),
        "allow_access": (
            f"{hide_link(pictures['Access granted'])}"
            "🎉 <b>Поздравляем!</b>\n\n"
            "Тебе открыт доступ к нашим приватным чатам.\n\n"
            "<b>Переходи по кнопкам</b> ниже и подавай заявку на вступление, я сразу же их одобрю!"
        ),
        "user_kicked": (
            "👮‍♀️ Пользователь {user} [{wallet}] был исключен из чата!"
        ),

        "welcome_to_chat": (
            f"{hide_link(pictures['Welcome to chat'])}"
            "👋 <b>Добро пожаловать {user_full_name}!</b>\n\n"
            "{balances}"
        ),
        "top_holders": (
            f"{hide_link(pictures['TOP holders'])}"
            f"🏆 <b>ТОП Держателей токенов:</b>\n\n"
            "{top_holders}"
        ),
        "top_select_token": (
            f"{hide_link(pictures['TOP select token'])}"
            "🔍 <b>Выберите токен:</b>"
        ),
        "balance_command": (
            f"{hide_link(pictures['Balance command'])}"
            "👤 {user_full_name}\n\n{balances}"
        ),
        "balance_command_no_tokens": (
            f"{hide_link(pictures['Balance command no tokens'])}"
            "👤 {user_full_name}\n\n"
            "<b>Токены отсутствуют!</b>"
        ),

        "connect_wallet": (
            f"<a href='https://ton.org/ru/wallets?locale=ru&filters[wallet_features][slug][$in]=dapp-auth&pagination[limit]=-1'>Установить кошелек</a>\n\n"
            "<b>Подключи свой {wallet_name}!</b>\n\n"
            "Отсканируй с помощью мобильного кошелька:"
        ),
        "connect_wallet_proof_wrong": (
            f"{hide_link(pictures['Connect'])}"
            "<b>Предупреждение</b>\n\n"
            "Подпись кошелька поддельна или истекло время ожидания подключения."
        ),
        "connect_wallet_timeout": (
            f"{hide_link(pictures['Connect'])}"
            "<b>Предупреждение</b>\n\n"
            "Время ожидания подключения истекло."
        ),
        "connect_wallet_rejected": (
            f"{hide_link(pictures['Connect'])}"
            "<b>Предупреждение</b>\n\n"
            "Подключение кошелька было отклонено."
        ),

        "admin_menu": (
            f"{hide_link(pictures['Main'])}"
            "<b>Панель администратора</b>\n\nВыберите действие:"
        ),
        "chats_menu": (
            f"{hide_link(pictures['Main'])}"
            "<b>Меню приватных чатов</b>\n\nВыберите действие:"
        ),
        "chat_info": (
            f"{hide_link(pictures['Main'])}"
            "• <b>Информация о приватном чате</b>\n\n"
            "• <b>ID:</b>\n"
            "<blockquote>{chat_id}</blockquote>\n"
            "• <b>Тип:</b>\n"
            "<blockquote>{chat_type}</blockquote>\n"
            "• <b>Название:</b>\n"
            "<blockquote>{chat_name}</blockquote>\n"
            "• <b>Ссылка приглашения:</b>\n"
            "<blockquote>{chat_invite_link}</blockquote>\n"
            "• <b>Дата создания:</b>\n"
            "<blockquote>{chat_created_at}</blockquote>"
        ),
        "tokens_menu": (
            f"{hide_link(pictures['Main'])}"
            "<b>Меню токенов</b>\n\nВыберите действие:"
        ),
        "token_info": (
            f"{hide_link(pictures['Main'])}"
            "• <b>Информация о токене</b>\n\n"
            "• <b>Тип:</b>\n"
            "<blockquote>{token_type}</blockquote>\n"
            "• <b>Название:</b>\n"
            "<blockquote>{token_name}</blockquote>\n"
            "• <b>Адрес:</b>\n"
            "<blockquote>{token_address}</blockquote>\n"
            "• <b>Минимальная сумма:</b>\n"
            "<blockquote>{token_min_amount}</blockquote>\n"
            "• <b>Дата создания:</b>\n"
            "<blockquote>{token_created_at}</blockquote>"
        ),
        "token_send_address": "<b>Введите адрес токена</b>\n\nРазрешены только адреса коллекций NFT и мастеров Jetton:",
        "token_send_address_error": "Недопустимый адрес токена:\n{}",
        "token_send_address_error_already_exist": "Токен с адресом {address} уже существует!",
        "token_send_address_error_not_supported": "Контракт {interfaces} не поддерживается.\nПоддерживаются только {supported_interfaces}.",
        "token_send_amount": (
            "<b>Информация о токене</b>:\n\n"
            "• <b>Тип:</b>\n{token_type}\n"
            "• <b>Название:</b>\n{token_name}\n\n"
            "<b>Введите минимальную сумму токена</b> для доступа к приватному чату:"
        ),
        "token_edit_amount": "<b>Введите новую сумму токена</b> для доступа к приватному чату:",
        "token_send_amount_error": "Неверная сумма токена!",
        "admins_menu": (
            f"{hide_link(pictures['Main'])}"
            "<b>Меню администраторов</b>\n\nВыберите действие:"
        ),
        "admin_info": (
            f"{hide_link(pictures['Main'])}"
            "• <b>Информация об администраторе</b>\n\n"
            "• <b>ID:</b>\n"
            "<blockquote>{admin_id}</blockquote>\n"
            "• <b>Имя:</b>\n"
            "<blockquote>{admin_full_name}</blockquote>\n"
            "• <b>Имя пользователя:</b>\n"
            "<blockquote>{admin_username}</blockquote>\n"
            "• <b>Дата создания:</b>\n"
            "<blockquote>{admin_created_at}</blockquote>"
        ),
        "admin_send_id": "<b>Введите ID администратора:</b>",
        "admin_send_id_error": "Недопустимый ID:\n{}",
        "admin_send_id_error_not_found": "Администратор не найден. Сначала пользователь должен начать диалог с ботом.",
        "admin_send_id_error_not_member": "ID администратора должен быть числом.",
        "confirm_item_add": "<b>Подтвердите</b> добавление {item} в {table}?",
        "item_added": "{item} добавлен в {table}!",
        "confirm_item_delete": "<b>Подтвердите</b> удаление {item} из {table}?",
        "item_deleted": "{item} удален из {table}!"
    },
    "en": {
        "loader_text": "⏳",
        "outdated_text": "...",

        "main_menu": (
            f"{hide_link(pictures['Welcome'])}"
            "🤖 <b>Welcome!</b>\n\n"
            "I'm your personal guide in the world of private chats. "
            "My main task is to provide you with access to our private chats, "
            "based on your possession of the corresponding tokens.\n\n"
            "<blockquote><b>Private Chats:</b>\n{chats}\n"
            "<b>Required Tokens:</b>\n{tokens}</blockquote>\n\n"
            "Click on <b>Check access availability</b> to find out if you'll be admitted!\n\n"
            "<b>Connected to:</b> {wallet}"
        ),
        "select_language": (
            f"{hide_link(pictures['Main'])}"
            "👋 <b>Hello!</b>\n\n"
            "Choose a language:"
        ),
        "change_language": (
            f"{hide_link(pictures['Main'])}"
            "<b>Choose a language:</b>"
        ),
        "deny_access": (
            f"{hide_link(pictures['Access denied'])}"
            "🚫 <b>Access Denied</b>\n\n"
            "Unfortunately, I did not detect the required tokens in your wallet.\n\n"
            "Don't worry, you can <b>purchase tokens by clicking the buttons</b> below and try again."
        ),
        "allow_access": (
            f"{hide_link(pictures['Access granted'])}"
            "🎉 <b>Congratulations!</b>\n\n"
            "You have access to our private chats.\n\n"
            "<b>Click on the buttons</b> below and submit an application to join, "
            "I will approve them immediately!"
        ),
        "user_kicked": (
            "👮‍♀️ User {user} [{wallet}] was kicked from chat!"
        ),

        "welcome_to_chat": (
            f"{hide_link(pictures['Welcome to chat'])}"
            "👋 <b>Welcome {user_full_name}!</b>\n\n"
            "{balances}"
        ),
        "top_holders": (
            f"{hide_link(pictures['TOP holders'])}"
            f"🏆 <b>TOP Token Holders:</b>\n\n"
            "{top_holders}"
        ),
        "top_select_token": (
            f"{hide_link(pictures['TOP select token'])}"
            "🔍 <b>Select token:</b>"
        ),
        "balance_command": (
            f"{hide_link(pictures['Balance command'])}"
            "👤 {user_full_name}\n\n{balances}"
        ),
        "balance_command_no_tokens": (
            f"{hide_link(pictures['Balance command no tokens'])}"
            "👤 {user_full_name}\n\n"
            "<b>Tokens missing!</b>"
        ),

        "connect_wallet": (
            f"<a href='https://ton.org/wallets?locale=en&filters[wallet_features][slug][$in]=dapp-auth&pagination[limit]=-1'>Get a Wallet</a>\n\n"
            "<b>Connect your {wallet_name}!</b>\n\n"
            "Scan with your mobile app wallet:"
        ),
        "connect_wallet_proof_wrong": (
            f"{hide_link(pictures['Connect'])}"
            "<b>Warning</b>\n\n"
            "The wallet signature is wrong or the connection timeout has expired."
        ),
        "connect_wallet_timeout": (
            f"{hide_link(pictures['Connect'])}"
            "<b>Warning</b>\n\n"
            "The connection timeout has expired."
        ),
        "connect_wallet_rejected": (
            f"{hide_link(pictures['Connect'])}"
            "<b>Warning</b>\n\n"
            "The connection was rejected."
        ),

        "admin_menu": (
            f"{hide_link(pictures['Main'])}"
            "<b>Administrator Panel</b>\n\nSelect action:"
        ),
        "chats_menu": (
            f"{hide_link(pictures['Main'])}"
            "<b>Private Chats Menu</b>\n\nSelect action:"
        ),
        "chat_info": (
            f"{hide_link(pictures['Main'])}"
            "• <b>Private Chat Information</b>\n\n"
            "• <b>ID:</b>\n"
            "<blockquote>{chat_id}</blockquote>\n"
            "• <b>Type:</b>\n"
            "<blockquote>{chat_type}</blockquote>\n"
            "• <b>Name:</b>\n"
            "<blockquote>{chat_name}</blockquote>\n"
            "• <b>Invite Link:</b>\n"
            "<blockquote>{chat_invite_link}</blockquote>\n"
            "• <b>Creation Date:</b>\n"
            "<blockquote>{chat_created_at}</blockquote>"
        ),
        "tokens_menu": (
            f"{hide_link(pictures['Main'])}"
            "<b>Tokens Menu</b>\n\nSelect action:"
        ),
        "token_info": (
            f"{hide_link(pictures['Main'])}"
            "• <b>Token Information</b>\n\n"
            "• <b>Type:</b>\n"
            "<blockquote>{token_type}</blockquote>\n"
            "• <b>Name:</b>\n"
            "<blockquote>{token_name}</blockquote>\n"
            "• <b>Address:</b>\n"
            "<blockquote>{token_address}</blockquote>\n"
            "• <b>Minimum Amount:</b>\n"
            "<blockquote>{token_min_amount}</blockquote>\n"
            "• <b>Creation Date:</b>\n"
            "<blockquote>{token_created_at}</blockquote>"
        ),
        "token_send_address": "<b>Enter Token Address</b>\n\nOnly NFT collection and Jetton master addresses are allowed:",
        "token_send_address_error": "Invalid token address:\n{}",
        "token_send_address_error_already_exist": "Token with address {address} already exists!",
        "token_send_address_error_not_supported": "Contract {interfaces} is not supported.\nOnly {supported_interfaces} are supported.",
        "token_send_amount": (
            "<b>Token Information</b>:\n\n"
            "• <b>Type:</b>\n"
            "<blockquote>{token_type}</blockquote>\n"
            "• <b>Name:</b>\n"
            "<blockquote>{token_name}</blockquote>\n\n"
            "<b>Enter the minimum token amount</b> to access the private chat:"
        ),
        "token_edit_amount": "<b>Enter the new token amount</b> to access the private chat:",
        "token_send_amount_error": "Invalid token amount!",
        "admins_menu": (
            f"{hide_link(pictures['Main'])}"
            "<b>Administrators Menu</b>\n\nSelect action:"
        ),
        "admin_info": (
            f"{hide_link(pictures['Main'])}"
            "• <b>Administrator Information</b>\n\n"
            "• <b>ID:</b>\n"
            "<blockquote>{admin_id}</blockquote>\n"
            "• <b>Name:</b>\n"
            "<blockquote>{admin_full_name}</blockquote>\n"
            "• <b>Username:</b>\n"
            "<blockquote>{admin_username}</blockquote>\n"
            "• <b>Creation Date:</b>\n"
            "<blockquote>{admin_created_at}</blockquote>"
        ),
        "admin_send_id": "<b>Enter Administrator ID:</b>",
        "admin_send_id_error": "Invalid ID:\n{}",
        "admin_send_id_error_not_found": "Administrator not found. First, the user needs to start a conversation with the bot.",
        "admin_send_id_error_not_member": "Administrator ID must be a number.",
        "confirm_item_add": "<b>Confirm</b> adding {item} to {table}?",
        "item_added": "{item} added to {table}!",
        "confirm_item_delete": "<b>Confirm</b> deleting {item} from {table}?",
        "item_deleted": "{item} deleted from {table}!"
    }
}
