from datetime import datetime 
import traceback,os

def loggingFile(file,data:list=[]):
    now = datetime.now()
    logData= f"{now.day}-{now.month}-{now.year}"

    if not os.path.exists('./log'):os.mkdir('./log')
    if not os.path.exists(f'./log/{logData}'):os.mkdir(f'./log/{logData}')
    with open(f"./log/{logData}/{file}.log",mode='a') as file:
        file.write(f"\n\nDATA: {str(datetime.now())} ->")
        traceback.print_exc(file=file)
        for item in data:file.write(f"{item}\n")
