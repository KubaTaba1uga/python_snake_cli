# python_snake_cli

# Ideas:
* 1\. Two game types  
  * 1\.1 Infinite (User can pick a board)
    * 1\.1\.1 User can't win
    * 1\.1\.2 When the game ends save session with end time
  * 1\.2 Level lead to level (max score dependent on a difficulty level)
    * 1\.2\.1 Story screens between levels
    * 1\.2\.2 Session remember which boards was played and which where not
    * 1\.2\.3 Game ends when there is no more boards to play
* 2\. High scores board
* 3\. Difficulty is a speed of game engine
  * 3\.1 must be very quick (like >300hz) so snake can influence user experience 
    * 3\.1\.1 make snake speed dependent on game engine speed
  * 3\.2 base - medium = 600 hz
  * 3\.3 easy = medium / 2
  * 3\.4 hard = medium * 2
* 4\. Boards can be of 4 sizes
  * 4\.1 small = 20x20
  * 4\.2 medium =  50x50
  * 4\.3 big = 75x75
  * 4\.4 large = 100x100 
