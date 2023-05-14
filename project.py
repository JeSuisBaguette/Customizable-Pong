# Imports needed. Game engine, sys exit, ball/color randomness, input validation, filepath for assets, math for distance calculation
import pygame
import sys
import random
import re
import os
import math


# Paddle class with methods: paddle objects, drawing, y-axis movement.
class Paddle(pygame.Rect):
    def __init__(self, x_coord, y_coord, width, height, paddle_speed):
        self.paddle_speed = paddle_speed
        # Inheriting from rect class in order to use in-built collision functionality.
        super().__init__(x_coord, y_coord, width, height)

    # Draws instantiated objects to the pygame window when called.
    def draw(self, surface, color):
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))

    # Handles paddle movement down at defined speed. Resets paddle to bottom of display minus the height of the paddle if exceeded
    def move_down(self):
        if self.y + self.height >= Config.DISPLAY_HEIGHT:
            self.y = Config.DISPLAY_HEIGHT - self.height
        else:
            self.y += self.paddle_speed

    # Handles paddle movement up at defined speed. Resets paddle to top of display if exceeded
    def move_up(self):
        if self.y <= 0:
            self.y = 0
        else:
            self.y -= self.paddle_speed


# Ball class with methods: ball objects, drawing, x and y axis movement
class Ball(pygame.Rect):
    def __init__(self, x_coord, y_coord, width, height, x_speed, y_speed):
        self.start_x = x_coord
        self.start_y = y_coord
        self.x_speed = x_speed 
        self.y_speed = y_speed 
        # Inheriting from rect class in order to use in-built collision functionality.
        super().__init__(x_coord, y_coord, width, height)

    # Draws instantiated objects to the pygame window when called.
    def draw(self, surface, color):
        pygame.draw.ellipse(surface, color, (self.x, self.y, self.width, self.height))

    # Handles ball movement, collision with top and bottom walls, and reset.
    def move(self):
        # Class variables for wall collision sound and miss/score sound.
        wall_sound = pygame.mixer.Sound(get_filepath(Config.SOUND_WALL))
        miss_sound = pygame.mixer.Sound(get_filepath(Config.SOUND_MISS))
        self.x += self.x_speed
        self.y += self.y_speed
        # Wall collision calculation.
        if self.y + self.height >= Config.DISPLAY_HEIGHT or self.y <= 0:
            pygame.mixer.Sound.play(wall_sound)
            self.y_speed *= -1
        # On exceeding furthest paddle x coor (causes collision bug if allowed to go past that), ball resets randomly along y-axis with random directionality. Score incremented.
        # Right side.
        if self.x + self.width > Config.DISPLAY_WIDTH - Config.PADDLE_EDGE:
            pygame.mixer.Sound.play(miss_sound)
            Config.left_score += 1
            self.x = self.start_x
            # Ball under screen bug if not set prior to edges + ball's height.
            self.y = random.randint(30, Config.DISPLAY_HEIGHT - 30)
            self.y_speed *= random.choice((1, -1))
            self.x_speed *= random.choice((1, -1))
        # Left side.
        if self.x < 0 + Config.PADDLE_EDGE:
            pygame.mixer.Sound.play(miss_sound)
            Config.right_score += 1
            self.x = self.start_x
            self.y = random.randint(30, Config.DISPLAY_HEIGHT - 30)
            self.x_speed *= random.choice((1, -1))
            self.y_speed *= random.choice((1, -1))


# All static variables + reassignable variables are housed here. In response to global variables messing up class objects instantiation prior to this.
class Config:
    # System
    window = None
    clock = None
    running = False

    # Display
    DISPLAY_WIDTH = 1200
    DISPLAY_HEIGHT = 800
    FPS = 60
    party_mode = False

    # Colours
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (16, 0, 48)
    PURPLE = (40, 0, 48)
    RED = (48, 0, 0)
    TEAL = (0, 43, 48)
    GREEN = (2, 38, 9)
    YELLOW = (56, 59, 1)
    BROWN = (59, 35, 1)

    # Specs
    PADDLE_EDGE = 10
    PADDLE_WIDTH = 5
    PADDLE_HEIGHT = 80
    BALL_WIDTH = 10
    BALL_HEIGHT = 10

    # Speed
    ball_dx = 5
    ball_dy = 5
    paddle_dy = 7

    # Count
    ball_count = 1
    left_score = 0
    right_score = 0
    game_score = 10

    # Player active sides, ai active, fonts
    FONT_SIZE = 30
    player_left = "Player One"
    player_right = "Player Two"
    player_active_left = True
    player_active_right = True
    ai = False

    # Packages. Folder/filename.
    FONT_ARIMO = "fonts/Arimo.ttf"
    FONT_CASKAYDIA = "fonts/Caskaydia.ttf"
    FONT_HEAVYDATA = "fonts/HeavyData.ttf"
    SOUND_PADDLE = "music/collect.ogg"
    SOUND_WALL = "music/select.ogg"
    SOUND_MISS = "music/explosion.ogg"
    SOUND_BGM = "music/pong.ogg"


# Let's goooo
def main():
    # Stops ball movement until True (beginning of game only).
    start = False
    # Starts with a random color.
    current_colour = get_colour()
    # Terminal prompts
    config = init_configs()
    # Need setup to change False conditions to allow for terminal prompts to be executed before game window pops up.
    setup()
    # Fonts and music initializations.
    font = pygame.font.Font(get_filepath(Config.FONT_HEAVYDATA), Config.FONT_SIZE)
    paddle_sound = pygame.mixer.Sound(get_filepath(Config.SOUND_PADDLE))
    pygame.mixer.music.load(get_filepath(Config.SOUND_BGM))
    # -1 denotes infinite loop of bgm
    pygame.mixer.music.play(-1)

    # Instantiating objects
    # Paddles spawm at the center of Y along respective X axis positions.
    left_paddle = Paddle(
        Config.PADDLE_EDGE,
        (Config.DISPLAY_HEIGHT / 2 - (Config.PADDLE_HEIGHT / 2)),
        Config.PADDLE_WIDTH,
        Config.PADDLE_HEIGHT,
        config.paddle_dy,
    )
    right_paddle = Paddle(
        (Config.DISPLAY_WIDTH - (Config.PADDLE_EDGE + Config.PADDLE_WIDTH)),
        (Config.DISPLAY_HEIGHT / 2 - (Config.PADDLE_HEIGHT / 2)),
        Config.PADDLE_WIDTH,
        Config.PADDLE_HEIGHT,
        config.paddle_dy,
    )
    # In order to accomodate multiple ball objects at the same time.
    list = []
    # Ball spawns randomly anywhere along the Y axis at half of X.
    for i in range(config.ball_count):
        list.append(
            Ball(
                (Config.DISPLAY_WIDTH / 2 - (Config.BALL_WIDTH / 2)),
                random.randint(30, Config.DISPLAY_HEIGHT - 30),
                Config.BALL_WIDTH,
                Config.BALL_HEIGHT,
                # Directionality of the balls(s) will be randomized across both x and y axis on start for unpredictability.
                config.ball_dx * random.choice((1, -1)),
                config.ball_dy * random.choice((1, -1)),
            )
        )

    # Main game loop
    while Config.running:
        # Input handling
        for event in pygame.event.get():
            # X button on window breaks out of game-loop.
            if event.type == pygame.QUIT:
                Config.running = False
        key = pygame.key.get_pressed()
        # Allows left paddle movement if player active.
        if config.player_active_left == True:
            if key[pygame.K_w]:
                left_paddle.move_up()
            if key[pygame.K_s]:
                left_paddle.move_down()
        # Allows right paddle movement if player active.
        if config.player_active_right == True:
            if key[pygame.K_UP]:
                right_paddle.move_up()
            if key[pygame.K_DOWN]:
                right_paddle.move_down()

        # AI control (extra check to ensure no players are active).
        if config.ai == True and config.player_active_right == False:
            filter_right = ball_direction_filter(list, right_side=True)
            # Provides the closest ball to the paddle
            target_right = nearest_ball(right_paddle, filter_right)
            # It is possible for the filter to return None if filter provides a list with no elements. No movement in that case.
            if target_right != None:
                if ai(right_paddle, target_right):
                    right_paddle.move_up()
                # False is explicitly stated so as to not move upon None/Continue returns
                elif ai(right_paddle, target_right) == False:
                    right_paddle.move_down()
        if config.ai == True and config.player_active_left == False:
            filter_left = ball_direction_filter(list, left_side=True)
            target_left = nearest_ball(left_paddle, filter_left)
            if target_left != None:
                if ai(left_paddle, target_left):
                    left_paddle.move_up()
                elif ai(left_paddle, target_left) == False:
                    left_paddle.move_down()

        # Paddle and ball collisions
        for ball in list:
            # It is entirely possible that rect method here can return true even if the ball reset is true. Additionally changes direction.
            if collision(left_paddle, ball):
                ball.x_speed *= -1
                pygame.mixer.Sound.play(paddle_sound)
            if collision(right_paddle, ball):
                ball.x_speed *= -1
                pygame.mixer.Sound.play(paddle_sound)

        # Score
        player1_text = font.render(
            f"{config.player_left}: {Config.left_score}", True, Config.WHITE
        )
        player2_text = font.render(
            f"{config.player_right}: {Config.right_score}", True, Config.WHITE
        )
        if Config.left_score >= config.game_score:
            pygame.quit()
            sys.exit(f"{config.player_left} wins!\nThanks for playing!")
        if Config.right_score >= config.game_score:
            pygame.quit()
            sys.exit(f"{config.player_right} wins!\nThanks for playing!")

        # Screen objects
        for ball in list:
            # Background colour changes on every hit.
            if collision(left_paddle, ball) or collision(right_paddle, ball):
                while True:
                    # Gets new colour and checks to ensure same color not used twice in a row.
                    change_colour = get_colour()
                    if change_colour == current_colour:
                        continue
                    else:
                        Config.window.fill(change_colour)
                        # Updates top variable that is then called in else condition. Prevents color change to original when no collision.
                        current_colour = change_colour
                        break
            # Party mode because why not? Would not recommend sustained use.
            else:
                if config.party_mode:
                    current_colour = get_colour()
                Config.window.fill(current_colour)
        # Draws the player information on screen. Centered relative to string length. Drawn in this order so ball moves "on-top".
        Config.window.blit(
            player1_text,
            (
                (Config.DISPLAY_WIDTH / 4 - (player1_text.get_width() / 2)),
                Config.DISPLAY_HEIGHT / 12,
            ),
        )
        Config.window.blit(
            player2_text,
            (
                (
                    Config.DISPLAY_WIDTH / 2
                    + ((Config.DISPLAY_WIDTH / 4) - (player2_text.get_width() / 2))
                ),
                Config.DISPLAY_HEIGHT / 12,
            ),
        )
        # Draws an antialiased line along the center for player reference.
        pygame.draw.aaline(
            Config.window,
            Config.WHITE,
            ((Config.DISPLAY_WIDTH / 2) - 0.5, 0),
            ((Config.DISPLAY_WIDTH / 2) - 0.5, Config.DISPLAY_HEIGHT),
            1,
        )
        # Draws left paddle, right paddle, and ball(s). Moves ball.
        left_paddle.draw(Config.window, Config.WHITE)
        right_paddle.draw(Config.window, Config.WHITE)
        for ball in list:
            # Ball starts moving only if space key is pressed first (on start only).
            if key[pygame.K_SPACE]:
                start = True
            if start:
                ball.move()
            ball.draw(Config.window, Config.WHITE)

        # Screen update
        Config.clock.tick(Config.FPS)
        pygame.display.update()
    pygame.quit()
    sys.exit("Thanks for playing!")


# All functions used in main chronologically.
# From the list below, randomly return  a color.
def get_colour():
    colours = [
        Config.BLACK,
        Config.BLUE,
        Config.PURPLE,
        Config.RED,
        Config.TEAL,
        Config.GREEN,
        Config.YELLOW,
        Config.BROWN,
    ]
    colour = random.choice(colours)
    return colour


# Returns all choices made by the user by modifying/instantiating the Config class.
def init_configs():
    # Allows for changes to be made per instantiation rather than direcly modifying the static values.
    config = Config()
    # User validation of specified inputs.
    while True:
        user_input = input(
            "Enter 'C' to view controls or 'P' to continue to game parameters. Enter any other key to start with default parameters: "
        ).lower()
        if user_input == "c":
            print(instruction())
        # Starts game in party mode with default parameters. No customizable choices here cause no one should use it.
        elif user_input == "party":
            config.party_mode = True
            break
        elif user_input == "p":
            # Sequential while loops for parameter modification in order.
            while True:
                # Player mode selection. 1/2/0.
                user_player_count = input(
                    "Enter '1' for single player and '2' for two players or '0' for only AI: "
                )
                # 1 player setup.
                if user_player_count == "1":
                    # Loop for side selection, name.
                    while True:
                        # Allows user to select the side they'd like to play on. Only 1-player.
                        user_side = input(
                            "Enter 'L' for left side or 'R' for right side: "
                        ).lower()
                        # Activates AI, deactivates right player, sets username.
                        if user_side == "l":
                            config.ai = True
                            config.player_active_left = True
                            config.player_active_right = False
                            user_player_left = input("Player name: ")
                            config.player_left = user_player_left
                            config.player_right = "AI"
                            break
                        # Activates AI, deactivates left player, sets username.
                        elif user_side == "r":
                            config.ai = True
                            config.player_active_right = True
                            config.player_active_left = False
                            user_player_right = input("Player name: ")
                            config.player_right = user_player_right
                            config.player_left = "AI"
                            break
                    break
                # 2 player setup.
                elif user_player_count == "2":
                    user_player_left = input("Player 1 name: ")
                    user_player_right = input("Plater 2 name: ")
                    config.player_active_left = True
                    config.player_active_right = True
                    config.player_left = user_player_left
                    config.player_right = user_player_right
                    break
                # Full AI setup
                elif user_player_count == "0":
                    config.ai = True
                    config.player_active_left = False
                    config.player_active_right = False
                    config.player_right = "AI"
                    config.player_left = "AI"
                    break
                # Stays in loop if not 1, 2, 0.
                else:
                    print("Invalid number.")
                    continue
            # Ball amount selection.
            while True:
                user_ball_count = input("Enter number of balls(1-5): ")
                if validate(ball_amount=user_ball_count):
                    config.ball_count = int(user_ball_count)
                    break
                else:
                    print("Only numbers from 1 to 5 are accepted.")
                    continue
            # Ball speed selection. Breaks collision at higher speeds if paddle width is not adjusted simultaneously.
            while True:
                user_ball_speed = input("Enter the speed of the ball(s)(1-9): ")
                if validate(ball_speed=user_ball_speed):
                    config.ball_dx = int(user_ball_speed)
                    config.ball_dy = int(user_ball_speed)
                    break
                else:
                    print("Only numbers from 1 to 9 are accepted.")
                    continue
            # Paddle speed selection.
            while True:
                user_paddle_speed = input("Enter the speed of your paddles(1-15): ")
                if validate(paddle_speed=user_paddle_speed):
                    config.paddle_dy = int(user_paddle_speed)
                    break
                else:
                    print("Only numbers from 1 to 15 are accepted.")
                    continue
            # Target score selection at which game should end.
            while True:
                user_end_score = input("At what score should the game end?(1-100): ")
                if validate(end_score=user_end_score):
                    config.game_score = int(user_end_score)
                    break
                else:
                    print("Only numbers from 1 to 100 are accepted.")
                    continue
            # Triggers break when all these lines have executed.
            break
        # Any other keyboard input will break out of the loop and start game with defaults.
        else:
            break
    # Function will not do anything if nothing is returned as no values will be set. Game will always run on defaults unless the Class itself is modified.
    return config


# Fairly unoptimal way to do this, but beats having all these variables within the function itself.
def instruction():
    left = "Press W/S to move the left-paddle up/down."
    right = "Press Up-arrow/Down-arrow to move the right-paddle up/down."
    start = "The ball will start moving when the space key is pressed."
    parameters_1 = "You can change the number of balls, ball-speed, or paddle-speed the game starts with in game parameters."
    parameters_2 = "You can even change player names or the number of points required to win the game!"
    parameters_3 = "If you wish to skip all that, the game is also able to start with default parameters for all the above."
    default = "For your information, the default parameters are: ball-amount = 1, ball-speed = 5, paddle-speed = 7, target = 10"
    return f"{left}\n{right}\n{start}\n{parameters_1}\n{parameters_2}\n{parameters_3}\n{default}"


# I got too excited with power and used regex to validate int inputs.
def validate(ball_amount=None, ball_speed=None, paddle_speed=None, end_score=None):
    if ball_amount:
        check = re.search(r"^[12345]$", ball_amount)
        return bool(check)
    elif ball_speed:
        check = re.search(r"^[123456789]$", ball_speed)
        return bool(check)
    elif paddle_speed:
        check = re.search(r"^[1][012345]$|^[123456789]$", paddle_speed)
        return bool(check)
    elif end_score:
        check = re.search(r"^[1][0][0]$|^[123456789][\d]$|^[123456789]$", end_score)
        return bool(check)
    else:
        return False


# Initializes pygame, the game window, clock, caption, and assigns value to ensure the main game loop runs.
def setup():
    pygame.init()
    Config.window = pygame.display.set_mode(
        (Config.DISPLAY_WIDTH, Config.DISPLAY_HEIGHT)
    )
    Config.clock = pygame.time.Clock()
    pygame.display.set_caption("King Pong")
    Config.running = True


# Needed in order to maintain portability to other systems. Gets absolute filepath and joins asset folders.
def get_filepath(file):
    # .dirname removes the last segment of the path. So in this case, we get the absolute path of the current file, then remove the current file.
    directory = os.path.dirname(os.path.abspath(__file__))
    # Joins the directory returned with the asset folder/file path.
    filePath = os.path.join(directory, file)
    return filePath


# Filters direction of the balls moving towards the right or left (set on function call) and appends them in a list. Returned list can be empty
def ball_direction_filter(list, right_side=False, left_side=False):
    direction = []
    if right_side == True:
        for ball in list:
            if ball.x_speed > 0:
                direction.append(ball)
        return direction
    elif left_side == True:
        for ball in list:
            if ball.x_speed < 0:
                direction.append(ball)
        return direction


# Selects the best ball from the filtered list and returns it. Returns None if the list it gets is empty
def nearest_ball(paddle, list):
    if len(list) > 0:
        target_ball = list[0]
        for ball in list:
            if distance_to(paddle, ball) < distance_to(paddle, target_ball):
                target_ball = ball
        return target_ball


# Calculates the distance from the center of the paddle to the center of the ball
def distance_to(rect1, rect2):
    distance = math.sqrt(
        ((rect1.centerx - rect2.centerx) ** 2) + (rect1.centery - rect2.centery) ** 2
    )
    return distance


# Compares ball to paddle position and returns a boolean which is evaluated for movement.
def ai(paddle, ball):
    if paddle.centery > ball.centery:
        return True
    else:
        return False


# Uses pygame's rect class and it's inbuilt class method of colliderect. Checks if two rectangles overlap.
def collision(rect1, rect2):
    collision = pygame.Rect.colliderect(rect1, rect2)
    return collision


if __name__ == "__main__":
    main()
