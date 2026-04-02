"""GoIPPro Voice Support Gateway — FreeSWITCH ESL on port 9002"""
import asyncio
import logging
from esl_server import ESLOutboundServer
from web_ui import start_web_ui
from config_loader import load_config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

async def main():
    config = load_config(path="config/config.yaml")
    logger.info("Starting GoIPPro Voice Support Gateway on ESL port 9002...")
    await start_web_ui(port=8083)
    esl = ESLOutboundServer(config, port=9003)
    await esl.start()

if __name__ == "__main__":
    asyncio.run(main())
