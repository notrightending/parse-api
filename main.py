import matplotlib.pyplot as plt
import matplotlib.animation as animation
import requests
import time

url = "https://kav-api.kovalev.team/servodrive/lastActualData?servoDriveId=1"

payload = {}
headers = {'Accept': 'application/json'}


dataJson = {
    'actVelocity': [],
    'actPhaseU': [],
    'actPhaseV': [],
    'actOutCurrent': []
}

x_values = []
y_values = dataJson['actVelocity']
y_values2 = dataJson['actPhaseU']
y_values3 = dataJson['actPhaseV']
y_values4 = dataJson['actOutCurrent']
colors = ['blue', 'red', 'orange']
cols = 2
rows = 2


figure, axis = plt.subplots(rows, cols)


def animate(i):
    response = (requests.request(
        "GET", url, headers=headers)).json()
    x_values.append(time.time() - time_start)
    actVelocity = float((response[0]['actVelocity']).replace(',', '.'))
    actPhaseU = float((response[0]['actPhaseU']).replace(',', '.'))
    actPhaseV = float((response[0]['actPhaseV']).replace(',', '.'))
    actOutCurrent = float((response[0]['actOutCurrent']).replace(',', '.'))
    dataJson['actVelocity'].append(actVelocity)
    dataJson['actPhaseU'].append(actPhaseU)
    dataJson['actPhaseV'].append(actPhaseV)
    dataJson['actOutCurrent'].append(actOutCurrent)
    for row in range(rows):
        for col in range(cols):
            axis[row, col].cla()
            axis[row, col].autoscale(enable=True, axis='both', tight=None)
    axis[0, 0].set_title('actVelocity')
    axis[0, 1].set_title('actPhaseU')
    axis[1, 0].set_title('actPhaseV')
    axis[1, 1].set_title('actOutCurrent')
    axis[0, 0].plot(x_values, y_values, c=colors[0] if actVelocity <
                    20 else colors[1], label='Active velocity')
    axis[0, 1].plot(x_values, y_values2, c=colors[0] if actPhaseU <
                    1 else colors[2], label='Active phase U')
    axis[1, 0].plot(x_values, y_values3, c=colors[0] if actPhaseV <
                    2 else colors[1], label='Active phase V')
    axis[1, 1].plot(x_values, y_values4, c=colors[0] if actOutCurrent <
                    2 else colors[1], label='Active out current')


time_start = time.time()
ani = animation.FuncAnimation(plt.gcf(), animate, interval=100)

plt.tight_layout()
plt.show()
