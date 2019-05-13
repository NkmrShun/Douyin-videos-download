import tkinter
import shutil
import os
import requests
import time
import threading
import pyperclip


class Video(object):
	def __init__(self):

		self.root = tkinter.Tk()
		self.root.minsize = (600, 400)
		self.frame = tkinter.Frame(self.root)
		self.frame.pack()

		self.root.title("视频下载")

		var = tkinter.StringVar()
		self.location_button = tkinter.Button(self.root, command=self.settext, textvariable=var)

		self.start_button = tkinter.Button(self.frame, command=self.start, text="开始")
		self.stop_button = tkinter.Button(self.frame, command=self.stop, text="结束")


		self.display_info = tkinter.Listbox(self.root, width=50)

		self.size = []
		self.url = []

		self.notice_text = '正在搜索'

		if not os.path.exists('./videos'):os.makedirs('./videos')
		if not os.path.exists('./log'):os.makedirs('./log')
		if not os.path.exists('./temp'):os.makedirs('./temp')

		self.log_location = os.path.abspath('./log')

		var.set('点击复制：' + self.log_location)
		
		self.video_total = 0
		
		self.video_compeleted = 0
		
		self.started = False
		
		self.headers = {
					"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}

	def gui(self):
		self.start_button.pack(side=tkinter.LEFT)
		self.stop_button.pack(side=tkinter.RIGHT)
		self.display_info.pack()
		self.location_button.pack()

	def load_media(self,list):
		size = []
		for url in list:
			num = time.time() * 1000
			path = './videos/%d.mp4' % num
			try:
				pre_content_length = 0
				while True:
					headers = {
						"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}
					if os.path.exists(path):
						headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
					res = requests.get(url, stream=True, headers=headers)
					content_length = int(res.headers['content-length'])
					if content_length < pre_content_length or (
							os.path.exists(path) and os.path.getsize(path) == content_length):
						break
					pre_content_length = content_length
					with open(path, 'ab') as file:
						file.write(res.content)
						file.flush()
						self.video_compeleted += 1
						text = '(%d/%d)正在下载视频，下载量 : %d	  总大小:%d' % (self.video_total, self.video_compeleted, os.path.getsize(path), content_length)
						self.display_info.insert(0, text)
			except Exception as e:
				print(e)

		self.load_record()

	def load_record(self):
		log_path = './log/'
		temp_path = './temp/'
		temp_list = os.listdir(log_path)
		if len(temp_list) > 0:
			for temp in temp_list:
				shutil.move(log_path + temp, temp_path + temp)
		file_list = os.listdir(temp_path)
		if len(file_list) > 0:
			list=[]
			for txt in file_list:
				with open(temp_path + txt) as f:
					data = f.readlines()
					for line in data:
						line = line.strip()
						if (line not in list and line not in self.url):
							self.url.append(line)
							res = requests.get(line, stream=True, headers=self.headers)
							content_length = int(res.headers['content-length'])
							if(content_length not in self.size and content_length>10000):
								self.size.append(content_length)
								self.video_total += 1
								list.append(line)
							
				os.remove(temp_path + txt)
			
			self.load_media(list)
		else:
			text = self.display_info.get(0)
			if text == self.notice_text:
				text = self.display_info.delete(0)
				if self.notice_text == '正在搜索....':
					self.notice_text = '正在搜索'
				else:
					self.notice_text += '.'
			text = self.display_info.insert(0, self.notice_text)
			time.sleep(1)
			self.load_record()

	def stop(self):
		quit()

	def start(self):
		if not self.started:
			self.started = True
			self.display_info.insert(0, self.notice_text)
			th = threading.Thread(target=self.load_record)
			th.setDaemon(True)
			th.start()

	def settext(self):
		text = self.log_location + '\\'
		pyperclip.copy(text.replace('\\',"/"))


def main():
	video = Video()
	video.gui()
	tkinter.mainloop()
	pass

if __name__ == "__main__":
	main()