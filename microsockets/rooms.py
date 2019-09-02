from collections import defaultdict


# optimize this more.
class RoomManager(object):
    def __init__(self):
        self.__sockets = defaultdict(list)
        self.__rooms = defaultdict(list)

    async def join(self, room, socket):
        if room not in self.__rooms[socket]:
            self.__rooms[socket].append(room)
            self.__sockets[room].append(socket)

    async def members(self, room):
        return self.__sockets[room].copy()

    async def rooms(self, socket):
        return self.__rooms[socket].copy()

    async def leave(self, room, socket):
        self.__rooms[socket].remove(room)
        if len(self.__rooms[socket]) == 0:
            del self.__rooms[socket]
        self.__sockets[room].remove(socket)
        if len(self.__sockets[room]) == 0:
            del self.__sockets[room]

    async def flush(self, socket):
        for room in self.__rooms[socket]:
            await self.leave(room, socket)
