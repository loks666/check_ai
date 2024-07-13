import time
import pyperclip
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_driver_path = "./chromedriver.exe"
plugin_path = "./xpathHelper.crx"

options = webdriver.ChromeOptions()
options.add_extension(plugin_path)
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)
wait_time = 15


def wait_for_element(xpath, timeout=wait_time):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def send_text(xpath, text, timeout=wait_time):
    time.sleep(1)  # 调整等待时间以确保元素已加载
    element = wait_for_element(xpath, timeout)
    element.clear()
    element.send_keys(text)


def click_element(xpath, timeout=wait_time):
    time.sleep(1)  # 调整等待时间以确保元素已加载
    element = wait_for_element(xpath, timeout)
    element.click()


def login(email, password):
    driver.get('https://canvas.illinois.edu/')
    send_text("//input[@type='email']", email)
    click_element("//input[@type='submit']")
    send_text("//input[@name='passwd']", password)
    click_element("//input[@type='submit']")


async def monitor_clipboard():
    global driver
    last_text = pyperclip.paste()
    print("监控剪贴板内容，复制文本将触发操作...")

    while True:
        await asyncio.sleep(1)
        current_text = pyperclip.paste()
        if current_text != last_text:
            print("检测到新的剪贴板内容...")
            print(f"复制的文本: {current_text}")

            # 打开新的窗口
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])

            # 打开指定网址并发送复制的文本
            driver.get('https://www.zerogpt.com/')
            await asyncio.sleep(1)
            send_text("//textarea[@id='textArea']", current_text)
            click_element("//button[@class='scoreButton']")

            # 切换回原始窗口
            driver.switch_to.window(driver.window_handles[0])

            last_text = current_text


async def main():
    global driver
    task = asyncio.create_task(monitor_clipboard())
    login("kehan5@illinois.edu", "LLl18010020413")
    await task


if __name__ == "__main__":
    asyncio.run(main())
