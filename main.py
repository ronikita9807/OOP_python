from tkinter import *
import time
import random

import forconst
import bankbranch
import externalworld
import interface

def main():
    root = Tk()
    root.overrideredirect(False)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.focus_set()
    root.bind("<Escape>", lambda e: e.widget.quit())


    world = externalworld.ExternalWorld(root)

    def refresher():
        if world.start_flag == 1:

            world.speed = int( world.interface.speed.get())+2

            world.tick()

            end_week = world.const.LEN_WEEK*world.const.LEN_HOUR*world.const.LEN_MIN

            if world.time < end_week and not(world.restart_flag):

                world.bank.made_stat(world.bank.clerk)

                world.interface.print_stat(world.bank.stat_day, world.bank.stat_week, world.bank.line)

                world.bank.work(world.time, world)

                #if it’s the right time to generate a new client
                if (world.time_befor_new_client-1 <= 0 
                    and world.hour >= world.const.START_WORK_DAY 
                    and world.hour < world.const.END_WORK_DAY 
                    and not(world.day == world.const.SHORT_WORK_DAY 
                    and world.hour >= world.const.END_SHORT_DAY)   
                    and not(world.day == world.const.NOT_WORK_DAY)) :
                
                
                    world.coef = world.what_is_coef_speed_time()
                    world.time_befor_new_client = abs(random.randint(0,10)) * world.coef * (int( world.interface.new_client_time_coef.get())/3)
                    #queue length does not exceed the maximum
                    if world.bank.line < world.bank.max_len_line:
                        world.bank.line += 1
                        world.bank.add_clients()
                    #losing customers
                    else:
                        world.bank.lost_clients()

                #reduce the time before a new client
                else:
                    world.time_befor_new_client -= 1

                #updated statistics
                world.interface.update_statistics()

                #if working hours  
                world.bank.work_day_clerks_stat()

                
                #change last hour
                if world.last_hour < world.hour:
                    world.last_hour = world.hour
                    world.bank.clients_wait(world.bank.line)
                
                #change last day num
                if world.last_day_num < world.day_num:
                    world.last_day_num = world.day_num 
                    world.bank.clients_waiting_week_step += world.bank.clients_waiting

                world.interface.label.configure(text = world.format_time_text())



            # when week end
            else: 
                #if you did not press the restart key
                world.start_flag = 0
                if not(world.restart_flag):
                    world.bank.made_stat_when_week_end()

                    world.interface.update_statistics_end_week(world.bank.stat_week)
    

            
        root.after(world.speed, refresher)


    refresher()

    root.mainloop()


if __name__ == "__main__":
    main()