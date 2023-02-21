import hid
import pydirectinput as pdi
import pyautogui as pag
from multiprocessing import Process
import time
import json

weight = 7
tolerance = 2
screen_offset = 70
pag.PAUSE = 0

gamepad = hid.device()
gamepad.open(0x054c, 0x05c4)
gamepad.set_nonblocking(True)

f = open("C:/Users/carlo/Desktop/controller_support/config.json")
data_json = json.load(f)

f.close()
def check_valid_cursor_direction(axis_x, axis_y):
    screen_width = pag.position()[0]
    screen_height = pag.position()[1]
    #print(screen_width + axis_x, screen_height + axis_y)
    return pag.onScreen(screen_width + axis_x, screen_height + axis_y)

def minmax(val):
    minimo = 0
    maximo = 255
    return 2 * ((val - minimo) / (maximo - minimo)) - 1

def get_mouse_cursor_position():
    while True:
        datastream = gamepad.read(64)
        if datastream:
            # o valor varia de 0 a 255 no eixo x e y onde 127 é o botão parado
            #[1] eixo x
            axis_x = 0
            axis_y = 0
            if datastream[data_json["cursor_posistion"]["axis_x"]["id"]] > data_json["cursor_posistion"]["axis_x"]["values"]["no_movement"] + tolerance:
                axis_x = minmax(datastream[1])
            elif datastream[1] < 127 - tolerance:
                axis_x = minmax(datastream[1])
            
            axis_x = int(axis_x * weight)
                
            #[2] eixo y
            if datastream[data_json["cursor_posistion"]["axis_y"]["id"]] > data_json["cursor_posistion"]["axis_y"]["values"]["no_movement"] + tolerance:
                axis_y = minmax(datastream[2])
                
            elif datastream[data_json["cursor_posistion"]["axis_y"]["id"]] < data_json["cursor_posistion"]["axis_y"]["values"]["no_movement"] - tolerance:
                axis_y = minmax(datastream[2])

            axis_y = int(axis_y * weight)
            
            
            if not check_valid_cursor_direction(axis_x, axis_y):
                axis_x = 0
                axis_y = 0
            pag.move(axis_x, axis_y)

def get_clicks():
    while True:
        datastream = gamepad.read(64)
        if datastream:

            click_r1 = datastream[data_json["cursor_btns"]["right_btn"]["id"]] == data_json["cursor_btns"]["right_btn"]["values"]["right_click"]
            if click_r1:
                pag.mouseDown(button='right')
                pag.mouseUp(button='right')
                time.sleep(0.4)
        
            click_l1 = datastream[data_json["cursor_btns"]["left_btn"]["id"]] == data_json["cursor_btns"]["left_btn"]["values"]["left_click"]
            if click_l1:
                pag.mouseDown(button='left')
                pag.mouseUp(button='left')
                time.sleep(0.4)

def get_skill_buttons():
    # datastream[data_json["skill_btns"]["btn_1"]["id"]]
    while True:
        datastream = gamepad.read(64)
        if datastream:
            btn = datastream[data_json["skill_btns"]["btn_1"]["id"]] # 136 ta apertado o triangulo
            #print('btn:', datastream[6])
            #datastream[6] F = 64, D = 128
            # 136 ta apertado
            # 24 é quadrado
            # x é 40
            # bolinha é 72
            if (btn == data_json["skill_btns"]["btn_1"]["values"]["skill_q"]):
                pdi.keyDown(data_json["skill_btns"]["btn_1"]["keys"][0])
                pdi.keyUp(data_json["skill_btns"]["btn_1"]["keys"][0])
            elif (btn == data_json["skill_btns"]["btn_1"]["values"]["skill_w"]):
                pdi.keyDown(data_json["skill_btns"]["btn_1"]["keys"][1])
                pdi.keyUp(data_json["skill_btns"]["btn_1"]["keys"][1])
            elif (btn == data_json["skill_btns"]["btn_1"]["values"]["skill_e"]):
                pdi.keyDown(data_json["skill_btns"]["btn_1"]["keys"][2])
                pdi.keyUp(data_json["skill_btns"]["btn_1"]["keys"][2])
            elif (btn == data_json["skill_btns"]["btn_1"]["values"]["skill_r"]):
                pdi.keyDown(data_json["skill_btns"]["btn_1"]["keys"][3])
                pdi.keyUp(data_json["skill_btns"]["btn_1"]["keys"][3])


def get_spell_buttons():
    while True:
        datastream = gamepad.read(64)
        if datastream:
            #datastream[data_json["spell_btns"]["btn_1"]["id"]]
            key = datastream[data_json["spell_btns"]["btn_1"]["id"]]
            if key == data_json["spell_btns"]["btn_1"]["values"]["spell_1"]:
                pdi.keyDown(data_json["spell_btns"]["btn_1"]["keys"][0])
                pdi.keyUp(data_json["spell_btns"]["btn_1"]["keys"][0])
                time.sleep(0.15)
            elif key == data_json["spell_btns"]["btn_1"]["values"]["spell_2"]:
                pdi.keyDown(data_json["spell_btns"]["btn_1"]["keys"][1])
                pdi.keyUp(data_json["spell_btns"]["btn_1"]["keys"][1])
                time.sleep(0.15)
                    

def get_utilities():
    while True:
        datastream = gamepad.read(64)
        if datastream:
            #datastream[data_json["utilities_btns"]["btn_1"]["id"]]
            key = datastream[data_json["utilities_btns"]["btn_1"]["id"]]
            if key == data_json["utilities_btns"]["btn_1"]["values"]["arrow_1"]:
                pdi.keyDown('4')
                pdi.keyUp('4')
                time.sleep(0.3)
            elif key == data_json["utilities_btns"]["btn_1"]["values"]["arrow_2"]:
                pdi.keyDown('1')
                pdi.keyUp('1')
                time.sleep(0.3)
            elif key == data_json["utilities_btns"]["btn_1"]["values"]["arrow_3"]:
                pdi.keyDown('b')
                pdi.keyUp('b')
                time.sleep(0.3)
            elif key == data_json["utilities_btns"]["btn_1"]["values"]["arrow_4"]:
                pdi.keyDown('p')
                pdi.keyUp('p')
                time.sleep(0.3)
            elif key < data_json["utilities_btns"]["btn_2"]["values"]["utl_1"]:
                while(datastream and datastream[data_json["utilities_btns"]["btn_2"]["id"]] > data_json["utilities_btns"]["btn_2"]["values"]["utl_1"]):# centralizar no personagem (espaço)
                    pdi.keyDown(data_json["utilities_btns"]["btn_2"]["keys"][0])
                    datastream = gamepad.read(64)
                pdi.keyUp(data_json["utilities_btns"]["btn_2"]["keys"][0])
                while(datastream and datastream[data_json["utilities_btns"]["btn_3"]["id"]] > data_json["utilities_btns"]["btn_3"]["values"]["utl_1"]):# tab
                    pdi.keyDown(data_json["utilities_btns"]["btn_3"]["keys"][0])
                    datastream = gamepad.read(64)
                pdi.keyUp(data_json["utilities_btns"]["btn_3"]["keys"][0])

                    

if __name__ == '__main__': 
    Process(target=get_mouse_cursor_position).start() 
    Process(target=get_clicks).start()
    Process(target=get_skill_buttons).start()
    Process(target=get_spell_buttons).start()
    Process(target=get_utilities).start()

