'''
Author: Bernard Hernandez
Filename:
Date: 
Description: 
'''

# Libraries.
from os import listdir

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import glob
import json
import os as os

#-------------------------------------------------------------------------
#                           HELPER METHODS
#-------------------------------------------------------------------------
def files_with_extension(folder, ext):
	""" This method return files with extension.
	
	Parameters
	----------
	folder : path containing the files.
	ext : selected extensions.

	Return
	------
	ext_files : files in folder with the extensions in ext.
	"""
	# Basic check.
	if isinstance(ext, str): ext = [ext]
	# List files and add selected ones.
	all_files, ext_files = os.listdir(folder), []
	for f in all_files:
		for e in ext:
			if f.endswith(e):
				ext_files.append(f)
				break
	# Return
	return ext_files

#-------------------------------------------------------------------------
#                           GENERIC READ METHOD
#-------------------------------------------------------------------------
def read_data(ftype, **kwargs):
	"""This method loads data from the specified format.

	Parameters
	----------
	ftype : type of files to be load. Currently supported (xls, xlsx, csv, mysql).
	rename_map : dict-like, with current name and desired name.
	std_cols : list of columns that want to be kept.
	url : Only for 'mysql' - url to connect to the mysql sever.
	query : Only for 'mysql' - query to be executed against the server.

	Return
	------
	dataframe - <DataFrame> from pandas with content.
	"""
	if kwargs is None: return None
	if (ftype=='xls' or ftype=='xlsx'): return read_excel(**kwargs)
	if (ftype=='csv'):                  return read_csv(**kwargs)
	elif (ftype=='mysql'):              return read_mysql_server(**kwargs)
	else:                  		     	return None


#-------------------------------------------------------------------------
#                            READ MYSQL
#-------------------------------------------------------------------------
def read_mysql_server(url=None, query=None, rename_map=None):
	"""This function rename codes (i.e. PAER1,PAER2 to PEAR)

	Parameters
	----------

	Return
	------
	"""
	# Import library.
	from sqlalchemy import create_engine
	# Create connection.
	engine = create_engine(url)
	connection = engine.raw_connection()
	# Read SQL into DataFrame.
	df = pd.read_sql(query, connection)
	# Rename columns.
	df.rename(columns=rename_map, inplace=True)
	# Return
	return df


#-------------------------------------------------------------------------
#                            READ EXCEL
#-------------------------------------------------------------------------
def read_excel(path):
	"""This function...

	Parameters
	----------

	Return
	------
	"""
	if not os.path.exists(path): return None
	if os.path.isfile(path): return read_excel_file(path, **kwargs) 
	if os.path.isdir(path): return read_excel_folder(path, **kwargs)
	return None

def read_excel_folder(path=None, **kwargs):
	"""Load all excel files into a pandas dataframe.

	Parameters
	----------
	path : 

	Returns
	-------
	"""
	# Find files.
	files = files_with_extension(path, ['.xls','.xlsx'])
	if len(files)==0: return None
	print("Loading files...%s" % files)
	# Load data.
	df = None
	for fname in files:
		filepath = "%s/%s" % (path, fname)
		df_aux = read_excel_file(filepath, **kwargs)
		df = pd.concat([df, df_aux])
	# Remove duplicates.
	df = df.drop_duplicates()
	# Return
	return df

def read_excel_file(path, rename_map={}, std_cols=None, **kwargs):
	"""This method...

	Parameters
	----------

	Return
	------

	"""
	# Read data and format it.
	df = pd.read_excel(path, **kwargs) #, quotechar='"', quoting=1)
	df.rename(columns=rename_map, inplace=True)
	if std_cols is not None:
		df = pd.DataFrame(df, columns=std_cols)
	# Return
	return df



#-------------------------------------------------------------------------
#                            READ CSV
#-------------------------------------------------------------------------
def read_csv(path, **kwargs):
	"""This method...

	Parameters
	----------

	Return
	------
	"""
	if not os.path.exists(path): return None
	if os.path.isfile(path): return read_csv_file(path, **kwargs) 
	if os.path.isdir(path): return read_csv_folder(path, **kwargs)
	return None

def read_csv_folder(path, **kwargs):
	"""Load all excel files into a pandas dataframe.

	Parameters
	----------
	folder : 
	rename_map :
	std_cols :

	Returns
	-------
	"""
	# Find files.
	files = files_with_extension(path, '.csv')
	if len(files)==0: return None
	print ("Loading files...%s" % files)
	# Load data.
	df = None
	dfs = []
	for fname in files:
		filepath = "%s/%s" % (path, fname)
		df_aux = read_csv_file(filepath, **kwargs)
		df = pd.concat([df, df_aux])
	# Remove duplicates.
	df = df.drop_duplicates()
	# Return
	return df

def read_csv_file(path, rename_map={}, 
												std_cols=None, 
												keep_cols=None,
												date_cols=[],
												**kwargs):
	"""This method reads a csv file.

	Note: 1. It uses the pandas function pd.read_csv.
	      2.

	Note: keep_cols is used instead of default usecols from pandas because when
	reading different files we cannot ensure that all have the same column names
	before renaming.

	Parameters
	----------
	rename_map :
	std_cols   :
	keep_cols  :
	date_cols  :

	Return
	------

	"""
	# Read data and format it.
	df = pd.read_csv(path, **kwargs)
	# Rename columns.
	df.rename(columns=rename_map, inplace=True)
	# Parse dates.
	for c in date_cols:
		if c in df.columns:
				df[c] = pd.to_datetime(df[c], infer_datetime_format=True)
	# Columns that compose the dataframe.
	if std_cols is not None:
		df = pd.DataFrame(df, columns=std_cols)
	# Select some columns (useful if MemoryError)
	if keep_cols is not None:
		df = df[keep_cols]
	# Return
	return df