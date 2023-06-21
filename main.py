import asyncio
import aiohttp

TOKEN = "Token"
WEBHOOK_URL = "Your Webhook URL"
SERVER_ID = "Your Server ID"
VANITY_LIST = ["url1", "url2", "url3"]
DELAY = 0.1
claimed = False

async def notify(url, json):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json) as response:
            return response.status

async def claim(url, json):
    global claimed
    if claimed:
        return
    claimed = True
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": TOKEN,
            "X-Audit-Log-Reason": "console vanity sniper",
            "Content-Type": "application/json",
        }
        async with session.patch(url, json=json, headers=headers) as response:
            print(response.status)
            if response.status in (200, 201):
                print(f"[+] Vanity claimed: {json['code']}")
                await notify(WEBHOOK_URL, {"content": f"||@everyone|| GG! {json['code']}"})
            else:
                print(f"[-] Failed to claim vanity: {json['code']} | status: {response.status}")
                await notify(WEBHOOK_URL, {"content": f"||@everyone|| Oops, something going wrong! {json['code']} | status: {response.status}"})
            return response.status

async def fetch_vanity(vanity, x):
    if not vanity:
        return
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": TOKEN}
        async with session.get(f"https://canary.discord.com/api/v10/invites/{vanity}", headers=headers) as response:
            status = response.status
            if status == 404:
                idk2 = await claim(
                    f"https://canary.discord.com/api/v10/guilds/{SERVER_ID}/vanity-url",
                    {"code": vanity}
                )
                if idk2 in (200, 201, 204):
                    print(f"[+] Claimed Vanity: {vanity}")
                    await notify(WEBHOOK_URL, {"content": f"||@everyone|| GG! {vanity}"})
                    claimed = True
                    raise SystemExit("SystemExit")
                else:
                    await notify(WEBHOOK_URL, {"content": f"||@everyone|| Oops, something going wrong! {vanity} | status: {idk2}"})
                    raise SystemExit
            elif status == 200:
                print(f"[+] Attempt: {x} | Vanity: {vanity}")
            elif status == 429:
                await notify(WEBHOOK_URL, {"content": "*[-] Rate Limit Problem, Lets change proxy.*"})
                print("[-] Rate Limit Problem")
                raise SystemExit(1)
            else:
                print("[-] An unexpected error occurred")
                raise SystemExit(1)
    await asyncio.sleep(DELAY)

async def thread_executor(vanity, x):
    while True:
        try:
            await fetch_vanity(vanity, x)
            break
        except Exception as error:
            print(f"[-] Thread is paused, Thread ID: {x}")
            continue

async def main():
    print("Clearing console and preparing...")
    print("Logging into the Discord account...")
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": TOKEN}
            async with session.get("https://canary.discord.com/api/v9/users/@me", headers=headers) as response:
                if response.status in (200, 201, 204):
                    user = await response.json()
                    id = user["id"]
                    username = user["username"]
                    print(f"Successfully logged in as {username} | {id}")
                elif response.status == 429:
                    raise SystemExit(1)
                else:
                    async with aiohttp.ClientSession() as session:
                        headers = {"Content-Type": "application/json"}
                        await session.post(WEBHOOK_URL, json={"content": "||@everyone|| Unable to establish a connection to the Discord websocket."}, headers=headers)
                    print("Bad Auth")
                    raise SystemExit(1)

        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/json"}
            await session.post(WEBHOOK_URL, json={"content": f"The client is now ready with the following vanity URLs: {VANITY_LIST}"}, headers=headers)

        for x in range(100000000):
            for i in range(len(VANITY_LIST)):
                if claimed:
                    raise SystemExit(1)
                await asyncio.sleep(DELAY)
                await thread_executor(VANITY_LIST[i], x)

    except Exception as error:
        print("An error occurred:", error)

asyncio.run(main())
