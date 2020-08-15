import os
import datetime

LEVELS = [
    'INFO',
    'WARNING',
    'ERROR'
]


class Logger:
    def __init__(self,file_path : str):
        self.path = file_path
        with open(self.path,'w',encoding='utf-8') as initial:
            initial.write("[{}] LOGGING BEGUN ON {} \n".format(LEVELS[0],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def log(self,level : str,message : str) -> None:
        """
            Logs a specific message specifying DATE and the type (INFO,WARNING,ERROR) in the following format : 
                => [type] \r {message} \r [time]

        """
        if not level in LEVELS:
            raise ValueError('Level must be either of the following options {}'.format(",".join(LEVELS)))
        with open(self.path,'a',encoding='utf-8') as logging:
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
            logging.write(f'[{level}] \r {message} \r [{time_now}]')
