from fastapi import FastAPI
import uvicorn
import domain.database as db_router
import logging
import utils
import asyncio
import signal

app = FastAPI()
app.include_router(router=db_router.router, prefix='/db', tags=['db'])
logging.basicConfig(filename=utils.create_current_log(), level=logging.INFO)


async def main():
    config = uvicorn.Config("main:app", host="127.0.0.1", port=8080, reload=True)
    server = uvicorn.Server(config)

    print('Kapellmeister waked up...')
    shutdown_event = asyncio.Event()

    def handle_signal():
        shutdown_event.set()

    if utils.is_unix_os():
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, handle_signal)
        loop.add_signal_handler(signal.SIGTERM, handle_signal)

    try:
        await asyncio.gather(
            server.serve(),
            shutdown_event.wait()
        )
    except asyncio.CancelledError:
        print("Server shutdown canceled or interrupted. Continuing cleanup...")
    finally:
        print("Gracefully shutting down...")
        utils.rename_current_log()
        try:
            await server.shutdown()
        except asyncio.CancelledError:
            print("Server shutdown was interrupted...")


if __name__ == '__main__':
    asyncio.run(main())
