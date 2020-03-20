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
    clients_waiting_step = 0
    clerks_waiting_day = 0
    clients_waiting_day = 0
    clients_in_hour = 0

    def __init__(self, pos_clerks ):

        self.const = forconst.ForConst()
        self.free_clerks = pos_clerks


    def format_stat(self, clerk ):
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

    def format_stat_when_week_end(self):
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


    def add_clients(self):
        self.clients += 1
        self.clients_in_hour += 1
        self.clients_week += 1


    def lost_clients(self):
        self.client_lost += 1
        self.client_lost_week += 1


    def work_day_clerks_stat(self):
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


