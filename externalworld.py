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
    clients_at_clerks_info = []
    speed = 50
    restart_flag = 0
    time_befor_new_client = abs(random.randint(0,10))
    day = 'Понедельник'
    day_num = 0
    last_day_num = 0
    weeks = 1
    hour = 0
    minute = 0

    def __init__(self):

        self.const = forconst.ForConst()
        self.interface = interface.Interface()
        self.interface.label['text'] = self.format_clock_text()
        self.interface.botton_start = Button(self.interface.master, width=12, height=1,
                                          text="НАЧАТЬ", font='Times',
                                          state=NORMAL, bg='green', 
                                          fg='white',
                                          command=self.make_clerks)

        self.interface.botton_start.grid(row=76, column=13,
                                     columnspan=22, rowspan=5)

        self.interface.botton_restart=Button(self.interface.master, width=12, height=1,
                                          text="ПЕРЕЗАПУСК", 
                                          font='Times 12', bg='red', 
                                          fg='white', state=NORMAL, 
                                          command=self.restart)

        self.interface.botton_restart.grid(row=74, column=13, 
                                        columnspan=22, rowspan=5)

        self.bank=bankbranch.BankBranch(self.pos_clients)
        


    def format_clock_text(self):
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

            self.bank.format_stat(self.clerk)

            self.interface.print_stat(self.bank.stat_day, self.bank.stat_week, self.line)

            self.time += 1
            #bank work on a short day
            if self.day == self.const.SHORT_WORK_DAY and self.hour == self.const.END_SHORT_DAY:
                self.bank.clients_waiting = self.bank.clients_waiting_step//self.const.LEN_SHORT_WORK_DAY
                self.bank.day_is_over(self.line, self.minute, self.clerk)
                self.line = 0
                self.delete_clients()
            #bank work on a normal day
            elif self.hour == self.const.END_WORK_DAY:
                self.bank.clients_waiting = self.bank.clients_waiting_step//self.const.LEN_WORK_DAY
                self.bank.day_is_over(self.line, self.minute, self.clerk)
                self.line = 0
                self.delete_clients()


            #clients_at_clerks_info[i]
            #[0] - pos clerk with client i
            #[1] - time before clerk free from client i
            #[2] - id client i
            #[3] - revenue from client i
            del_num = 0
            #time tracking of clients staying with clerks
            for num in range(len(self.clients_at_clerks_info)):
                
                self.clients_at_clerks_info[num-del_num][1] -= 1
                #if the work with the client is over
                #drawing his departure and freeing the clerk
                if self.clients_at_clerks_info[num-del_num][1] <= 0:
                    del_num += 1
                    self.interface.canvas_up.delete(self.clients_at_clerks_info[num-del_num][2])
                    self.bank.revenue += self.clients_at_clerks_info[num-del_num][3]
                    self.bank.revenue_week += self.clients_at_clerks_info[num-del_num][3]
                    self.bank.free_clerks.append(self.clients_at_clerks_info[num-del_num][0])
                    del(self.clients_at_clerks_info[num-del_num])

            #summing up the day
            if self.hour == 0 :
                self.last_hour = 0
                self.bank.clerks_salary = 0
                if self.day_num != self.const.NOT_WORK_DAY_NUM:
                    self.bank.clients_waiting_step = 0

            #if it’s the right time to generate a new client
            if (self.time_befor_new_client-1 <= 0 
                and self.hour >= self.const.START_WORK_DAY 
                and self.hour < self.const.END_WORK_DAY 
                and not(self.day == self.const.SHORT_WORK_DAY 
                and self.hour >= self.const.END_SHORT_DAY)   
                and not(self.day == self.const.NOT_WORK_DAY)) :
                
                
                self.coef = self.what_is_coef_speed_time()
                self.time_befor_new_client = abs(random.randint(0,10)) * self.coef * (int( self.interface.new_client_time_coef.get())/3)
                #queue length does not exceed the maximum
                if self.line < self.max_len_line:
                    self.line += 1
                    self.bank.clients += 1
                    self.bank.clients_in_hour += 1
                    self.bank.clients_week += 1
                #losing customers
                else:
                    self.bank.client_lost += 1
                    self.bank.client_lost_week += 1

            #reduce the time before a new client
            else:
                self.time_befor_new_client -= 1

            #if there is a queue
            if self.line > 0:
                pos_free_clerks = self.bank.give_pos_free_clerks()
                #if there is a free clerk
                if pos_free_clerks != 0:
                    self.line -= 1
                    del(self.bank.free_clerks[0])

                    objects = [pos_free_clerks]
                    objects.append(self.bank.time_before_free_clerks())
                    objects.append(self.interface.canvas_up.create_oval(pos_free_clerks-self.lenth_client,
                                                                    55,pos_free_clerks+self.lenth_client,
                                                                    55+self.lenth_client*2, 
                                                                    fill='green'))
                    objects.append(self.bank.revenue_one_client())

                    self.clients_at_clerks_info.append(objects)

            #updated statistics
            self.interface.update_statistics()
            #if working hours
            if (self.hour >= self.const.START_WORK_DAY 
                and self.hour < self.const.END_WORK_DAY 
                and not(self.day == self.const.SHORT_WORK_DAY 
                and self.hour >= self.const.END_SHORT_DAY) 
                and not(self.day == self.const.NOT_WORK_DAY) 
                and self.bank.free_clerks != []):
  
  
                self.bank.work_day_clerks_stat()
            #change last hour
            if self.last_hour < self.hour:
                self.last_hour = self.hour
                self.bank.clients_wait(self.line)
                
            #change last day num
            if self.last_day_num < self.day_num:
                self.last_day_num = self.day_num 
                self.bank.clients_waiting_week_step += self.bank.clients_waiting

            self.interface.label.after(self.speed, self.tick)
            self.interface.label['text'] = self.format_clock_text()

        # when week end
        else: 
            #if you did not press the restart key
            if not(self.restart_flag):
                self.bank.format_stat_when_week_end()

                self.interface.update_statistics_end_week(self.bank.stat_week)
    
                self.interface.label.after(self.speed, self.tick)
                self.interface.label['text'] = self.format_clock_text()


        

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


    def make_clerks(self):
        self.restart()
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
        self.clerk = int(self.interface.clerk.get())
        self.max_len_line = int(self.interface.max_line.get())
        lenth_clerk = self.interface.canvas_len/((self.clerk+1)*4)
        self.lenth_client = lenth_clerk/2
        position = lenth_clerk
        self.pos_clients = []
        for i in range(self.clerk):
            position += self.interface.canvas_len/(self.clerk+1)
            self.pos_clients.append(position)
            self.interface.canvas_up.create_rectangle(position-lenth_clerk,
                                                    0,position+lenth_clerk,
                                                    50, width=1, fill='red')
        self.bank = bankbranch.BankBranch(self.pos_clients)
        self.restart_flag = 0
        self.clients_at_clerks_info = []
        self.interface.label.after_idle(self.tick)

        

    def delete_clients(self):
        for i in range(len(self.clients_at_clerks_info)):
            self.bank.client_lost += 1
            self.bank.client_lost_week += 1
            self.clients_at_clerks_info[i][1] = 0



    def restart(self):
        self.time = 0
        self.weeks = 1
        self.interface.label['text'] = self.format_clock_text()
        self.clerk = 0
        self.line = 0
        self.interface.canvas_up.delete("all")
        self.interface.canvas_down.delete("all")
        self.restart_flag = 1
        self.clients_at_clerks_info = []
        self.last_hour = 0
        self.max_len_line = 0
        self.pos_clients = []
        self.speed = 50
        self.time_befor_new_client = abs(random.randint(0,10))
        self.day = 'Понедельник'
        self.last_day_num = 0
        self.hour = 0
        self.minute = 0
        self.day_num = 0

        self.bank.free_clerks = []
        self.bank.clerks_salary = 0
        self.bank.clerks_salary_week = 0
        self.bank.clerks_waiting = 0 
        self.bank.clients_waiting = 0
        self.bank.clerks_waiting_day = 0
        self.bank.clients_waiting_day = 0
        self.bank.clients_in_hour = 0
        self.bank.revenue = 0
        self.bank.client_lost = 0
        self.bank.clients = 0
        self.bank.revenue_week = 0
        self.bank.client_lost_week = 0
        self.bank.clients_week = 0 
        self.bank.stat_day = ''
        self.bank.stat_week = ''
        self.bank.clerks_salary = 0
        self.bank.clerks_salary_week = 0
        self.bank.clerks_waiting = 0
        self.bank.clients_waiting = 0
        self.bank.clients_waiting_week = 0
        self.bank.clients_waiting_week_step = 0
        self.bank.clients_waiting_step = 0
        self.bank.clerks_waiting_day = 0
        self.bank.clients_waiting_day = 0
        self.bank.clients_in_hour = 0
