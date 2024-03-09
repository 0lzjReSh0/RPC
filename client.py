import xmlrpc.client
import time

#%%
def recall(proxy, method, *args, retry=3, delay=2):
    for attempt in range(retry):
        try:
            return getattr(proxy, method)(*args)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt + 1 == retry:
                print("Failed to communicate with the server. Try again later.")
                return None
            time.sleep(delay)


port = input("Enter the server port you like: ")
server_address = f"http://localhost:{port}"
server = xmlrpc.client.ServerProxy(server_address)


#%%
def add_note():
    topic = input("Enter topic: ")
    text = input("Enter text: ")
    timestamp = input("Enter timestamp: ")
    success = recall(server, 'add_note', topic, text, timestamp)
    if success:
        print("Success.")
    else:
        print("Failed.")

def get_notes():
    topic = input("Enter topic: ")
    notes = recall(server, 'get_notes', topic)
    if notes:
        print(f"Notes for {topic}:")
        for note in notes:
            print(note)
    else:
        print("No notes found.")
        
        
def add_wiki():
    topic = input("Enter topic to fetch from Wikipedia: ")
    success = recall(server, 'add_wiki', topic)
    if success:
        print("Wikipedia information added successfully.")
    else:
        print("Failed to add from Wikipedia or no information found.")

while True:
    print("\n1. Add Note\n2. Get Notes\n3. Add Wikipedia Note\n4. Exit\n")
    choice = input("Choose: ")
    if choice == '1':
        add_note()
    elif choice == '2':
        get_notes()
    elif choice == '3':
        add_wiki()
    elif choice == '4':
        break
    else:
        print("Invalid input!")


