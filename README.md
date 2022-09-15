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
