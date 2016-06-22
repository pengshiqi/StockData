# -*- coding: UTF-8 -*-

import requests
import sqlite3
from bs4 import BeautifulSoup
from flask import Blueprint, render_template,request

stock = Blueprint('stock', __name__, template_folder = '../templates')

@stock.route('/stock', methods = ['GET', 'POST'])
def StockState():
	if request.method == 'GET':
		return render_template('stock.html')
	elif request.method == 'POST':
		code = request.form['code']
		url = "https://finance.yahoo.com/q/hp?s=" + "%" + "5E%s+Historical+Prices" % code
		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')
		TableData = soup.select('table.yfnc_datamodoutline1 > tr > td > table > tr')
		DataList = []
		row = 0
		context0 = '<tr>\n' + '<td>Date</td> <td>Open</td> <td>High</td> <td>Low</td> <td>Close</td> <td>Volume</td> <td>AdjClose</td>\n' + '</tr>'

		for RowData in TableData:
			DataList.append([])
			data = RowData.select('td.yfnc_tabledata1')
			for a in data:
				DataList[row].append(a.get_text(strip = True))
			row = row + 1

		#print DataList

		cx = sqlite3.connect('Data_%s.db' % code)
		cu = cx.cursor()
		cu.execute("create table Data%s (Date text primary key, Open real, High real, Low real,  Close real, Volume integer, AdjClose real)" % code)
		for i in range(1, row - 1):
			t = DataList[i]
			Tuple = (t[0], t[1], t[2], t[3], t[4], t[5], t[6])
			cx.execute("insert into Data%s values(?, ?, ?, ?, ?, ?, ?)" % code, Tuple)
			context0 = context0 + '<tr>\n' + '<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>\n' % Tuple + '</tr>\n'  
		cx.commit()


		context = '<table align = "center" width = "85%" border = "1">\n' + '<tbody>\n'+ context0 + '</tbody>\n' + '</table>'

		#print context
		file = open('./templates/table.html', 'w')
		file.write(context)
		file.close()

		return render_template('table.html')



