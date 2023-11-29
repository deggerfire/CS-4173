# CS-4173

# Running program

### Setup
#### Libaries used

pyngrok
Flask
Crypto
Requests
Pillow

#### Libary install commands (these commands are for anaconda)

```
conda install -c conda-forge pyngrok
conda install -c conda-forge Flask
conda install -c anaconda pycryptodome
conda install -c anaconda cryptography
conda install -c anaconda requests
conda install -c anaconda pillow
```

### Runing

navigate to the folder with main.py and run the command:
```
python main.py
```

# Useage

## Start a room

Have the computer which will be the host start the program and select the host room option and enter a username and password. Safely have the password handed out to all users that will join the room **(!Room security is depended on this password remaining secure!)**. After the room is open on the top of the host screen there is a room url, this needs to be sent to all users that are to be in the room, this can be done insecurely.

## Join a room

Have all computers that will enter the room start the program an select the join room option. Enter a username, the url provided by the host, and the password.
