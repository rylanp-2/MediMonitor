from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket
import asyncio
import boot_RENAME as boot
from Temperature_Sensing import read_temps

# import machine

# Initialize MicroDot
app = Microdot()
Response.default_content_type = "text/html"


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

    try:
        while True:
            # temp1, temp2, temp3, avg_temp, hum, unix_time
            await ws.send(read_temps())
            await asyncio.sleep(2)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print(f"WebSocket closed: {request.client_addr}")


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
