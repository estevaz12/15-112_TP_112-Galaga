Title: 112 Galaga

Description: This program is a remake of the classic arcade game Galaga with Python. It 
	     consists of the player being a spaceship that is defending himself against 
	     aliens. The goal is to kill all the aliens in the stage in the shortest time
	     possible.

How to run:
- Just run 112Galaga.py
	- If you don't have pygame installed, it'll install it for you

How to play:
- Enable audio (enjoy the sound effects!)
- When in game, use arrow keys (left and right) to move the spaceship and 'space' to shoot
	- You can only have 2 bullets in the screen at a time (think carefully about this)
- Watch out for the bosses (green aliens), they're pretty fast
- There's a delay of 3 seconds when you die, so you have time to respawn

If you wanna skip to the scoreboard without actually winning (lame!):
- In 112Galaga.py go to line 20 and change it to self.state = "score"
- Then, in scoreState.py:
	- line 7 change to self.screen = "board"
	- line 56: change "scores-"+self.difficulty+".txt" to "scores-easy.txt" (with 
	  quotes) to view a preview of the scoreboard
		- If you want, you can add entries to the file
