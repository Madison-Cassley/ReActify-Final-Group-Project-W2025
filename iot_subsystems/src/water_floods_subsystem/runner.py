import os
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv

#load env
dotenv_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path)

from water_floods_subsystem.interfaces.system_interface import WaterFloodsSystem

env = os.getenv("ENVIRONMENT", "DEVELOPMENT").upper()

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
)
root.addHandler(ch)

fh = logging.FileHandler("system.log")
fh.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
)
root.addHandler(fh)

logger = logging.getLogger(__name__)

def main() -> None:
    """
    Instantiate the WaterFloodsSystem and hand control over to its async loop.
    """
    system = WaterFloodsSystem()
    logger.info("Starting WaterFloodsSystem...")
    try:
        asyncio.run(system.run())
    except Exception as e:
        logger.exception("Unexpected error in main loop", exc_info=e)
    else:
        logger.info("WaterFloodsSystem shut down cleanly.")

if __name__ == "__main__":
    main()
