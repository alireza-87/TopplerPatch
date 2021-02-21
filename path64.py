#! /usr/bin/env python3

from pwn import *
import os
import stat

def path_life_infinitive(game):
    #Make Topler lifes infinitve
    assert game.read(0x00414005,3) == b'\x83\xe8\x01'
    game.write(0x00414005+2,b'\x00')
    assert game.read(0x00414005,3) == b'\x83\xe8\x00'

    assert game.read(0x00413fc2,3) == b'\x83\xc0\x01'
    game.write(0x00413fc2+2,b'\x00')
    assert game.read(0x00413fc2,3) == b'\x83\xc0\x00'

def path_life_more(game):
    #Make Topler init lifes 9 
    assert game.read(0x00404288,3) == b'\x83\xf8\x03'
    game.write(0x00404288,b'\x83\xf8\x02')
    assert game.read(0x00404288,3) == b'\x83\xf8\x02'

    assert game.read(0x00404291,7) == b'\xc7@@\x03\x00\x00\x00'
    game.write(0x00404291,b'\xc7@@\t\x00\x00\x00')
    assert game.read(0x00404291,7) == b'\xc7@@\t\x00\x00\x00'

def path_topler_gost(game):
    #Make Topler gost
    assert game.read(0x00414a4e,7) == b'\xc7E\xfc\x00\x00\x00\x00'
    game.write(0x00414a4e,b'\xc7E\xfc\x04\x00\x00\x00')
    assert game.read(0x00414a4e,7) == b'\xc7E\xfc\x04\x00\x00\x00'

def path_without_robot(game):
    pass

def path_disable_timer(game):
    #disable timer
    assert game.read(0x004069bd,5) == b'\xe8\xf0\xf9\xff\xff'
    game.write(0x004069bd,b'\x90')
    game.write(0x004069bd+1,b'\x90')
    game.write(0x004069bd+2,b'\x90')
    game.write(0x004069bd+3,b'\x90')
    game.write(0x004069bd+4,b'\x90')

def path_all():
    path_disable_timer(game)
    path_life_infinitive(game)
    path_life_more(game)
    path_topler_gost(game)
    #path_without_robot(game)

def save_out(game):
    assert game.read(0x4217ac,19) == b'Nebulous version %s'
    game.write(0x4217ac,b'Nebulous PATHED_ %s')
    assert game.read(0x4217ac,19) == b'Nebulous PATHED_ %s'

    game.save('./topler64_pathed')
    st = os.stat('./topler64_pathed')
    os.chmod('./topler64_pathed', st.st_mode | stat.S_IEXEC)

    print("Game Has pathed : topler64_pathed")

def menu():
    game = ELF('./toppler64')
    print("*********** Tpploer 64bit patcher ***********")
    #print("(1) Patch All")
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
