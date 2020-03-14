from tkinter import *
import time
import random

import forconst

class Interface:

	def __init__(self):

		self.const=forconst.ForConst()
		self.master = Tk()
		self.master.title("Моделирование обслуживания в филиале банка")
		self.master.geometry("1710x825")

		self.canvas_len=self.const.WIDTH-self.const.WIDTH/4

		self.canvas_up = Canvas(self.master, 
								width=self.const.WIDTH-self.const.WIDTH/4, 
								height=self.const.HEIGHT/2, bg="#FFDAB9")
		self.canvas_up.grid(row=0, column=41, 
							rowspan=40, columnspan=120)

		self.canvas_down = Canvas(self.master, 
									width=self.const.WIDTH-self.const.WIDTH/4, 
									height=self.const.HEIGHT/2, bg="#FFFACD")
		self.canvas_down.grid(row=41, column=41, 
								rowspan=40, 
								columnspan=120)

		self.stat = Label(width=150, height=1, 
						text='СТАТИСТИКА',
						bg='white', 
						font='Times 12', 
						fg='black', bd=1)
		self.stat.grid(row=40, column=41, 
						rowspan=1, 
						columnspan=120)
		
		self.param= Label(width=50, height=2,  
						text='ПАРАМЕТРЫ',
						font='Times 15', 
						bg='white', fg='black', 
						bd=1)
		self.param.grid(row=0, column=0, 
						rowspan=2, 
						columnspan=40)
		
		self.fon = Label(width=1, 
						height=48, 
						bg='grey')
		self.fon.grid(row=0, column=40, 
						columnspan=1, 
						rowspan=81)
		
		self.l_entry1=Label(width=30, height=1,  text='КОЛИЧЕСТВО КЛЕРКОВ',
							font='Times', bg='#87CEFA', 
							fg='black', bd=1)
		self.l_entry1.grid(row=76, column=0, columnspan=8)
		
		self.clerk= Scale(self.master,orient=HORIZONTAL ,length=200,
							font='Times',from_=2,to=7,
							tickinterval=1,resolution=1)
		self.clerk.grid(row=77, column=0, columnspan=6)
		
		self.l_entry2=Label(width=40, height=1,  
							text='МАКСИМАЛЬНАЯ ДЛИНА ОЧЕРЕДИ', 
							font='Times',bg='#87CEFA', 
							fg='black', bd=1)
		self.l_entry2.grid(row=79, column=0, columnspan=12)
		
		self.max_line = Scale(self.master,orient=HORIZONTAL,
							length=400,font='Times',
							from_=10,to=25,tickinterval=1,
							resolution=1)
		self.max_line.grid(row=80, column=0, columnspan=18)
		
		self.l_speed=Label(width=20, height=1,  
							text='СКОРОСТЬ ПОКАЗА', 
							font='Times',bg='#87CEFA', 
							fg='black', bd=1)
		self.l_speed.grid(row=17, column=2, columnspan=30)
		
		self.speed = Scale(self.master,orient=HORIZONTAL,
							length=400,font='Times',
							from_=0,to=100,resolution=10, 
							showvalue=False)
		self.speed.grid(row=18, column=2, columnspan=30)

		self.text_max = Label(width=10, height=1,
							font='Times 12', 
							text='max')
		self.text_max.grid(row=19, column=1, columnspan=3)

		self.text_min = Label(width=10, height=1,
							font='Times 12', 
							text='min')
		self.text_min.grid(row=19, column=30, columnspan=3)

		self.l_step=Label(width=40, height=1,  
							text='ЧАСТОТА ПРИХОДА КЛИЕНТОВ', 
							font='Times',bg='#87CEFA', 
							fg='black', bd=1)
		self.l_step.grid(row=30, column=1, columnspan=40)
		
		self.new_client_time_coef = Scale(self.master,orient=HORIZONTAL,
							length=400,font='Times',
							from_=1,to=10,resolution=1,
							showvalue=False)
		self.new_client_time_coef.grid(row=35, column=2, columnspan=30)

		self.text_max2 = Label(width=10, height=1,
							font='Times 12', 
							text='max')
		self.text_max2.grid(row=36, column=1, columnspan=3)

		self.text_min2 = Label(width=10, height=1,
							font='Times 12', 
							text='min')
		self.text_min2.grid(row=36, column=30, columnspan=3)

		self.label = Label(width=30, height=7,
							font='Times 15', 
							bg="#AFEEEE")
		self.label.grid(row=5, column=2 , columnspan=30, rowspan=5)



		self.id_for_update_stat_day_last=0
		self.id_for_update_stat_week_last=0
		self.id_for_update_line_last=0


	def print_stat(self, stat_day, stat_week, line):
		self.id_for_update_stat_day=self.canvas_down.create_text(270, 190, fill='black', 
															text=stat_day,
															font='Times 13')

		self.id_for_update_stat_week=self.canvas_down.create_text(800, 210, fill='black', 
															text=stat_week,
															font='Times 13')

		self.id_for_update_line=self.canvas_up.create_text(550, 250, fill='black', 
															text='ДЛИНА ОЧЕРЕДИ\n\t'+str(line),
															font='Times 16')

	def update_statistics(self):
		self.canvas_down.delete(self.id_for_update_stat_day_last)
		self.canvas_down.delete(self.id_for_update_stat_week_last)
		self.canvas_up.delete(self.id_for_update_line_last)

		self.id_for_update_stat_day_last=self.id_for_update_stat_day
		self.id_for_update_stat_week_last=self.id_for_update_stat_week
		self.id_for_update_line_last=self.id_for_update_line


	def update_statistics_end_week(self, stat_week):
		self.id_for_update_stat_week=self.canvas_down.create_text(800, 210, fill='black', 
																			text=stat_week,
																			font='Times 13')
		self.canvas_down.delete(self.id_for_update_stat_week_last)
		self.id_for_update_stat_week_last=self.id_for_update_stat_week
