"""Server.py file which has class server"""
import socket
import json
import os
import time
import shutil
import _thread

from config import USERS_JSON_PATH, DATA_PATH, ADMIN_LIST, PORT

class Server:
    """Handles the server"""

    def __init__(self):
        """Initialize variables"""
        self.host = None
        self.port = None
        self.soc = None
        self.login_data = self.load_login_data()
        self.users_current_directory = {}
        self.client_response = None
        self.all_connections = []
        self.all_address = []
        self.login_validation = {}
        self.thread_running_status = {}
        self.read_file_status = {}
        self.logged_in_users = []

    def create_socket(self):
        """Create socket"""
        try:
            self.host = ""
            self.port = PORT
            self.soc = socket.socket()

        except socket.error as msg:
            print("Socket creation error: " + str(msg))


    def bind_socket(self):
        """Binding the socket and listening for connections"""
        try:
            print("Binding the Port: " + str(self.port))

            self.soc.bind((self.host, self.port))
            self.soc.listen(5)

        except socket.error as msg:
            print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
            self.bind_socket()


    def accepting_connections(self):
        """
        Handling connection from multiple clients and saving to a list
        Closing previous connections when server.py file is restarted
        """
        for available_conn in self.all_connections:
            available_conn.close()

        del self.all_connections[:]
        del self.all_address[:]

        while True:
            try:
                conn, address = self.soc.accept()
                self.soc.setblocking(1)  # prevents timeout

                self.all_connections.append(conn)
                self.all_address.append(address)
                self.login_validation[address] = None
                self.thread_running_status[address] = False
                print("Connection has been established :" + address[0])
            except:
                print("Error accepting connections")

    def listen_and_respond(self, conn, addr):
        """Listen and respond to every connected client"""
        try:
            self.thread_running_status[addr] = True
            client_response = str(conn.recv(4096), "utf-8")
            out_data = self.server_api(client_response, addr)
            conn.send(str.encode(out_data))
            self.thread_running_status[addr] = False
        except:
            pass
            self.quit(addr)
            try:
                conn.send(str.encode("\nSome error occured from server side. You have been logged out for this. you need to login again."))
            except:
                pass

    def manage_connections(self):
        """Manage all connections"""
        while True:
            for conn, address in zip(self.all_connections, self.all_address):
                try:
                    if not self.thread_running_status[address]:
                        _thread.start_new_thread(self.listen_and_respond, (conn, address))
                except:
                    pass

    def load_login_data(self):
        """Load login data from json"""
        try:
            with open(USERS_JSON_PATH) as json_file:
                return json.load(json_file)
        except:
            print("Error opening json data")

    def print_commands(self):
        """Print all available commands of server"""
        output = "\n"
        output += "-----------------------------------" + "\n"
        column = ["Service command", "Description"]
        data = [["change_folder <name>", "Move the current working directory"],
                ["list", "Print all files & folders in current directory"],
                ["read_file <name>", "Read 100 char from the file <name> in the current working directory"],
                ["write_file <name> <input>", "Write data in <input> to end of file <name> in current directory"],
                ["create_folder <name>", "Create a new folder with the <name> in the current working directory"],
                ["register <username> <password> <privileges>", "Register a new user with the <privileges> to the server using the <username> and <password> provided"],
                ["login <username> <password>", "Log in the user conforming with <username>"],
                ["delete <username> <password>", "Delete the user conforming with <username> from the server"]]
        output += "{:<50}".format(column[0]) + "   -->   " + column[1] + "\n"
        for row in data:
            output += "{:<50}".format(row[0]) + "   -->   " + row[1] + "\n"
        output += "-----------------------------------" + "\n"
        return output

    def login(self, user, password, address):
        """Login"""
        if self.login_validation[address] is None:
            if user in list(self.login_data["users"].keys()):
                if password == self.login_data["users"][user]:
                    if user not in self.logged_in_users:
                        self.login_validation[address] = user
                        self.users_current_directory[user] = ""
                        self.logged_in_users.append(user)
                        return "\nLogin successfull"
                    else:
                        return "\nUser already loggin in from other IP."
                return "\nWrong password"
            return "\nUser not registered"
        return "\nAlready logged in"

    def get_information(self, directory):
        file_list = []
        for i in os.listdir(directory):
            a = os.stat(os.path.join(directory, i))
            file_list.append([i, a.st_size, time.ctime(a.st_ctime)]) #[file,most_recent_access,created]
        return file_list

    def list(self, address):
        """List"""
        if self.login_validation[address] is not None:
            directory = self.users_current_directory[self.login_validation[address]]
            directory = os.path.join(DATA_PATH, self.login_validation[address], directory)
            output = "\n"
            output += "{:<50}".format("Name") + "   ---   " + "{:<25}".format("Size") + "   ---   " + "{:<50}".format("Created at") + "\n"
            for file in self.get_information(directory):
                output += "{:<50}".format(file[0]) + "   ---   " + "{:<25}".format(file[1]) + "   ---   " + "{:<50}".format(file[2]) + "\n"
            return output
        return "\nLogin First"

    def change_folder(self, directory, address):
        """Change directory"""
        if self.login_validation[address] is not None:
            total_dir = []
            for i, j, k in os.walk(os.path.join(DATA_PATH, self.login_validation[address])):
                total_dir.append(os.path.normpath(os.path.realpath(i)))
            # print(os.path.normpath(os.path.realpath(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], directory))), total_dir)
            if os.path.normpath(os.path.realpath(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], directory))) in total_dir:
                self.users_current_directory[self.login_validation[address]] = os.path.join(self.users_current_directory[self.login_validation[address]], directory)
                return "\nChanged directory successfully"
            return "\nUnable to change requested directory"
        return "\nLogin First"

    def read_file(self, path, address):
        """Read file"""
        if self.login_validation[address] is not None:
            files = []
            for file in os.listdir(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]])):
                if os.path.isfile(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], file)):
                    files.append(file)
            # print(path, files)
            if path in files:
                if os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], path) not in list(self.read_file_status.keys()):
                    self.read_file_status[os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], path)] = 0
                file_f = open(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], path), "r")
                contents = file_f.read()
                content_from = str(self.read_file_status[os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], path)]*100)
                contents1 = contents[self.read_file_status[os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], path)]*100:(self.read_file_status[os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], path)]+1)*100]
                self.read_file_status[os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], path)] += 1
                self.read_file_status[os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], path)] %= len(contents)//100 + 1
                file_f.close()
                return "\n" + "Content from characters : " + content_from + " - " + str(int(content_from) + 100) + "\n" + contents1
            return "\nNo such file found"
        return "\nLogin First"

    def write_file(self, path, inp, address):
        """Write file"""
        if self.login_validation[address] is not None:
            files = []
            for file in os.listdir(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]])):
                if os.path.isfile(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], file)):
                    files.append(file)
            # print(path, files)
            if path in files:
                file_f = open(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], path), "a+")
                file_f.write("\n" + inp)
                file_f.close()
                return "\nWritten successfully"
            file_f = open(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], path), "w+")
            file_f.write("\n" + inp)
            file_f.close()
            return "\nNo such file found\nWritten a new file\n"
        return "\nLogin First"


    def create_folder(self, path, address):
        """Create folder"""
        if self.login_validation[address] is not None:
            directories = []
            for file in os.listdir(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]])):
                if os.path.isdir(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], file)):
                    directories.append(file)
            if path in directories:
                return "\nDirectory Already Present"
            os.mkdir(os.path.join(DATA_PATH, self.login_validation[address], self.users_current_directory[self.login_validation[address]], path))
            return "\nSuccessfully made directory"
        return "\nLogin First"

    def register(self, user, password, privileges):
        """Register"""
        if user in list(self.login_data["users"].keys()):
            return "\nUsername already taken"
        with open(USERS_JSON_PATH) as json_file:
            users = json.load(json_file)
        users["users"][user] = password
        with open(USERS_JSON_PATH, 'w') as outfile:
            json.dump(users, outfile)
        if privileges == "admin":
            with open(ADMIN_LIST) as json_file:
                admins = json.load(json_file)
            admins["users"].append(user)
            with open(ADMIN_LIST, 'w') as outfile:
                json.dump(admins, outfile)
        self.login_data = self.load_login_data()
        os.mkdir(os.path.join(DATA_PATH, user))
        return "\nRegistered successfully"

    def delete(self, user, password, address):
        """Delete"""
        if self.login_validation[address] is not None:
            with open(ADMIN_LIST) as json_file:
                admins = json.load(json_file)
            if self.login_validation[address] in admins["users"]:
                if user in list(self.login_data["users"].keys()):
                    if password == self.login_data["users"][self.login_validation[address]]:
                        if user in self.logged_in_users:
                            for key, value in self.login_validation.items():
                                if value == user:
                                    useraddr = key
                            self.quit(key)
                        del self.login_data["users"][user]
                        with open(USERS_JSON_PATH, 'w') as outfile:
                            json.dump(self.login_data, outfile)
                        with open(ADMIN_LIST) as json_file:
                            admins = json.load(json_file)
                        if user in admins["users"]:
                            admins["users"].remove(user)
                            with open(ADMIN_LIST, 'w') as outfile:
                                json.dump(admins, outfile)
                        if user == self.login_validation[address]:
                            self.login_validation[address] = None
                        shutil.rmtree(os.path.join(DATA_PATH, user))
                        return "\nDeleted user successfully. If user is logged in from your IP itself, then we have logged out you too for security reasons."
                    return "\nWrong password"
                return "\nNo such user found"
            return "\nYou are not an admin!"
        return "\nLogin First"

    def quit(self, address):
        """quit"""
        try:
            if self.login_validation[address] in self.logged_in_users:
                self.logged_in_users.remove(self.login_validation[address])
            self.users_current_directory[self.login_validation[address]] = ""
            self.login_validation[address] = None
            self.all_connections.remove(self.all_connections[self.all_address.index(address)])
            self.all_address.remove(address)
            del self.thread_running_status[address]
            return "\nLogged out successfully"
        except:
            return "\nLogged out successfully"

    def server_api(self, command, address):
        """Server API"""
        command = command.rstrip("\n")
        if command == "commands":
            data = self.print_commands()
            return data
        if command == "quit":
            data = self.quit(address)
            return data
        if command.split(" ")[0] == "login":
            if len(command.split(" ")) == 3:
                data = self.login(command.split(" ")[1], command.split(" ")[2], address)
                return data
            return "Invalid arguments given"
        if command.split(" ")[0] == "list":
            data = self.list(address)
            return data
        if command.split(" ")[0] == "change_folder":
            data = self.change_folder(command.split(" ")[1], address)
            return data
        if command.split(" ")[0] == "read_file":
            file = " ".join(command.split(" ")[1:])
            file = file.lstrip(" ").rstrip(" ")
            data = self.read_file(file, address)
            return data
        if command.split(" ")[0] == "write_file":
            data = self.write_file(command.split(" ")[1], " ".join(command.split(" ")[2:]), address)
            return data
        if command.split(" ")[0] == "create_folder":
            data = self.create_folder(command.split(" ")[1], address)
            return data
        if command.split(" ")[0] == "register":
            if len(command.split(" ")) == 4:
                data = self.register(command.split(" ")[1], command.split(" ")[2], command.split(" ")[3])
                return data
            return "Invalid arguments given"
        if command.split(" ")[0] == "delete":
            data = self.delete(command.split(" ")[1], command.split(" ")[2], address)
            return data
        return "Invalid service name"



if __name__ == '__main__':
    SERVER = Server()
    SERVER.create_socket()
    SERVER.bind_socket()
    _thread.start_new_thread(SERVER.accepting_connections, ())
    SERVER.manage_connections()
