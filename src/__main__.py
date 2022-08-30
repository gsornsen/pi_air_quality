from cli import get_cli_args
from config import get_config
from typing import Dict
import asyncio
from app import App
import signal


async def main():  
    args = await get_cli_args()
    operating_mode: str = 'sim' if 'sim' in args.mode.lower() else 'normal'
    write_flag: bool = True if args.write else False
    verbose_flag: bool = True if args.verbose else False
    simulation_flag: bool = True if 'sim' in operating_mode else False
    config: Dict = await get_config(operating_mode)
    app = App(config, write_data=write_flag, verbose=verbose_flag)
    await app.run(simulation_flag)


async def sig_handler():
    await kill_tasks()


async def kill_tasks():
    pending_tasks = asyncio.all_tasks()
    for task in pending_tasks:
        task.cancel()


if __name__ == "__main__":
    signal.SIGINT
    signal.SIGTERM
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(main())
    for signame in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(getattr(signal, signame),
                                    lambda: asyncio.create_task(sig_handler()))
    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        loop.run_until_complete(kill_tasks())
    finally:
        loop.close()
