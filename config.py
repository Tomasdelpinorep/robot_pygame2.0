import csv


# Devuelve una lista donde cada elemento es una fila del csv
def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = [''.join(row) for row in reader]

    num_spikes = int(data[15])
    num_diamonds = int(data[16])
    num_water = int(data[17])

    return data[:15], num_spikes, num_diamonds, num_water


WIN_WIDTH = 640
WIN_HEIGHT = 480
TILE_SIZE = 32
FPS = 60

PLAYER_LAYER = 3
PLAYER_SPEED = 3

SPIKE_LAYER = 2

GROUND_LAYER = 1

TILEMAP, NUM_SPIKES, NUM_DIAMONDS, NUM_WATER = read_csv("assets/tilemap.csv")