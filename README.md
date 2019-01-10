# Tic-Tac-Toe
Tic-Tac-Toe using Reinforcement Learning (Q-LEarning)

AI learns to play tic-tca-toe using Q-Learning algorithm. 
Interesting thing: AI does not know the concept of tic-tac-toe game. It only receives 9 sensory inputs for 9 positions i.e +1 if AI holds
the position, -1 if opponent holds the posisition, 0 if position is empty. It outputs the desired position to play and receives reward 
for the play i.e -1 (variable:loose_reward) if it looses the game, +1(variable:win_reward), -0.1(variable: simple_move_reward) for a 
simple move (necessary to compail AI to quickly finish the game by taking best steps), -0.1(variable: wrong_move_reward) if AI outputs the
position which is already played by it or by opponent.

Initially, AI plays and trains itself against the random move player which plays on any available empty place.

Human can play with the AI by setting variable human_plays=True, which is more effective to train AI quickly and efficently.

Already trained AI brains are available in the folder 'brain backup'. Instead of sarting from the scratch each time, these trained brains can
be used by setting variable load_brain=True, and copying these brains(named 'last_brain.pth') to the main folder. 
Program automatically stores the brain after 10000 plays.

----

AI vs AI matches can also be played by running main_1o1 file.

-----

Current AI gives 77% performance against random move player, whcih is not so high; but this project gives outline for anyone who wants to 
further twist and tune the basic strategy.

Environment: python, pytorch, kivy

Reference: Udemy AI course

Email: paras.v.prabhu@gmail.com
