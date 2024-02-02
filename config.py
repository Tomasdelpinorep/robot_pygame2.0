import csv


# Devuelve una lista donde cada elemento es una fila del csv
def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = [''.join(row) for row in reader]

    num_spikes = int(data[15])
    num_diamonds = int(data[16])
    num_water = int(data[17])
    num_red_shroom = int(data[18])
    num_blue_shroom = int(data[19])

    return data[:15], num_spikes, num_diamonds, num_water, num_red_shroom, num_blue_shroom


WIN_WIDTH = 640
WIN_HEIGHT = 510
LIFEBAR_HEIGHT = 60
TILE_SIZE = 32
FPS = 60

PLAYER_LAYER = 3
PLAYER_SPEED = 3

SPIKE_LAYER = 2

GROUND_LAYER = 1

LIFEBAR_LAYER = 4

LIFEBAR_ITEM_SPRITE_HEIGHT = 20
LIFEBAR_ITEM_SPRITE_WIDTH = 20

TILEMAP, NUM_SPIKES, NUM_DIAMONDS, NUM_WATER, NUM_RED_SHROOMS, NUM_BLUE_SHROOMS = read_csv("assets/tilemap.csv")

SINGLE_ITEM = 1