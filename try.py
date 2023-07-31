import random
ssid_data = [2798141443, 2798359950, 2798462340, 2804557409, 2798365345, 2798459643, 2798459646]

room_data = [(1451119354, 2798141443), (1451119354, 2798359950), (1451119354, 2798462340),
             (1451119354, 2804557409),
             (1451119354, 2798365345)]
data = []
room_ssid_data = []

for i in range(len(room_data)):
    room_ssid_data.append(room_data[i][1])
print(room_ssid_data)

for x in range(len(ssid_data)):
    if ssid_data[x] not in room_ssid_data:
        print(ssid_data[x])
        data.append(ssid_data[x])
print(data)
print(len(data))
print(random.randint(0, len(data)-1))