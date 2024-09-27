import os
import json
import asyncio
import argparse
import aiofiles
import httpx as hatetepe
import requests
import re
from datetime import datetime
from warna import *
from utilities import *
from logger import log

import logging
from colorlog import ColoredFormatter

# Define the log level (e.g., INFO, DEBUG, etc.)
LOG_LEVEL = logging.DEBUG  # You can change this to INFO, WARNING, ERROR, etc.

# Define the log format using your requested format with color support
LOGFORMAT = (
    "[%(asctime)s] "                # Timestamp (this will be formatted by `datefmt`)
    "| %(log_color)s%(levelname)-8s%(reset)s "  # Log level (colored)
    "| Line %(cyan)s%(lineno)d%(reset)s "       # Line number (in cyan)
    " - %(white)s%(message)s%(reset)s"          # The actual log message (in white)
)

# Create a colored formatter with the custom log format and date format
formatter = ColoredFormatter(
    LOGFORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",  # Specify the date/time format
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    },
    secondary_log_colors={},
    style='%',  # Using '%' style formatting
)

# Set up the stream handler (for logging to stdout)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)  # Apply the custom formatter to the stream

# Create and configure the log
log = logging.getLogger("pythonConfig")
log.setLevel(LOG_LEVEL)
log.addHandler(stream)  # Add the stream handler to the log


try:
    from config import *
except ImportError:
    os.system("cls")
    print(f"""
                   {rt}>>Config file not found<<
    Create a copy of {wt}config.py.example{rs}{rt} and rename it to {wt}config.py{rs}{rt}
    And fill in the required fields.{rs}
    """)
    exit()


# MENU
menu = f"""Please enter your selection:

    {rt}[0]{rs} Exit
    {g}[1]{rs} Hamster Skin
    {g}[3]{rs} Hamster Referral Link
"""


class Config:
    def __init__(self, settings):
        self.useragent = settings.get("UserAgent", None)
        self.countdown = settings.get("countdown", 300)
        self.interval = settings.get("interval", 3)
        self.skin_id = settings["HamsterSkin"]["skin_id"]
        self.card_max_lvl = settings["HamsterCard"]["card_max_lvl"]
        self.card_max_price = settings["HamsterCard"]["card_max_price"]
        
# Skin Buyer
class Hamster:
    def __init__(self, data: str, config: Config, acc_num: int):
        self.data = data,
        self.Authorization = f"Bearer {self.data[0]}"
        self.acc_num = acc_num
        self.skin_id = config.skin_id
        self.countdown = config.countdown
        self.interval = config.interval
        self.useragent = config.useragent
        self.isAndroidDevice = "Android" in self.useragent
        self.hams_url = "https://api.hamsterkombatgame.io",
        self.configVersion = ""
        self.ProfitPerHour = 0
        self.SpendTokens = 0
        self.card_max_lvl = config.card_max_lvl
        self.card_max_price = config.card_max_price
    
    async def Http(
        self,
        url,
        headers=None,
        method=None,
        validStatusCodes=200,
        default=None,
        json_payload=None
    ):
        defaultHeaders = {
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Host": "api.hamsterkombatgame.io",
            "Origin": "https://hamsterkombatgame.io",
            "Referer": "https://hamsterkombatgame.io/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": self.useragent,
        }
        
        # Add default headers for Android devices to avoid detection, Not needed for iOS devices
        if self.isAndroidDevice:
            defaultHeaders["HTTP_SEC_CH_UA_PLATFORM"] = '"Android"'
            defaultHeaders["HTTP_SEC_CH_UA_MOBILE"] = "?1"
            defaultHeaders["HTTP_SEC_CH_UA"] = (
                '"Android WebView";v="125", "Chromium";v="125", "Not.A/Brand";v="24"'
            )
            defaultHeaders["HTTP_X_REQUESTED_WITH"] = "org.telegram.messenger.web"
        
        # Add and replace new headers to default headers
        
        if default and headers: # GET
            for key, value in headers.items():
                defaultHeaders[key] = value
            headers = defaultHeaders
        
        try:
            if method == "GET":
                if json_payload:
                    res = await self.ses.get(url, headers=headers, json=json_payload)
                else:
                    res = await self.ses.get(url, headers=headers)
            elif method == "POST":
                if json_payload:
                    res = await self.ses.post(url, headers=headers, json=json_payload)
                else:
                    res = await self.ses.post(url, headers=headers)
            elif method == "OPTIONS":
                res = await self.ses.options(url, headers=headers)
            else:
                log.error(f"✖ Invalid method: {method}")
                return None

            if res.status_code != validStatusCodes:
                log.error(f"{gt}[Account Number {self.acc_num}]{rs}: ✖ Status code is not {rt}{validStatusCodes}{rs}")
                log.error(f"{gt}[Account Number {self.acc_num}]{rs}: ✖ Response: {rt}{res.text}{rs}")
                # log.error(f"{gt}[Account Number {self.acc_num}]{rs}: ✖ Response: {rt}{res.text.replace('<', '\\<')}{rs}")
                return None

            if "config-version" in res.headers:
                self.configVersion = res.headers["config-version"]

            if method == "OPTIONS":
                return True

            # print(res.text)
            return res.json()
        except Exception as err:
            log.opt(colors=False).error(f"{gt}[Account Number {self.acc_num}]{rs}: ✖ Http exception error: {rt}{err}{rs}")
            return None
    
    async def AccountInfo(self):
        url = f"https://api.hamsterkombatgame.io/auth/account-info"
        headers = {
            "Access-Control-Request-Headers": "authorization",
            "Access-Control-Request-Method": "POST",
        }

        # Send OPTIONS request
        await self.Http(url=url, headers=headers, method="OPTIONS", validStatusCodes=204)

        headers = {
            "Authorization": self.Authorization,
        }
        # Send POST request
        return await self.Http(url=url, headers=headers, method="POST", validStatusCodes=200)
    
    async def check_ip(self):
        headers = {
            "Accept": "application/json",
            "Access-Control-Request-Headers": "authorization",
            "Access-Control-Request-Method": "GET",
        }
        try:
            res = await self.Http(url="https://ipinfo.io/json", method="GET", headers=headers)
            ip = res.get("ip")
            city = res.get("city")
            region = res.get("region")
            country = res.get("country")
            log.info(f"{gt}[Account Number {self.acc_num}]{rs}: Using IP {wt}{ip}{rs}")
            log.info(f"{gt}[Account Number {self.acc_num}]{rs}: Country {wt}{country}{rs} | City {wt}{city}{rs}\n")
        except:
            log.error(f"{gt}[Account Number {self.acc_num}]{rs}: {rt}✖ Failed to get IP{rs}\n")
            return
    
    async def syncRequest(self):
        url = f"https://api.hamsterkombatgame.io/interlude/sync"
        headers = {
            "Access-Control-Request-Headers": self.Authorization,
            "Access-Control-Request-Method": "POST",
        }

        # Send OPTIONS request
        await self.Http(url=url, headers=headers, method="OPTIONS", validStatusCodes=204)

        headers = {
            "Authorization": self.Authorization,
        }
        # Send POST request
        return await self.Http(url=url, headers=headers, method="POST", validStatusCodes=200)
    
    async def getAccountData(self):
        account_data = await self.syncRequest()
        if account_data is None or account_data is False:
            log.error(f"{gt}[Account Number {self.acc_num}]{rs}: {rt}🌐 Unable to get account data.{rs}")
            return False

        if "interludeUser" not in account_data:
            log.error(f"{gt}[Account Number {self.acc_num}]{rs}: {rt}✖ Invalid account data.{rs}")
            return False

        if "balanceDiamonds" not in account_data["interludeUser"]:
            log.warning(f"{gt}[Account Number {self.acc_num}]{rs}: {rt}⚠ Invalid balance coins.{rs}")
            return False
        
        self.account_data = account_data
        self.balanceCoins = account_data["interludeUser"]["balanceDiamonds"]
        # self.availableTaps = account_data["interludeUser"]["availableTaps"]
        # self.maxTaps = account_data["interludeUser"]["maxTaps"]
        self.earnPassivePerHour = account_data["interludeUser"]["earnPassivePerHour"]
        # self.totalKeys = account_data["interludeUser"].get("totalKeys", 0)
        self.achievements = account_data['interludeUser']['achievements']
        self.skin = account_data['interludeUser']['skin']['available']

        return account_data
    
    async def GetAccountConfigVersionRequest(self):
        if self.configVersion == "":
            return None

        url = f"https://api.hamsterkombatgame.io/interlude/config/{self.configVersion}"
        headers = {
            "Access-Control-Request-Headers": "authorization",
            "Access-Control-Request-Method": "GET",
        }

        # Send OPTIONS request
        await self.Http(url=url, headers=headers, method="OPTIONS", validStatusCodes=204)

        headers = {
            "Authorization": self.Authorization,
        }

        # Send GET request
        return await self.Http(url=url, headers=headers, method="GET", validStatusCodes=200, default=True)
    
    async def GetAccountConfigRequest(self):
        url = "https://api.hamsterkombatgame.io/interlude/config"
        headers = {
            "Access-Control-Request-Headers": "authorization",
            "Access-Control-Request-Method": "POST",
        }

        # Send OPTIONS request
        await self.Http(url=url, headers=headers, method="OPTIONS", validStatusCodes=204)

        headers = {
            "Authorization": self.Authorization,
        }

        # Send POST request
        return await self.Http(url=url, headers=headers, method="POST", validStatusCodes=200)
    
    async def GetSkins(self):
        url = "https://api.hamsterkombatgame.io/interlude/get-skin"
        headers = {
            "Access-Control-Request-Headers": "authorization,content-type",
            "Authorization": self.Authorization,
            "Access-Control-Request-Method": "POST",
        }

        # Send OPTIONS request
        await self.Http(url=url, headers=headers, method="OPTIONS", validStatusCodes=204)

        headers = {
            "Accept": "application/json",
            "Authorization": self.Authorization,
            "Access-Control-Request-Method": "POST",
        }

        # Send POST request
        return await self.Http(url=url, headers=headers, method="POST", validStatusCodes=200)
    
    async def BuySkin(self, skinId):
        for skin in self.skin:
            if skin['skinId'] == skinId:
                log.warning(f"{gt}[Account Number {self.acc_num}]{rs}: {yt}⚠ {wt}{skinId} {yt}is already exist in account.{rs}")
                return False
        url = "https://api.hamsterkombatgame.io/interlude/buy-skin"
        headers = {
            "Access-Control-Request-Headers": "authorization,content-type",
            "Authorization": self.Authorization,
            "Access-Control-Request-Method": "POST",
        }

        # Send OPTIONS request
        await self.Http(url=url, headers=headers, method="OPTIONS", validStatusCodes=204)

        headers = {
            "Accept": "application/json",
            "Authorization": self.Authorization,
            "Content-Type": "application/json",
        }

        payload = {
            "skinId": str(skinId),
            "timestamp": int(datetime.now().timestamp()),
        }

        headers = {
            "Authorization": self.Authorization
        }
        # Send POST request
        return await self.Http(url=url, headers=headers, method="POST", validStatusCodes=200, json_payload=payload)
    
    async def accountloading(self):
            # log.info(f"{gt}[Account Number {self.acc_num}]{rs}: 📡 Getting account IP.")
            # await self.check_ip()
            
            log.info(f"{gt}[Account Number {self.acc_num}]{rs}: 🛸 Getting basic account data.")
            AccountBasicData = await self.AccountInfo()
            if (
                AccountBasicData is None
                or AccountBasicData is False
                or "accountInfo" not in AccountBasicData
                or "id" not in AccountBasicData["accountInfo"]
            ):
                log.error(f"{gt}[Account Number {self.acc_num}]{rs}: {rt}✖ Unable to get account basic data.{rs}")
                return False
            
            log.info(f"{gt}[Account Number {self.acc_num}]{rs}: ├─ Account ID: {wt}{AccountBasicData['accountInfo']['id']}{rs}")
            log.info(f"{gt}[Account Number {self.acc_num}]{rs}: └─ Account Name: {wt}{AccountBasicData['accountInfo']['name']}{rs}\n")
            
            log.info(f"{gt}[Account Number {self.acc_num}]{rs}: 🌱 Getting account data.")
            getAccountDataStatus = await self.getAccountData()
            if getAccountDataStatus is False:
                return False
            
            log.info(f"{gt}[Account Number {self.acc_num}]{rs}: 💰 Account Balance Coins: {wt}{number_to_string(round(self.balanceCoins, 2))}{rs}")
            return True
            # log.info(f"{gt}[Account Number {self.acc_num}]{rs}: ├─ Available Taps: {wt}{self.availableTaps}{rs} | Max Taps: {wt}{self.maxTaps}{rs}")
            # log.info(f"{gt}[Account Number {self.acc_num}]{rs}: └─ Total Keys: {wt}{self.totalKeys}{rs}\n")

            # log.info(f"{gt}[Account Number {self.acc_num}]{rs}: 📝 Getting account config data.")
            # AccountConfigVersionData = None
            # if self.configVersion != "":
            #     AccountConfigVersionData = await self.GetAccountConfigVersionRequest()
            #     self.configData = AccountConfigVersionData.get("config", {})
            #     log.info(f"{gt}[Account Number {self.acc_num}]{rs}: └─ Account config version: {wt}{self.configVersion}{rs}\n")
            
            # AccountConfigData = await self.GetAccountConfigRequest()
            # if AccountConfigData is None or AccountConfigData is False:
            #     log.error(f"{gt}[Account Number {self.acc_num}]{rs}: {rt}✖ Unable to get account config data.{rs}")
            #     return
    
    async def BuyUpgradeRequest(self, UpgradeId):
        url = "https://api.hamsterkombatgame.io/interlude/buy-upgrade"
        headers = {
            "Access-Control-Request-Headers": "authorization,content-type",
            "Access-Control-Request-Method": "POST",
        }

        # Send OPTIONS request
        await self.Http(url=url, headers=headers, method="OPTIONS", validStatusCodes=204)

        headers = {
            "Authorization": self.Authorization,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        payload = {
                "upgradeId": UpgradeId,
                "timestamp": int(datetime.now().timestamp() * 1000),
            }

        # Send POST request
        return await self.Http(url=url, headers=headers, method="POST", validStatusCodes=200, json_payload=payload)
    
    async def UpgradesForBuyRequest(self):
        url = "https://api.hamsterkombatgame.io/interlude/upgrades-for-buy"
        headers = {
            "Access-Control-Request-Headers": "authorization",
            "Access-Control-Request-Method": "POST",
        }

        # Send OPTIONS request
        await self.Http(url=url, headers=headers, method="OPTIONS", validStatusCodes=204)

        headers = {
            "Authorization": self.Authorization,
        }

        # Send POST request
        return await self.Http(url=url, headers=headers, method="POST", validStatusCodes=200)
    
    async def BuyCard(self, card):
        upgradesResponse = await self.BuyUpgradeRequest(card["id"])
        
        if upgradesResponse:
            log.info(f"{gt}[Account Number {self.acc_num}]{rs}: ✅ {wt}{card["name"]}{rs} bought successfully.")
            self.balanceCoins -= int(card["price"])
            self.ProfitPerHour += card["profitPerHourDelta"]
            self.SpendTokens += int(card["price"])
            self.earnPassivePerHour += card["profitPerHourDelta"]
            return True
    
    async def BuyCardForAchive(self):
        count = 0
        await self.getAccountData()
        for achiev in self.achievements:
            exist = False
            if achiev['id'] == "upgrade_card_to_level_15_5":
                exist = True
                break
        if not exist:
            log.info(f"{gt}[Account Number {self.acc_num}]{rs}: 🃏 Get card list.")
            upgradesResponse = await self.UpgradesForBuyRequest()
            if upgradesResponse is None:
                log.error(f"{gt}[Account Number {self.acc_num}]{rs}: ✖ Failed to get upgrades list.")
                return False
            
            upgrades = [
                item
                for item in upgradesResponse["upgradesForBuy"]
                if not item["isExpired"]
                and item["isAvailable"]
                and item["profitPerHourDelta"] > 0
            ]
            if len(upgrades) == 0:
                log.warning(f"{gt}[Account Number {self.acc_num}]{rs}: 🍃 No upgrades available.")
                return False
            
            log.info(f"{gt}[Account Number {self.acc_num}]{rs}: 💠 Checking for upgrade.")
            for card in upgrades:
                if int(card['level']) < self.card_max_lvl and round(card['price'], 2) < self.card_max_price:
                    continue
                if round(self.balanceCoins, 2) < round(card['price'], 2):
                    log.warning(f"{gt}[Account Number {self.acc_num}]{rs}: {yt}😪 For {wt}{card['name']} {yt}Balance is too low to buy.{rs}")
                    continue
                count += 1
                await self.BuyCard(card)
                await countdown(2)
        return count
    
    async def start(self, proxy=None, type=None):
        if proxy is None:
            self.ses = hatetepe.AsyncClient()
        else:
            self.ses = hatetepe.AsyncClient(proxy=proxy)
        
        # Acoount Loading
        accountloading = await self.accountloading()
        if not accountloading:
            log.error(f"{gt}[Account Number {self.acc_num}]{rs}: {rt}Accountloading not working!{rs}")
            return
        
        # Option Selection
        if type == "skin":
            # Sking Buying
            while True:
                try:
                    skins = await self.GetSkins()  # Await the coroutine to get the result
                    break
                except:
                    log.error(f"{gt}[Account Number {self.acc_num}]{rs}: {rt}GetSkins is not working!{rs}")
            for skin in skins['skins']:
                res_buy = await self.BuySkin(skin['id'])
                if res_buy:
                    log.info(f"{gt}[Account Number {self.acc_num}]{rs}: ✔ {skin['id']} bought successfully!")
                # await countdown(2)
            log.info(f"{gt}All skins bought for accounts!{rs}")
            # await countdown(self.countdown)
        elif type == "card_achive":
            # Card Buying
            while True:
                res = await self.BuyCardForAchive()
                log.info(f"{gt}All cards bought for accounts!{rs}")
                await countdown(self.countdown)
                if res == 0:
                    break
        

async def main():
    banner = rf"""
    {gb} _   _                     _             {mb} _____           _     
    {gb}| | | | __ _ _ __ ___  ___| |_ ___ _ __  {mb}|_   _|__   ___ | |___
    {gb}| |_| |/ _` | '_ ` _ \/ __| __/ _ \ '__|   {mb}| |/ _ \ / _ \| / __|
    {gb}|  _  | (_| | | | | | \__ \ ||  __/ |      {mb}| | (_) | (_) | \__ \
    {gb}|_| |_|\__,_|_| |_| |_|___/\__\___|_|      {mb}|_|\___/ \___/|_|___/
    """
    arg = argparse.ArgumentParser()
    arg.add_argument("-D", "--data", default="data.txt")
    arg.add_argument("-P", "--proxy", default="proxies.txt")
    arg.add_argument("-A", "--action", type=int, help="Action to perform")
    args = arg.parse_args()
    action = arg.parse_args().action
    
    if not os.path.exists(args.data):
        print(f"{rt}File {wt}{args.data}{rt} is not found!{rs}")
        exit()
    if not os.path.exists(args.proxy):
        print(f"{rt}File {wt}{args.proxy}{rt} is not found!{rs}")
        exit()
    
    # MENU
    if action == None or action not in [1, 2]:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{banner}{rs}\n    Version: 1.1 {"~" * 33} Developed by: {cb}Mmd{rs}\n")
        print(menu)
        while True:
            try:
                action = input(f"{wb}>{rs} ")
            except EOFError:
                break
            if not action.isdigit():
                print(f"{rt}Action must be number!{rs}")
            elif action not in ["0", "1", "2"]:
                print(f"{rt}Action must be in menu!{rs}")
            else:
                action = int(action)
                break
    
    if action == 0:
        exit()
    elif action == 1:
        print(f"{mb}Hamster Skin Selected!{rs}")
        # await countdown(2)
        async with aiofiles.open(args.data) as dr:
            dread = await dr.read()
            datas = [i for i in dread.splitlines() if len(i) > 10]
        use_proxy = False
        async with aiofiles.open(args.proxy) as pr:
            pr = await pr.read()
            proxies = [i for i in pr.splitlines() if len(i) > 0]
            if len(proxies) > 0:
                use_proxy = True
        log.info(f"{gt}Total Account: {wt}{len(datas)}{rs}")
        if len(datas) <= 0:
            log.info(f"{rt}0 Account detected, please input your data first!{rs}")
            exit()
        log.info(f"{gt}Use Proxy: {wt}{use_proxy}{rs}")
        print(wt + "~" * 60)
        config = Config(settings)
        while True:
            for acc_num, data in enumerate(datas):
                if use_proxy:
                    proxy = proxies[acc_num % len(proxies)]
                else:
                    proxy = None
                await Hamster(data, config, acc_num + 1).start(proxy=proxy, type="skin")
                print(wt + "~" * 60)
                log.info(f"{rs}Cooldown for {rt}{config.interval}{rs} second.")
                await countdown(config.interval)
    elif action == 2:
        print(f"{mb}Hamster Referral Link Selected!{rs}")
        with open('data.txt', 'r') as data:
            lines = data.readlines()
        auth = [line.strip() for line in lines]

        ref = []
        count = 0
        for token in auth:
            count += 1
            # match = re.search(r'\d+$', token)
            match = re.search(r'\d{10}$', token)
            id = match.group()
            ref.append(f"https://t.me/hamster_koMbat_bot/start?startapp=kentId{id}")

        with open('referral.txt', 'w') as referral:
            referral.write('\n'.join(ref) + '\n')
        
        print(f"{wt}{count} {gt}Referral links generated.{rs}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info(f"{r}Stop by user!{rs}")
        exit()
