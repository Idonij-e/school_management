import asyncio
from pyppeteer import launch

async def main():
    print('lllllllllllllllll')
    browser = await launch({'headless': True})
    print(browser)
    print('ddddddddddddddddddd')
    page = await browser.newPage()
    print('aaaaaaaaaaaaaaaaaa')
    await page.goto('https://google.com')
    print('bbbbbbbbbbbbbbbbbbbbbb')

    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')
    print('cccccccccccccccccccccccccccccc')

    # print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()

asyncio.run(main())
