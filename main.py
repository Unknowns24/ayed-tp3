# Comision 104
# Alumnos:
# Ferrere, Santiago
# Civilotti, Genaro
# Finelli, Constantino
# Costamagna Mayol, Ricardo Luis 

import os
import pickle
import os.path
import maskpass
from datetime import date
from datetime import datetime

#**********#
#* CLASES *#
#**********#

class Usuario:
    def __init__(self):
        self.codUsuario = 0
        self.nombreUsuario = ""
        self.claveUsuario = ""
        self.tipoUsuario = ""
class Locales:
    def __init__(self):
        self.codLocal = 0
        self.nombreLocal = ""
        self.ubicacionLocal = ""
        self.rubroLocal = ""
        self.codUsuario  = 0
        self.estado = "A"
class Promocion:
    def __init__(self):
        self.codPromo = 0
        self.textoPromo = ""
        self.fechaDesdePromo = date
        self.fechaHastaPromo = date
        self.diasSemana = [0]*7
        self.estado  = ""
        self.codLocal = 0
class UsoPromocion:
    def __init__(self):
        self.codCliente = 0
        self.codPromo = 0
        self.fechaUsoPromo = date
class Novedad:
    def __init__(self):
        self.codNovedad = 0
        self.textoNovedad = ""
        self.fechaDesdePromo = date
        self.fechaHastaPromo = date
        self.tipoUsuario  = ""
        self.estado = "A"

# Declaramos "variables" que contienen codigo de colores
COLOR_RED="\033[31m"
COLOR_RESET="\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"

# Declaramos "variables" que contienen los tamaños de los campos a utilizar
USER_NAME_LENGHT = 100
USER_PASS_LENGHT = 8
USER_TYPE_LENGHT = 20

LOCAL_NAME_LENGHT = 50
LOCAL_ADDR_LENGHT = 50
LOCAL_CATG_LENGHT = 50

PROMO_TEXT_LENGHT = 200

NEW_TEXT_LENGHT = 200
NEW_TYPE_LENGHT = 20

# Declaramos "variables" de los tipos de usuarios existentes
USER_TYPE_ADMIN = "administrador"
USER_TYPE_CLIENT = "cliente"
USER_TYPE_LOCALOWNER = "dueñoLocal"

# Declaramos las "variables" de los tipos de locales que existen
LOCAL_TYPE_FOOD = "comida"
LOCAL_TYPE_PERFUME = "perfumeria"
LOCAL_TYPE_FASHION = "indumentaria"

# Declaramos las "variables" de los estados de los descuentos
DISCOUNT_STATUS_PENDING="pendiente"
DISCOUNT_STATUS_APPROVED="aceptada"
DISCOUNT_STATUS_REJECTED="rechazada"

# Declaramos "variable" para los dias de la semana
DAYS=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

# Declaramos "variable" para el comando clear
CLEAR_COMMAND = "cls"

# Declaramos la variable donde se guardaran el usuario y contraseña correctas
attempts = 0 # Variable tipo INT

# Declaramos el path a los archivos
mainPath = "C:\\tp3\\"
userFilePath = mainPath+"usuarios.dat"
localsFilePath = mainPath+"locales.dat"
promsFilePath = mainPath+"promociones.dat"
promsUseFilePath = mainPath+"uso_promociones.dat"
newsFilePath = mainPath+"novedades.dat"

# Declaramos las variables donde se guardaran los archivos logicos ya cargados
userFile = 0
localsFile = 0
promsFile = 0
promsUseFile = 0
newsFile = 0

# Declaramos donde se almacena
MY_USER = Usuario()

# Contadores para locales segun su rubro
lCategories = ["perfumeria", "indumentaria", "comida"]
lCategoriesCount = [0] * 3

# funcion abrir archivo
def openFile(filePath):
    if not os.path.exists(filePath):
        logicFile = open(filePath, "w+b")
    else:
        logicFile = open(filePath, "r+b")

    return logicFile

# funcion para setear paths si estas en un sistema posix
def setPath():
    global mainPath, userFilePath, localsFilePath, promsFilePath, promsUseFilePath, newsFilePath, CLEAR_COMMAND

    if os.name == "posix":
        CLEAR_COMMAND = "clear"
        mainPath = "./files/"
        userFilePath = mainPath+"usuarios.dat"
        localsFilePath = mainPath+"locales.dat"
        promsFilePath = mainPath+"promociones.dat"
        promsUseFilePath = mainPath+"uso_promociones.dat"
        newsFilePath = mainPath+"novedades.dat" 


# funcion para cargar archivos
def loadFiles():
    global userFile, localsFile, promsFile, promsUseFile, newsFile

    # crea la carpeta del tp3 si no existe 
    os.makedirs(mainPath, 775, True)

    userFile = openFile(userFilePath)
    if os.path.getsize(userFilePath) == 0:
        loadAdmin()

    localsFile = openFile(localsFilePath)
    if os.path.getsize(localsFilePath) > 0: 
        loadLocals()

    promsFile = openFile(promsFilePath)
    promsUseFile = openFile(promsUseFilePath)
    newsFile = openFile(newsFilePath)

# funcion para cerrar archivos
def unloadFiles():
    userFile.close()
    localsFile.close()
    promsFile.close()
    promsUseFile.close()
    newsFile.close()

# funcion para guardar un usuario en el archivo
def saveUser(user):
    userFile.seek(0, os.SEEK_END)

    user.codUsuario = str(user.codUsuario).ljust(10)
    user.tipoUsuario = user.tipoUsuario.ljust(USER_TYPE_LENGHT)
    user.claveUsuario = user.claveUsuario.ljust(USER_PASS_LENGHT)
    user.nombreUsuario = user.nombreUsuario.ljust(USER_NAME_LENGHT)

    pickle.dump(user, userFile)
    userFile.flush()

# funcion para limpiar los valores del usuario
def parseUser(user):
    user.codUsuario = int(user.codUsuario)
    user.tipoUsuario = user.tipoUsuario.strip()
    user.claveUsuario = user.claveUsuario.strip()
    user.nombreUsuario = user.nombreUsuario.strip()

    return user

# funcion para guardar un local en el archivo
def saveLocal(local, pos):
    localsFile.seek(0, os.SEEK_END)

    if pos != 0:
        localsFile.seek(pos, 0)

    local.codLocal = str(local.codLocal).ljust(10)
    local.codUsuario  = str(local.codUsuario).ljust(10)
    local.nombreLocal = local.nombreLocal.ljust(LOCAL_NAME_LENGHT)
    local.ubicacionLocal = local.ubicacionLocal.ljust(LOCAL_ADDR_LENGHT)
    local.rubroLocal = local.rubroLocal.ljust(LOCAL_CATG_LENGHT)

    pickle.dump(local, localsFile)
    localsFile.flush()

# funcion para limpiar los valores del local
def parselocal(local):
    local.codLocal = int(local.codLocal)
    local.codUsuario  = int(local.codUsuario)
    local.nombreLocal = local.nombreLocal.strip()
    local.ubicacionLocal = local.ubicacionLocal.strip()
    local.rubroLocal = local.rubroLocal.strip()

    return local

# funcion para guardar promocion en el archivo
def saveProm(prom, pos):
    promsFile.seek(0, os.SEEK_END)

    if pos != 0:
        promsFile.seek(pos, 0)

    prom.codPromo = str(prom.codPromo).ljust(10)
    prom.textoPromo = prom.textoPromo.ljust(200)
    prom.fechaDesdePromo = prom.fechaDesdePromo.ljust(10)
    prom.fechaHastaPromo = prom.fechaHastaPromo.ljust(10)
    prom.codLocal = str(prom.codLocal).ljust(10)

    pickle.dump(prom, promsFile)
    promsFile.flush()

# funcion para limpiar los valores de la promocion
def parseProm(prom):
    prom.codPromo = int(prom.codPromo)
    prom.textoPromo = prom.textoPromo.strip()
    prom.fechaDesdePromo = prom.fechaDesdePromo.strip()
    prom.fechaHastaPromo = prom.fechaHastaPromo.strip()
    prom.codLocal = int(prom.codLocal)
    
    return prom

# funcion para la carga de usuario
def loadAdmin():
    adminUser = Usuario()
    adminUser.codUsuario = 1
    adminUser.nombreUsuario = "a"#@shopping.com"
    adminUser.tipoUsuario = USER_TYPE_ADMIN
    adminUser.claveUsuario = "12345"

    saveUser(adminUser)

# funcion para cargar la cantidad de locales por rubro en lCategories
def loadLocals():
    fileSize = os.path.getsize(localsFilePath)
    localsFile.seek(0,0)

    while localsFile.tell() < fileSize:
        localsFile.tell()
        local = parselocal(pickle.load(localsFile))
        addToCategory(local.rubroLocal)

# funcion para leer opciones numericas en rango
def askValidOption(start, end):
    o = optionRange(start, end)
    while o == -1:
        o = optionRange(start, end)
    
    return o

def optionRange(start, end):
    try:
        opc = input('[?] Ingrese el indice de la opcion requerida\n')
        
        if opc == "" or opc == " ":
            return -1
        
        opc = int(opc)

        while opc > end or opc < start:
            opc = int(input('[?] Ingrese un indice de opcion valido\n'))
        return opc 
    except:
        return -1

# funciones para el menu de autenticacion:FL
def authMenuOpts():
    print('1. Ingresar con usuario registrado')
    print('2. Registrarse como cliente')
    print('3. Salir')

def authMenu():    
    authMenuOpts()
    opc = askValidOption(1, 3)

    while opc != 3:
        match opc:
            case 1: loginUser()
            case 2: registerUser(USER_TYPE_CLIENT) 
        os.system(CLEAR_COMMAND)
        authMenuOpts()
        opc = askValidOption(1, 3)

# funcion para registrar usuarios
def registerUser(uType):
    user = Usuario()
    mail = input('Ingrese un mail: ')
    invLenghtPromptText = 'Has superado el limite de caracteres('+ str(USER_NAME_LENGHT) +'), ingrese un mail valido: '

    user.codUsuario = getActualRecordsAmount(userFilePath, userFile) + 1

    while searchUserByMail(mail).nombreUsuario != "" or len(mail) > USER_NAME_LENGHT:
        while len(mail) > USER_NAME_LENGHT:
            mail = input(invLenghtPromptText)

        mail = input('Email ya registrado, pruebe con otro: ')
    
    user.nombreUsuario = mail
    user.claveUsuario = input('Ingrese una contraseña nueva(tiene que tener '+str(USER_PASS_LENGHT)+' caracteres): ')
    
    while len(user.claveUsuario) != USER_PASS_LENGHT:
        user.claveUsuario = input('La contraseña que acaba de ingresar no tiene '+str(USER_PASS_LENGHT)+' caracteres, ingrese otra: ')
    
    user.tipoUsuario = uType
    saveUser(user)
    print('Registrado correctamente')

# funciones para buscar un local
def searchPromEnginge(code):
    T = os.path.getsize(promsFilePath)
    proms = Locales()
    promsFound = False
    promsFile.seek(0,0)

    while not promsFound and promsFile.tell() < T:
        promsFile.tell()
        tmp = parseProm(pickle.load(promsFile))
        if tmp.codPromo == code:
            proms = tmp
            promsFound = True
    
    return proms

def getPromPosByCode(code):
    T = os.path.getsize(promsFilePath)
    pos = -1 
    promsFound = False
    promsFile.seek(0,0)

    while not promsFound and promsFile.tell() < T:
        p = promsFile.tell()
        tmp = parseProm(pickle.load(promsFile))
        if tmp.codPromo == code:
            pos = p
            promsFound = True
    
    return pos

def searchPromByCode(code):
    return searchPromEnginge(code)

# funciones para buscar un local
def searchLocalEnginge(code):
    T = os.path.getsize(localsFilePath)
    locals = Locales()
    localsFound = False
    localsFile.seek(0,0)

    while not localsFound and localsFile.tell() < T:
        localsFile.tell()
        tmp = parselocal(pickle.load(localsFile))
        if tmp.codLocal == code:
            locals = tmp
            localsFound = True
    
    return locals

def searchLocalByCode(code):
    return searchLocalEnginge(code)

def getLocalPosByCode(code):
    T = os.path.getsize(localsFilePath)
    pos = -1 
    localsFound = False
    localsFile.seek(0,0)

    while not localsFound and localsFile.tell() < T:
        p = localsFile.tell()
        tmp = parselocal(pickle.load(localsFile))
        if tmp.codLocal == code:
            pos = p
            localsFound = True
    
    return pos

# funciones para buscar un usuario en base a ciertos datos
def searchUserEnginge(mail, code):
    T = os.path.getsize(userFilePath)
    usr = Usuario()
    usrFound = False
    userFile.seek(0,0)

    while not usrFound and userFile.tell() < T:
        userFile.tell()
        tmp = pickle.load(userFile)
        tmp = parseUser(tmp)
        if mail != "" and tmp.nombreUsuario == mail:
            usr = tmp
            usrFound = True

        if code != 0 and tmp.codUsuario == code:
            usr = tmp
            usrFound = True
    return usr

def searchUserByMail(mail):
    return searchUserEnginge(mail, 0)

def searchUserByCode(code):
    return searchUserEnginge("", code)

# funcion para validar si el nombre del local es valido
def invalidLocalName(nombre):
    total = 0
    inicio = 0

    fileSize = os.path.getsize(localsFilePath)
    localsFile.seek(0, 0)
   
    if fileSize > 0:
        _ = pickle.load(localsFile)        
   
    singleT = localsFile.tell()
   
    if singleT != 0:
        total = fileSize // singleT

    fin = total - 1
    founded = False

    while (inicio <= fin and not founded):
        medio = (inicio + fin)//2
        localsFile.seek(medio*singleT, 0)
        l = parselocal(pickle.load(localsFile))

        if l.nombreLocal == nombre:
            founded = True
        elif l.nombreLocal < nombre:
           inicio = medio + 1
        elif l.nombreLocal > nombre:
            fin = medio - 1
    
    return founded

# funcion para ordenar las categorias de mayor a menor
def orderCategories():
    global lCategories, lCategoriesCount
            
    for i in range(0, len(lCategoriesCount) - 1):
        for r in range(0, len(lCategoriesCount)):
            if r != 2 and lCategoriesCount[i] < lCategoriesCount[r + 1]:
                auxRubs = lCategories[i]
                auxRubsCnt = lCategoriesCount[i]

                lCategories[i] = lCategories[r + 1]
                lCategoriesCount[i] = lCategoriesCount[r + 1]
                
                lCategories[r + 1] = auxRubs
                lCategoriesCount[r + 1] = auxRubsCnt

# funcion para listar locales
def listLocals():
    quantityOfLocals = getActualRecordsAmount(localsFilePath, localsFile)
    localsFile.seek(0, 0)
    
    if quantityOfLocals > 0:
        if askConfirm("Desea ver los locales guardados hasta el momento?"):
            local = parselocal(pickle.load(localsFile))

            for i in range(quantityOfLocals):
                color = COLOR_GREEN
                if local.estado != "A":
                    color = COLOR_RED

                print(f"{color}============ LOCAL Nº {str(i)} ============{COLOR_RESET}")
                print(f'Codigo local: {local.codLocal}, Nombre: {local.nombreLocal}, Ubicacion: {local.ubicacionLocal}, Rubro: {local.rubroLocal}, Estado: {local.estado} ')
                print(f"{color}===================================={COLOR_RESET}\n")
                if i < quantityOfLocals - 1:
                    local = parselocal(pickle.load(localsFile))
            _ = input("[?] Presione cualquier tecla para continuar")
    

#Procedimiento para conseguir la cantidad de registros existentes en un determinado archivo
def getActualRecordsAmount(filePath, file):
    T = os.path.getsize(filePath)
    if T == 0:
        return 0
    else:
        file.seek(0,0)
        pickle.load(file)
        singleT = file.tell()
        cant = T // singleT
        return cant

# funcion para ordenar locales por nombre
def orderLocalsByName():
    fileSize = os.path.getsize(localsFilePath)
    localsFile.seek (0, 0)
    _ = pickle.load(localsFile)
    regSize = localsFile.tell() 
    total = int(fileSize // regSize)

    if total > 1:
        for lNum in range (0, total - 1): 
            for lNumS in range(lNum + 1, total):
                localsFile.seek(lNum*regSize, 0)
                aux1 = pickle.load(localsFile)
                localsFile.seek(lNumS*regSize, 0)
                aux2 = pickle.load(localsFile)

                if (aux1.nombreLocal > aux2.nombreLocal):
                    localsFile.seek(lNum*regSize, 0)
                    pickle.dump(aux2, localsFile)
                    localsFile.seek(lNumS*regSize, 0)
                    pickle.dump(aux1, localsFile)
                    localsFile.flush()

# funcion para el index de la categoria
def getCategoryIndex(rub): # parametro rub de tipo STRING, retorna un INT
    global lCategories
    found = False
    rubIdx = 0
    while (not found and rubIdx <= len(lCategories) - 1):
        if lCategories[rubIdx] == rub:
            found = True
        else:
            rubIdx += 1
    
    return rubIdx

# funcion para añadir uno a la cuenta de la categoria
def addToCategory(cat):
    lCategoriesCount[getCategoryIndex(cat)] += 1

# funcion para restar uno a la cuenta de la categoria
def removeFromCategory(cat):
    lCategoriesCount[getCategoryIndex(cat)] +- 1

# Function para registrar locales
def newLocals():
    os.system(CLEAR_COMMAND)
    
    lName = input("[?] Ingrese el nombre del local (ingrese \".\" para salir)\n")

    # Se saca el número de locales para poder poner el codigo de del mismo de manera secuencial
    registeredLocals = 0

    while lName != ".":
        local = Locales()
        registeredLocals = registeredLocals + 1

        while invalidLocalName(lName):
            print("[-] Nombre de local en uso")
            lName = input("[?] Ingrese el nombre del local\n")

        local.nombreLocal = lName
        local.codLocal = getActualRecordsAmount(localsFilePath, localsFile) + 1
        local.ubicacionLocal = input("[?] Ingrese la ubicacion del local\n")
        
        local.rubroLocal = input(f"[?] Ingrese el rubro del local ({LOCAL_TYPE_FASHION}, {LOCAL_TYPE_FOOD}, {LOCAL_TYPE_PERFUME})\n").lower()
        while local.rubroLocal != LOCAL_TYPE_FASHION and local.rubroLocal != LOCAL_TYPE_PERFUME and local.rubroLocal != LOCAL_TYPE_FOOD:
            print("[-] Rubro invalido")
            local.rubroLocal = input(f"[?] Ingrese un rubro de local valido ({LOCAL_TYPE_FASHION}, {LOCAL_TYPE_FOOD}, {LOCAL_TYPE_PERFUME})\n").lower()

        local.codUsuario = int(input("[?] Ingrese el codigo de usuario del dueño del local\n"))
        while (searchUserByCode(local.codUsuario).tipoUsuario != USER_TYPE_LOCALOWNER):
            print("[-] El codigo de usuario ingresado no existe o no pertenece a un dueño de local")
            local.codUsuario = int(input("[?] Ingrese el codigo de usuario del dueño del local\n"))

        # sumar uno a la categoria
        addToCategory(local.rubroLocal)

        # Se guarda el nuevo local en archivo con la función "saveLocal"
        saveLocal(local, 0)
        orderLocalsByName()

        os.system(CLEAR_COMMAND)
        lName = input("[?] Ingrese el nombre del siguiente local (ingrese \".\" para salir)\n")
    
    # flush file
    localsFile.flush()

    #valida que al menos se haya ejecutado una vez el while
    if registeredLocals > 0:
        # Si se ingreso al menos un local nuevo se reordenan las categorias
        orderCategories()

        os.system(CLEAR_COMMAND)
        print("[+] Locales por rubro: ")

        for rubro in range(0, len(lCategories)):
            print(" " + lCategories[rubro] + ": " + str(lCategoriesCount[rubro]))

def askConfirm(texto): #parametro localIndex tipo INT y parametro texto de tipo STRING
    opt = input("[?] " + texto + " (S - si, N - no)\n").lower()
    while opt != "s" and opt != "n":
        print("[-] Opcion invalida")
        opt = input("[?] " + texto + " (S - si, N - no)\n").lower()

    return opt == "s" or opt == "si"

def enableLocalPrompt(localData, posL): #parametro localIndex tipo INT
    if askConfirm("Desea activar nuevamente este local"):
        localData.estado = 'A'
        saveLocal(localData, posL)
        
def disableLocalPrompt(localData, posL): #parametro localIndex tipo INT
    if askConfirm("Desea eliminar este local"):
        localData.estado = 'B'
        saveLocal(localData, posL)

def modifyLocal():
    lCode = input("[?] Ingrese el codigo del local\n")
    pos = getLocalPosByCode(int(lCode))

    while pos == -1:
        print("[-] Codigo de local invalido")
        lCode = input("[?] Ingrese el codigo del local\n")
        pos = getLocalPosByCode(int(lCode))

    localData = searchLocalByCode(int(lCode))

    if localData.estado != "A":
        enableLocalPrompt(localData, pos)
    
    if localData.estado == "A":
        localData.nombreLocal = input("[?] Ingrese el nombre del local (ingrese \".\" para salir)\n")
        
        if localData.nombreLocal != ".":
            while invalidLocalName(localData.nombreLocal):
                print("[-] Nombre de local en uso")
                localData.nombreLocal = input("[?] Ingrese el nombre del local\n")

            localData.ubicacionLocal = input("[?] Ingrese la ubicacion del local\n")

            r = input("[?] Ingrese el rubro del local\n").lower()
            while r != LOCAL_TYPE_FASHION and r != LOCAL_TYPE_FOOD and r != LOCAL_TYPE_PERFUME:
                print("[-] Rubro invalido")
                r = input("[?] Ingrese el rubro del local\n").lower()

            localData.codUsuario = int(input("[?] Ingrese el codigo de usuario del dueño del local\n"))
            while (searchUserByCode(localData.codUsuario).tipoUsuario != USER_TYPE_LOCALOWNER):
                print("[-] El codigo de usuario ingresado no existe o no pertenece a un dueño de local")
                localData.codUsuario = int(input("[?] Ingrese el codigo de usuario del dueño del local\n"))

            # Si se modifica el rubro, se resta uno al actual y se suma uno al nuevo
            if r != localData.rubroLocal:
                removeFromCategory(localData.rubroLocal)
                localData.rubroLocal = r
                addToCategory(localData.rubroLocal)

            saveLocal(localData, pos)

            orderCategories()
            orderLocalsByName()

def deleteLocal():
    lCode = input("[?] Ingrese el codigo del local\n")
    pos = getLocalPosByCode(int(lCode))

    while pos == -1:
        print("[-] Codigo de local invalido")
        lCode = input("[?] Ingrese el codigo del local\n")
        pos = getLocalPosByCode(int(lCode))

    localData = searchLocalByCode(int(lCode))

    if localData.estado != 'A':
        print("[-] Este local ya fue dado de baja")

    if localData.estado == 'A':
        disableLocalPrompt(localData, pos)
        print("[+] Local eliminado")
    
def localMaps():
    fileSize = os.path.getsize(localsFilePath)
    localsFile.seek (0, 0)
    _ = pickle.load(localsFile)
    regSize = localsFile.tell() 
    total = int(fileSize / regSize)  
    
    for fila in range(0,10):
        inicio = 5 * fila
        fin = 5 * (fila + 1)
        
        print("+--+--+--+--+--+")
        for local in range(inicio, fin):
            lId = "0"
            if local < total:
                localsFile.seek(local*regSize, 0)
                l = parselocal(pickle.load(localsFile))
                color = COLOR_GREEN
                if l.estado != "A":
                    color = COLOR_RED

                if l.codLocal < 10:
                    lId = color + lId + str(l.codLocal) + COLOR_RESET
                else:
                    lId = color + str(l.codLocal) + COLOR_RESET
            else:
                lId = lId +"0"

            if local != fin - 1:
                print(f"|{str(lId)}", end="")
            else:
                print(f"|{str(lId)}|")
    print("+--+--+--+--+--+")
    if total > 50:
        print("proximamente se habilitara un mapa con los demas locales")

# Funcion que muestra el menu de Gestion de locales
def localManageMenuOpts():
    print("a) Crear locales")
    print("b) Modificar local")
    print("c) Eliminar local")
    print("d) Mapa de locales")
    print("e) Volver")

def localManage():
    localManageMenuOpts()
    opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()

    while opcion == "" or ord(opcion) != 101: # cuando la opcion sea distinta de E 
        while (opcion == "" or (ord(opcion) < 97 or ord(opcion) > 101)): # Valida que la opcion sea una letra entre A y E
            print("[-] La opcion ingresada no es valida")
            opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()

        match ord(opcion):
            case 97:
                listLocals()
                newLocals()
            case 98:
                listLocals()
                modifyLocal()
            case 99:
                listLocals()
                deleteLocal()
            case 100: 
                localMaps()
        
        localManageMenuOpts()
        opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()

# Funcion que se encarga de mostrar el menu de Gestion de novedades
def newsManageMenuOpts():
    print("a) Crear novedades")
    print("b) Modificar novedad")
    print("c) Eliminar novedad")
    print("d) Ver reporte de novedades")
    print("e) Volver")

def newsManage():
    newsManageMenuOpts()
    opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()
    
    while opcion == "" or ord(opcion) != 101: # cuando la opcion sea distinta de E 
        while (opcion == "" or (ord(opcion) < 97 or ord(opcion) > 101)): # Valida que la opcion sea una letra entre A y E
            print("[-] La opcion ingresada no es valida")
            opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()

        print("[-] Diagramado en chapin...")
        newsManageMenuOpts()
        opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()

# Funcion que se encarga del menu principal
def adminMenuOpts():
    print("1. Gestion de locales")
    print("2. Crear cuentas de dueños de locales")
    print("3. Aprobar / Denegarsolicitud de descuento")
    print("4. Gestión de novedades")
    print("5. Reporte de utilización de descuentos")
    print("0. Cerrar sesion")
    
def adminMenu():
    adminMenuOpts()
    opcion = askValidOption(0, 5)

    while opcion != 0:
        match opcion:
            case 1:
                os.system(CLEAR_COMMAND)
                localManage()
            case 2:
                os.system(CLEAR_COMMAND)
                registerUser(USER_TYPE_LOCALOWNER)
            case 3:
                os.system(CLEAR_COMMAND)
                manageDiscounts()
            case 4:
                os.system(CLEAR_COMMAND)
                newsManage()
            case 5:
                os.system(CLEAR_COMMAND)
                print("[-] En construccion...")

        adminMenuOpts()
        opcion = askValidOption(0, 5)

# Funcion que se encarga del menu para dueños de local
def localOwnerMenuOpts():
    print("1. Crear descuento")
    print("2. Reporte de uso de descuentos")
    print("3. Ver novedades")
    print("0. Cerrar sesion")

def localOwnerMenu():
    localOwnerMenuOpts()
    opc = askValidOption(0, 3)

    while opc != 0:
        os.system(CLEAR_COMMAND)
        match opc:
            case 1: createDiscount()
            case 2: reportOfUsedDiscount()
            case 3: print("[-] Diagramado en chapin")

        localOwnerMenuOpts()
        opc = askValidOption(0, 3)

# Funcion que se encarga del menu para dueños de local
def clientMenuOpts():
    print("1. Buscar descuentos en locales")
    print("2. Solicitar descuento")
    print("3. Ver novedades")
    print("0. Cerrar sesion")

def clientMenu():
    clientMenuOpts()
    opcion = askValidOption(0, 3)

    while opcion != 0:
        os.system(CLEAR_COMMAND)
        print("[-] En construccion...")

        clientMenuOpts()
        opcion = askValidOption(0, 3)

        
    print("[-] El programa ha finalizado")

# funcion que retorna un booleano dependiendo si el usuario ingresado existe
def validLogin(mail, passwd): # parametro mail y passwd de tipo string
    global MY_USER
    logged = False

    user = searchUserByMail(mail)
    if user.nombreUsuario == "":
        return logged

    if user.claveUsuario == passwd:
        logged = True
        MY_USER = user

    return logged; 

# Funcion encargada del inicioSesion de usuarios
def loginUser():
    global attempts
    os.system(CLEAR_COMMAND)

    username = input("[?] Ingrese su nombre de usuario: ")
    password = maskpass.askpass("[?] Ingrese su contraseña: ")
    
    while ((not validLogin(username, password)) and attempts <= 3):
        if attempts > 0 and attempts < 3:
            print("[-] Intentos fallidos: " + str(attempts) + "/3")
            username = input("[?] Ingrese su nombre de usuario: ")
            password = maskpass.askpass("[?] Ingrese su contraseña: ")
        elif attempts >= 3:
            os.system(CLEAR_COMMAND)
            print("[-] Demasiados intentos fallidos, el programa se cerrara!")
            
        attempts = attempts + 1

    if MY_USER.nombreUsuario != "":
        os.system(CLEAR_COMMAND)
        print("[+] Sesion iniciada como " + MY_USER.tipoUsuario)
        
        match MY_USER.tipoUsuario:
            case "administrador":
                adminMenu()
            case "dueñoLocal":
                localOwnerMenu()
            case "cliente":
                clientMenu()

def createDiscount():
    listDiscounts(True, True, False)
    disc = Promocion()

    localCode = int(input('[?] Ingrese un codigo de local para crear un descuento (ingrese 0 para salir): '))

    while localCode != 0:
        currentL = searchLocalByCode(localCode)
        
        while (currentL.codUsuario != MY_USER.codUsuario) and localCode != 0 :
            localCode = int(input('[?] Ese codigo de local no pertenece a ninguno de tus locales, ingrese uno valido: '))
            currentL = searchLocalByCode(localCode)

        if currentL.estado != "A":
            print("[-] Local dado de baja, reactivelo para crear descuentos")
            localCode = 0

        if localCode != 0:
            disc.codLocal = localCode
            disc.textoPromo = input('[?] Ingrese la descripcion del descuento: ')
            disc.estado = DISCOUNT_STATUS_PENDING
            disc.fechaDesdePromo = askDate("[?] Ingrese la fecha de inicio del descuento")
            disc.fechaHastaPromo = askDate("[?] Ingrese la fecha de finalizacion del descuento")

            while datetime.strptime(disc.fechaDesdePromo, '%d/%m/%Y').timestamp() >= datetime.strptime(disc.fechaHastaPromo, '%d/%m/%Y').timestamp(): 
                print("[-] Fechas de promocion invalida, el inicio no puede ser despues del final")
                disc.fechaDesdePromo = askDate("[?] Ingrese la fecha de inicio del descuento")
                disc.fechaHastaPromo = askDate("[?] Ingrese la fecha de finalizacion del descuento")

            disc.codPromo = getActualRecordsAmount(promsFilePath, promsFile) + 1
            
            for dayIndex in range(0, len(DAYS)):
                print(f"[?] El descuento es valido el dia {DAYS[dayIndex]}? (1 - si, 0 - no)")
                valid = askValidOption(0, 1)
                disc.diasSemana[dayIndex] = valid
            
            saveProm(disc)
            
            localCode = int(input('[?] Ingrese un codigo de local para crear un descuento(para volver ingrese 0): '))

def listDiscounts(onlyFromActualUser, onlyOnDate, onlyPending):
    quantityOfPromotions = getActualRecordsAmount(promsFilePath, promsFile)
    promsFile.seek(0, 0)
    
    if quantityOfPromotions > 0:
        print("Promociones activas de tus locales: ")
        for i in range(quantityOfPromotions):
            if i < quantityOfPromotions:
                prom = parseProm(pickle.load(promsFile))
                showNoPending = True

                if onlyPending:
                    showNoPending = prom.estado == DISCOUNT_STATUS_PENDING

                if showNoPending:
                    if not onlyOnDate or (datetime.strptime(prom.fechaDesdePromo, '%d/%m/%Y').timestamp() <= datetime.now().timestamp() and datetime.strptime(prom.fechaHastaPromo, '%d/%m/%Y').timestamp() >= datetime.now().timestamp()):
                        local = searchLocalByCode(prom.codLocal)
                        showAll = True

                        if onlyFromActualUser:
                            showAll = local.codUsuario == MY_USER.codUsuario

                        if showAll and local.estado == "A":
                            color = COLOR_GREEN
                            if prom.estado == DISCOUNT_STATUS_PENDING:
                                color = COLOR_YELLOW
                            elif prom.estado == DISCOUNT_STATUS_REJECTED: 
                                color = COLOR_RED
                                

                            availableDays = ""

                            for i in range(0, 6):
                                if prom.diasSemana[i] == 1:
                                    space = " "
                                    if availableDays == "":
                                        space = ""

                                    availableDays = f"{availableDays}{space}{DAYS[i]}," 

                            availableDays = availableDays[:-1]

                            print(f"{color}==========================={COLOR_RESET}")
                            print(f"Codigo del descuento: {str(prom.codPromo)}")
                            print(f"Codigo del local: {str(prom.codLocal)}")
                            if onlyPending:
                                print(f"Nombre del local: {local.nombreLocal}")
                            print(f"Descripcion del descuento: {prom.textoPromo}")
                            print(f"Fecha inicio: {prom.fechaDesdePromo}")
                            print(f"Fecha finalizacion: {prom.fechaHastaPromo}")
                            print(f"Dias disponibles: {availableDays}")
                            print(f"Estado: {color}{prom.estado}{COLOR_RESET}")
                            print(f"{color}==========================={COLOR_RESET}")


def askDate(txt):
    finalDate = _askDatesLogic(txt)
    while finalDate == "":
        print('[-] Usted ha ingresado una fecha invalida, intente de nuevo')
        finalDate = _askDatesLogic(txt)
    
    return finalDate

def _askDatesLogic(txt):
    try:
        dateInput = input(f'{txt} (dd/mm/aaaa): ')
        date = datetime.strptime(dateInput, '%d/%m/%Y')
        now = datetime.now()

        if date.timestamp() < datetime.strptime(f"{now.day}/{now.month}/{now.year}", '%d/%m/%Y').timestamp():
            print("[-] La fecha no puede ser anterior al dia de hoy")
            return ""

        return dateInput
    except ValueError:
        return ""
    
def manageDiscounts():
    listDiscounts(False, False, True)
    codProm = int(input('[?] Ingrese un codigo de descuento: '))
    prom = searchPromByCode(codProm)

    while prom.codPromo != codProm or prom.estado != DISCOUNT_STATUS_PENDING:
        codProm = int(input('[?] Codigo de descuento invalido, ingrese un codigo de descuento: '))
        prom = searchPromByCode(codProm)
    
    pos = getPromPosByCode(codProm)
    
    print("[?] Que accion quiere realizar con el descuento (1 - aceptar, 0 - rechazar)")
    opt = askValidOption(0, 1)
    state = DISCOUNT_STATUS_APPROVED
    if opt == 0:
        state = DISCOUNT_STATUS_REJECTED

    prom.estado = state
    saveProm(prom, pos)
    
def reportOfUsedDiscount():
    print("TODO:")

# Programa Principal
def entryPoint():
    print('''
███████╗██╗  ██╗ ██████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗ 
██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ 
███████╗███████║██║   ██║██████╔╝██████╔╝██║██╔██╗ ██║██║  ███╗
╚════██║██╔══██║██║   ██║██╔═══╝ ██╔═══╝ ██║██║╚██╗██║██║   ██║
███████║██║  ██║╚██████╔╝██║     ██║     ██║██║ ╚████║╚██████╔╝
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
    \n''')
        
    setPath()
    loadFiles()
    authMenu()
    print("[-] El programa se esta cerrando")
    unloadFiles()

entryPoint()
