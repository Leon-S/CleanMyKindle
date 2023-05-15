#!/usr/bin/python
# -*- coding:utf-8 -*-

# http://zetcode.com/gui/tkinter/dialogs/

# 引入Tkinter
from tkinter import *
import os, sys, glob, shutil, datetime, re, codecs, webbrowser, importlib, sys
import tkinter.font as tkFont
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox

#fix ''ascii' codec can't decode byte 0xe8 in position ...'
importlib.reload(sys)

# 定义窗口框架
class CF(Frame) :
	# 创建类定义
	def __init__(self, parent) :
		Frame.__init__(self, parent) #窗口背景
		self.parent = parent #定义父窗体
		self.initUI() #应用软件UI
	#窗口位置居中
	def centerWindow(self) :
		w = 480 #窗口宽度
		h = 200 #窗口高度
		sw = self.parent.winfo_screenwidth() #屏幕宽度
		sh = self.parent.winfo_screenheight() #屏幕高度
		x = (sw - w)/2 #屏幕宽度减去窗口宽度除以二
		y = (sh - h)/2 #屏幕高度减去窗口高度除以二
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y)) #使用geometry()方法使窗口居中
		self.parent.resizable(False, False) #禁止改变窗体大小
	#窗口元素
	def initUI(self) :
		self.centerWindow() #应用窗口居中
		self.parent.title('Clean My Kindle（Kindle SDR 文件夹清理器） v1.0') #窗口标题
		self.pack(fill=BOTH, expand=YES, padx=30, pady=15) #pack方法

		#设置控件自适应
		#self.rowconfigure( 1, weight = 1 )
		#self.columnconfigure( 1, weight = 1 )

		#默认文件路径
		self.filePath = '/Volumes/Kindle' #Mac 下默认 Kindle 路径
		self.filePathVer = os.path.exists(self.filePath) #检测文件是否存在

		#标签
		self.label = Label(self, text='指定 Kindle 磁盘路径：')
		self.label.grid(row=0, column=0, pady=10, sticky=W)
		#路径输入框
		self.entry = Entry(self, width=39)
		self.entry.grid(row=1, column=0)

		#文件路径选择按钮
		def btnSlectTxt() :
			entryVer = os.path.exists(self.filePath)
			return '重选' if entryVer else '选择' #为真时的结果 if 判定条件 else 为假时的结果  
		self.btnSelect = Button(self, text=btnSlectTxt(), command=self.onSelect)
		self.btnSelect.grid(row=1, column=1)

		#立即清理按钮
		btn = Button(self, text='立即清理', command=self.onProcess)
		btn.grid(row=2, column=0, pady=20, columnspan=2, sticky=S)

		#生成日志复选框
		self.var = IntVar()
		ckbtn = Checkbutton(self, text='在 Kindle 根目录生成清理日志', variable=self.var)
		ckbtn.grid(row=3, column=0, columnspan=2, padx=100, sticky=W)

		#清理截图复选框
		self.var2 = IntVar()
		ckbtn = Checkbutton(self, text='清理截图', variable=self.var2)
		ckbtn.grid(row=3, column=0, columnspan=2, sticky=W)


		#菜单
		menubar = Menu(self.parent)
		self.parent.config(menu=menubar)
		fileMenu = Menu(menubar)
		menubar.add_cascade(label='帮助', menu=fileMenu)
		fileMenu.add_command(label='关于', command=self.aboutInfo)

		#判断文件路径
		if( self.filePathVer ) :
			self.entry.insert(END, self.filePath) #存在显示
		else:
			self.entry.insert(END, u'未检测到 Kindle 磁盘，请手动选择') #不存在显示



	def onSelect(self) :
		#调用打开对话框
		self.filePath = tkFileDialog.askdirectory(title='请选择 Kindle 磁盘...')
		#如果确认选择
		if self.filePath :
			self.entry.delete(0,END) #清空路径
			self.entry.insert(END, self.filePath) #填入路径
			if self.btnSelect['text'] != u'重选' :
				self.btnSelect['text'] = u'重选'

	#导入文件
	def onProcess(self) :
		#路径赋值
		kindlePath = self.entry.get()
		documentsPath = kindlePath + '/documents'
		checkDocumentsPathVer = os.path.exists(documentsPath)

		#检查路径
		if checkDocumentsPathVer == False :
			self.checkAlert()
		else :
			list_dirs = os.walk(documentsPath)
			root_dirs = os.listdir(kindlePath)

			sdr_list_s = ''
			sdr_list_f = ''
			dir_list_s = ''
			dir_list_f = ''
			scs_list = ''

			sdr_s_count = 0
			sdr_f_count = 0
			dir_s_count = 0
			dir_f_count = 0
			shot_count = 0

			clean = False

			if self.var2.get() == 1 :
				#清理截图
				for files in root_dirs:
					if ( files[:10] == 'screenshot' and files[-4:] == '.png' ) or ( files[:18] == 'wininfo_screenshot' and files[-4:] == '.txt'):
						os.chdir(kindlePath)
						os.remove(files)
						#仅统计图片
						if files[:10] == 'screenshot' and files[-4:] == '.png':
							scs_list += u'\u25cf ' + files +'\n'
							shot_count += 1
							clean = True

			# 如果输入正确执行查找
			for root, dirs, files in list_dirs:
				for numb in dirs:
					if numb:
						os.chdir(root)
						
						# 遍历所有文件名和文件夹名
						sdr = glob.glob(r'*.sdr')
						_dir = glob.glob(r'*.dir')
						azw = glob.glob(r'*.azw')
						azw3 = glob.glob(r'*.azw3')
						pdf = glob.glob(r'*.pdf')
						txt = glob.glob(r'*.txt')
						prc = glob.glob(r'*.prc')
						mobi = glob.glob(r'*.mobi')
						pobi = glob.glob(r'*.pobi')
						epub = glob.glob(r'*.epub')
						azw4 = glob.glob(r'*.azw4')
						kfx = glob.glob(r'*.kfx')

						format_sdr = False
						format_dir = False

						# 判断 SDR 文件夹是否存在
						for unsdr in sdr:
							if unsdr[-4:] == '.sdr':
								format_sdr = True
								break
							
						for undir in _dir:
							if undir[-4:] == '.dir':
								format_dir = True
								break

						# 如果 SDR 文件夹存在判断 SDR 文件夹是否和遍历出的文件对应
						# KPW 系列 SDR 文件夹
						if format_sdr == True:

							for unsdr in sdr:
								# 定义所在文件夹的路径
								sdr_self = os.path.dirname(os.path.abspath('__file__'))

								# 如果当前文件夹和它的父文件夹的后缀相同就放弃重新循环
								if unsdr[-4:] == sdr_self[-4:]:
									continue

								found = False
								# azw ebook name
								for n1 in azw:
									if unsdr[:-4] == n1[:-4]:
										found = True
										break
								# azw3 ebook name
								for n2 in azw3:
									if unsdr[:-4] == n2[:-5]:
										found = True
										break
								# pdf ebook name
								for n3 in pdf:
									if unsdr[:-4] == n3[:-4]:
										found = True
										break
								# txt ebook name
								for n4 in txt:
									if unsdr[:-4] == n4[:-4]:
										found = True
										break
								# prc ebook name
								for n5 in prc:
									if unsdr[:-4] == n5[:-4]:
										found = True
										break
								# mobi ebook name
								for n6 in mobi:
									if unsdr[:-4] == n6[:-5]:
										found = True
										break
								# pobi ebook name
								for n7 in pobi:
									if unsdr[:-4] == n7[:-5]:
										found = True
										break
								# epub ebook name
								for n8 in epub:
									if unsdr[:-4] == n8[:-5]:
										found = True
										break
								# kfx ebook name
								for n9 in kfx:
									if unsdr[:-4] == n9[:-4]:
										found = True
										break
								# azw4 ebook name
								for n10 in azw4:
									if unsdr[:-4] == n10[:-5]:
										found = True
										break
								# delete the empty dir
								if found == False:
									try:
										shutil.rmtree(unsdr)
									except OSError, (errno, strerror):
										sdr_f_count += 1
										sdr_list_f += u'\u25cf ' + unsdr +'\n'
									else:
										sdr_s_count += 1
										sdr_list_s += u'\u25cf ' + unsdr +'\n'
									clean = True
						
						# 如果 DIR 文件夹存在判断 DIR 文件夹是否和遍历出的文件对应
						# Kindle 4 系列 DIR文件夹
						if format_dir == True:

							for undir in _dir:

								dir_self = os.path.dirname(os.path.abspath('__file__'))

								if undir[-4:] == dir_self[-4:]:
									continue

								found = False
								# azw ebook name
								for n1 in azw:
									if undir[:-8] == n1[:-4]:
										found = True
										break
								# azw3 ebook name
								for n2 in azw3:
									if undir[:-9] == n2[:-5]:
										found = True
										break
								# pdf ebook name
								for n3 in pdf:
									if undir[:-8] == n3[:-4]:
										found = True
										break
								# txt ebook name
								for n4 in txt:
									if undir[:-8] == n4[:-4]:
										found = True
										break
								# prc ebook name
								for n5 in prc:
									if undir[:-8] == n5[:-4]:
										found = True
										break
								# mobi ebook name
								for n6 in mobi:
									if undir[:-9] == n6[:-5]:
										found = True
										break
								# pobi ebook name
								for n7 in pobi:
									if undir[:-9] == n7[:-5]:
										found = True
										break
								# epub ebook name
								for n8 in epub:
									if undir[:-9] == n8[:-5]:
										found = True
										break
								# kfx ebook name
								for n9 in kfx:
									if undir[:-8] == n9[:-4]:
										found = True
										break
								# azw4 ebook name
								for n10 in azw4:
									if undir[:-9] == n10[:-5]:
										found = True
										break
								# delete the empty dir
								if found == False:
									try:
										shutil.rmtree(undir)
									except OSError, (errno, strerror):
										dir_f_count += 1
										dir_list_f += u'\u25cf ' + undir +'\n'
									else:
										dir_s_count += 1
										dir_list_s += u'\u25cf ' + undir +'\n'
									clean = True
						break

			if clean == True:
				sdr_s_count_str = str(sdr_s_count) #计数
				sdr_f_count_str = str(sdr_f_count) #计数
				dir_s_count_str = str(dir_s_count) #计数
				dir_f_count_str = str(dir_f_count) #计数
				shot_count_str = str(shot_count) #计数
				#清理成功
				self.doneAlert(sdr_s_count_str,sdr_f_count_str,dir_s_count_str,dir_f_count_str,shot_count_str)
				#清理日志
				if self.var.get() == 1 :
					now = datetime.datetime.now()
					nowStyle = now.strftime('%Y-%m-%d %H:%M:%S')
					new_log = open(kindlePath + '/sdrCleaner_log.txt','w')
					new_log.write('清理时间 ' + nowStyle + '\n=================================\n')
					if sdr_list_s :
						new_log.write('共删除成功 ' + sdr_s_count_str +' 个无用 SDR 文件夹：\n---------------------------------\n')
						new_log.write(sdr_list_s)
						new_log.write('=================================\n')
					if sdr_list_f :
						new_log.write('有 ' + sdr_f_count_str + ' 个 SDR 文件夹没有删除成功：\n---------------------------------\n')
						new_log.write(sdr_list_f)
						new_log.write('=================================\n')
					if dir_list_s :
						new_log.write('共删除成功 ' + dir_s_count_str +' 个无用 DIR 文件夹：\n---------------------------------\n')
						new_log.write(dir_list_s)
						new_log.write('=================================\n')
					if dir_list_f :
						new_log.write('有 ' + dir_f_count_str + ' 个 DIR 文件夹没有删除成功：\n---------------------------------\n')
						new_log.write(dir_list_f)
						new_log.write('=================================\n')
					if sdr_list_f or dir_list_f :
						new_log.write('* 删除失败是因为该文件名中含有特殊字符无法被删除，目前还没找到好的办法解决，请暂时手动删除。\n')
						new_log.write('---------------------------------\n')
					if scs_list :
						new_log.write('共删除成功 ' + shot_count_str +' 个截图：\n---------------------------------\n')
						new_log.write(scs_list)
						new_log.write('=================================\n')
					new_log.write('Kindle  - 为精心阅读而生\n')
					new_log.close()
			else:
				#不需要清理
				self.noneAlert()

	def checkAlert(self) :
		tkMessageBox.showwarning(
			'提示',
			'请设置正确的 Kindle 磁盘路径！\r\n比如，你的 Kindle 磁盘名称为“Kindle”，则路径应该是：/Volumes/Kindle'
		)

	def noneAlert(self) :
		tkMessageBox.showwarning(
			'提示',
			'您的 Kindle 磁盘很干净，无需清理！'
		)

	def doneAlert(self,num1,num2,num3,num4,num5) :
		da1 = ''
		da2 = ''
		da3 = ''
		da4 = ''
		da5 = ''
		if num1 != '0':
			da1 = '\r\n清理成功：' + num1 + ' 个 SDR'
		if num2 != '0':
			da2 = '\r\n清理失败：' + num2 + ' 个 SDR'
		if num3 != '0':
			da3 = '\r\n清理成功：' + num3 + ' 个 DIR'
		if num4 != '0':
			da4 = '\r\n清理失败：' + num4 + ' 个 DIR'
		if num5 != '0':
			da5 = '\r\n清理成功：' + num5 + ' 个截图'
		tkMessageBox.showwarning(
			'提示',
			'搞定，已经帮您清理完毕！' + da1 + da2 + da3 + da4 + da5
		)

	def aboutInfo(self) :
		tkMessageBox.showinfo(
			'关于',
			'欢迎使用Kindle SDR 文件夹清理器。当您在 Kindle 中删除一本电子书后，会遗留下来与电子书同名的 SDR 文件夹，它的作用是用来记录所对应电子书的页码等信息，如果确认不再需要，可使用本工具进行清理，使用愉快。'
		)

	#退出程序
	def onExit(self) :
		self.quit()

#创建窗口主体
def main() :
	root = Tk() #创建Tkinter窗口
	#root.config(bg='red') #窗口背景色
	app = CF(root) #应用窗口框架
	root.mainloop()

if __name__ == '__main__' :
	main()