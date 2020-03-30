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
        self.interface = interface.Interface(master)
        self.interface.label['text'] = self.format_time_text()
        self.interface.botton_start = Button(master, width=12, height=1,
                                          text="НАЧАТЬ", font='Times',
                                          state=NORMAL, bg='green', 
                                          fg='white',
                                          command=self.make_bank)

        self.interface.botton_start.grid(row=76, column=13,
                                     columnspan=22, rowspan=5)

        self.interface.botton_restart=Button(master, width=12, height=1,
                                          text="ПЕРЕЗАПУСК", 
                                          font='Times 12', bg='red', 
                                          fg='white', state=NORMAL, 
                                          command=self.restart)

        self.interface.botton_restart.grid(row=74, column=13, 
                                        columnspan=22, rowspan=5)

        


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
        self.speed = int( self.interface.speed.get())+2
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
        self.interface.canvas_up.delete("all")
        self.interface.canvas_down.create_rectangle(50, 50, 500, 350, fill = '#FFDAB9')
        self.interface.canvas_down.create_rectangle(550, 50, 1050, 350, fill = '#FFDAB9')
        self.interface.canvas_up.create_rectangle(400, 200, 700, 300, fill = '#FFFACD')
        self.delete = self.interface.canvas_down.create_text(250, 80, fill = 'black', 
                                                        text = 'ЗА ДЕНЬ:',
                                                        font = 'Times 15')
        self.delete = self.interface.canvas_down.create_text(750, 80, fill = 'black', 
                                                        text = 'ЗА НЕДЕЛЮ:',
                                                        font = 'Times 15')
        clerk = int(self.interface.clerk.get())
        lenth_clerk = self.interface.canvas_len/((clerk+1)*4)
        self.lenth_client = lenth_clerk/2
        position = lenth_clerk
        self.pos_clients = []
        for i in range(clerk):
            position += self.interface.canvas_len/(clerk+1)
            self.pos_clients.append(position)
            self.interface.canvas_up.create_rectangle(position-lenth_clerk,
                                                    0,position+lenth_clerk,
                                                    50, width=1, fill='red')
        self.bank = bankbranch.BankBranch(self.pos_clients)
        self.bank.clerk = clerk
        self.bank.max_len_line = int(self.interface.max_line.get())
        self.restart_flag = 0
        self.bank.clients_at_clerks_info = []
        self.interface.label.after_idle(self.tick)

        



    def restart(self):
        #if self.start_flag == 1:
            self.time = 0
            self.weeks = 1
            self.interface.label.configure(text = self.format_time_text())
            self.interface.canvas_up.delete("all")
            self.interface.canvas_down.delete("all")
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

        
