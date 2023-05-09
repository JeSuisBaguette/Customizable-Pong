import pytest

# Classes
from project import Config, Ball, Paddle

# Functions
from project import (
    instruction,
    validate,
    get_filepath,
    ball_direction_filter,
    nearest_ball,
    distance_to,
    ai,
    collision,
)


# Returns text using the following format.
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


# Returns either True or False based on user validation and whichever function parameter != None. If no parameters, returns False
def test_validate():
    assert validate(ball_amount="1") == True
    assert validate(ball_amount="0") == False
    assert validate(ball_speed="4") == True
    assert validate(ball_speed="10") == False
    assert validate(paddle_speed="15") == True
    assert validate(paddle_speed="-3") == False
    assert validate(end_score="94") == True
    assert validate(end_score="0@") == False
    assert validate("40") == False


# Returns the filepath of the folder/file entered as string in relation to the directory of the project.
def test_get_filepath():
    directory = r"C:\Users\fedwa\pythonprojects\cs50p\final_project"
    assert get_filepath("fonts/Arimo.ttf") == f"{directory}\\fonts/Arimo.ttf"
    assert get_filepath("music/collect.ogg") == f"{directory}\\music/collect.ogg"
    assert get_filepath("music/pong.ogg") != f"{directory}\\music/collect.ogg"


# Returns a list of all balls moving towards the direction set in the function parameter. List can be empty. Returns None if no parameters set to True.
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

    assert ball_direction_filter([ball1, ball3], left_side=True) == []
    assert ball_direction_filter([ball1, ball2, ball3]) == None

    ball_list_right_side = ball_direction_filter([ball1, ball2, ball3], right_side=True)
    assert ball_list_right_side == [ball1, ball2]
    assert ball_list_right_side != [ball1, ball2, ball3]
    assert ball_list_right_side != None

    ball_list_left_side = ball_direction_filter([ball1, ball2, ball3], left_side=True)
    assert ball_list_left_side == [ball2]
    assert ball_list_left_side != None


# Returns nearest ball to the paddle based on distance calculation. Returns None if an empty list is returned.
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
    assert nearest_ball(right_paddle, []) == None


# Returns distance between two rect objects. Rounded to the nearest whole number for the purposes of unit testing. Returns Float in main().
def test_distance_to():
    ball = Ball(
        30,
        45,
        Config.BALL_WIDTH,
        Config.BALL_HEIGHT,
        5,
        5,
    )

    left_paddle = Paddle(
        10,
        560,
        Config.PADDLE_WIDTH,
        Config.PADDLE_HEIGHT,
        Config.paddle_dy,
    )

    # ball_centerx = 35
    # ball_centery = 50
    # paddle_centerx = 12
    # paddle_centery = 600
    assert (round(distance_to(ball, left_paddle))) == 550
    assert (round(distance_to(left_paddle, ball))) == 550
    assert (round(distance_to(ball, left_paddle))) != 0


# Returns True if the paddle.centery is below the ball or False if it's above.
def test_ai():
    ball = Ball(
        100,
        45,
        Config.BALL_WIDTH,
        Config.BALL_HEIGHT,
        5,
        5,
    )

    right_paddle = Paddle(
        (Config.DISPLAY_WIDTH - (Config.PADDLE_EDGE + Config.PADDLE_WIDTH)),
        300,
        Config.PADDLE_WIDTH,
        Config.PADDLE_HEIGHT,
        Config.paddle_dy,
    )

    left_paddle = Paddle(
        Config.PADDLE_EDGE,
        10,
        Config.PADDLE_WIDTH,
        Config.PADDLE_HEIGHT,
        Config.paddle_dy,
    )

    assert ai(right_paddle, ball) == True
    assert ai(right_paddle, ball) != False
    assert ai(left_paddle, ball) == False
    assert ai(left_paddle, ball) != None


# Returns True if two rect objects overlap. False if they don't.
def test_collision():
    ball = Ball(
        12,
        15,
        Config.BALL_WIDTH,
        Config.BALL_HEIGHT,
        5,
        5,
    )

    left_paddle = Paddle(
        10,
        10,
        Config.PADDLE_WIDTH,
        Config.PADDLE_HEIGHT,
        Config.paddle_dy,
    )

    right_paddle = Paddle(
        (Config.DISPLAY_WIDTH - (Config.PADDLE_EDGE + Config.PADDLE_WIDTH)),
        300,
        Config.PADDLE_WIDTH,
        Config.PADDLE_HEIGHT,
        Config.paddle_dy,
    )

    assert collision(left_paddle, ball) == True
    assert collision(right_paddle, ball) == False
    with pytest.raises(TypeError):
        assert collision()
