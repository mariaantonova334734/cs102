def get_greeting(name: str) -> str:
    message = "Hello, " + name +"!"
    return message



if __name__ == "__main__":
    name=input()
    print(get_greeting(name))
