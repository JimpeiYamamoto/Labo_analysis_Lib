# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    LibCV.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: yjimpei <yjimpei@student.42tokyo.jp>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/02/01 19:19:40 by yjimpei           #+#    #+#              #
#    Updated: 2022/02/01 21:48:24 by yjimpei          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pandas as pd
import matplotlib.pyplot as plt

def show_cv_graph(df_name_lst):
	'''
	cvのfile名のリストを引数渡すと可視化される
	返り値はなし
	'''
	cv_df_lst = []
	for name in df_name_lst:
		df = pd.read_csv(name)
		i = 0
		while (df[df.columns.values[0]][i] != 'Potential/V'):
			i += 1
		j = 0
		while (('Init' in df[df.columns.values[0]][j]) == False):
			j += 1
		print('------' + name + '------')
		while (j < i):
			print(df[df.columns.values[0]][j])
			j += 1
		cv_df = df.copy().iloc[i + 1:]
		cv_df = cv_df.rename(columns={df.columns.values[0]:'Potential/V'})
		cv_df = cv_df.rename(columns={df.columns.values[1]:'Current/A'})
		cv_df[cv_df.columns.values[0]] = cv_df[cv_df.columns.values[0]].astype(float)
		cv_df[cv_df.columns.values[1]] = cv_df[cv_df.columns.values[1]].astype(float)
		cv_df_lst.append(cv_df)
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_xlabel('Potential/V')
	ax.set_ylabel('Current/A')
	i = 0
	for cv_df in cv_df_lst:
		ax.scatter(cv_df[cv_df.columns.values[0]], cv_df[cv_df.columns.values[1]], s=2, label=str(df_name_lst[i]))
		i += 1
	plt.rcParams["font.size"] = 16
	plt.show()


def cv_file_to_df(df_name):
	'''
	file_pathを引数としてcsvのデータをDataFrameに変換して返す
	'''
	df = pd.read_csv(df_name)
	i = 0
	while (df[df.columns.values[0]][i] != 'Potential/V'):
		i += 1
	j = 0
	while (('Init' in df[df.columns.values[0]][j]) == False):
		j += 1
	while (j < i):
		print(df[df.columns.values[0]][j])
		j += 1
	cv_df = df.copy().iloc[i + 1:]
	cv_df = cv_df.rename(columns={df.columns.values[0]:'Potential/V'})
	cv_df = cv_df.rename(columns={df.columns.values[1]:'Current/A'})
	cv_df[cv_df.columns.values[0]] = cv_df[cv_df.columns.values[0]].astype(float)
	cv_df[cv_df.columns.values[1]] = cv_df[cv_df.columns.values[1]].astype(float)
	time_lst = []
	cv_df = cv_df.reset_index(drop=True)
	for i in range(len(cv_df['Current/A'])):
		time_lst.append(i)
	cv_df['time'] = time_lst
	return (cv_df)