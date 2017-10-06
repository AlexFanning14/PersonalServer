def validateUser(username, pw): #Read Values from file stored on pi
    if username == "alex.fanning" and pw == "test":
        return True
    else:
        return False
