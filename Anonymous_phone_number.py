#!/usr/bin/env python
# -*- encoding:utf8 -*-

import requests
import re
import time
import random

def formOutput():
	'''
	格式输出
	'''
	print 'Count\tPhone_Number\t\tUse_of_Time'
	form = '%s\t\t%s\t\t\t%s'
	return form

def getInfo():
	'''
	访问资源，提取关键信息
	'''
	count = 1
	nums = {}
	for page in xrange(4):
		url = 'https://www.pdflibr.com/?page='+str(page+1)
		res = requests.get(url)
		pat = re.compile('<h3>.*?</h3>[\s\S]*?href=".*?"')
		#pat_info = re.compile('<h3>(.*?)</h3>[\s\S]*?(<b>|)(.*?)(</b>||)[\s\S]*?href="(.*?)"')
		num = pat.findall(res.text)
		for i in num:
			phone_number = re.search('<h3>(.*?)</h3>',i).group(1)
			try:
				number_of_use = re.search("<p>.*?<b>(.*?)</b>",i).group(1)
			except:
				number_of_use = ''
			page_num = re.search('href="(.*?)"',i).group(1)
			nums[str(count)] = [phone_number,number_of_use,page_num]
			count += 1
	time.sleep(random.randint(0,3))
	return count,nums

def chosePhone(nums,c):
	'''
	选择手机号，获取验证码
	'''
	url2 = 'https://www.pdflibr.com/'+nums[str(c)][2]
	res2 = requests.get(url2)
	pat2 = '<tr>\s*<td>1</td>\s*<td>\s([*\d]*)\s</td>\s*<td>\s(.*?)\s</td>\s*<td>\s*<time>(.*?)</time>\s*</td>\s*</tr>'
	for i in xrange(3):
		print re.search(pat2,res2.text).group(i+1)
	yon = raw_input('is there your code ?(y or n)')
	while(yon == 'n'):
		chosePhone()
		yon = raw_input('is there your code ?(y or n)')

def main():
	count,nums = getInfo()
	form = formOutput()
	for i in xrange(1,count):
		#print nums
		print form%(str(i),nums[str(i)][0],nums[str(i)][1])
	c = raw_input('Plz input a num: ')
	chosePhone(nums,c)

if __name__ == '__main__':
	main()