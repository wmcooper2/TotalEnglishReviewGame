#std lib
from pprint import pprint
import random

#3rd party
import pyglet
from pyglet.window import key

#custom
from animations import transfer_item
from constants import Constants as c
from constants import Screens
from draw_loop import draw_menu, draw_problem, draw_sprites
import items as i
# from key_presses import (
#     game_loop_keys)
#     options_loop_keys,
#     options_loop_keys2,
#     title_loop_keys)
from title_screen import TitleScreen
from options_screen import OptionsScreen
import util as u
import sprites as s

#TODO, add the star, feather and question block to the game
#NOTE, the business logic is separated from the drawing of the sprites in the update loops

#Music
# source = pyglet.media.load('explosion.wav')
# source = pyglet.resource.media('overworld.mp3')
source = pyglet.media.load('./music/overworld.mp3')
source.play()

#SPRITES
background = s.Background()
# selector = s.Selector()
yammy = s.Yammy()

#floaters
fire_light = s.FireLight()
big_boo = s.BigBoo()

#walkers
dragon = s.Dragon()
green_koopa = s.GreenKoopa()
big_mole = s.BigMole()
mario = s.Mario()
luigi = s.Luigi()

#PLAYERS
c.ALL_PLAYERS = [
    mario,
    luigi,
    fire_light,
    dragon,
    big_boo,
    green_koopa,
    big_mole]


c.WALKING_PLAYERS = [
    dragon,
    green_koopa,
    big_mole,
    mario,
    luigi]

c.FLOATING_PLAYERS = [
    fire_light,
    big_boo]

#SOME SETUP
#Items
u.set_item_spots()
i.add_items()

#Players
u.set_player_spots()
u.add_players()

#Scores
#TODO, move these to their respective classes?
u.set_score_spots()
u.set_score_indices()
u.set_player_score_sprites()
u.assign_x_pos_to_player_score_sprites()
u.set_score_values_x()

#Problems
question = c.NEW_QUESTION
problem = s.Problem()

#Screens
title = TitleScreen()
options = OptionsScreen()

@c.GAME_WINDOW.event
def on_key_release(symbol, modifiers):
    #OPTIONS
    if u.is_options_screen():
        if symbol == key.UP:
            options.selector_up()
        elif symbol == key.DOWN:
            options.selector_down()
        elif u.key_b():
            c.SCREEN = Screens.TITLE

    #TITLE
    elif u.is_title_screen():
#         if u.key_up():
        if symbol == key.UP:
            title.selector_up()
        elif symbol == key.DOWN:
            title.selector_down()

        #make a selection
        elif symbol == key.ENTER:
            if title.is_game_selected():
                c.SCREEN = Screens.GAME
            elif title.is_options_selected():
                c.SCREEN = Screens.OPTIONS

    #GAME
    elif u.is_game_screen():
        """
            Digits:     1
            Letters:    ADFOSUX
            Arrows:     Left Right Up
        """
        player = u.player_in_front()
        if not u.any_movement():
            if u.key_1():
                if not problem.showing:
                    problem.question.draw()
                    problem.toggle()
                player.use_item()
                yammy.wave_wand()
                c.TRANSFER_ITEM = u.remove_item_from_platform()
                i.add_item()

            elif u.key_left():
                u.rotate_players_left()

            elif u.key_right():
                u.rotate_players_right()

            elif u.key_up():
                c.PLAYERS = u.mix(c.PLAYERS)

            #plus one point
            elif u.key_o():
                u.right_answer(player)
                u.rotate_players_left()

                if problem.showing:
                    problem.toggle()

                #delete prior problem letter sprites

            #minus one point
            elif u.key_x():
                u.wrong_answer(player)
                if player.item:
                    player.item.poof()
                    player.item = None
                u.rotate_players_left()

                if problem.showing:
                    problem.toggle()

                #delete prior problem letter sprites

            elif u.key_a():
                u.rotate_items_left()

            elif u.key_d():
                u.rotate_items_right()

            elif u.key_s():
                c.ALL_ITEMS = u.mix(c.ALL_ITEMS)

            elif u.key_u():
                player.use_item()
                

def update_items(dt) -> None:
    for item in c.ALL_ITEMS:
        item.dest_x = c.ITEM_SPOTS[c.ALL_ITEMS.index(item)]
        item.update(dt)
    if c.TRANSFER_ITEM is not None:
        c.TRANSFER_ITEM.update(dt)
    
def update_players(dt) -> None:
    #update player positions
    for p in c.PLAYERS:
        p.spot = c.PLAYER_SPOTS[c.PLAYERS.index(p)]
        p.update(dt)

def game_loop(dt) -> None:
    """Handles the business logic for the game loop."""
    yammy.update()
    update_players(dt)
    update_items(dt)
#     game_loop_keys(yammy, problem)
    transfer_item()
    draw_sprites()
    if problem.showing:
        draw_problem(problem)

def title_loop(dt) -> None:
    """Handles the business logic for the Title screen."""
    c.GAME_WINDOW.clear()
    title.update()
#     title_loop_keys(title)

def options_loop(dt) -> None:
    """Handles the business logic for the Options screen."""
    c.GAME_WINDOW.clear()
    options.update()
#     options_loop_keys(options)
#     options_loop_keys2(options)

def screen_choices(dt):
    """Screens are changed here."""
    if u.is_title_screen():
        title_loop(dt)
    elif u.is_options_screen():
        options_loop(dt)
    else:
        game_loop(dt)
 
if __name__ == "__main__":
    pyglet.clock.schedule_interval(screen_choices, c.FRAME_SPEED)
    pyglet.app.run()
