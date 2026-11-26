import ctypes
import logging
import threading
import time

DRY_RUN = False
COUNTDOWN_SECONDS = 60

lock = threading.Lock()
state = "off"  # off / armed / countdown
seen_work = False
deadline = 0.0


def status():
    remaining = max(0, round(deadline - time.time())) if state == "countdown" else 0
    return {"state": state, "remaining": remaining}


def set_state(new_state):
    global state, seen_work, deadline
    state = new_state
    seen_work = False
    deadline = time.time() + COUNTDOWN_SECONDS if new_state == "countdown" else 0.0
    server.PromptServer.instance.send_sync("auto_sleep.status", status())


def suspend():
    if DRY_RUN:
        logging.info("[AutoSleep] Dry run: would enter S4 hibernate now.")
        return
    ctypes.windll.powrprof.SetSuspendState(True, False, False)


def watch_queue():
    global seen_work
    queue = server.PromptServer.instance.prompt_queue
    while True:
        time.sleep(1)
        tasks = queue.get_tasks_remaining()
        fire = False
        with lock:
            if state == "armed":
                if tasks > 0:
                    seen_work = True
                elif seen_work:
                    logging.info(f"[AutoSleep] Queue empty, sleeping in {COUNTDOWN_SECONDS}s.")
                    set_state("countdown")
            elif state == "countdown":
                if tasks > 0:
                    logging.info("[AutoSleep] New task queued, countdown cancelled.")
                    set_state("off")
                elif time.time() >= deadline:
                    set_state("off")
                    fire = True
        if fire:
            suspend()


try:
    import server
except ImportError:
    pass
else:
    from aiohttp import web

    @server.PromptServer.instance.routes.get("/auto_sleep/status")
    async def auto_sleep_status(request):
        with lock:
            return web.json_response(status())

    @server.PromptServer.instance.routes.post("/auto_sleep/toggle")
    async def auto_sleep_toggle(request):
        with lock:
            set_state("armed" if state == "off" else "off")
            return web.json_response(status())

    threading.Thread(target=watch_queue, daemon=True).start()
