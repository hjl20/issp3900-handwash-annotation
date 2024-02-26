## This is a short guide on some of the problems you may encounter trying to run the scripts in bash.
### 1. **-bash: cd: $'../\r': No such file or directory**
file being in **CRLF** (Windows) format and not **LF** (Linux). 
    
#### Method 1: 
        
Install dos2unix 
        
```
sudo apt-get update
sudo apt-get install dos2unix
```
and run the commands:
        
```
dos2unix get-and-preprocess-dataset.sh
dos2unix separate-frames.py
```

#### Method 2:
Open the scripts 'get-and-preprocess-dataset.sh' and 'separate-frames.py' in Visual Studio Code (VSCode).

At the very bottom of the VSCode window, you should see UTF-8, **CRLF**, Shell Script or Python.

Click on **CRLF** and change it to **LF**.

Save the file and try running 'get-and-preprocess-dataset.sh' again in your terminal.



