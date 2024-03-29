# **Pong+**

### **Created by:**
JeSuisBaguette

## **Introduction**

### **Project description:**
A game of pong with options to customize gameplay experience at the terminal or run at default parameters. Customizable options include the ability to choose whether the game will launch in a single-player, two-players, or only-AI mode. If the single-player option is chosen, the user can further select which side of the game window they wish to play on, with the opposite paddle being controlled by the game AI. Customizable options available in common between single-player and two-player modes are player names, number of balls the game starts with, the speed of the balls, the speed of the paddles, and at what score the game should end. If the game starts in only-AI mode, all these options are still available apart from player name assignment. Starting the game with default parameters skips all prompts for customizability and initializes a game with one ball, set ball and paddle speeds, no AI, and a game ending score of 10. 

### **Note:**
This project was created to be submitted as the final project for the CS50P online Harvard course. I had no prior experiences in coding before this, and this project serves as the first programming project that I have undertaken on my own. 

## **File Structure**

### **Fonts:**
Contains font .ttf files that can be used in the game. While only one font is initialized within the main project file, other downloaded fonts can be saved and loaded from here.
Fonts currently included: Arimo Nerd Font, CaskaydiaCove Nerd Font, HeavyData Nerd Font. All fonts were downloaded from [Nerd Fonts](https://www.nerdfonts.com/).

### **Music:**
Contains all sound files required for the game saved in .ogg format. This include sounds for paddle-ball collision (collect.ogg), ball-wall collision (select.ogg), and sound for when the ball goes out of bounds (explosion.ogg). Lastly, the background music played in a loop over the course of the game is also stored here (pong.ogg).

Credit for the sounds files of collect.ogg, select.ogg, and explosion.ogg goes to Christian DeTamble - http://therefactory.bplaced.net. Sound collection downloaded from [OpenGameArt](https://opengameart.org/content/8-bit-retro-sfx). These sounds are licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/).

Credit for the background music used in the game goes to user [yesme](https://opengameart.org/users/yesme) and has been downloaded from [OpenGameArt](https://opengameart.org/content/pong-0).

### **Main file (project.py):**
Contains the code of the project. Houses all classes, functions, and the main game loop required to make the code run.

### **Unit tests (test_project.py):**
Contains unit tests for the functions defined within the project.py file.

### **Features.txt:**
This is a text file that lists the features and customizability options for the game. Also contains a breakdown for how the game AI works.

### **Requirements.txt:**
Contains the pip-installable libraries and their respective versions used in the project which are required for it to run. 

## **Documentation**

### **Classes and methods:**
This program has three classes. These are a Paddle class, a Ball class, and a Config class. Among these, the Paddle class and Ball class are responsible for object instantiation for their respective objects while the Config class houses static variables called by the Paddle and Ball classes as well as other functions. 

As such, the Config class has constants such as the display height and width, the ball height and width, the paddle heigh and width, and so on. To appropriately customize parameters of the game, this class is instantiated, and based on user input and validation, the individual variables of the instantiated object is then manipulated. Consequently, while the Config class constants are used for all non-customizable parameters by accessing Config directly, the customizable variables are accessed by other classes and functions through the instantiation of a Config object, whereby a new value is assigned to that object variable. This approach was chosen so as to prevent the user from being able to directly access and reassign the values of the Config class while setting up the paramenters. The use of the class also allows for the negation of global variable usage which had previously proven to be incredibly disadvantegous to the use of the Paddle and Ball classes which had to access the global variables to instantiate. Overall, the purpose of the Config class in this program is to hold all variables and constants related to the functioning of the game such that these crucial aspects need not be defined within a function or class method individually. Doing this allows for further modification of the code beyond the designated customizable variables and ensures that a change in value within the Config class is sufficient to reflect that change in all other aspects of the program which use it. Personally, the use of this Config class and the lack of any hard-coded values within the other classes and functions has been a huge help in both experimenting with new configurations for the game, and as well as in debugging. 

The Paddle class is used to instantiate both the right and left paddle objects in the game. Furthermore, the class inherits from Pygame's rect module so as to have access to all rect properties such as centerx, centery, and crucially, pygame's colliderect function. Additional methods for the class are draw(), which instructs pygame to draw the paddle object on the screen after it has instantiated, and move_up() and move_down() which control the respective y-axis movement of the paddles at the defined speed. 

Similarly, the Ball class, which also inherits from the rect module, is used to instantiate ball objects within the game. Accordingly, the class also has a draw method which instructs pygame to draw the objects onto the game window, as well as a move() method. This method contains the logic behind ball-wall collisions, which checks the y-coordinates of the balls and reverses their y-axis speed should the ball 'hit' the top or bottom of the game window. Similarly, this method also houses the logic for ball resetting should the ball go past the paddles on either side. If this happens, the ball is reset to the middle of the game window along the x-axis, and it's respawn location is randomized along the y-axis of this x-coordinate. Additionally, both the x-axis speed and the y-axis speed is also randomized using the random module upon ball respawn. Lastly, within the move method, when the conditions for the ball-wall collisions is true, or the conditions for the ball having moved past the respective paddle is true, the appropriate sound is played.   

### **Functions:**
A brief explanation of each of the functions used in the program, excluding main(), is provided below:

**get_color():** Returns a color from a list using the random module. 

**init_configs():** Function called at the beginning of the program for user input at the terminal. Instantiates Config class and returns user defined parameters.

**instructions():** Returns strings of text to do with control scheme, game parameters, and customizability.

**validate():** Performs user validation on customizable game options and returns a boolean based on whether the input is valid or not.

**setup():** Initializes pygame, sets up the game window, game clock, and caption.

**get_filepath():** Returns an absolute filepath based on the current directory and the passed in filepath of assets used in the game.

**ball_direction_filter():** Filters direction of the balls moving towards the right or left paddle (set on function call) and appends them to a list which is then returned. 

**nearest_ball():** From a list of balls, returns the ball that is closest to the paddle (set on function call).

**distance_to():** Calculates the distance from the center of the paddle to the center of the ball, which is then returned as a float.

**ai():** Compares ball to paddle position along the y-axis and returns a boolean which is evaluated for movement.

**collision():** Uses pygame's rect class and it's inbuilt class method of colliderect. Checks if two rectangles overlap. Returns a boolean based on whether there is a overlap (collision) between the two objects.  

### **main() and game loop:**
This is the part of the code where all class objects are instantiated, user parameters are considered, pygame is initialized, and the game window is displayed to the user. The game runs at 60fps. Instead of explaining the code that runs within main() or the game loop (since it is quite typical as far as pygame programs go), in this section, I wish to highlight some of the atypical design decisions that the user of this program would notice upon running it.

One perhaps peculiar aspect of the program is that customization regarding the game is done at the terminal instead of an in-game UI. The limiting factor for this was my own inexperience and the scope of the project. For this project, I wished to learn how to use pygame and allow customizations to the main game, and I felt that the additional aspect of learning how to program a UI would significantly alter the scope of the project beyond my abilities at this time. However, allowing customization at the terminal led to a problem where the pygame window would pop up the moment the program was run. As such, this led to the design choice to have a separate function called setup() which contains the pygame initialization code as well as the code that actually sets up the display window for pygame. Admittedly, this is a workaround solution to not wishing to have the pygame window initialize until all terminal interactions are complete, which would otherwise lead to having to minimize the game window and then proceeding with the terminal prompts. However, for the purposes of a first project coded on my own, this serves as an adequate solution until I learn how to code actual UI.

Another design choice that needed to be made as a result of having pygame initialize after terminal usage, was to make sure that the ball did not start moving the moment the game window popped up. This would normally be a design consideration under normal circumstances, but was further exacerbated in this case as the game window would open 'behind' the terminal window. This meant that if the ball started moving on game window initialization, by the time the user would have navigated to the game window, there was a high possibility that points would already be scored depending on the direction the ball started moving in. In order to combat this, an additional 'start' condition was added to main() under which the ball(s) would only start moving once the spacebar key has been pressed after the game window pops up. This condition is only evaluated once at the very start of the game. Ball respawns after it goes out of bounds do not share this condition and will start moving in a random direction the moment it appears on screen. 

## **Final remarks**
That was it! Thank you for checking out this project! You are welcome to use the code if you want. Overtime, I do wish to update this program to include an actual UI instead of terminal prompts. Along with this, I also wish to create unit tests for every class method and function created in this project as not all of them are being currently tested. All in all, while this project might have come to an end in terms of submission (as I have met my previously self-assigned goals at the conception of the project), I don't intend to stop working on it as the scope keeps getting bigger (UI and unit tests for all functions). 