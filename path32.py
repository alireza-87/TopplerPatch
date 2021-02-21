#! /usr/bin/env python3

from pwn import *
import os
import stat

def path_life_infinitive(game):
    #Make Topler lifes infinitve
    assert game.read(0x08056417,7) == b'\x83-\x9c\x91\x06\x08\x01'
    game.write(0x08056417+6,b'\x00')
    assert game.read(0x08056417,7) == b'\x83-\x9c\x91\x06\x08\x00'

    assert game.read(0x080563c2,3) == b'\x83\xc0\x01'
    game.write(0x080563c2+2,b'\x00')
    assert game.read(0x080563c2,3) == b'\x83\xc0\x00'

def path_life_more(game):
    #Make Topler init lifes 9
    assert game.read(0x080563a8,5) == b'\xa1\xf8d\x06\x08'
    game.write(0x080563a8,b'\xb8\t\x00\x00\x00')
    assert game.read(0x080563a8,5) == b'\xb8\t\x00\x00\x00'

def path_topler_gost(game):
    #Make Topler gost
    assert game.read(0x080568f7,5) == b'\xb8\x00\x00\x00\x00'
    game.write(0x080568f7,b'\xb8\x04\x00\x00\x00')
    assert game.read(0x080568f7,5) == b'\xb8\x04\x00\x00\x00'

def path_without_robot(game):
    #With out robot
    assert game.read(0x08056a64,5) == b'\xbe\x00\x00\x00\x00'
    game.write(0x08056a64,b'\xbe\x05\x00\x00\x00')
    assert game.read(0x08056a64,5) == b'\xbe\x05\x00\x00\x00'

def path_disable_timer(game):
    #disable timer
    assert game.read(0x0804d125,5) == b'\xe8\x9f\xf3\xff\xff'
    game.write(0x0804d125,b'\x90')
    game.write(0x0804d125+1,b'\x90')
    game.write(0x0804d125+2,b'\x90')
    game.write(0x0804d125+3,b'\x90')
    game.write(0x0804d125+4,b'\x90')

def path_all(game):
    path_disable_timer(game)
    path_life_infinitive(game)
    path_life_more(game)
    path_topler_gost(game)
    path_without_robot(game)

def save_out(game):
    assert game.read(0x0805f549,19) == b'Nebulous version %s'
    game.write(0x0805f549,b'Nebulous PATHED_ %s')
    assert game.read(0x0805f549,19) == b'Nebulous PATHED_ %s'

    game.save('./topler32_pathed')
    st = os.stat('./topler32_pathed')
    os.chmod('./topler32_pathed', st.st_mode | stat.S_IEXEC)

    print("Game Has pathed : topler32_pathed")

def menu():
    game = ELF('./toppler32')
    print("*********** Tpploer 32bit patcher ***********")
    print("(1) Patch All")
    print("(2) Patch Infinitive life")
    print("(3) Patch more life")
    print("(4) Patch gost")
    print("(5) Patch no robot")
    print("(6) Patch no timer")

    selected_menu = int(input("Enter Menu number :"))
    if selected_menu == 1:
        path_all(game)
    elif selected_menu == 2:
        path_life_infinitive(game)
    elif selected_menu == 3:
        path_life_more(game)
    elif selected_menu == 4:
        path_topler_gost(game)
    elif selected_menu == 5:
        path_without_robot(game)
    elif selected_menu == 6:
        path_disable_timer(game)
    save_out(game)

if __name__ == '__main__':
    menu()
