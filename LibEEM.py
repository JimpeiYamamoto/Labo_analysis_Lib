import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

def eem_file_to_df(file_path):
	'''
	filepathから読み込んでDataFrameに変換して返す
	'''
	df = pd.read_csv(file_path)
	df = df.rename(columns={df.columns.values[1]:'EX/EM'})
	df = df.iloc[16:]
	df['EX'] = df['EX/EM'].str.split('/', expand=True)[0]
	df['EM'] = df['EX/EM'].str.split('/', expand=True)[1]
	df = df.iloc[:, 2:]
	df = df.astype(float)
	return (df)

def show_eem_graph(df, span_set=False, max_=10, min_=-10):
	'''
	EEM_DataFrameを可視化する
	強度の範囲を設定する場合はspan_set=True
	'''
	for value in df.columns.values:
		if (value != 'EM') & (value != 'EX'):
			df_pivot = pd.pivot_table(data=df, values=value, columns='EM', index='EX')
			plt.figure(figsize=(12, 7))
			if (span_set == True):    
				plt.imshow(df_pivot, extent=[df['EM'].min(),df['EM'].max(),df['EX'].min(),df['EX'].max()], vmin=min_, vmax=max_, origin='lower')
			else:
				plt.imshow(df_pivot, extent=[df['EM'].min(),df['EM'].max(),df['EX'].min(),df['EX'].max()])
			plt.colorbar().ax.tick_params(labelsize=15)
			plt.xlabel("EM(nm)", fontsize=18)
			plt.ylabel("EX(nm)", fontsize=18)
			plt.title(value, fontsize=18)
			plt.tick_params(labelsize=18)
			print(value)
			plt.show()

def show_calibration_curve(df, ex, em, dic):
	'''
	dic=[濃度:濃度]
	'''
	info = df[(df['EX'] == ex) & (df['EM'] == em)]
	x_lst = []
	y_lst = []
	for key in dic:
		y_lst.append(dic[key])
		x_lst.append(info[key].iloc[0])
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.xlabel("Data", fontsize=15)
	plt.ylabel("NADH(nM)", fontsize=15)
	plt.tick_params(labelsize=12)
	ax.grid(True)
	ax.scatter(x_lst, y_lst, s=20)
	ab = np.polyfit(x_lst, y_lst, 1)
	y = np.poly1d(ab)(x_lst)
	plt.plot(x_lst, y)
	plt.title("EX="+str(ex)+",EM="+str(em), fontsize=18)
	print("y={0:.3f}x+{1:.3f}".format(ab[0], ab[1]))
	print("R^2={0:.5f}".format(np.corrcoef(x_lst, y_lst)[0][1]))
	plt.show()
	return (np.std(x_lst))

def time_eem_file_to_df(path):
	'''
	時間変化測定の結果のfilepathからDataFrameに変換して返す
	'''
	eem_time_df = pd.read_csv(path,encoding="shift-jis")
	i = 0
	while (eem_time_df[eem_time_df.columns.values[0]][i] != 's'):
		i += 1
	time_df = eem_time_df.copy().iloc[i + 1:]
	time_df = time_df.rename(columns={time_df.columns.values[0]:'s'})
	time_df = time_df.rename(columns={time_df.columns.values[1]:'Data'})
	time_df[time_df.columns.values[0]] = time_df[time_df.columns.values[0]].astype(float)
	time_df[time_df.columns.values[1]] = time_df[time_df.columns.values[1]].astype(float)
	df = pd.DataFrame()
	df['s'] = time_df['s']
	df['Data'] = time_df['Data']
	df = df.reset_index(drop=True)
	return (df)

def time_plt(df):
	'''
	時間変化測定のDataFrameを可視化
	'''
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_xlabel('time')
	ax.set_ylabel('Data')
	ax.grid(True)
	ax.scatter(df[df.columns.values[0]], df[df.columns.values[1]], s=3)
	plt.show()

def all_csv_to_many_txt(eem_path, save_path):
	'''
	EEM連続測定の結果が全てある.csvファイルから、測定毎の.txtファイルに変換する
	(3D Spectalyzeに使用可能なフォーマットに変換する)
	eem_path:.csv
	save_path:.txtファイルの保存先のフォルダ
	'''
	df1_1 = pd.read_csv(eem_path)
	f = open('./Labo_analysis_Lib/eem_example_file/1_-03(FD3).TXT', 'r')
	data = f.read()
	lines = data.split('\n')
	hituyo_line = lines[:49]
	for name in df1_1.columns.values:
		df_pivot = pd.pivot_table(data=df1_1, values=name, columns='EX', index='EM')
		df_pivot.to_csv('./Labo_analysis_Lib/tmp/'+name+'.txt')
		time.sleep(1)
		f2 = open('./Labo_analysis_Lib/tmp/'+name+'.txt', 'r')
		data2 = f2.read()
		data2_2 = data2.replace(',', '\t')
		data2_3 = data2_2.replace('EM', '')
		hituyo_  = "\n".join(hituyo_line)
		all_ = hituyo_ + '\n' + data2_3
		f3 = open(save_path + name + '.txt', 'a')
		f3.write(all_)

def calc_mq_subtraction_df(df, mq_df, mq_colname):
	'''
	MQ引き算後のdfを作成する
	'''
	return_df = pd.DataFrame()
	for colum in df.columns.values:
		if (colum != 'EX') & (colum != 'EM'):
			return_df[colum] = df[colum] - mq_df[mq_colname]
	return_df['EX'] = df['EX']
	return_df['EM'] = df['EM']
	return (return_df);	

def calcu_std(df, ex, em):
	'''
	任意のex/emの標準偏差を算出して返す
	'''
	info = df[(df['EX'] == ex) & (df['EM'] == em)]
	kyodo_lst = []
	colum_lst = df.columns.values
	for name in colum_lst:
		if (name != 'EX') & (name != 'EM'):
			kyodo_lst.append(info[name].iloc[0])
	return (np.std(kyodo_lst))

def	get_std_df(df):
	'''
	標準偏差等高線図用のdfを作成する
	'''
	std_lst = []
	for index in range(df.shape[0]):
		ex = df['EX'].iloc[index]
		em = df['EM'].iloc[index]
		std_lst.append(calcu_std(df, ex, em))
	df['STD'] = std_lst
	return (df)

def show_time_intensity(df, ex, em, max_, min_):
	'''
	任意のex/emの蛍光強度の変化を可視化する
	'''
	info = df[(df['EX'] == ex) & (df['EM'] == em)]
	x_lst = []
	y_lst = []
	y = 0
	print("ex=", ex)
	print("em=", em)
	colum_lst = df.columns.values
	for name in colum_lst:
		if (name != 'EX') & (name != 'EM'):
			x_lst.append(info[name].iloc[0])
			y_lst.append(y)
			y += 1
	print("std=", np.std(x_lst))
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.rcParams["font.size"] = 16
	ax.set_xlabel('time')
	ax.set_ylabel('Fluorescence intensity(a.u)')
	plt.ylim(min_, max_)
	plt.plot(y_lst, x_lst)
	plt.show()
	return_df = pd.DataFrame()
	return_df['time'] = y_lst
	return_df['au'] = x_lst
	return (return_df)