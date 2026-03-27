import datetime

def log_message(level, message):
    try:
        with open(r"C:\Users\hrithik.k\Desktop\python\Day1\login_system\logs.txt", "a") as file:
            time = datetime.datetime.now()
            file.write(f"{time} - {level} - {message}\n")
    except:
        print("Logging failed")