import time
import asyncio
from src.helpers.loader import loader
from .run_monitor import run_monitor
from src.services.summary_maker import summary_maker

data = loader()
config = data[1]
websites = data[0]

async def main():
    result = await run_monitor(config, websites)
    summary_maker(result)

cycle_count = 1
while cycle_count != 2: #intenialy using 2, so that logic exist while reducing waiting time in testing
    print(f"**************** Cycle: {cycle_count} *************")
    asyncio.run(main())
    cycle_count += 1
    time.sleep(config.interval_minutes)