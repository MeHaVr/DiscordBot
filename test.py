import asyncio

async def main():
    while True:
        await asyncio.sleep(1)
        print("Running...")

loop = asyncio.get_event_loop()
task = loop.create_task(main())

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("KeyboardInterrupt detected. Shutting down...")
finally:
    print("Stopping the program...")
    task.cancel()
    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass
    loop.close()
    print("Program stopped.")

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("KeyboardInterrupt detected. Shutting down...")
finally:
    print("Stopping the program...")
    web_task.cancel()
    bot_task.cancel()
    loop.run_until_complete(asyncio.gather(web_task, bot_task, return_exceptions=True))
    loop.close()
    print("Program stopped.")