import asyncio
from tkinter.filedialog import askopenfile
from Agents.agent_router import route
from database.db import DatabaseAgent
import httpx

# Initialise database agent globally
dbAgent = DatabaseAgent()

# main function to get file form the user and process the data.
def main():

    try :
        # Asks user to provide a file
        file = askopenfile('r')

        # If not provided a file return None
        if file is None:
            print('Please provide a valid file!')
            return None
        else: 

            # Runs the routing program and returns a dict of file data or error
            file_data = asyncio.run(route(file))

            if file_data:

                # If the dictionary containes the key error then print the error and return None
                if 'error' in file_data:
                    print(file_data['error'])
                    return None

                else:

                    # Inserts file data to the database table
                    # print(file_data)
                    dbAgent.insert(data=file_data)
                    
                    #  Asks user if wants to see the data table
                    showdata = str(input('Do you want to fetch the data (y/n) : '))

                    if showdata.lower() =='y':
                        df = dbAgent.fetch_data()
                        print(df)
                        return None

                    elif showdata.lower() =='n':
                        print('Exited program')
                        return None
                    
                    else:
                        print('Invalid input!')
                        return None
            
            # If the file_data variable is None
            else: 
                print(f'Filetype is not supported, Please enter a valid file.')
                return None
                

    except KeyboardInterrupt:
        print('Keyboard Interrupted. Restart the program.')
        return None

    # If the user is not connected to the internet then this error occurs
    except httpx.ConnectError as e:
        # Prints the error message and returns None
        print(f'Connect error: {e}, please connect to the internet.')
        return None

if __name__ == '__main__':
    
    while True:
        main()
        choice = input("Do you want to process another file? (y/n): ").lower()
        if choice != 'y':
            print("Closing DB connection. Goodbye!")
            dbAgent.conn.close()
            break