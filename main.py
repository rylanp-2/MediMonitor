from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket
import asyncio
import boot_RENAME as boot
from read_temps import read_temps, convert_list, hum_status
from LEDs_test import LEDs
from history_write import update_history


# Config
global temp_range

with open("/static/config", "r") as config:
    temp_range = config.read().strip()


# Writes to file, which is picked up by other subprocesses
def write_config(data):
    with open("/static/config", "w") as config:
        config.seek(0)
        config.write(data + "\n")
        config.append()


global current_status_str
global full_history

# initial status
a = read_temps()
current_status = LEDs(a[0], a[1], a[2])
_ = a

with open("/static/history", "r") as history:
    full_history = history.read().strip()


# prevents repeated history inputs
def do_status(t1, t2, t3):
    global current_status_str, current_status

    temp_status = LEDs(t1, t2, t3)

    if temp_status == current_status:
        pass
    else:
        current_status_str = update_history(temp_status, current_status)
        current_status = temp_status
        for ws in active_websockets:
            ws.send_history = True

    return temp_status


# Initialize MicroDot
app = Microdot()
Response.default_content_type = "text/html"
active_websockets = set()


# prints connections
@app.before_request
async def log_request(request):
    print(f"{request.client_addr} - {request.method} {request.path}")


# root route
@app.route("/")
async def index(request):
    return render_template("index.html")


# websocket data handler
@app.route("/ws")
@with_websocket
async def websocket_handler(request, ws):
    print(f"WebSocket connection established: {request.client_addr}")
    global temp_range, full_history

    has_config = False
    ws.send_history = False
    active_websockets.add(ws)  # track active connection
    try:
        while True:
            # Sends stored config range, initial history
            if has_config is not True:
                await ws.send("config, " + temp_range)
                has_config = True

                # only sends full history once
                await ws.send("history, " + full_history)

            temp_data = read_temps()  # temp1, temp2, temp3, avg_temp, hum, unix_time
            temp_status = do_status(temp_data[0], temp_data[1], temp_data[2])

            # watches for immediate changes in status
            if ws.send_history is True:
                await ws.send("addition, " + current_status_str)
                ws.send_history = False

            temp_data.append(temp_status)
            temp_data.append(hum_status(temp_data[4]))

            await ws.send("data, " + convert_list(temp_data))
            await asyncio.sleep(0.5)

            # Attempt to receive data with a timeout
            try:
                new_temp_range = await asyncio.wait_for(ws.receive(), timeout=0.1)

                if temp_range != new_temp_range:  # Ensure it's not the same
                    print(f"Recieved new range: {new_temp_range} Old: {temp_range}")
                    temp_range = new_temp_range
                    write_config(temp_range)  # Write to /static/config

            except asyncio.TimeoutError:
                pass  # No data received, continue loop

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print(f"WebSocket closed: {request.client_addr}")
        active_websockets.delete(ws)


# Static CSS/JSS
@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)


# shutdown
@app.get("/shutdown")
def shutdown(request):
    boot.led.value(0)
    request.app.shutdown()
    print("Server Shutdown")
    return "Shutdown"


if __name__ == "__main__":
    try:
        app.run(debug=True, port=80)  # Serve on port 80
    except Exception as e:
        print(f"Server error: {e}")
