import re
from simple_salesforce import Salesforce
import configparser
import subprocess as sp
import pandas as pd
import traceback

def login():
    config_file_name = "path_for_login_config_file"
    config = configparser.ConfigParser()
    config.read(config_file_name)
    user = config['LOGIN']['user']
    pw = config['LOGIN']['pw']
    tok = config['LOGIN']['tok']
    dom = config['LOGIN']['dom']
    sf = Salesforce(username=user, password=pw, security_token=tok, domain=dom)
    return sf

def filter_table():
    ID = str(input('Message to request input'))
    print('Input received')
    if "string_to_check_for_input_acceptance" in ID:
        print('Input accepted')
    else:
        print('Input not accepted')
        filter_table()
    return ID

def get_table_names():
    config_file_name = "path_for_table_config_file"
    config = configparser.ConfigParser()
    config.read(config_file_name)
    first_table = config['TABLES']['first_table_to_get']
    second_table = config['TABLES']['second_table_to_get']
    third_table = config['TABLES']['third_table_to_get']
    fourth_table = config['TABLES']['fourth_table_to_get']
    fifth_table = config['TABLES']['fifth_table_to_get']
    return first_table, second_table, third_table, fourth_table, fifth_table

def get_column_names():
    config_file_name = "path_for_column_config_file"
    config = configparser.ConfigParser()
    config.read(config_file_name)
    first_table_fields = [config['COLUMNS']['first_table_columns']]
    second_table_fields = [config['COLUMNS']['second_table_columns']]
    third_table_fields = [config['COLUMNS']['third_table_columns']]
    fourth_table_fields = [config['COLUMNS']['fourth_table_columns']]
    fifth_table_fields = [config['COLUMNS']['fifth_table_columns']]
    return first_table_fields, second_table_fields, third_table_fields, fourth_table_fields, fifth_table_fields

def create_sub_table(columns, table, filter_column, filter, sf): #only 1 filter
    query = "SELECT {} FROM {} WHERE {} = '{}'".format(','.join(columns), table, filter_column, filter)
    sub_table = pd.DataFrame(sf.query_all(query)['records']).drop(columns=['attributes'])
    return sub_table

def create_sub_table2(fields, table, filter, second_table_df, sf): #potential for multiple filters
    column_name = 'T2C9'
    id1 = second_table_df[column_name][0]
    try:
        id2 = second_table_df[column_name][1]
        query = "SELECT {} FROM {} WHERE {} = '{}' OR {} = '{}'".format(','.join(fields), table, filter, id1, filter, id2)
        print('Query to check for KeyError created')
        df = pd.DataFrame(sf.query_all(query)['records']).drop(columns=['attributes'])
        print('Secondary object df created')
        df.to_csv('path_to_save_df_to.csv', sep='\t', index=False)
        return df
    except KeyError:
        query = "SELECT {} FROM {} WHERE {} = '{}'".format(','.join(fields), table, filter, id1)
        print('No secondary object query created')
        df = pd.DataFrame(sf.query_all(query)['records']) #.drop(columns=['attributes'])
        print('No secondary object df created')
        df.to_csv('path_to_save_df_to.csv', sep='\t', index=False)
        return df

def join_table(table1, table2, table1_key, table2_key):
    joined_table = pd.merge(table1, table2, how='inner', left_on=table1_key, right_on=table2_key)
    return joined_table

def draft_primary_object_message(table):
    if table['T1C1'][0] != None:
        first_data_point = "$" + format(table['T1C1'][0], '.2f')
    else:
        first_data_point = "Not found"
    if table['T1C3'][0] != None:
        second_data_point = "$" + format(int(table['T1C3'][0]), '.2f')
    else:
        second_data_point = "Not found"
    if table['T1C4'][0] != None:
        third_data_point = format(round(((table['T1C4'][0])*100),2), '.2f') + "%"
    else:
        third_data_point = "Not found"
    if table['T3C2'][0] != None:
        fourth_data_point = "$" + format(table['T3C2'][0], '.2f')
    else:
        fourth_data_point = "Not found"
    fifth_data_point = table['T1C2'][0]
    sixth_data_point = table['T2C2'][0]
    seventh_data_point = table['T2C3'][0]
    eighth_data_point = table['T2C4'][0]
    ninth_data_point = table['T2C5'][0]
    tenth_data_point = table['T2C6'][0]
    if table['T2C7'][0] != None:
        eleventh_data_point = "$" + format(table['T2C7'][0], '.2f')
    else:
        eleventh_data_point = "Not found"
    if table['T3C2'][0] != None:
        twelfth_data_point = "$" + format(table['T3C2'][0], '.2f')
    else:
        twelfth_data_point = "Not found"
    thirteeth_data_point = (table['T5C2'][0]).lower()
    fourteenth_data_point = (table['T5C3'][0]).lower()
    if table['T4C1'].str.contains(thirteeth_data_point, flags = re.IGNORECASE, regex = True).any():
        thirteeth_data_point = "Yes"
    else:
        thirteeth_data_point = "No"
    if table['T4C1'].str.contains(fourteenth_data_point, flags = re.IGNORECASE, regex = True).any():
        fourteenth_data_point = "Yes"
    else:
        fourteenth_data_point = "No"
    print('Primary object data points assigned')
    primary_object_string = "First data point: {}"\
                     "\nSecond data point: {}"\
                     "\nThird data point: {}"\
                     "\nFourth data point: {}"\
                     "\nFifth data point: {}"\
                     "\nReasons: "\
                     "\nSixth data point: {}\t Seventh data point: {}\t Eighth data point: {}"\
                     "\nNinth data point - {}, Tenth data point - {}"\
                     "\nEleventh data point: {}"\
                     "\nTwelfth data point: {}"\
                     "\nThirteenth data point:"\
                     "\nFourteenth data point: {}\t Fifteenth data point: {}".format(first_data_point, second_data_point, third_data_point, fourth_data_point, fifth_data_point, sixth_data_point, seventh_data_point, eighth_data_point,
                                       ninth_data_point, tenth_data_point, eleventh_data_point, twelfth_data_point, thirteeth_data_point, fourteenth_data_point)
    return primary_object_string

def draft_secondary_object_message(table):
        try:
            first_data_point = table['T1C2'][1]
            second_data_point = table['T2C2'][1]
            third_data_point = table['T2C3'][1]
            fourth_data_point = table['T2C4'][1]
            fifth_data_point = table['T2C5'][1]
            sixth_data_point = table['T2C6'][1]
            if table['T2C7'][1] != None:
                seventh_data_point = "$" + format(table['T2C7'][1], '.2f')
            else:
                seventh_data_point = "Not found"
            if table['T3C2'][1] != None:
                eighth_data_point = "$" + format(table['T3C2'][1], '.2f')
            else:
                eighth_data_point = "Not found"
            ninth_data_point = (table['T5C2'][1]).lower()
            tenth_data_point = (table['T5C3'][1]).lower()
            if table['T4C1'].str.contains(ninth_data_point, flags=re.IGNORECASE, regex=True).any():
                ninth_data_point = "Yes"
            else:
                ninth_data_point = "No"
            if table['T4C1'].str.contains(tenth_data_point, flags=re.IGNORECASE, regex=True).any():
                tenth_data_point = "Yes"
            else:
                tenth_data_point = "No"
            print('Secondary object data points assigned')
            secondary_object_string = "\n\nFirst data point" \
                           "\nSecond data point: {}" \
                           "\nThird data points: " \
                           "\nFourth data point: {}\t Fifth data point: {}\t Sixth data point: {}" \
                           "\nSeventh data point - {}, Eighth data point - {}" \
                           "\nNinth data point: {}" \
                           "\nTenth data point: {}" \
                           "\nEleventh data point: " \
                           "\nTwelfth data point: {}\t Thirteenth data point: {}".format(first_data_point, second_data_point, third_data_point, fourth_data_point,
                                                                                             fifth_data_point,
                                                                                             sixth_data_point, seventh_data_point, eighth_data_point, ninth_data_point,
                                                                                             tenth_data_point)
            return secondary_object_string
        except KeyError:
            print('File does not contain secondary object.')
            return None

def draft_suggested_message(table):
    suggested_message_intro = "\n\nBeginning of message. "
    suggested_message_end = "\n\nEnding of message."
    suggested_message = suggested_message_intro
    scenario_1 = "Scenario 1 message"
    scenario_2 = "Scenario 2 message"
    scenario_3 = "Scenario 3 message"
    scenario_4 = "Scenario 4 message"
    if table['T1C2'][0] == "string to check field for" or table['T1C2'][0] == "string to check field for" or table['T1C2'][0] == "string to check field for":
        if table['T1C8'][0] == "string to check field for":
            suggested_message = suggested_message + scenario_1
        if table['T2C2'].str.contains("string to check field for", flags=re.IGNORECASE, regex=True).any():
            suggested_message = suggested_message + scenario_2
        if table['T2C3'].str.contains("string to check field for", flags=re.IGNORECASE, regex=True).any():
            suggested_message = suggested_message + scenario_3
        if table['T2C2'].str.contains("string to check field for", flags=re.IGNORECASE, regex=True).any():
            suggested_message = suggested_message + scenario_4

    suggested_message = suggested_message + suggested_message_end

    return suggested_message


def write_message_to_text_file(primary_object_string, secondary_object_string, suggested_message):
    if secondary_object_string is None:
        file = open("path_to_write_message_to_text_file.txt", "w")
        file.write(primary_object_string + suggested_message)
        file.close()
    else:
        file = open("path_to_write_message_to_text_file.txt", "w")
        file.write(primary_object_string + secondary_object_string + suggested_message)
        file.close()

def main():
    ID = filter_table() #receive ID from user
    sf = login() #access API
    #defining API table and column names
    first_table, second_table, third_table, fourth_table, fifth_table = get_table_names()
    first_table_fields, second_table_fields, third_table_fields, fourth_table_fields, fifth_table_fields = get_column_names()
    #creation of tables below
    first_table_df = create_sub_table(columns=first_table_fields, table=first_table, filter_column='T1C5', filter=ID,
                                      sf=sf)
    print('First table dataframe created')
    first_table_df.to_csv('path_to_save_first_dataframe.csv', sep='\t', index=False)
    fourth_table_df = create_sub_table(columns=fourth_table_fields, table=fourth_table,
                                         filter_column='T4C2', filter=first_table_df['T1C6'][0], sf=sf)
    print('Fourth table dataframe created')
    fourth_table_df.to_csv('path_to_save_fourth_dataframe.csv', sep='\t', index=False)
    second_table_df = create_sub_table(columns=second_table_fields, table=second_table,
                                     filter_column='T2C8', filter=first_table_df['T1C6'][0], sf=sf)
    second_table_df = second_table_df[second_table_df.column__to__check != 'string contained in fields to exclude rows']
    print('Second table dataframe created')
    second_table_df.to_csv('path_to_save_second_dataframe.csv', sep='\t', index=False)
    third_table_df = create_sub_table2(fields=third_table_fields, table=third_table, filter='T3C3', second_table_df=second_table_df, sf=sf)
    print('Third table dataframe created')
    third_table_df.to_csv('path_to_save_third_dataframe.csv', sep='\t', index=False)
    #merging tables below
    join_first_df_fourth_df = join_table(first_table_df, fourth_table_df, 'T1C6', 'T4C2')
    print('First join table created')
    join_first_df_fourth_df.to_csv('path_to_save_first_join.csv')
    add_second_df = join_table(join_first_df_fourth_df, second_table_df, 'T1C6', 'T2C8')
    print('Second join table created')
    add_second_df.to_csv('path_to_save_second_join.csv')
    add_third_df = join_table(add_second_df, third_table_df, 'T2C9', 'T3C3')
    print('Third join table created')
    add_third_df.to_csv('path_to_save_third_join.csv')
    fifth_table_df = create_sub_table2(fields=fifth_table_fields, table=fifth_table, filter='T5C4', second_table_df=second_table_df, sf=sf)
    print('Fifth table dataframe created')
    fifth_table_df.to_csv('path_to_save_fifth_dataframe.csv', sep='\t', index=False)
    add_fifth_df = join_table(add_third_df, fifth_table_df, 'T1C6', 'T5C4')
    print('Fourth join table created')
    add_fifth_df.to_csv('path_to_save_fourth_join.csv')
    table = add_fifth_df[add_fifth_df.column__to__check != 'string contained in fields to exclude rows']
    table = table.reset_index(drop=True)
    table = table.replace(to_replace='<br>', value=' ', regex=True)
    #formatting notes
    primary_object_string = draft_primary_object_message(table=table)
    secondary_object_string = draft_secondary_object_message(table=table)
    suggested_message = draft_suggested_message(table=table)
    print(primary_object_string, secondary_object_string)
    #writing notes to notepad
    write_message_to_text_file(primary_object_string=primary_object_string, secondary_object_string=secondary_object_string, suggested_message=suggested_message)
    sp.Popen(["notepad", "path_to_write_text_file_to.txt"])
    print(table)

if __name__ == "__main__":
    main()