import asyncio
import websockets
import json
import os

players = {}  # {id: {"x": int, "y": int}}
next_id = 0

async def handler(websocket, path):
    global next_id
    player_id = next_id
    next_id += 1

    # добавляем игрока
    players[player_id] = {"x": 0, "y": 0}
    await websocket.send(json.dumps({"id": player_id, "players": players}))

    print(f"Игрок {player_id} подключился")

    try:
        async for message in websocket:
            data = json.loads(message)  # {"x": int, "y": int}
            players[player_id] = {"x": data["x"], "y": data["y"]}

            # рассылаем всем игрокам обновлённый список
            msg = json.dumps({"id": player_id, "players": players})
            websockets.broadcast(set(connections), msg)

    except:
        print(f"Игрок {player_id} отключился")
    finally:
        del players[player_id]
        connections.remove(websocket)
        await websocket.close()

connections = set()

async def main():
    port = int(os.environ.get("PORT", 1234))  # Render даст порт
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"Сервер запущен на порту {port}")
        await asyncio.Future()  # держим сервер

asyncio.run(main())