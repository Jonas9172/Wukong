import socket
import threading
from _thread import *
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = ''
port = 5555
try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))
s.listen(2)
print("Waiting for a connection")

a = 0
match_queue_battle = []
rooms = {}
all_user = {}
ID = 0
last_cloud_x = [50, 250, 450, 650, 850]
last_cloud_y = [200, 250, 325, 400, 475, 550, 625, 700]
x = {}
y = {}
b = {}
cpl1 = {}
cpl3 = {}
c = 1
index_y = {}
d = 1
level3 = {}
level12 = {}
pos = {}
reach = {}


def threaded_client(conn):
    global pos
    global match_queue_battle, a
    global ID
    global last_cloud_x, b, c, d
    global x, y, index_y
    global rooms

    all_user[conn] = 1
    i = 0
    y_i = 0
    reply = ''
    while all_user[conn] != 0:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
        except Exception as e:
            if conn in all_user.keys():
                del all_user[conn]
                print("Connection Closed")
                conn.close()
                return

        print("Recieved: " + reply)

        if reply[0:3] == 'u b':
            if conn not in match_queue_battle and all_user[conn] == 1:
                match_queue_battle.append(conn)
            if a == 0:
                conn.send(str.encode("wait"))
                print("Sending: wait")
            elif a == 2 or a == 1:
                conn.send(str.encode("ready"))
                print("Sending: ready")
                a -= 1

        elif reply[0:4] == 'id r':
            if ID % 2 == 0:
                pos[ID + 1] = "200,750,1,1,1"
                b[ID] = random.randint(0, 4)
                b[ID + 1] = b[ID]
                index_y[ID] = 7
                index_y[ID + 1] = 7
                x[ID] = last_cloud_x[b[ID]]
                x[ID + 1] = last_cloud_x[b[ID + 1]]
                cpl1[ID], cpl1[ID + 1] = 0, 0
                cpl3[ID], cpl3[ID + 1] = 0, 0
                reach[conn] = 0
                level3[ID] = False
                level3[ID + 1] = False
                level12[ID] = True
                level12[ID + 1] = True
            if ID % 2 == 1:
                reach[conn] = 0
                pos[ID - 1] = "200,750,1,1,1"

            conn.send(str.encode(str(ID)))
            print("Sending: ID is " + str(ID))
            ID += 1

        elif reply[0:5] == 'reach':
            print("reach")
            if reach[conn] == 0 and reach[rooms[conn]] == 0:
                conn.send(str.encode("w"))
                reach[conn] = 1
            else:
                conn.send(str.encode("l"))

        elif reply[0:5] == 'leave':
            print("left")
            all_user[conn] = 0

        elif reply[0:3] == 'l q':
            print("left")
            all_user[conn] = 0
            match_queue_battle.clear()

        elif reply[2:6] == 'cpl1':
            i = int(reply[0:1])
            if i % 2 == 0:
                y_i = i + 1
            if i % 2 == 1:
                y_i = i - 1

            if level3[y_i]:
                cpl1[i] = 0
                cpl1[y_i] = 0

            if cpl1[i] == 0 and cpl1[y_i] == 0:
                if b[i] == 0:
                    b[i] = 1
                elif b[i] == 4:
                    b[i] = 3
                else:
                    if random.randint(0, 1):
                        b[i] = b[i] + 1
                    else:
                        b[i] = b[i] - 1
                y[i] = random.randint(-50, -40)
                y[y_i] = y[i]
                b[y_i] = b[i]
                cpl1[i] = 1

            if cpl1[i] == 0 and cpl1[y_i] == 1:
                cpl1[y_i] = 0

            x[i] = last_cloud_x[b[i]]
            conn.send(str.encode(str(x[i]) + "," + str(y[i])))
            print("Sending: random number is " + str(x[i]) + "," + str(y[i]))

        elif reply[2:6] == 'cpl3':
            i = int(reply[0:1])
            if i % 2 == 0:
                y_i = i + 1
            if i % 2 == 1:
                y_i = i - 1

            if level12[y_i] or reach[rooms[conn]]:
                cpl3[i] = 0
                cpl3[y_i] = 0

            if cpl3[i] == 0 and cpl3[y_i] == 0:
                if index_y[i] == 7:
                    index_y[i] -= 1
                elif index_y[i] == 0:
                    index_y[i] = random.randint(1, 5)
                else:
                    if random.randint(0, 1):
                        index_y[i] -= 1
                    else:
                        index_y[i] = random.randint(index_y[i], 7)
                x[i] = random.randint(1050, 1060)
                x[y_i] = x[i]
                index_y[y_i] = index_y[i]

                cpl3[i] = 1

            if cpl3[i] == 0 and cpl3[y_i] == 1:
                cpl3[y_i] = 0

            y[i] = last_cloud_y[index_y[i]]
            conn.send(str.encode(str(x[i]) + "," + str(y[i])))
            print("Sending: random number is " + str(x[i]) + "," + str(y[i]))

        else:
            my_id = int(reply.split(":")[0])
            pos[my_id] = reply.split(":")[1]
            if my_id % 2 == 0:
                your_id = my_id + 1
            if my_id % 2 == 1:
                your_id = my_id - 1

            if int(pos[my_id].split(",")[4]) == 3:
                level3[my_id] = True
                level3[your_id] = True
                level12[my_id] = False

            reply = str(your_id) + ":" + pos[your_id]

            print("Sending: " + reply)

            conn.sendall(str.encode(reply))
    print("Connection Closed")
    conn.close()


def queue_to_rom_battle():
    global match_queue_battle, a
    global rooms
    while True:
        if len(match_queue_battle) >= 2:
            rooms[match_queue_battle[0]] = match_queue_battle[1]
            rooms[match_queue_battle[1]] = match_queue_battle[0]

            a = 2

            all_user[match_queue_battle[0]] = 2
            all_user[match_queue_battle[1]] = 2
            match_queue_battle = match_queue_battle[2:]


if __name__ == '__main__':
    battle_match = threading.Thread(target=queue_to_rom_battle, args=())
    battle_match.start()

    while True:
        conn, addr = s.accept()

        print("Connected to: ", addr)

        start_new_thread(threaded_client, (conn,))
