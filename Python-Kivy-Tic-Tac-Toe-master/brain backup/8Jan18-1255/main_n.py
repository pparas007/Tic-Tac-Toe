# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 10:25:58 2019

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
from my_ai import Dqn
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
    #load_brain=True 
    load_brain=False
    brain = Dqn(27,9,0.80) # initiate AI brain
    positions=[0,0,0,0,0,0,0,0,0]
    training_demos=5000000 # train brain for these many examples
    buttons=[]
    last_reward=0
    
    #numbers to calculate statistics
    AI_wins=0
    Bot_wins=0
    Draws=0
    
    #rewards
    draw_reward= 1
    simple_move_reward=0
    wrong_move_reward=-0.5
    win_reward=5
    loose_reward=-3
    
    AI_pressed_the_button=False
    
    #to play manuaaly with AI
    human_plays=False
    
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
            random=randint(0, 8)
            if(self.positions[random]==0):
                self.buttons[random].text=self.bot_choice
                self.positions[random]=-1 # mark the box
                break
        
        self.check_winner()
        self.check_draw()
    def take_decision(self):
        self.check_winner()
        self.check_draw()
        while True:
            #print('\nsending',self.last_reward,  self.positions)
            new_positions=[None] * 27
            for i in range(0,len(self.positions)):
                new_positions[i*3]= 1 if self.positions[i] == -1 else 0
                new_positions[i*3+1]= 1 if self.positions[i] == 0 else 0
                new_positions[i*3+2]= 1 if self.positions[i] == 1 else 0
            box_number = self.brain.update(self.last_reward,  new_positions)
            #print('output',box_number)
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
                self.check_winner()
                self.check_draw()
                
                button.text = self.bot_choice
                self.positions[int(button.id)]=-1
                self.take_decision()
                
                self.check_winner()
                self.check_draw()
    # Initializes players
    def init_players(self):
        if self.load_brain:
            self.brain= self.load()
        
        self.bot_choice = self.choices[randint(0,1)];
        self.player = "X" if self.bot_choice == "O" else "O"
        
        #AI vs Bot
        if self.human_plays==False:
            first_time=1
            while True:
                if randint(0,1) == 1 and first_time==1:
                    self.make_move()
                    first_time=0
                self.take_decision() # AI 
                
                if self.human_plays==False:
                    self.make_move() # Bot
                
                # if total no. of games is greater than training example, exit.
                if( (self.AI_wins+self.Bot_wins+self.Draws) >self.training_demos):
                    break
        #AI vs Human
        #else:
            
        self.save()

    def check_winner(self):
        for combo in self.winning_combos:
            if self.board[combo[0]].text == self.board[combo[1]].text == self.board[combo[2]].text and self.board[combo[0]].text != '':
                self.game_over = True
                if self.board[combo[0]].text == self.player:
                    self.last_reward=self.win_reward
                    self.AI_wins=self.AI_wins+1
                    self.reset_game('AI wins!')
                else:
                    self.last_reward=self.loose_reward
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
        if(total_games%10000==0):
            with open('log.txt', 'a') as the_file:
                the_file.write('\n\n##################Statistics################## \nTotal Plays: '+str(total_games))
                the_file.write('\nAI wins: '+str(self.AI_wins)+'\nAI loses: '+str(self.Bot_wins)+'\nDraws: '+str(self.Draws)+'\nPerformance: '+str("{0:.2f}".format(self.AI_wins/(total_games+1)))+'\n###################################')
            self.save()          
        
        if self.game_over:
            for button in self.board:
                button.text = ''
            self.positions=[0,0,0,0,0,0,0,0,0]
            self.game_over = False
        
    def save(self):
        print("saving brain...")
        self.brain.save()

    def load(self):
        print("loading last saved brain...")
        return self.brain.load()

if __name__ == '__main__':
    TicTacToeApp().run()
