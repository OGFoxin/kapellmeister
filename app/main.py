from fastapi import FastAPI
import app.drivers.http_controller as db_router
from utils import is_unix_os, rename_current_log, get_config_path
from infrastructure.config_controller import AsyncFileConfig
from use_cases.config_reader import ConfigReader
import asyncio
import signal

async def main():
    app = FastAPI()
    app.include_router(router=db_router.router, prefix='/db', tags=['db'])

    app_cfg = AsyncFileConfig(config_path=get_config_path(), reload_interval=5)
    cfg_use_case = ConfigReader(app_cfg, app)
    server, logger = await cfg_use_case.execute()
    asyncio.create_task(app_cfg.check_for_updates())

    logger.info(f'waked up...')
    shutdown_event = asyncio.Event()

    def handle_signal():
        shutdown_event.set()

    if is_unix_os():
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, handle_signal)
        loop.add_signal_handler(signal.SIGTERM, handle_signal)

    try:
        await asyncio.gather(
            server.serve(),
            shutdown_event.wait()
        )
    except asyncio.CancelledError:
        logger.info("Server shutdown canceled or interrupted. Continuing cleanup...")
    finally:
        logger.info("Gracefully shutting down...")
        rename_current_log()
        try:
            await server.shutdown()
        except asyncio.CancelledError:
            logger.info("Server shutdown was interrupted...")


if __name__ == '__main__':
    asyncio.run(main())
