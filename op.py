import asyncio
from pyppeteer import launch

async def request_optimism_faucet(wallet_address: str):
    browser = await launch(headless=False, args=['--no-sandbox'])
    page = await browser.newPage()
    
    # Navigate to the Optimism Goerli faucet page
    await page.goto('https://faucet.quicknode.com/optimism/goerli', {'waitUntil': 'networkidle2'})
    
    # Wait for the wallet address input field
    await page.waitForSelector('input[placeholder="Enter your wallet address"]')
    
    # Type the wallet address
    await page.type('input[placeholder="Enter your wallet address"]', wallet_address)
    
    # Click the "Request funds" button
    # Adjust selector if necessary; here we look for a button containing the text "Request funds"
    buttons = await page.xpath("//button[contains(., 'Request funds')]")
    if buttons:
        await buttons[0].click()
    else:
        print("Request button not found.")
        await browser.close()
        return
    
    # Wait for success confirmation message (adjust selector if needed)
    try:
        await page.waitForSelector('.chakra-alert', timeout=10000)  # Example class for alert messages
        print(f"Successfully requested Optimism Goerli tokens for wallet {wallet_address}")
    except asyncio.TimeoutError:
        print("No confirmation message detected. Request may have failed or is pending.")
    
    await browser.close()

if __name__ == '__main__':
    wallet = '0xYourOptimismWalletAddressHere'
    asyncio.run(request_optimism_faucet(wallet))
