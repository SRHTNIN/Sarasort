import toml, os, datetime, re, shutil

Conf = None
ConfVars = None
ConfDirs = None
ConfNames = None
ConfLog = None

Start = True

def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def LoadConf():
    global Conf, ConfVars, ConfDirs, ConfNames, ConfLog

    LocalConf = toml.load("Config.toml")
    Conf = LocalConf
    ConfVars = Conf["Variables"]
    ConfDirs = Conf["DirectoryPaths"]
    ConfNames = Conf["Names"]
    ConfLog = Conf["Log"]


def CheckConf():
    for Parameter, Value in ConfVars.items():
        if (Value == None or Value == "Unset"):
            TextOutput = Parse(ConfLog["Unset"], Parameter)
            LogWrite(TextOutput)
            Speak(TextOutput)
            Error()
    
    for Parameter, Value in ConfDirs.items():
        if (Value == None or Value == "Unset"):
            TextOutput = Parse(ConfLog["Unset"], Parameter)
            LogWrite(TextOutput)
            Speak(TextOutput)
            Error()
    
    for Parameter, Value in ConfNames.items():
        if (Value == None or Value == "Unset"):
            TextOutput = Parse(ConfLog["Unset"], Parameter)
            LogWrite(TextOutput)
            Speak(TextOutput)
            Error()    

    for Parameter, Value in ConfLog.items():
        if (Value == None or Value == "Unset"):
            TextOutput = Parse(ConfLog["Unset"], Parameter)
            LogWrite(TextOutput)
            Speak(TextOutput)
            Error()    


def GetConf(Parameter):
    if Parameter in Conf:
        return (Conf[Parameter])
    
    for Key, Value in Conf.items():
        if (isinstance(Value, dict)):
            if (Parameter in Value):
                return Value[Parameter]
    
    return None


def UpdateConf(Path, Parameter, Value, Append = False):
    ConfData = toml.load(Path)

    if (not Append):
        ConfData[Parameter] = Value
    
    else:
        if (Parameter not in ConfData):
            ConfData[Parameter] = []
        
        elif (not isinstance(ConfData[Parameter], list)): 
            TextOutput = Parse(ConfLog["WrongType"], Parameter, "list")    
            LogWrite(TextOutput)
            Speak(TextOutput)
        
        if (Value not in ConfData[Parameter]):
            ConfData[Parameter].append(Value)

    with open(Path, 'w', encoding='utf-8') as File:
        toml.dump(ConfData, File)


def Error():
    global Start
    if (Conf["SafeMode"] == 1):
            Start = False


def Speak(Text):
    if (Conf["SilentMode"] != 1):
        print(Text)


def Parse(String = None, Var = None, Path = None):
    def Replacer(Match):
        Content = Match.group(1)

        if (Content == None or Content == ""):
            if (Var != None):
                return str(Var)
            else:
                return ""
        
        Value = GetConf(Content)
        if (Value != None):
            return Value
            
    
    Now = datetime.datetime.now()

    VarValues = {
        ConfVars["NextNum"]: "NOT ADDED",
        ConfVars["NextChar"]: "NOT ADDED",
        ConfVars["Parent"]: Var,
        ConfVars["OrgFileName"]: Var,
        ConfVars["OrgFileType"]: Var,
        ConfVars["Year"]: str(Now.year),
        ConfVars["Month"]: str(Now.month),
        ConfVars["Day"]: str(Now.day),
        ConfVars["Hour"]: str(Now.hour),
        ConfVars["Minute"]: str(Now.minute),
        ConfVars["Second"]: str(Now.second),
        ConfVars["VarCall"]: Var
    }

    for Key, Value in VarValues.items():
        if Key in String and Value is not None:
            String = String.replace(Key, Value)

    VarCall0 = re.escape(ConfVars["VarCall"][0])
    VarCall1 = re.escape(ConfVars["VarCall"][1])

    Pattern = f"{VarCall0}(.*?){VarCall1}"

    String = re.sub(Pattern, Replacer, String)
    return String


def Clone(Source, Destination, NewName):
    shutil.copy(Source, Destination)

    NewPath = f"{Destination}/{NewName}"
    shutil.move(f"{Destination}/{Source}", NewPath)


def Dir(Path, Output = True, CopyConf = True):
    ParentName = os.path.basename(os.path.dirname(Path))
    os.makedirs(Path, exist_ok=True)
    
    if (CopyConf):
        Clone("DirConfig.toml", Path, f"{Parse(ConfNames["DirConfName"], ParentName)}.toml")  
        
        UpdateConf(f"{Path}/{Parse(ConfNames["DirConfName"], ParentName)}.toml", "ParentDir", ParentName)
        UpdateConf(f"{Path}/{Parse(ConfNames["DirConfName"], ParentName)}.toml", "Title", f"{ParentName} Config")

    if (Output):
        UpdateConf("Config.toml", "OutputDir", Output, True)


def LogWrite(Text):
    if (ConfDirs["LogDir"] != None and ConfNames != "Unset"):
        if (ConfNames["LogFileName"] != None and ConfNames["LogFileName"] != "Unset"):
            Dir(Parse(ConfDirs["LogDir"]), "Log")
            LogFile = f"{Parse(ConfDirs["LogDir"])}/{Parse(ConfNames["LogFileName"])}.log"
            with open(LogFile, "w", encoding="utf-8") as File:
                File.write(f"{Parse(ConfLog["All"])}{Text}\n")


def Init():
    global Conf, ConfVars, ConfDirs, ConfNames, ConfLog
    
    LoadConf()
    if (Conf != None):
        CheckConf()
        
        if (Start):
            TextOutput = Parse(ConfLog["Start"])
            LogWrite(TextOutput)
            Speak(TextOutput)

            Main()
        
        else:
            TextOutput = Parse(ConfLog["NotStart"])
            LogWrite(TextOutput)
            Speak(TextOutput)
    
    else:
        print("NO CONFIG FOUND! Make sure the 'Config.toml' is in the same directory as 'SaraSortd.py'")


def Main():
    while True:
        pass


Init()