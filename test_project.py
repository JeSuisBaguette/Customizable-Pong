import pytest
# Classes
from project import Config, Ball, Paddle
# Functions
from project import (
    instruction,
    validate,
    get_filepath,
    init_configs,
    ball_direction_filter,
    nearest_ball,
    distance_to,
    right_ai,
    left_ai,
    collision
)


Config.BALL_HEIGHT = 10
Config.BALL_WIDTH = 10
Config.PADDLE_WIDTH = 5
Config.PADDLE_HEIGHT = 80
Config.DISPLAY_HEIGHT = 800
Config.DISPLAY_WIDTH = 1200
Config.paddle_dy = 5
Config.ball_dx = 5
Config.ball_dy = 5


def test_instruction():
    assert instruction() == (
        "Press W/S to move the left-paddle up/down.\
\nPress Up-arrow/Down-arrow to move the right-paddle up/down.\
\nThe ball will start moving when the space key is pressed.\
\nYou can change the number of balls, ball-speed, or paddle-speed the game starts with in game parameters.\
\nYou can even change player names or the number of points required to win the game!\
\nIf you wish to skip all that, the game is also able to start with default parameters for all the above.\
\nFor your information, the default parameters are: ball-amount = 1, ball-speed = 5, paddle-speed = 7, target = 10"
    )
    with pytest.raises(TypeError):
        instruction(1)


def test_validate():
    assert validate(ball_amount="1") == True
    assert validate(ball_amount="0") == False
    assert validate(ball_speed="4") == True
    assert validate(ball_speed="10") == False
    assert validate(paddle_speed="15") == True
    assert validate(paddle_speed="-3") == False
    assert validate(end_score="94") == True
    assert validate(end_score="0@") == False


def test_get_filepath():
    directory = r"C:\Users\fedwa\pythonprojects\cs50p\final_project"
    assert get_filepath("fonts/Arimo.ttf") == f"{directory}\\fonts/Arimo.ttf"
    assert get_filepath("music/collect.ogg") == f"{directory}\\music/collect.ogg"
    assert get_filepath("music/pong.ogg") != f"{directory}\\music/collect.ogg"


def test_ball_direction_filter():
    ball1 = Ball(
        (Config.DISPLAY_WIDTH / 2 - (Config.BALL_WIDTH / 2)),
        Config.DISPLAY_HEIGHT - 395,
        Config.BALL_WIDTH,
        Config.BALL_HEIGHT,
        5,
        5,
    )

    ball2 = Ball(
        (Config.DISPLAY_WIDTH / 2 - (Config.BALL_WIDTH / 2)),
        Config.DISPLAY_HEIGHT - 395,
        Config.BALL_WIDTH,
        Config.BALL_HEIGHT,
        -5,
        5,
    )

    ball3 = Ball(
        (Config.DISPLAY_WIDTH / 2 - (Config.BALL_WIDTH / 2)),
        Config.DISPLAY_HEIGHT - 395,
        Config.BALL_WIDTH,
        Config.BALL_HEIGHT,
        10,
        -5,
    )

    left_paddle = Paddle(
        Config.PADDLE_EDGE,
        (Config.DISPLAY_HEIGHT / 2 - (Config.PADDLE_HEIGHT / 2)),
        Config.PADDLE_WIDTH,
        Config.PADDLE_HEIGHT,
        Config.paddle_dy,
    )

    ball_list_right_side = ball_direction_filter([ball1, ball2, ball3], right_side=True)
    assert ball_list_right_side == [ball1, ball2]
    assert ball_list_right_side != [ball1, ball2, ball3]
    assert ball_list_right_side != None

    ball_list_left_side = ball_direction_filter([ball1, ball2, ball3], left_side=True)
    assert ball_list_left_side == [ball2]
    assert ball_list_left_side != None


def test_nearest_ball():
    ball1 = Ball(
        30,
        Config.DISPLAY_HEIGHT - 395,
        Config.BALL_WIDTH,
        Config.BALL_HEIGHT,
        5,
        5,
    )

    ball2 = Ball(
        100,
        Config.DISPLAY_HEIGHT - 395,
        Config.BALL_WIDTH,
        Config.BALL_HEIGHT,
        -5,
        5,
    )

    ball3 = Ball(
        150,
        Config.DISPLAY_HEIGHT - 395,
        Config.BALL_WIDTH,
        Config.BALL_HEIGHT,
        10,
        -5,
    )
    
    left_paddle = Paddle(
        Config.PADDLE_EDGE,
        (Config.DISPLAY_HEIGHT / 2 - (Config.PADDLE_HEIGHT / 2)),
        Config.PADDLE_WIDTH,
        Config.PADDLE_HEIGHT,
        Config.paddle_dy,
    )
    
    right_paddle = Paddle(
        (Config.DISPLAY_WIDTH - (Config.PADDLE_EDGE + Config.PADDLE_WIDTH)),
        (Config.DISPLAY_HEIGHT / 2 - (Config.PADDLE_HEIGHT / 2)),
        Config.PADDLE_WIDTH,
        Config.PADDLE_HEIGHT,
        Config.paddle_dy,
    )  
     
    assert nearest_ball(left_paddle, [ball1, ball2, ball3]) == ball1
    assert nearest_ball(left_paddle, [ball1, ball2, ball3]) != ball3
    assert nearest_ball(right_paddle, [ball1, ball2, ball3]) == ball3
    assert nearest_ball(right_paddle, [ball1, ball2, ball3]) != ball2
    
    
def test_distance_to():
    ball = Ball(
        30, #centerx =
        45, #centery = 
        Config.BALL_WIDTH,
        Config.BALL_HEIGHT,
        5,
        5,
    )

    left_paddle = Paddle(
        10, #centerx =
        560, #centery =
        Config.PADDLE_WIDTH,
        Config.PADDLE_HEIGHT,
        Config.paddle_dy,
    )  
    
    ball_centerx = 35
    ball_centery = 50
    paddle_centerx = 12
    paddle_centery = 600
    assert(round(distance_to(ball, left_paddle))) == 550
    assert(round(distance_to(left_paddle, ball))) == 550
    assert(round(distance_to(ball, left_paddle))) != 0
    
# def test_init_configs(monkeypatch):
#     config = Config.party_mode = False
#     monkeypatch.setattr("builtins.input", lambda _: "party")
#     # i = input()
#     # assert i == "party"
#     assert init_configs() == config
