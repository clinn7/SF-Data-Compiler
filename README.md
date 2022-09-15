# SF-Data-Compiler
Gathers API table data points to present in text file with conditional messaging

Overview

The program utilizes Python along with the pandas and Simple Salesforce packages to accomplish 9 main functions:

1.	Receiving input from the user.
2.	Providing SalesForce API credentials via configuration file (.CONFIG).
3.	Querying SalesForce API for tables and columns defined via configuration file.
4.	Storing gathered tables into separate pandas dataframes in memory.
5.	Combining dataframes based on shared ID/key values into final dataframe.
6.	Pulling fields from dataframe to define data values needed.
7.	Formatting values (label strings, %/monetary formatting, parsing for search terms).
8.	Checking whether file contains 1 object or 2 objects for values needed for contents and writing to Notepad file.
9.	Opening Notepad file.

Examples:

.format() Format string:  Used to streamline definition of variables in a string. Brackets are essentially placeholders for variables in the function

	“SELECT {} FROM {} WHERE Name = ‘{}’”.format(variable1, variable2, variable3)
	translates to
	“SELECT variable1 FROM variable2 WHERE Name = ‘variable3’”
	

sf.query_all() Query Salesforce API: Gathers & filters tables/columns/rows, etc. specified with language similar to that used in SQL queries

	query = “SELECT ‘column_name1’, ‘column_name2’ FROM ‘table_name’ WHERE ‘column_name1’ = ‘filter’
	sf.query_all(query)

translates to
	
	sf.query_all(“SELECT ‘column_name1’, ‘column_name2’ FROM ‘table_name’ WHERE ‘column_name1’ = ‘filter’)


pd.DataFrame() Create pandas dataframe from Salesforce query: Takes data gathered from Salesforce API and creates a table within Python

	df = pd.DataFrame(sf.query_all(query)[‘records’])
	
Takes query above and selects all items under Salesforce key “records” and stores it as object “df”


.drop() Drop columns/rows from pandas dataframe: Removes columns/rows based on specified conditions

	df = df.drop(columns=[‘attributes’]

Takes previous dataframe above and removes all columns with the Salesforce key 
‘attributes’


df = df[] Modify pandas dataframe: Creates new dataframe from original based on conditions specified in brackets
	
	df = df[df.column/row_name == ‘filter’]

Creates new dataframe where all columns or rows are equal to the specified filter string

	
pd.merge() Merge pandas dataframes: Combines 2 or more pandas dataframes and combines them where specified row/column values are equal

	pd.merge(df1, df2, how=’inner’, left_on = ‘df1_column/row_name’, right_on = ‘df2_column/row_name’)

Joins all columns/rows of df1 and df2 where column/row value of df1 rows/columns are equal to column/row values of df2 rows/columns


df[][] Select value of dataframe field based on index: 

	df[‘column_name’][0]

Returns the value in the first row of the specified column ‘column_name’
