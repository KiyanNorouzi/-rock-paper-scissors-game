from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import PeerIdInvalid
from collections import defaultdict

# Use your own API ID and Hash obtained from my.telegram.org
api_id = "24568836"
api_hash = "508ece28c77bb7f33bcd326ef179b890"
bot_token = "6438444330:AAEWP3WyU7gsxKL2cNojxhMFh9XN1cvgcWs"

# Initialize the Pyrogram Client
app = Client("rock_paper_scissors_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Dictionaries to keep track of games, points, and language preferences
rooms = defaultdict(dict)  # Stores players and their choices in a room
invite_status = defaultdict(dict)  # Keeps track of which player is inviting and expecting inputs
language_preferences = defaultdict(lambda: "ru")  # Default language is Russian for all users

# Language translations (English, Russian, Persian, Arabic, and Turkish)
translations = {
    "en": {
        "welcome": "Welcome to the 3-player Rock-Paper-Scissors Game!\nClick the button below to invite players.",
        "invite": "You have been invited to a 3-player Rock-Paper-Scissors game by {}.\nClick /accept to start playing.",
        "enter_player2": "Please enter the username for Player 2:",
        "enter_player3": "Please enter the username for Player 3:",
        "accept": "You accepted the invitation! Let's play.",
        "make_choice": "Make your choice:",
        "game_restart": "Game is being restarted as either all chose the same or all chose different!",
        "outcome_win": "{} beats {}. Winner: {}",
        "winner": "🎉 Winner: {}",
        "loser": "❌ Loser: {}",
        "ranking": "Final Rankings:\n1st: {}\n2nd: {}\n3rd: {}",
        "end_game_button": "End Game ❌",
        "next_round_button": "Next Round 🔄",
        "rock": "Rock 🪨",
        "paper": "Paper 📄",
        "scissors": "Scissors ✂️",
        "player_accepted": "Player {} has accepted the invitation!",
        "accept_button": "Accept ✅",
        "result_table": "Current Points:\n{}",
        "next_round_prompt": "All players have finished this round. Click the button to start the next round.",
        "invite_button": "Invite Players",
        "choose_language": "Please choose your language:",
        "lang_english": "English 🇬🇧",
        "lang_russian": "Russian 🇷🇺",
        "lang_persian": "Persian 🇮🇷",
        "lang_arabic": "Arabic 🇸🇦",
        "lang_turkish": "Turkish 🇹🇷"
    },
    "ru": {
        "welcome": "Добро пожаловать в игру Камень-Ножницы-Бумага для 3 игроков!\nНажмите кнопку ниже, чтобы пригласить игроков.",
        "invite": "Вас пригласил {} в игру Камень-Ножницы-Бумага для 3 игроков.\nНажмите /accept, чтобы начать играть.",
        "enter_player2": "Введите имя пользователя для игрока 2:",
        "enter_player3": "Введите имя пользователя для игрока 3:",
        "accept": "Вы приняли приглашение! Давайте играть.",
        "make_choice": "Сделайте ваш выбор:",
        "game_restart": "Игра перезапущена, так как все выбрали одинаково или все выбрали разные!",
        "outcome_win": "{} побеждает {}. Победитель: {}",
        "winner": "🎉 Победитель: {}",
        "loser": "❌ Проигравший: {}",
        "ranking": "Итоговый рейтинг:\n1-е: {}\n2-е: {}\n3-е: {}",
        "end_game_button": "Завершить игру ❌",
        "next_round_button": "Следующий раунд 🔄",
        "rock": "Камень 🪨",
        "paper": "Бумага 📄",
        "scissors": "Ножницы ✂️",
        "player_accepted": "Игрок {} принял приглашение!",
        "accept_button": "Принять ✅",
        "result_table": "Текущие очки:\n{}",
        "next_round_prompt": "Все игроки закончили этот раунд. Нажмите кнопку, чтобы начать следующий раунд.",
        "invite_button": "Пригласить игроков",
        "choose_language": "Пожалуйста, выберите язык:",
        "lang_english": "Английский 🇬🇧",
        "lang_russian": "Русский 🇷🇺",
        "lang_persian": "Персидский 🇮🇷",
        "lang_arabic": "Арабский 🇸🇦",
        "lang_turkish": "Турецкий 🇹🇷"
    },
    "fa": {
        "welcome": "به بازی سنگ-کاغذ-قیچی سه نفره خوش آمدید!\nبرای دعوت از بازیکنان دکمه زیر را فشار دهید.",
        "invite": "شما به بازی سنگ-کاغذ-قیچی سه نفره توسط {} دعوت شده‌اید.\nبرای شروع بازی، کلیک کنید /accept.",
        "enter_player2": "لطفاً نام کاربری بازیکن دوم را وارد کنید:",
        "enter_player3": "لطفاً نام کاربری بازیکن سوم را وارد کنید:",
        "accept": "شما دعوت را پذیرفتید! بیایید بازی کنیم.",
        "make_choice": "انتخاب خود را انجام دهید:",
        "game_restart": "بازی دوباره شروع می‌شود چون همه همان انتخاب را انجام دادند یا انتخاب‌های متفاوت داشتند!",
        "outcome_win": "{} {} را شکست داد. برنده: {}",
        "winner": "🎉 برنده: {}",
        "loser": "❌ بازنده: {}",
        "ranking": "رتبه‌بندی نهایی:\nاول: {}\nدوم: {}\nسوم: {}",
        "end_game_button": "پایان بازی ❌",
        "next_round_button": "دور بعد 🔄",
        "rock": "سنگ 🪨",
        "paper": "کاغذ 📄",
        "scissors": "قیچی ✂️",
        "player_accepted": "بازیکن {} دعوت را پذیرفت!",
        "accept_button": "پذیرفتن ✅",
        "result_table": "امتیازات فعلی:\n{}",
        "next_round_prompt": "همه بازیکنان این دور را به پایان رساندند. برای شروع دور بعد دکمه را فشار دهید.",
        "invite_button": "دعوت از بازیکنان",
        "lang_persian": "فارسی 🇮🇷"
    },
    "ar": {
        "welcome": "مرحبًا بك في لعبة حجر-ورق-مقص الثلاثية!\nاضغط الزر أدناه لدعوة اللاعبين.",
        "invite": "تمت دعوتك إلى لعبة حجر-ورق-مقص ثلاثية بواسطة {}.\nاضغط /accept لبدء اللعب.",
        "enter_player2": "يرجى إدخال اسم المستخدم للاعب الثاني:",
        "enter_player3": "يرجى إدخال اسم المستخدم للاعب الثالث:",
        "accept": "لقد قبلت الدعوة! دعنا نلعب.",
        "make_choice": "اختر خيارك:",
        "game_restart": "يتم إعادة تشغيل اللعبة لأن الجميع اختاروا نفس الخيار أو اختاروا خيارات مختلفة!",
        "outcome_win": "{} يهزم {}. الفائز: {}",
        "winner": "🎉 الفائز: {}",
        "loser": "❌ الخاسر: {}",
        "ranking": "الترتيب النهائي:\nالأول: {}\nالثاني: {}\nالثالث: {}",
        "end_game_button": "إنهاء اللعبة ❌",
        "next_round_button": "الجولة التالية 🔄",
        "rock": "صخرة 🪨",
        "paper": "ورق 📄",
        "scissors": "مقص ✂️",
        "player_accepted": "اللاعب {} قد قبل الدعوة!",
        "accept_button": "قبول ✅",
        "result_table": "النقاط الحالية:\n{}",
        "next_round_prompt": "أنهى جميع اللاعبين هذه الجولة. اضغط على الزر لبدء الجولة التالية.",
        "invite_button": "دعوة اللاعبين",
        "lang_arabic": "العربية 🇸🇦"
    },
    "tr": {
        "welcome": "3 kişilik Taş-Kağıt-Makas Oyununa Hoş Geldiniz!\nOyuncuları davet etmek için aşağıdaki düğmeye tıklayın.",
        "invite": "{} tarafından 3 kişilik Taş-Kağıt-Makas oyununa davet edildiniz.\nOynamaya başlamak için /accept'e tıklayın.",
        "enter_player2": "Lütfen 2. oyuncunun kullanıcı adını girin:",
        "enter_player3": "Lütfen 3. oyuncunun kullanıcı adını girin:",
        "accept": "Daveti kabul ettiniz! Hadi oynayalım.",
        "make_choice": "Seçiminizi yapın:",
        "game_restart": "Tüm oyuncular aynı seçimi yaptı veya herkes farklı şeyler seçtiği için oyun yeniden başlıyor!",
        "outcome_win": "{} {} yendi. Kazanan: {}",
        "winner": "🎉 Kazanan: {}",
        "loser": "❌ Kaybeden: {}",
        "ranking": "Nihai Sıralama:\n1. {}\n2. {}\n3. {}",
        "end_game_button": "Oyunu Bitir ❌",
        "next_round_button": "Sonraki Raunt 🔄",
        "rock": "Taş 🪨",
        "paper": "Kağıt 📄",
        "scissors": "Makas ✂️",
        "player_accepted": "{} oyuncusu daveti kabul etti!",
        "accept_button": "Kabul Et ✅",
        "result_table": "Mevcut Puanlar:\n{}",
        "next_round_prompt": "Tüm oyuncular bu raundu tamamladı. Sonraki raundu başlatmak için düğmeye tıklayın.",
        "invite_button": "Oyuncuları Davet Et",
        "lang_turkish": "Türkçe 🇹🇷"
    }
}

# Helper function to get player identity (Username or "Anonymous" if not available)
def get_player_identity(user):
    return f"@{user.username}" if user.username else user.first_name

# Helper function to format result table using Telegram username/first name instead of user ID
async def format_result_table(client, points, lang):
    table = ""
    for player_id, point in points.items():
        user = await client.get_users(player_id)
        table += f"{get_player_identity(user)}: {point} points\n"
    return table

# Helper function to get the preferred language of the user
def get_translation(user_id, key):
    lang = language_preferences[user_id]
    return translations[lang][key]

# Start Command with Language Selection
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    # Ask for language preference
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(translations["en"]["lang_english"], callback_data="set_lang_en"),
         InlineKeyboardButton(translations["ru"]["lang_russian"], callback_data="set_lang_ru")],
        [InlineKeyboardButton(translations["fa"]["lang_persian"], callback_data="set_lang_fa"),
         InlineKeyboardButton(translations["ar"]["lang_arabic"], callback_data="set_lang_ar")],
        [InlineKeyboardButton(translations["tr"]["lang_turkish"], callback_data="set_lang_tr")]
    ])
    await message.reply(translations["en"]["choose_language"], reply_markup=keyboard)

# Set language to English
@app.on_callback_query(filters.regex("set_lang_en"))
async def set_language_english(client, callback_query):
    user_id = callback_query.from_user.id
    language_preferences[user_id] = "en"  # Set language to English
    await callback_query.answer()
    
    # Send welcome message in English
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(translations["en"]["invite_button"], callback_data="invite_button")]
    ])
    await client.send_message(user_id, translations["en"]["welcome"], reply_markup=keyboard)

# Set language to Russian
@app.on_callback_query(filters.regex("set_lang_ru"))
async def set_language_russian(client, callback_query):
    user_id = callback_query.from_user.id
    language_preferences[user_id] = "ru"  # Set language to Russian
    await callback_query.answer()

    # Send welcome message in Russian
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(translations["ru"]["invite_button"], callback_data="invite_button")]
    ])
    await client.send_message(user_id, translations["ru"]["welcome"], reply_markup=keyboard)

# Set language to Persian
@app.on_callback_query(filters.regex("set_lang_fa"))
async def set_language_persian(client, callback_query):
    user_id = callback_query.from_user.id
    language_preferences[user_id] = "fa"  # Set language to Persian (Farsi)
    await callback_query.answer()

    # Send welcome message in Persian
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(translations["fa"]["invite_button"], callback_data="invite_button")]
    ])
    await client.send_message(user_id, translations["fa"]["welcome"], reply_markup=keyboard)

# Set language to Arabic
@app.on_callback_query(filters.regex("set_lang_ar"))
async def set_language_arabic(client, callback_query):
    user_id = callback_query.from_user.id
    language_preferences[user_id] = "ar"  # Set language to Arabic
    await callback_query.answer()

    # Send welcome message in Arabic
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(translations["ar"]["invite_button"], callback_data="invite_button")]
    ])
    await client.send_message(user_id, translations["ar"]["welcome"], reply_markup=keyboard)

# Set language to Turkish
@app.on_callback_query(filters.regex("set_lang_tr"))
async def set_language_turkish(client, callback_query):
    user_id = callback_query.from_user.id
    language_preferences[user_id] = "tr"  # Set language to Turkish
    await callback_query.answer()

    # Send welcome message in Turkish
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(translations["tr"]["invite_button"], callback_data="invite_button")]
    ])
    await client.send_message(user_id, translations["tr"]["welcome"], reply_markup=keyboard)

# When the "Invite Players" button is clicked
@app.on_callback_query(filters.regex("invite_button"))
async def invite_players(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.answer()  # Close the button callback

    # Set the invite_status to expect the second player's username
    invite_status[user_id] = {'stage': 'player2', 'player1_id': user_id}
    await client.send_message(user_id, get_translation(user_id, "enter_player2"))

# When the user enters a username (for Player 2 or Player 3)
@app.on_message(filters.private)
async def process_invitation(client, message: Message):
    user_id = message.from_user.id

    # Check if the user is in the invite process
    if user_id in invite_status:
        status = invite_status[user_id]
        stage = status['stage']

        # Handling Player 2's username
        if stage == 'player2':
            try:
                player_2 = await client.get_users(message.text)
                invite_status[user_id]['player2_id'] = player_2.id
                invite_status[user_id]['stage'] = 'player3'  # Move to next stage (Player 3)
                await client.send_message(user_id, get_translation(user_id, "enter_player3"))
            except PeerIdInvalid:
                await message.reply("Invalid username for Player 2. Please enter a valid username.")

        # Handling Player 3's username
        elif stage == 'player3':
            try:
                player_3 = await client.get_users(message.text)
                player_2_id = invite_status[user_id]['player2_id']
                player_1_id = invite_status[user_id]['player1_id']

                room_id = f"room_{player_1_id}_{player_2_id}_{player_3.id}"  # Create a unique room ID

                # Initialize room data, including points
                rooms[room_id] = {
                    'players': [player_1_id, player_2_id, player_3.id],
                    'choices': {player_1_id: None, player_2_id: None, player_3.id: None},
                    'points': {player_1_id: 0, player_2_id: 0, player_3.id: 0}  # Points start at 0 for all players
                }

                # Send invitations to both players with an Accept button
                inviter = await client.get_users(player_1_id)
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(get_translation(player_2_id, "accept_button"), callback_data="accept")],
                ])
                await client.send_message(player_2_id, get_translation(player_2_id, "invite").format(get_player_identity(inviter)), reply_markup=keyboard)

                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(get_translation(player_3.id, "accept_button"), callback_data="accept")]
                ])
                await client.send_message(player_3.id, get_translation(player_3.id, "invite").format(get_player_identity(inviter)), reply_markup=keyboard)

                # Send the same accept button to the inviter (Player 1)
                await client.send_message(player_1_id, get_translation(player_1_id, "invite").format(get_player_identity(inviter)),
                                          reply_markup=keyboard)

                # Send confirmation to the inviter and clean up invite_status
                await message.reply(f"Invitations sent to {get_player_identity(player_2)} and {get_player_identity(player_3)}!")
                del invite_status[user_id]

            except PeerIdInvalid:
                await message.reply("Invalid username for Player 3. Please enter a valid username.")

# Accept Command for a 3-player game via Button
@app.on_callback_query(filters.regex("accept"))
async def accept_via_button(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.answer()  # Close the button callback
    room_id = next((room_id for room_id, room in rooms.items() if user_id in room['players']), None)

    if room_id:
        room = rooms[room_id]
        room['choices'][user_id] = ""  # Indicate that this player has accepted

        # Notify all players that the player has accepted the invite
        user = await client.get_users(user_id)
        for player in room['players']:
            await client.send_message(player, get_translation(player, "player_accepted").format(get_player_identity(user)))

        # Check if all players have accepted
        if all(room['choices'][player] == "" for player in room['players']):
            await start_game(client, room_id)  # Start the game automatically
    else:
        await callback_query.answer("You are not invited to any game.")

# Function to start the game
async def start_game(client, room_id):
    room = rooms[room_id]
    await play_game(client, room_id)

# Play the game
async def play_game(client, room_id):
    room = rooms[room_id]
    for player in room['players']:
        await send_choice_keyboard(client, player)

# Send Choice Keyboard to Players (Rock, Paper, Scissors)
async def send_choice_keyboard(client, user_id):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(get_translation(user_id, "rock"), callback_data="rock")],
        [InlineKeyboardButton(get_translation(user_id, "paper"), callback_data="paper")],
        [InlineKeyboardButton(get_translation(user_id, "scissors"), callback_data="scissors")]
    ])
    await client.send_message(user_id, get_translation(user_id, "make_choice"), reply_markup=keyboard)

# Handle Player Choices
@app.on_callback_query(filters.regex("rock|paper|scissors"))
async def handle_choice(client, callback_query):
    user_id = callback_query.from_user.id
    choice = callback_query.data

    # Find the room that this player is in
    room_id = next((room_id for room_id, room in rooms.items() if user_id in room['players']), None)

    if room_id:
        room = rooms[room_id]
        room['choices'][user_id] = choice  # Store the player's choice

        # Check if all players have made their choices
        if all(room['choices'][player] for player in room['players']):
            await resolve_game(client, room_id)
    else:
        await callback_query.answer("You are not in a game!")

# Resolve the game between three players
async def resolve_game(client, room_id):
    room = rooms[room_id]
    choices = [room['choices'][player] for player in room['players']]

    # If all players chose the same, or all chose different, restart the game
    if len(set(choices)) == 1 or len(set(choices)) == 3:
        for player in room['players']:
            await client.send_message(player, get_translation(player, "game_restart"))
        await play_game(client, room_id)
    else:
        await determine_winner(client, room_id)

# Determine the winner based on Rock-Paper-Scissors rules
async def determine_winner(client, room_id):
    room = rooms[room_id]
    choices = room['choices']
    points = room['points']  # Points dictionary

    player_1, player_2, player_3 = room['players']
    choice_1, choice_2, choice_3 = choices[player_1], choices[player_2], choices[player_3]

    # Standard Rock-Paper-Scissors logic
    wins = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    winners = []
    losers = []

    # Determine who wins based on two matching choices
    if wins[choice_1] == choice_2:
        winners.append(player_1)
        losers.append(player_2)
    elif wins[choice_2] == choice_1:
        winners.append(player_2)
        losers.append(player_1)
    if wins[choice_2] == choice_3:
        winners.append(player_2)
        losers.append(player_3)
    elif wins[choice_3] == choice_2:
        winners.append(player_3)
        losers.append(player_2)
    if wins[choice_1] == choice_3:
        winners.append(player_1)
        losers.append(player_3)
    elif wins[choice_3] == choice_1:
        winners.append(player_3)
        losers.append(player_1)

    # Award points to winners
    for winner in winners:
        points[winner] += 5  # Add 5 points to the winner's score

    # Announce winners and losers
    for player in room['players']:
        if player in winners:
            user = await client.get_users(player)
            for p in room['players']:
                await client.send_message(p, get_translation(p, "winner").format(get_player_identity(user)))
        if player in losers:
            user = await client.get_users(player)
            for p in room['players']:
                await client.send_message(p, get_translation(p, "loser").format(get_player_identity(user)))

    # Display result table using Telegram ID or first name
    result_table = await format_result_table(client, points, language_preferences)
    for player in room['players']:
        await client.send_message(player, get_translation(player, "result_table").format(result_table))

    # Offer next round button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(get_translation(player, "next_round_button"), callback_data="next_round")]
    ])
    for player in room['players']:
        await client.send_message(player, get_translation(player, "next_round_prompt"), reply_markup=keyboard)

# Handle next round button
@app.on_callback_query(filters.regex("next_round"))
async def next_round(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.answer()  # Close the button callback

    # Find the room that this player is in
    room_id = next((room_id for room_id, room in rooms.items() if user_id in room['players']), None)

    if room_id:
        room = rooms[room_id]
        room['choices'][user_id] = ""  # Mark this player as ready for the next round

        # Check if all players are ready for the next round
        if all(room['choices'][player] == "" for player in room['players']):
            await start_game(client, room_id)  # Start the next round
    else:
        await callback_query.answer("You are not in a game!")

if __name__ == "__main__":
    app.run()
