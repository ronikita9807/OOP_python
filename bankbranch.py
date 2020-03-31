from tkinter import *
import time
import random

import forconst


class BankBranch:
    revenue = 0
    client_lost = 0
    clients = 0
    revenue_week = 0
    client_lost_week = 0
    clients_week = 0
    stat_day = ''
    stat_week = ''
    clerks_salary = 0
    clerks_salary_week = 0
    clerks_waiting = 0
    clients_waiting = 0
    clients_waiting_week = 0
    clients_waiting_week_step = 0
    clerk = 0
    clients_waiting_step = 0
    clerks_waiting_day = 0
    clients_waiting_day = 0
    clients_in_hour = 0
    line = 0
    clients_at_clerks_info = []
    max_len_line = 0

    def __init__(self, pos_clerks ):

        self.const = forconst.ForConst()
        self.free_clerks = pos_clerks


    def made_stat(self, clerk ):
        if clerk != 0:
            self.stat_day = 'ПОТЕРЯНО КЛИЕНТОВ: ' + str(self.client_lost)
            self.stat_day += '\nВЫРУЧКА: ' + str(self.revenue)
            self.stat_day += '\nЗАРПЛАТЫ КЛЕРКОВ: ' + str(self.clerks_salary)
            self.stat_day += '\nЧИСТАЯ ВЫРУЧКА: ' + str(self.revenue-self.clerks_salary)
            self.stat_day += '\nКЛИЕНТОВ ОБРАБОТАНО: ' + str(self.clients)
            self.stat_day += '\nСУММАРНОЕ ВРЕМЯ ПРОСТОЯ КЛЕРКОВ: ' + str(self.clerks_waiting_day)
            self.stat_day += '\nСРЕДНЕЕ ВРЕМЯ ОЖИДАНИЯ КЛИЕНТА\n\tЗА ПРОШЛЫЙ ЧАС: ' + str(self.clients_waiting_day)

            self.stat_week = 'ПОТЕРЯНО КЛИЕНТОВ: ' + str(self.client_lost_week)
            self.stat_week += '\nВЫРУЧКА БАНКА: ' + str(self.revenue_week)
            self.stat_week += '\nЗАРПЛАТЫ КЛЕРКОВ: ' + str(self.clerks_salary_week)
            self.stat_week += '\nЧИСТАЯ ВЫРУЧКА: ' + str(self.revenue_week-self.clerks_salary_week)
            self.stat_week += '\nКЛИЕНТОВ ОБРАБОТАНО: ' + str(self.clients_week)
            self.stat_week += '\nСУММАРНОЕ ВРЕМЯ ПРОСТОЯ КЛЕРКОВ: ' + str(self.clerks_waiting)
            self.stat_week += '\nСРЕДНЕЕ ВРЕМЯ ОЖИДАНИЯ КЛИЕНТА\n\tЗА ПРОШЛЫЙ ДЕНЬ: ' + str(self.clients_waiting)
            self.stat_week += '\nСРЕДНЕЕ ВРЕМЯ ОЖИДАНИЯ КЛИЕНТА\n\tЗА ВСЮ НЕДЕЛЮ: ' + str(self.clients_waiting_week)

        else:
            self.stat_day = ''
            self.stat_week = ''

    def made_stat_when_week_end(self):
        self.clients_waiting_week = self.clients_waiting_week_step // 6
        self.stat_week = 'ПОТЕРЯНО КЛИЕНТОВ: ' + str(self.client_lost_week)
        self.stat_week += '\nВЫРУЧКА БАНКА: ' + str(self.revenue_week)
        self.stat_week += '\nЗАРПЛАТЫ КЛЕРКОВ: ' + str(self.clerks_salary_week)
        self.stat_week += '\nЧИСТАЯ ВЫРУЧКА: ' + str(self.revenue_week-self.clerks_salary_week)
        self.stat_week += '\nКЛИЕНТОВ ОБРАБОТАНО: ' + str(self.clients_week)
        self.stat_week += '\nСУММАРНОЕ ВРЕМЯ ПРОСТОЯ КЛЕРКОВ: ' + str(self.clerks_waiting)
        self.stat_week += '\nСРЕДНЕЕ ВРЕМЯ ОЖИДАНИЯ КЛИЕНТА\n\tЗА ПРОШЛЫЙ ДЕНЬ: ' + str(self.clients_waiting)
        self.stat_week += '\nСРЕДНЕЕ ВРЕМЯ ОЖИДАНИЯ КЛИЕНТА\n\tЗА ВСЮ НЕДЕЛЮ: ' + str(self.clients_waiting_week)


    def day_is_over(self, line, minute, clerk):
        self.client_lost += line
        self.client_lost_week += line
        if minute == 0:
            self.clerks_salary += clerk * self.const.SALARY
            self.clerks_salary_week += clerk * self.const.SALARY
                
        self.revenue = 0
        self.client_lost = 0
        self.clients = 0
        self.clients_hour = 0
        self.clerks_salary = 0
        self.clerks_waiting_day = 0
        self.clients_waiting_day = 0

    def delete_clients(self):
        for i in range(len(self.clients_at_clerks_info)):
            self.client_lost += 1
            self.client_lost_week += 1
            self.clients_at_clerks_info[i]['time_before_clerks_free'] = 0


    def clients_wait(self, line):
        if self.clients_in_hour != 0:
            self.clients_waiting_day = line // (self.clients_in_hour/60)
            self.clients_waiting_step += self.clients_waiting_day
        else:
            self.clients_waiting_day = 0    
        self.clients_in_hour = 0  


    def give_pos_free_clerks(self):
        if self.free_clerks != []:
            return self.free_clerks[0]
        else:
            return 0


    def make_time(self, time):
        self.minute = time % self.const.LEN_MIN
        self.hour = (time//self.const.LEN_MIN) % self.const.LEN_HOUR

        if (time//self.const.LEN_MIN)//self.const.LEN_HOUR < self.const.LEN_WEEK:
            index = (time//self.const.LEN_MIN) // self.const.LEN_HOUR
            self.day = self.const.WEEK[index]
            self.day_num = (time//self.const.LEN_MIN) // self.const.LEN_HOUR
        else:
            index = ((time//self.const.LEN_MIN) // self.const.LEN_HOUR) % self.const.LEN_WEEK
            self.day = self.const.WEEK[index]
            self.day_num = ((time//self.const.LEN_MIN) // self.const.LEN_HOUR) % self.const.LEN_WEEK

            if ((time//self.const.LEN_MIN)//self.const.LEN_HOUR) // self.const.LEN_WEEK > self.weeks-1:
                self.weeks += 1



    def clients_processing(self, world):
        #bank.clients_at_clerks_info[i]
        #[0] - pos clerk with client i
        #[1] - time before clerk free from client i
        #[2] - id client i
        #[3] - revenue from client i
        del_num = 0
        #time tracking of clients staying with clerks
        for num in range(len(self.clients_at_clerks_info)):
                
            self.clients_at_clerks_info[num-del_num]['time_before_clerks_free'] -= 1
            #if the work with the client is over
            #drawing his departure and freeing the clerk
            if self.clients_at_clerks_info[num-del_num]['time_before_clerks_free'] <= 0:
                del_num += 1
                world.interface.canvas_up.delete(self.clients_at_clerks_info[num-del_num]['id_client'])
                self.revenue += self.clients_at_clerks_info[num-del_num]['revenue']
                self.revenue_week += self.clients_at_clerks_info[num-del_num]['revenue']
                self.free_clerks.append(self.clients_at_clerks_info[num-del_num]['pos_clerk'])
                del(self.clients_at_clerks_info[num-del_num])



    def work(self, time , world):
        self.make_time(time)
        #bank work on a short day
        if self.day == self.const.SHORT_WORK_DAY and self.hour == self.const.END_SHORT_DAY:
            self.clients_waiting = self.clients_waiting_step//self.const.LEN_SHORT_WORK_DAY
            self.day_is_over(self.line, self.minute, self.clerk)
            self.line = 0
            self.delete_clients()
        #bank work on a normal day
        elif self.hour == self.const.END_WORK_DAY:
            self.clients_waiting = self.clients_waiting_step//self.const.LEN_WORK_DAY
            self.day_is_over(self.line, self.minute, self.clerk)
            self.line = 0
            self.delete_clients()


        self.clients_processing(world)
        
        #summing up the day
        if self.hour == 0 :
            world.last_hour = 0
            self.clerks_salary = 0
            if self.day_num != self.const.NOT_WORK_DAY_NUM:
                self.clients_waiting_step = 0

        #if there is a queue
        if self.line > 0:
            pos_free_clerks = self.give_pos_free_clerks()
            #if there is a free clerk
            if pos_free_clerks != 0:
                self.line -= 1
                del(self.free_clerks[0])

                objects = dict()
                objects['pos_clerk'] = pos_free_clerks
                objects['time_before_clerks_free'] = self.time_before_free_clerks()
                objects['id_client'] = world.interface.canvas_up.create_oval(pos_free_clerks-world.lenth_client,
                                                                55,pos_free_clerks+world.lenth_client,
                                                                55+world.lenth_client*2, 
                                                                fill='green')
                objects['revenue'] = self.revenue_one_client()

                self.clients_at_clerks_info.append(objects)

        



    def add_clients(self):
        self.clients += 1
        self.clients_in_hour += 1
        self.clients_week += 1


    def lost_clients(self):
        self.client_lost += 1
        self.client_lost_week += 1


    def work_day_clerks_stat(self):
        #if working hours
        if (self.hour >= self.const.START_WORK_DAY 
            and self.hour < self.const.END_WORK_DAY 
            and not(self.day == self.const.SHORT_WORK_DAY 
            and self.hour >= self.const.END_SHORT_DAY) 
            and not(self.day == self.const.NOT_WORK_DAY) 
            and self.free_clerks != []):
        
            self.clerks_waiting += len(self.free_clerks)
            self.clerks_waiting_day += len(self.free_clerks)


    def time_before_free_clerks(self):
        return abs(random.randint(2,30))


    def revenue_one_client(self):
        return abs(random.randint(50,3000)) 

    def restart(self):
        self.free_clerks = []
        self.clerks_salary = 0
        self.clerks_salary_week = 0
        self.clerks_waiting = 0 
        self.clients_waiting = 0
        self.clerks_waiting_day = 0
        self.clients_waiting_day = 0
        self.clients_in_hour = 0
        self.revenue = 0
        self.client_lost = 0
        self.clients = 0
        self.revenue_week = 0
        self.client_lost_week = 0
        self.clients_week = 0 
        self.stat_day = ''
        self.stat_week = ''
        self.clerks_salary = 0
        self.clerks_salary_week = 0
        self.clerks_waiting = 0
        self.clients_waiting = 0
        self.clients_waiting_week = 0
        self.clients_waiting_week_step = 0
        self.clients_waiting_step = 0
        self.clerks_waiting_day = 0
        self.clients_waiting_day = 0
        self.clients_in_hour = 0
        self.line = 0
        self.max_len_line = 0
        self.clerk = 0
        self.clients_at_clerks_info = []

