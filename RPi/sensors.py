# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 18:11:58 2020

@author: ME
"""
try:
    import keyboard
    import board
    import busio as io
    import adafruit_mlx90614
    import adafruit_vl53l0x
    i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
    temperature_sensor = adafruit_mlx90614.MLX90614(i2c)
    proximity_sensor = adafruit_vl53l0x.VL53L0X(i2c)     
except Exception as e:
    print(e)
    pass

def init_sensors(rpi):
    if rpi:
        return (get_temperature_rpi, get_proximity_rpi)
    else:
        return (get_temperature_pc, get_proximity_pc) 
       
def temperature_adjusted(x):
    return (0.81+0.0000486382 * (x) + 0.0000208635*pow(x,2))*100

def get_temperature_rpi():
    temperature = temperature_sensor.object_temperature
    temperature_F = (9 / 5) * temperature + 32
    temperature_F = temperature_adjusted(temperature_F)
    if temperature_F > 90:
        is_human = True
    else:
        is_human = False
    
    temperature_str = "{} C".format(temperature_F)
    
    return is_human, temperature_str

def get_proximity_rpi():    
    proximity = proximity_sensor.range

    if proximity < 50:     
        return True
    else:
        return False
    
def get_proximity_pc():
    
    if keyboard.is_pressed('p'):  # if key 'q' is pressed 
        print('Pressed p!')
        return True
    else:
        return False
            
def get_temperature_pc():
    if keyboard.is_pressed('t'):  # if key 'd' is pressed 
        print('Pressed d!')
        return True, '96 F'
    else:
        return False, '89 F'
    