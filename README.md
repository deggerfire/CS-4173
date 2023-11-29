# Super Stealth Chat

## Running program

### Installed libaries

Note: Anaconda is used to manage libraries

#### Libaries used

pyngrok - Used for commucation over the internet

Flask - Used for commucation over the internet

Crypto - Used for encrypting and decrypting messages

Requests - Used for commucation over the internet

Pillow - Used to send images

#### Way 1: Import SSC_anaconda_setup.yaml into anaconda

#### Way 2: Libary install commands (these commands are for anaconda)

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

## Useage

## Start a room

Have the computer which will be the host start the program and select the host room option and enter a username and password. Safely have the password handed out to all users that will join the room **(!Room security is depended on this password remaining secure!)**. After the room is open on the top of the host screen there is a room url, this needs to be sent to all users that are to be in the room, this can be done insecurely.

## Join a room

Have all computers that will enter the room start the program an select the join room option. Enter a username, the url provided by the host, and the password.
