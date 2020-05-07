from aiohttp import web
import socketio
import os
import json

# creates a new Async Socket IO Server
sio = socketio.AsyncServer()
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)
teams = [["bot", "bot"],["bot", "bot"]]
gameStats = {
    "players": 0
}

# we can define aiohttp endpoints just as we normally
# would with no change
async def index(request):
    with open('../client/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

# If we wanted to create a new websocket endpoint,
# use this decorator, passing in the name of the
# event we wish to listen out for
# @sio.on('message')
# async def print_message(sid, message):
#     # When we receive a new event of type
#     # 'message' through a socket.io connection
#     # we print the socket ID and the message
#     print("Socket ID: " , sid)
#     print(message)

@sio.on('message')
async def print_message(sid, message):
    print("Socket ID: " , sid)
    print(message)
    # await a successful emit of our reversed message
    # back to the client
    await sio.emit('message', message)

@sio.on('joinTeam')
async def print_connect(sid, team):
    print("Socket ID: " , sid)
    print("Current players connected: " , gameStats.get("players"))
    print("Requesting to join team: " , team)
    ally = int(team)
    opponent = 1
    if (ally == 1):
        opponent = 0
    if (not sid in teams[ally]):
        if (sid in teams[opponent]):
            for i in range (2):
                if (teams[opponent][i] == sid):
                    teams[opponent][i] = "bot"
                    gameStats["players"] = gameStats.get("players") - 1
                    break
        for i in range (2):
            if (teams[ally][i] == "bot"):
                    teams[ally][i] = sid
                    gameStats["players"] = gameStats.get("players") + 1
                    break
    gameState = {
        "playersConnected": gameStats.get("players"),
        "team1": [
            {"id": teams[0][0]},
            {"id": teams[0][1]}
        ],
        "team2": [
            {"id": teams[1][0]},
            {"id": teams[1][1]}
        ]
    }
    await sio.emit('connectReceipt', json.dumps(gameState))

# We bind our aiohttp endpoint to our app
# router
app.router.add_get('/', index)

# We kick off our server
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)