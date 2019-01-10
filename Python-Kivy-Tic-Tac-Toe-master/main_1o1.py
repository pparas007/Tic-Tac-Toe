# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 13:19:49 2019

@author: 007Paras
"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.config import Config
#from ai import Ai
from random import randint
from my_ai_1o1 import Dqn
import time
class TicTacToeApp(App):

    title = 'Tic Tac Toe'
    board = []
    choices = ["X","O"]
    game_over = False
    winning_combos = [
        [0,1,2], [3,4,5], [6,7,8], # Horizontal
        [0,3,6], [1,4,7], [2,5,8], # Vertical
        [0,4,8], [2,4,6]           # Diagonal
    ]
    
    #load already trained brain  
    load_brain=True
    brain = Dqn(9,9,0.80) # initiate AI brain
    brain_Player = Dqn(9,9,0.80) # initiate AI brain
    positions=[0,0,0,0,0,0,0,0,0]
    training_demos=5000000 # train brain for these many examples
    buttons=[]
    last_reward=0
    last_reward_Player=0
    
    #numbers to calculate statistics
    AI_wins=0
    Bot_wins=0
    Draws=0
    
    #rewards
    draw_reward= 0.1
    simple_move_reward=-0.1
    wrong_move_reward=-0.1
    win_reward=1
    loose_reward=-1
    
    AI_pressed_the_button=False
    
    #to play manuaaly with AI
    human_plays=True
    
    def build(self):
        Config.set('graphics', 'width', '450')
        Config.set('graphics', 'height', '450')
        Config.set('graphics','resizable', False)
        self.layout = StackLayout()
        for x in range(9): 
            bt = Button(text='', font_size=120, width=150, height=150, size_hint=(None, None), id=str(x))
            bt.bind(on_release=self.btn_pressed)
            self.board.append(bt)
            self.layout.add_widget(bt)
            self.buttons.append(bt)
        return self.layout

    # On application start handler
    def on_start(self):
        self.init_players();
        
    
    def make_move(self):
        self.check_winner()
        self.check_draw()
        
        while True:
            new_positions=  [x * -1 for x in self.positions] 
            box_number = self.brain_Player.update(self.last_reward_Player,  new_positions)
            if(self.positions[box_number]==0):
                self.AI_pressed_the_button=False
                self.btn_pressed(self.buttons[box_number])
                self.AI_pressed_the_button=True
                
                self.positions[box_number]=-1 # mark the box
                self.last_reward_Player=self.simple_move_reward
                break
            else:
                self.last_reward_Player=self.wrong_move_reward
        
        self.check_winner()
        self.check_draw()
        
    def take_decision(self):
        self.check_winner()
        self.check_draw()
        while True:
            #print('\nsending',self.last_reward,  self.positions)
            box_number = self.brain.update(self.last_reward,  self.positions)
            #print('output',box_number)
            #time.sleep(7)
            if(self.positions[box_number]==0):
                self.AI_pressed_the_button=True
                self.btn_pressed(self.buttons[box_number])
                self.AI_pressed_the_button=False
                
                self.positions[box_number]=1 # mark the box
                self.last_reward=self.simple_move_reward
                break
            else:
                self.last_reward=self.wrong_move_reward
        self.check_winner()
        self.check_draw()
        
    # On button pressed handler
    def btn_pressed(self, button):
        if len(button.text.strip()) < 1: # Continue only if the button has no mark on it...
            if self.AI_pressed_the_button:
                button.text = self.player
            else:
                button.text = self.bot_choice
    
    # Initializes players
    def init_players(self):
        if self.load_brain:
            self.brain= self.load(self.brain)
            #self.brain_Player= self.load(self.brain_Player,"_Player")
        
        self.bot_choice = self.choices[randint(0,1)];
        self.player = "X" if self.bot_choice == "O" else "O"
        
        
        #AI vs AI
        if randint(0,1) == 1:
                self.make_move()
        while True:
            self.take_decision()
            self.make_move()

    def check_winner(self):
        for combo in self.winning_combos:
            if self.board[combo[0]].text == self.board[combo[1]].text == self.board[combo[2]].text and self.board[combo[0]].text != '':
                self.game_over = True
                if self.board[combo[0]].text == self.player:
                    self.last_reward=self.win_reward
                    self.last_reward_Player=self.loose_reward
                    self.AI_wins=self.AI_wins+1
                    self.reset_game('AI wins!')
                else:
                    self.last_reward=self.loose_reward
                    self.last_reward_Player=self.win_reward
                    self.Bot_wins=self.Bot_wins+1
                    self.reset_game('Bot wins!')

    def check_draw(self):
        flag=1;
        for i in range (0,9):
            if(self.positions[i]==0):
                flag=0
        if(flag==1):
            self.game_over = True
            self.Draws=self.Draws+1
            self.last_reward=self.draw_reward
            self.win_reward=self.draw_reward
            self.reset_game('A Draw')
    # Resets game state by deleting button values...
    def reset_game(self, popup):
        
        total_games=(self.AI_wins+self.Bot_wins+self.Draws)
        
        #print(popup)
        #print('##################Statistics################## \nTotal Plays: ',total_games)
        #print('AI wins: ',self.AI_wins,'\nAI loses: ',self.Bot_wins,'\nDraws: ',self.Draws,'\nPerformance: ',"{0:.2f}".format(self.AI_wins/(total_games+1)),'\n###################################')
        #print('Restarting!\n')
        #print only intermittently
        if(total_games%100==0):       	
            print(popup)
            print('##################Statistics################## \nTotal Plays: ',total_games)
            print('AI wins: ',self.AI_wins,'\nAI loses: ',self.Bot_wins,'\nDraws: ',self.Draws,'\nPerformance: ',"{0:.2f}".format(self.AI_wins/(total_games+1)),'\n###################################')
            print('Restarting!\n')
            
        #save brain and write to log file only intermittently
        if(total_games%1000==0):
            with open('log.txt', 'a') as the_file:
                the_file.write('\n\n##################Statistics################## \nTotal Plays: '+str(total_games))
                the_file.write('\nAI wins: '+str(self.AI_wins)+'\nAI loses: '+str(self.Bot_wins)+'\nDraws: '+str(self.Draws)+'\nPerformance: '+str("{0:.2f}".format(self.AI_wins/(total_games+1)))+'\n###################################')
            self.save(self.brain)          
            self.save(self.brain_Player,"_Player")
        
        if self.game_over:
            for button in self.board:
                button.text = ''
            self.positions=[0,0,0,0,0,0,0,0,0]
            self.game_over = False
        
    def save(self,brain,append=""):
        print("saving brain...")
        brain.save(append)

    def load(self,brain,append=""):
        print("loading last saved brain...")
        return brain.load(append)
    
if __name__ == '__main__':
    TicTacToeApp().run()
