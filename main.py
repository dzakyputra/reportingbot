from telegram.ext import Updater, CommandHandler

import pandas as pd
import telegram
import sqlite3
import logging


# Set the logging function to print the error message whenever it happens
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def read_table(database_name, table_name):
    """
    Create a connection with the sqlite database and read the request table then return it as dataframe

    INPUT
      - database_name: name of the sqlite database with the format *.db
      - table_name: table name we want to select

    OUTPUT
      - The query result as a pandas dataframe
    """

    # Initiate the connection and query the data
    conn = sqlite3.connect(database_name)
    df = pd.read_sql_query('SELECT * FROM {}'.format(table_name), conn)
    return df


def total_users(df):
    """
    Get the total users and total users per service in the table

    INPUT
      - df: table from the database in the format of pandas dataframe

    OUTPUT
      - users: Total users
      - users_per_service: Total users per service
    """

    # Find total users and users per service
    users = len(df['chat_id'].unique())
    users_per_service = df.groupby('bot')['chat_id'].nunique().to_dict()
    
    # Return the result
    return users, users_per_service


def total_usages(df):
    """
    Get the total usages and total usages per service in the table

    INPUT
      - df: table from the database in the format of pandas dataframe

    OUTPUT
      - usages: Total usages
      - usages_per_service: Total usages per service
    """

    # Find total usages and usages per service
    usages = len(df)
    usages_per_service = df.groupby('bot')['id'].count().to_dict()
    
    # Return the result
    return usages, usages_per_service


def send_report(update, context):

    # Read the database and table
    df = read_table('database.db', 'requests')

    # Get total users per_service
    users, users_per_service = total_users(df)

    text = '`Total Users: {} \n -doggobot: {} \n -sentweetbot: {} \n -automatebot: {} \n -hangeulbot: {}`'.format(users, 
                                                                                                                  users_per_service['doggobot'], 
                                                                                                                  users_per_service['sentweetbot'], 
                                                                                                                  users_per_service['automatebot'], 
                                                                                                                  users_per_service['hangeulbot'])


    # Get total clicks per_service
    usages, usages_per_service = total_usages(df)

    text = text + '\n\n`Total Usages: {} \n -doggobot: {} \n -sentweetbot: {} \n -automatebot: {} \n -hangeulbot: {}`'.format(usages, 
                                                                                                                              usages_per_service['doggobot'], 
                                                                                                                              usages_per_service['sentweetbot'], 
                                                                                                                              usages_per_service['automatebot'], 
                                                                                                                              usages_per_service['hangeulbot'])
    

    # Send the result
    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN_V2)


def main():
  
    # Initiate the bot and add command handler  
    updater = Updater('TOKEN', use_context=True)
    updater.dispatcher.add_handler(CommandHandler('report', send_report))

    # Run the bot
    updater.start_polling()
    updater.idle()
  
if __name__ == '__main__':
    main()
