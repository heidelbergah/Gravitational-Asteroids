James Bouchat
jbouchat@uvm.edu
CS021F

This project is the game of asteroids, but each individual asteroid
has a gravitational pull. All asteroids and the player are affected
by gravity. The player is given 3 lives. If the player crashes into
an asteroid, a life is lost and the player respawns with 2 seconds 
of immunity.

The only pip-installable module used is Pygame.

Run the main.py file to open the project. This will open the main-menu.
Once in the main menu, you can navigate between the different buttons
with the up and down arrows on the keyboard. Pressing enter / return
will select your currently selected button. Pressing the escape button
will return you to the previous menu. In the customize menu, pressing
enter / return will cycle you through the different available colors for
the spaceship and gravity indicator.

Once in game, to control the player, use 'W' to engage the thrusters,
'A' to rotate the ship left, and 'D' to rotate the ship right. Pressing
the space bar will fire a missile. You may also notice an indicator moving
on its own. This indicator tells you what direction the player is being
pulled into.