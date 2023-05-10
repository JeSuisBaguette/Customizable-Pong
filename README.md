# Pong+

### Created by:
Ferdinand Edward Bitan

### Video demo:

## Introduction

### Project description:
A game of pong with options to customize gameplay experience at the terminal or run at default parameters. Customizabile options include the ability to choose whether the game will launch in a single-player, two-players, or only-AI mode. If the single-player option is chosen, the user can further select which side of the game window they wish to play on, with the opposite paddle being controlled by the game AI. Customizable options available in common between single-player and two-player modes are player names, number of balls the game starts with, the speed of the balls, the speed of the paddles, and at what score the game should end. If the game starts in only-AI mode, all these options are still available apart from player name assignment. Starting the game with default parameters skips all prompts for customizability and initializes a game with one ball, set ball and paddle speeds, no AI, and a game ending score of 10. 

### Note:
This project was created to be submitted as the final project for the CS50P online Harvard course. I had no prior experiences in coding before this, and this project serves as the first programming project that I have undertaken on my own. 

## File Structure

### Fonts:
Contains font .ttf files that can be used in the game. While only one font is initialized within the main project file, other downloaded fonts can be saved and loaded from here.
Fonts currently included: Arimo Nerd Font, CaskaydiaCove Nerd Font, HeavyData Nerd Font. All fonts were downloaded from [Nerd Fonts](https://www.nerdfonts.com/).

### Music:
Contains all sound files required for the game saved in .ogg format. This include sounds for paddle-ball collision (collect.ogg), ball-wall collision (select.ogg), and sound for when the ball goes out of bounds (explosion.ogg). Lastly, the background music played in a loop over the course of the game is also stored here (pong.ogg).

Credit for the sounds files of collect.ogg, select.ogg, and explosion.ogg goes to Christian DeTamble - http://therefactory.bplaced.net. Sound collection downloaded from [OpenGameArt](https://opengameart.org/content/8-bit-retro-sfx). These sounds are licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/).

Credit for the background music used in the game goes to user [yesme](https://opengameart.org/users/yesme) and has been downloaded from [OpenGameArt](https://opengameart.org/content/pong-0).

### Main file (project.py):
Contains the code of the project. Houses all classes, functions, and the main game loop required to make the code run.

### Unit tests (test_project.py):
Contains unit tests for the functions defined within the project.py file.

### Features.txt:
This is a text file that lists the features and customizability options for the game. Also contains a breakdown for how the game AI works.

### Requirements.txt:
Contains the pip-installable libraries and their respective versions used in the project which are required for it to run. 

## Documentation

### Classes:
### Functions:
### Main game loop: explain terminal