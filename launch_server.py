import threading
import time
import webbrowser
import uvicorn

HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}"


def open_browser():
    time.sleep(2)
    webbrowser.open(URL, new=2)


if __name__ == "__main__":
    thread = threading.Thread(target=open_browser, daemon=True)
    thread.start()
    uvicorn.run("API.main:app", host=HOST, port=PORT, reload=True)
