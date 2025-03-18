from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket
import time
import boot_RENAME as boot

# import machine

# Initialize MicroDot
app = Microdot()
Response.default_content_type = "text/html"


# prints connections
@app.before_request
async def log_request(request):
    # print("{request.client_addr} - {request.method} {request.path}")
    boot.check_clients()


# root route
@app.route("/")
async def index(request):
    return render_template("index.html")


@app.route("/ws")
@with_websocket
async def websocket_handler(request, ws):
    print(f"WebSocket connection established: {request.client_addr}")

    try:
        while True:
            message = await ws.receive()
            print(f"Received message: {message}")
            await ws.send(f"Echo: {message}")  # Echo received message
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
    request.app.shutdown()
    return "The server is shutting down..."


if __name__ == "__main__":
    try:
        app.run(debug=True, port=80)  # Serve on port 80
    except Exception as e:
        print(f"Server error: {e}")
