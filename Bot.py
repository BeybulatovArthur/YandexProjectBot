import telebot
import Telega
import time
import pyautogui
import cv2Code

connection = False
user_id = 0
HotkeyMode = False


with open(r"teletoken.txt") as token:
    token = token.readline()
bot = telebot.TeleBot(token)

print("Session started: {}")
Session_name = input("Name: ")
Session_passw = input("Password: ")

@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.chat.id,"Bot enabled")
    TL = Telega.Telega(message)
    TL.Reply_btns("///",True,1,"/session")


@bot.message_handler(commands = ["session"])
def sesion_connect(message):

    if not(connection):
        bot.send_message(message.chat.id,f"Session name: {Session_name}")
        password_check(message)
    if connection:
        TL = Telega.Telega(message)
        TL.Reply_btns(f"Session name: {Session_name}",True,1, "/disconnect")

def password_check(message):
    bot.send_message(message.chat.id,"Enter password:")
    bot.register_next_step_handler(message, password_enter)
def password_enter(message):
    global connection, id
    if message.text == Session_passw:
        connection = True
        TL = Telega.Telega(message)
        id = message.from_user.id
        TL.Reply_btns("Connection established",True,3, "/LKM","/2LKM","/RKM","/Hotkey","/PrtSc", "/Cam","/session")
    else:
        bot.send_message(message.chat.id,"Wrong password, try again.")
        password_check(message)

@bot.message_handler(commands = ["disconnect"])
def disconnect(message):
    global connection, id
    if message.from_user.id == id:
        TL = Telega.Telega(message)
        TL.Reply_btns("Disconnected", True, 1, "/session", "/start")
        connection = False
        id = 0

@bot.message_handler(commands = ["PrtSc"])
def PrtSc(message):
    if connection and message.from_user.id == id:
        time.sleep(1)
        screen = pyautogui.screenshot('screenshot1.png')
        cv2Code.add_cursor('screenshot1.png')
        with open("screenshot1.png","rb") as screen:
            bot.send_photo(message.chat.id, screen)

@bot.message_handler(commands = ["Cam"])
def Cam(message):
    if connection and message.from_user.id == id:
        for i in range(4,-1,-1):
            if cv2Code.PhotoCam(i):
                with open("cam_old.png", "rb") as screen:
                    bot.send_photo(message.chat.id, screen)

@bot.message_handler(commands = ["LKM"])
def LKM(message):
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"'Lclick'")
        pyautogui.click(button='left')
        PrtSc(message)

@bot.message_handler(commands = ["2LKM"])
def double_LKM(message):
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"'2Lclick'")
        pyautogui.click(clicks = 2,button='left')
        PrtSc(message)

@bot.message_handler(commands = ["RKM"])
def RKM(message):
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"'Rclick'")
        pyautogui.click(button='right')
        PrtSc(message)

@bot.message_handler(commands = ["Hotkey"])
def Hotkey(message):
    global HotkeyMode
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"Enter hotkey")
        HotkeyMode = True

@bot.message_handler(content_types = ["text"])
def message_check(message):
    global HotkeyMode
    text = message.text
    if HotkeyMode:
        pyautogui.hotkey(text.split("+"))
        HotkeyMode = False
    else:
       text = message.text
       pyautogui.write(text)

@bot.message_handler(content_types = ["photo"])
def message_check(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("screenshot.png", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Catched")
    x,y = cv2Code.coords("screenshot.png")
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(x,y)
    PrtSc(message)


bot.polling(none_stop=True,interval = 0,long_polling_timeout = 100)