# Password manager

Includes 4 files `encryption.py`,`logger.py`,`main.py` and `UI.py` each today what it's name suggests:

| `encryption.py` has built-in functions that allow encryption and decription of strings

- The main functions are :
```
def encrypt(msg : str) -> list: ...
def decrpyt(encrypted_msg : str,encrypted_iterations : str,charvar_length : str) -> str:

```
- Both have the following dependencies for extra protection :
```
def encryptIterations(iterations : Union[str,int]) -> str: ...
temp1 = encryptIterations(223456)
#Outputs : 0b100101101010110b100101101010110b10001010011001110b1111110101011110b10101000100001110b100001000001
```
- And for decryption
```
def decryptIterations(iterations : Union[bytes,str]) -> str: ...
decryptIterations(temp1) #223456
```
Iterations is the `str` sum of the length of  the `hex_token`'s generated in the below code

```
 length = len(msg)
 ITERATIONS = []
 INTS = [2,3,4]
 for j in range(length):
      int_choice = secrets.choice(int(INTS))
      ITERATIONS.append(str(len(choice_token)))
 ....
 return "".join(ITERATIONS)

```

- A sample output from the `encrypt(msg : str)` function is the following
```
 terry_alive = False
 isAlive = 'is' if terry_alive else 'was'
 encrypt("Terry Davis {} the smartest programmer that has ever lived.".format(isAlive))
 
 #Outputs this:
[
   "4935833384fa270c101af071149aa6114297E1211cdC322AEA316821e43797eF42000f118f6deD2fc10537694e27115A71D3245d16710588b3385911587c583322F9125d3116dB4A49104847367101d8053266A75c62115F0431097aA4F5e297673011426ead01166Cf810164121153887cD311160Cf032A4761122fC2A51149a941118d961f103cCa91148B9B8C978Fc34590109041b948E109916a048B1017cd8114CA789432759eb32f116680B66104Bde321f897BcA5fb7E1166283033284e9104B4582a975E20a2115e9CA933200Ea1017e3Cd8118F09D9E101a6EC1141472324c0d5A108DcC9105a5541181836101B20Bb510017215f46OHYZJ",
   (
      "86444466888468686648484644844646468884686886466646644644466",
      "2_3_3_3_3_2_2_2_3_3_3_2_3_3_2_3_3_3_2_3_3_2_3_3_3_3_3_2_3_3_3_3_3_2_3_3_3_3_2_3_3_2_3_2_3_2_3_2_3_3_3_3_2_3_3_3_3_3_2"
   )
]

```

* Encryption is currently not used in any of the other files

| `logger.py` takes care of logging actions that are being executed in the `logs` folder
 - It's just a simple logging module that was written because there was no need to use the built-in

```
class Logger:
  def __init__(self, file_path: str):
         self.path = file_path
         ....
  def log(self, level: str, message: str) -> None:
     with open(self.file, 'a', encoding='utf-8') as logging:
         time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         logging.write(f'[{level}]  {message}  [{time_now}] \n')

```

| `main.py` handles communication with the local SQLite database
  - It contains the following methods : `INSERT`,`DELETE`,`SELECT like (%str%),SELECT (absolute)`,`update`

```
class Database:
    def __init__(self):
        #Creates the database if it cannot find it located locally
        pass
    def add(*args):
        #Adds data to the database
        pass
    def delete(self,platform :str):
        #Deletes data given a platform
        pass

    def quickQuery(self):
        #Does small queries
        pass

       ...
    #And a few more

```

| `UI.py` is the "frontend" which communicates with the user, Sample Screenshot:

![](https://i.imgur.com/z6j1fVN.png)

- Uses [`colorama.py`](https://pypi.org/project/colorama/) for terminal colors
