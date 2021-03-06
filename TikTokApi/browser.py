import asyncio
import pyppeteer
import random
import time
from pyppeteer_stealth import stealth


class browser:
    def __init__(self, url, language='en', proxy=None, find_redirect=False):
        self.url = url
        self.proxy = proxy
        self.language = language
        self.userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        self.args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-infobars",
            "--window-position=0,0",
            "--ignore-certifcate-errors",
            "--ignore-certifcate-errors-spki-list",
            "--user-agent=" + self.userAgent,
        ]

        if proxy != None:
            if "@" in proxy:
                self.args.append("--proxy-server=" + proxy.split(":")[0] + "://" + proxy.split("://")[1].split(":")[1].split("@")[1] + ":" + proxy.split("://")[1].split(":")[2])
            else:
                self.args.append("--proxy-server=" + proxy)
        self.options = {
            'args': self.args,
            'headless': True,
            'ignoreHTTPSErrors': True,
            'userDataDir': "./tmp",
            'handleSIGINT': False,
            'handleSIGTERM': False,
            'handleSIGHUP': False
        }

        loop = asyncio.new_event_loop()

        if find_redirect:
            loop.run_until_complete(self.find_redirect())
        else:
            loop.run_until_complete(self.start())

    async def start(self):
        self.browser = await pyppeteer.launch(self.options)
        self.page = await self.browser.newPage()

        # Check for user:pass proxy
        if self.proxy != None:
            if "@" in self.proxy:
                await  self.page.authenticate({ 
                'username': self.proxy.split("://")[1].split(":")[0], 
                'password': self.proxy.split("://")[1].split(":")[1].split("@")[0] 
                })

        await stealth(self.page)

        await self.page.emulate({'viewport': {
            'width': random.randint(320, 1920),
            'height': random.randint(320, 1920),
            'deviceScaleFactor': random.randint(1, 3),
            'isMobile': random.random() > 0.5,
            'hasTouch': random.random() > 0.5
        }})

        await self.page.setUserAgent(self.userAgent)

        await self.page.setExtraHTTPHeaders({
            'Accept-Language': self.language
        })

        await self.page.goto("https://www.tiktok.com/trending?lang=" + self.language, {
            'waitUntil': "load"
        })

        self.signature = await self.page.evaluate('''() => {
          var url = "''' + self.url + '''"
          var token = window.byted_acrawler.sign({url: url});
          return token;
          }''')
        await self.browser.close()

    
    async def find_redirect(self):
        self.browser = await pyppeteer.launch(self.options)
        self.page = await self.browser.newPage()

        await stealth(self.page)

        await self.page.emulate({'viewport': {
            'width': random.randint(320, 1920),
            'height': random.randint(320, 1920),
            'deviceScaleFactor': random.randint(1, 3),
            'isMobile': random.random() > 0.5,
            'hasTouch': random.random() > 0.5
        }})

        await self.page.setUserAgent(self.userAgent)

        await self.page.setExtraHTTPHeaders({
            'Accept-Language': self.language
        })

        await self.page.goto(self.url, {
            'waitUntil': "load"
        })

        self.redirect_url = self.page.url
