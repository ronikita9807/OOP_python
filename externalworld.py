from tkinter import *
import time
import random

import forconst
import bankbranch
import interface


class ExternalWorld:
    time = 0
    clerk = 0
    line = 0
    last_hour = 0
    max_len_line = 0
    pos_clients = []
    speed = 50
    restart_flag = 0
    start_flag = 0
    time_befor_new_client = abs(random.randint(0,10))
    day = 'Понедельник'
    day_num = 0
    last_day_num = 0
    weeks = 1
    hour = 0
    minute = 0

    def __init__(self, master):

        self.const = forconst.ForConst()
        self.interface = interface.Interface(master, self)
        

        


    def format_time_text(self):
        self.minute = self.time % self.const.LEN_MIN
        self.hour = (self.time//self.const.LEN_MIN) % self.const.LEN_HOUR

        if (self.time//self.const.LEN_MIN)//self.const.LEN_HOUR < self.const.LEN_WEEK:
            index = (self.time//self.const.LEN_MIN) // self.const.LEN_HOUR
            self.day = self.const.WEEK[index]
            self.day_num = (self.time//self.const.LEN_MIN) // self.const.LEN_HOUR
        else:
            index = ((self.time//self.const.LEN_MIN) // self.const.LEN_HOUR) % self.const.LEN_WEEK
            self.day = self.const.WEEK[index]
            self.day_num = ((self.time//self.const.LEN_MIN) // self.const.LEN_HOUR) % self.const.LEN_WEEK

            if ((self.time//self.const.LEN_MIN)//self.const.LEN_HOUR) // self.const.LEN_WEEK > self.weeks-1:
                self.weeks += 1


        if self.minute >= 10:
            minute = str(self.minute)
        else: 
            minute = '0' + str(self.minute)

        
        if self.hour >= self.const.START_WORK_DAY:
            hour = str(self.hour)
        else: 
            hour = '0' + str(self.hour)

        
        return 'Неделя ' + str(self.weeks) + ' \n' + str(self.day) + ' ' + hour + ':' + minute
    

    def tick(self):
        self.speed = self.interface.get_speed()
        #until the end of the week
        if self.time < self.const.LEN_WEEK*self.const.LEN_HOUR*self.const.LEN_MIN and not(self.restart_flag):            

            self.time += 1
            
            


        

    def what_is_coef_speed_time(self):

        if (self.hour == self.const.HOUR_WHEN_LINES_CLIENTS_WILL_MORE 
            and not(self.day == self.const.NOT_WORK_DAY)):
            
            coef = self.const.COEF_NORM_TIME_SPEED
        elif (self.hour < self.const.START_WORK_DAY 
                or self.hour > self.const.END_WORK_DAY 
                or self.day == self.const.SHORT_WORK_DAY
                and self.hour == self.const.END_SHORT_DAY 
                or self.day == self.const.NOT_WORK_DAY):
                
            coef = 0
        elif self.hour < self.const.HOUR_WHEN_LINES_CLIENTS_WILL_MORE :
            coef = 1.0
        else:
            if self.last_hour < self.hour:
                self.last_hour = self.hour
                coef = self.coef - self.const.STEP_COEF_NORM_TIME_SPEED
            else:
                coef = self.coef


        if (self.day_num == self.last_day_num 
            or self.day == self.const.SHORT_WORK_DAY 
            and self.hour == END_SHORT_DAY 
            or self.day == self.const.NOT_WORK_DAY):
            
            return coef

        else:
            self.last_day_num = self.day_num
            return coef - self.const.STEP_COEF_NORM_TIME_SPEED


    def make_bank(self):
        self.start_flag = 1
        self.last_day_num = 0 
        self.interface.create_canvas()
        clerk = self.interface.get_clerk()
        lenth_clerk = self.interface.canvas_len/((clerk+1)*4)
        self.lenth_client = lenth_clerk/2
        
        self.pos_clients = self.interface.print_clerks(clerk)

        max_len_line = self.interface.get_max_line()

        self.bank = bankbranch.BankBranch(self.pos_clients, clerk, max_len_line)

        self.restart_flag = 0
        

        



    def restart(self):
        #if self.start_flag == 1:
            self.time = 0
            self.weeks = 1
            self.restart_flag = 1
            self.last_hour = 0
            self.pos_clients = []
            self.speed = 50
            self.time_befor_new_client = abs(random.randint(0,10))
            self.day = 'Понедельник'
            self.last_day_num = 0
            self.hour = 0
            self.minute = 0
            self.day_num = 0

            self.bank.restart()

            self.interface.restart(self)

        
