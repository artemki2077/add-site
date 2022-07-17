from flask import Flask, render_template, redirect, session, request
from os import listdir
from hashlib import sha256
from threading import Thread
import telebot
import json


def read_bot_setting():
    with open("bot_settings.json", "r") as f:
        return json.load(f)


def write_bot_setting(b_set):
    with open("bot_settings.json", "w") as f:
        json.dump(b_set, f, indent=4)


bot_settings = read_bot_setting()
bot = telebot.TeleBot(bot_settings["bot_token"])
app = Flask(__name__)
app.secret_key = 'maxar2005'

blogs = {}

users = {
    "artem": 'd9cc3330ec40a15465b0e9d348a20a3a6270c3788320ed5be734ef2bfda9d4de',
    "admin": 'd9cc3330ec40a15465b0e9d348a20a3a6270c3788320ed5be734ef2bfda9d4de'
}
def get_blogs():
    return json.load(open("etc/blog.json", "r"))

def save_blog(e):
    json.dump(e, open("etc/blog.json", "w"), indent=4)


def get_price():
    global pricing, additional_services
    pricing = json.load(open("etc/pricing.json", "r"))
    additional_services = json.load(open("etc/additional_services.json", "r"))

def save_price(s_price, s_addit):
    json.dump(s_price, open("etc/pricing.json", "w"), indent=4)
    json.dump(s_addit, open("etc/additional_services.json", "w"), indent=4)
    
@bot.message_handler(commands=["start", "help", "h"])
def start(message: telebot.types.Message):
    if message.chat.id not in bot_settings["all_ids"]:
        bot_settings["all_ids"].append(message.chat.id)
        bot_settings["active_ids"].append(message.chat.id)
        write_bot_setting(bot_settings)
    bot.send_message(message.chat.id, 'hi, this bot serves so that you receive requests for cleaning on the site, you do not need to write anything to the bot, it will send everything to you automatically, if you do not want to receive a message, then write /stop')

@bot.message_handler(commands=["stop"])
def start(message: telebot.types.Message):
    if message.chat.id not in bot_settings["all_ids"]:
        bot_settings["all_ids"].append(message.chat.id)
        bot_settings["active_ids"].append(message.chat.id)
    bot_settings["active_ids"].remove(message.chat.id)
    write_bot_setting(bot_settings)
    bot.send_message(message.chat.id, 'Вы не будете получать сообщения\nДля активации сообщений пропишите /active')


@bot.message_handler(commands=["active"])
def start(message: telebot.types.Message):
    if message.chat.id not in bot_settings["all_ids"]:
        bot_settings["all_ids"].append(message.chat.id)
        bot_settings["active_ids"].append(message.chat.id)
    if message.chat.id not in bot_settings["active_ids"]:
        bot_settings["active_ids"].append(message.chat.id)
    write_bot_setting(bot_settings)
    bot.send_message(message.chat.id, 'Вы будете получать сообщения\nДля дезактивации сообщений пропишите /stop')

@app.route("/")
def page_main():
    global pricing, additional_services
    return render_template("main.html", pricing=pricing, additional_services=additional_services)


@app.route("/adminka")
def page_admin_main():
    if session.get('login') not in users:
        return redirect('/admin')
    return render_template("admin.html")


@app.route("/adminka/pricing", methods=['POST', 'GET'])
def page_admin_pricing_main():
    if session.get('login') not in users:
        return redirect('/admin')
    if request.method == "POST":
        req_json = request.json
        s_pricing = req_json.get('pricing')
        s_addit = req_json.get('addit')
        if req_json and s_pricing and s_addit:
            save_price(s_pricing, s_addit)
            get_price()
            return "SUCCESS"
        else:
            return "error"
    get_price()
    return render_template("pricing.html", pricing=json.dumps(pricing), additional_services=json.dumps(additional_services))


@app.route("/adminka/blogs", methods=["POST", "GET"])
def page_admin_blogs_main():
    global blogs
    if session.get('login') not in users:
        return redirect('/admin')
    if request.method == "POST":
        s_blog = request.json
        if s_blog:
            save_blog(s_blog)
            blogs = get_blogs()
            return "success"
        else:
            return 'error'
    print(blogs)
    return render_template('admin_blogs.html',  blogs=blogs)
    


@app.route("/admin", methods=['POST', 'GET'])
def page_admin():
    if session.get('login') in users:
        redirect('/adminka')
    error = ''
    if request.method == "POST":
        login = str(request.form.get('login'))
        password = str(request.form.get('password'))
        if users.get(login) and sha256(password.encode()).hexdigest() == users[login]:
            session['login'] = login
            return redirect("/adminka")
        else:
            error = 'error with login or password'
    return render_template("login.html", error=error)


@app.route("/Book", methods=['POST', "GET"])
def page_book():
    if request.method == "POST":
        all_p = pricing.copy()
        for key, value in additional_services.items():  # use for loop to iterate dict2 into the dict3 dictionary 
            all_p[key] = value 
        name = str(request.form.get('name'))
        phone = str(request.form.get('phone'))
        mail = str(request.form.get('mail'))
        addr = str(request.form.get('addr'))
        apt = str(request.form.get('apt'))
        books = list(filter(lambda x: request.form[x] == 'on', request.form))
        answer = f'name: {name}\nphone: {phone}\nemail: {mail}\naddress: {addr}\napt/suite: {apt}\nbook:'
        su = 0
        for i in books:
            su += all_p[i]
            answer += f"\n  •{i} - ${all_p[i]}"
        answer += f'sum: {su}\ntax: {su * 0.13}\nTOTAL: {su * 1.13}'
        for i in bot_settings["active_ids"]:
            bot.send_message(i, answer)
        return 'ok'

    return render_template("book.html", pricing=pricing, additional_services=additional_services)


@app.route("/Blog")
def page_blog():
    global blogs
    return render_template("blog.html", blogs=blogs)

def start_web():
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)


if __name__ == "__main__":
    get_price()
    blogs = get_blogs()
    th = Thread(target=start_web, args=())
    th.start()
    bot.polling(non_stop=True)
