try:
    import os
    import hashlib
    import secrets
    import mysql.connector as connector
    from cryptography.fernet import Fernet
except ImportError:
    print('unable to import required modules')
sqluser=input('-->Enter sql username: ')
sqlpw=input('-->Enter sql passwd: ')
try:
    ctr=connector.connect(host='localhost',
    user=sqluser,
    passwd=sqlpw,
    database='')
    if ctr.is_connected():
        print('Database successfully connected')
except Exception:
    print('DATABASE CONNECTION ERROR')
    raise SystemExit(0)
    
try:
    cur=ctr.cursor()
    query='CREATE DATABASE IF NOT EXISTS project;'
    cur.execute(query)
    query1='use project'
    cur.execute(query1)
    query2='create table IF NOT EXISTS Information(user_name varchar(300 ) NOT NULL UNIQUE ,password varchar(300))'
    cur.execute(query2)
    ctr.commit()
except Exception:
    print('ERROR IN CREATING DATABASE')

def generate_key():
    '''This function generate key for encryption'''
    key=Fernet.generate_key()
    with open('key.key','wb') as key_file:
        key_file.write(key)

def start():
    '''Main Front end '''
    print('''
-------------------------------------- 
-- Welcome to Password Manager       
-->1 for adding new Record           
-->2 for checking existing password  
-->3 for updating password           
-->4 Delete Record
-->5 Quit!
--------------------------------------
    ''')

def load_key():
    'This loads key for encryption and decryption'
    with open('key.key','rb') as key:
        x=key.read()
    return x
def addinfo():
    'add info to database'
    name=input('Enter Username: ')
    paswd=input('Enter Password: ')
    query3="INSERT INTO information(user_name,password) values('{}','{}')".format(name,fer.encrypt(paswd.encode()).decode())
    cur.execute(query3)
    ctr.commit()
    print(cur.rowcount,'Password Inserted Succesfully!')
def getinfo():
    'retrieve info from database'
    name=input('Enter Username: ')
    query4=f'select password from information where user_name="{name}"'
    cur.execute(query4)
    
    passw=cur.fetchone()
    x=''
    if cur.rowcount==0:
        print('No Record Currently')
    else:
        for i in range(len(passw)):
            x+=passw[i]
        print(f'USERNAME: {name}','PASSWORD: ',fer.decrypt(x.encode()).decode())
    

def updaterec():
    'update info in database'
    name=input('Enter Username: ')
    passw=input('Enter New Password: ')
    query5=f"update information set password='{fer.encrypt(passw.encode()).decode()}' where exists(select user_name where user_name='{name}')"
    cur.execute(query5)
    ctr.commit()
    print('PASSWORD UPDATED SUCCESSFULLY')
def deleterec():
    'deletes record from database'
    name=input('Enter Username Name')
    query6=f"delete from information where exists(select user_name where user_name='{name}')"
    cur.execute(query6)
    ctr.commit()
    if cur.rowcount!=0:
        print(cur.rowcount,'Record Successfully Deleted')
    elif cur.rowcount==0:
        print('Record Not Found')
MASTER_HASH_FILE = "master.txt"

# compare given password with salted hash master password file
def masterHashComapare(password):
    'checks master password'
    master = open(MASTER_HASH_FILE)
    masterLines = master.read().splitlines()
    salt = masterLines[0]
    hash = hashlib.sha512((salt + password).encode('utf-8')).hexdigest()
    if (hash == masterLines[1]):
        return True
    else:
        return False
def createMasterHashFile(password):
    'create master password'
    master = open(MASTER_HASH_FILE, 'w')
    salt = secrets.token_hex(64)
    hash = hashlib.sha512((salt + password).encode('utf-8')).hexdigest()
    master.write("%s\n" % salt)
    master.write("%s\n" % hash)
    master.close()
passwordAttempts=0
def main1():
    'runs the program'
    while True:
        start()
        user_input=input("Enter your choice: ")
        try:
            if user_input=='1':
                addinfo()
            elif user_input=='2':
                getinfo()
            elif user_input=='3':
                updaterec()
            elif  user_input=='4':
                deleterec()
            elif user_input=='5':
                break
            else:
                print('INVALID INPUT')
            
        except TypeError:
            print('INVALID INPUT')
if os.path.exists('key.key') is False:
    generate_key() 
          
key=load_key()
fer = Fernet(key)
while(True):
    try:
        password = input("Enter master password: ")
        if(not masterHashComapare(password)):
            if (passwordAttempts > 1):
                print("\n**TOO MANY WRONG ATTEMPTS**\n")
                raise SystemExit(0)
            else:
                print("\n**WRONG PASSWORD**\n")
                passwordAttempts += 1
                continue
        else:
            print("\nPASSWORD CORRECT\n")
            main1()
            break
    except FileNotFoundError:
        print("\nMaster password file doesn't exist. Creating master file. Initializing Database.\n")
        createMasterHashFile(password)
        break


cur.close()
ctr.close()

