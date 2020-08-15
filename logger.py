import os
import datetime

LEVELS = [
    'INFO',
    'WARNING',
    'ERROR'
]


class Logger:
    def __init__(self, file_path: str):
        self.path = file_path
        file_name = str(datetime.datetime.now()).replace(".",'_').replace(" ",'_').replace("-",'_').replace(":","_") + ".log"
        self.file = f'{self.path}\\{file_name}'
        with open(self.file, 'w', encoding='utf-8') as initial:
            initial.write("[{}] LOGGING BEGUN  [{}] \n".format(
                LEVELS[0], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def log(self, level: str, message: str) -> None:
        """
            Logs a specific message specifying DATE and the type (INFO,WARNING,ERROR) in the following format : 
                => [type]  {message}  [time]

        """
        if not level in LEVELS:
            raise ValueError(
                'Level must be either of the following options {}'.format(",".join(LEVELS)))
        with open(self.file, 'a', encoding='utf-8') as logging:
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.write(f'[{level}]  {message}  [{time_now}] \n')


def main():
    pass


if __name__ == "__main__":
    main()
