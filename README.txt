The executable is located at "dist/main/main.exe"

Starting a chat server:
1. Launch "main.exe" -or- main.py from the command line
2. Select "Create Chat Room"
3. A cmd window will open and log connections until closed
4. Upon closing the cmd window, the server will close

Joining an existing server:
1. Launch "main.exe" -or- main.py from the command line
2. Select "Join a Chat Room"
3. A cmd window will open and ask for a hostname (IP addr or localhost)
4. Once connected, enter a username to begin


Notes:
The port# is hardcoded to 55555, so only one server can be up at once.
Multiple clients may connect to the same server. There is no limit (for now).
The executable creates a new instance of the program without killing the previous one. 
This means you can use the executable to launch a server then use it again to connect to it.