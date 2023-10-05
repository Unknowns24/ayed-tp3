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
        self.diasSemana = [""]*6
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

# Declaramos variables que contienen los tamaños de los campos a utilizar
USER_NAME_LENGHT = 100
USER_PASS_LENGHT = 8
USER_TYPE_LENGHT = 20

LOCAL_NAME_LENGHT = 50
LOCAL_ADDR_LENGHT = 50
LOCAL_CATG_LENGHT = 50

PROMO_TEXT_LENGHT = 200

NEWNESS_TEXT_LENGHT = 200
NEWNESS_TYPE_LENGHT = 20

# Declaramos variables de los tipos de usuarios existentes
USER_TYPE_ADMIN = "administrador"
USER_TYPE_CLIENT = "cliente"
USER_TYPE_LOCALOWNER = "cliente"

# Declaramos la variable donde se guardaran el usuario y contraseña correctas
attempts = 0 # Variable tipo INT

# Declaramos el path a los archivos
mainPath = "C:\\tp3\\"
userFilePath = mainPath+"usuarios.dat"
localsFilePath = mainPath+"locales.dat"
promsFilePath = mainPath+"promociones.dat"
promsUseFilePath = mainPath+"uso_promociones.dat"
newnessFilePath = mainPath+"novedades.dat"

# Declaramos las variables donde se guardaran los archivos logicos ya cargados
userFile = 0
localsFile = 0
promsFile = 0
promsUseFile = 0
newnessFile = 0

# Declaramos variable sobre el usuario
MY_USER = -1 # Variable tipo INT

# contador global de locales
lCount = 0 # Variables tipo INT

# Contadores para locales segun su rubro
lRubs = ["perfumeria", "indumentaria", "comida"]
lRubsCount = [0] * 3

# funcion abrir archivo
def openFile(filePath):
    exists = False 

    if not os.path.exists(filePath):
        logicFile = open(filePath, "w+b")
    else:
        logicFile = open(filePath, "r+b")
        exists = True

    return logicFile, exists


# funcion para cargar archivos
def loadFiles():
    global userFile, localsFile, promsFile, promsUseFile, newnessFile
    
    # crea la carpeta del tp3 si no existe 
    os.makedirs(mainPath, 775, True)

    userFile, exists = openFile(userFilePath)
    if not exists:
        loadAdmin()

    localsFile, _ = openFile(localsFilePath)
    promsFile, _ = openFile(promsFilePath)
    promsUseFile, _ = openFile(promsUseFilePath)
    newnessFile, _ = openFile(newnessFilePath)
    
# funcion para la carga de usuario
def loadAdmin():
    adminUser = Usuario()
    adminUser.codUsuario = 1
    adminUser.nombreUsuario = "admin@shopping".ljust(USER_NAME_LENGHT)
    adminUser.tipoUsuario = USER_TYPE_ADMIN.ljust(USER_TYPE_LENGHT)
    adminUser.claveUsuario = "12345678"

    pickle.dump(adminUser, userFile)
    userFile.flush()

# funcion para leer opciones numericas en rango
def optionRange(inicio, fin):
    opc = int(input('Elije una opcion: '))
    while opc > fin or opc < inicio:
        opc = int(input('Elije una opcion valida: '))
    return opc 

# funciones para el menu de autenticacion:
def authMenuOpts():
    print('1. Ingresar con usuario registrado')
    print('2. Registrarse como cliente')
    print('3. Salir')

def authMenu():    
    opc = optionRange(1,3)
    authMenuOpts()

    while opc != 3:
        match opc:
            case 1: loginUser()
            case 2: registerUser() 
        os.system('cls')
        authMenuOpts()
        opc = optionRange(1,3)
    print('Saliendo...')

# funcion para registrar usuarios
def registerUser():
    user = Usuario()
    mail = input('Ingrese su mail: ')
    invLenghtPromptText = 'Has superado el limite de caracteres('+ str(USER_NAME_LENGHT) +'), ingrese un mail valido: '

    while searchUserByMail(mail).nombreUsuario != "" or len(mail) > USER_NAME_LENGHT:
        while len(mail) > USER_NAME_LENGHT:
            mail = input(invLenghtPromptText)

        mail = input('Email ya registrado, pruebe con otro: ')
    
    user.nombreUsuario = mail.ljust(USER_NAME_LENGHT)
    user.claveUsuario = input('Ingrese una contraseña nueva(tiene que tener '+str(USER_PASS_LENGHT)+' caracteres): ')
    
    while len(user.claveUsuario) != USER_PASS_LENGHT:
        user.claveUsuario = input('La contraseña que acaba de ingresar no tiene '+str(USER_PASS_LENGHT)+' caracteres, ingrese otra: ')
    
    user.tipoUsuario = 'cliente'.ljust(USER_TYPE_LENGHT)
    pickle.dump(user, userFile)
    userFile.flush()
    print('Registrado correctamente')

# funcion para buscar un email dentro del archivo de usuarios
def searchUserByMail(mail):
    T = os.path.getsize(userFilePath)
    usr = Usuario()
    usrFound = False
    userFile.seek(0,0)

    while not usrFound and userFile.tell() < T:
        # lee puntero
        userFile.tell()

        # carga contenido
        tmp = pickle.load(userFile)
        
        # chequea si el nombre es igual al mail
        if tmp.nombreUsuario == mail:
            usrFound = True
        
        usr = tmp

    return usr
    

# funcion que retorna un booleano dependiendo si el codigo de usuario ingresado es dueño de local
def isLocalOwner(userCode): # parametro userCode tipo INT
    global USERS
    global USERS_CODE
    founded = False
    isOwner = False
    uIndex = 0

    while (not founded and uIndex <= 3):
        if USERS_CODE[uIndex] == userCode:
            founded = True
            if USERS[uIndex][2] == "dueñoLocal":
                isOwner = True
        else:
            uIndex = uIndex + 1
    
    return isOwner;
    
def nombreInvalido(nombre):
    global lCount
    inicio = 0
    fin = lCount - 1
    founded = False

    while (inicio <= fin and not founded):
        medio = (inicio + fin)//2
        if LOCALES[medio][0] == nombre:
            founded = True
        elif LOCALES[medio][0] < nombre:
           inicio = medio + 1
        elif LOCALES[medio][0] > nombre:
            fin = medio - 1
    
    return founded
            
def ordenarRubros():
    global lRubs
    global lRubsCount
            
    for i in range(0, len(lRubsCount) - 1):
        for r in range(0, len(lRubsCount)):
            if r != 2 and lRubsCount[i] < lRubsCount[r + 1]:
                auxRubs = lRubs[i]
                auxRubsCnt = lRubsCount[i]

                lRubs[i] = lRubs[r + 1]
                lRubsCount[i] = lRubsCount[r + 1]
                
                lRubs[r + 1] = auxRubs
                lRubsCount[r + 1] = auxRubsCnt

def verLocalesPrompt():
    global lCount;
    global LOCALES
    global LOCALES_CODE

    if pedirConfirmacion("Desea ver los locales guardados hasta el momento") and lCount > 0:
        for local in range(0, lCount):
            print("Local " + str(local) + ") nombre: " + LOCALES[local][0] + ", ubicacion: " + LOCALES[local][1] + ", rubro: " + LOCALES[local][2] + " - Estado: " + LOCALES[local][3] + ", codigo del local: " + str(LOCALES_CODE[local][0]) + ", codigo del dueño: " + str(LOCALES_CODE[local][1]))

def ordenarAlfabeticamente():
    global LOCALES
    global LOCALES_CODE
    global lCount

    if lCount > 1:
        for lNum in range (0, lCount - 1): 
            for lNumS in range(lNum + 1, lCount):
                if (LOCALES[lNum][0] > LOCALES[lNumS][0]):
                    auxLocales = LOCALES[lNum]
                    auxLocalesCode = LOCALES_CODE[lNum]
        
                    LOCALES[lNum] = LOCALES[lNumS] 
                    LOCALES_CODE[lNum] = LOCALES_CODE[lNumS] 
        
                    LOCALES[lNumS] = auxLocales
                    LOCALES_CODE[lNumS] = auxLocalesCode

def conseguirIndiceRub(rub): # parametro rub de tipo STRING, retorna un INT
    global lRubs
    founded = False
    rubIdx = 0
    while (not founded and rubIdx <= len(lRubs) - 1):
        if lRubs[rubIdx] == rub:
            founded = True
        else:
            rubIdx += 1
    
    return rubIdx


# Function para registrar locales
def registroLocales():
    os.system('cls')
    global lCount
    global lRubs
    global LOCALES
    global LOCALES_CODE
    
    lName = input("[?] Ingrese el nombre del local (ingrese \".\" para salir)\n")

    while lName != ".":
        while nombreInvalido(lName):
            print("[-] Nombre de local en uso")
            lName = input("[?] Ingrese el nombre del local\n")

        lAddress = input("[?] Ingrese la ubicacion del local\n")

        lHeading = input("[?] Ingrese el rubro del local\n").lower()
        while lHeading != "indumentaria" and lHeading != "perfumeria" and lHeading != "comida":
            print("[-] Rubro invalido")
            lHeading = input("[?] Ingrese el rubro del local\n").lower()

        lUserCode = int(input("[?] Ingrese el codigo de usuario del dueño del local\n"))
        while (not isLocalOwner(lUserCode)):
            print("[-] El codigo de usuario ingresado no existe o no pertenece a un dueño de local")
            lUserCode = int(input("[?] Ingrese el codigo de usuario del dueño del local\n"))

        # Se registra el local
        LOCALES[lCount] = [lName, lAddress, lHeading, "A"]
        LOCALES_CODE[lCount] = [lCount + 1, lUserCode]

        lCount = lCount + 1
        if lHeading == "indumentaria":
            lRubsCount[conseguirIndiceRub("indumentaria")] += 1
        elif lHeading == "perfumeria":
            lRubsCount[conseguirIndiceRub("perfumeria")] += 1
        else: 
            lRubsCount[conseguirIndiceRub("comida")] += 1



        os.system('cls')
        lName = input("[?] Ingrese el nombre del siguiente local (ingrese \".\" para salir)\n")

    #valida que al menos se haya ejecutado una vez el while
    if lCount > 0:
        # Si se ingresaron al menos dos locales se los ordena alfabeticamente
        ordenarAlfabeticamente()
        ordenarRubros()

        os.system('cls')
        print("[+] Locales por rubro: ")

        for rubro in range(0, len(lRubs)):
            print(" " + lRubs[rubro] + ": " + str(lRubsCount[rubro]))

def conseguirIndiceLocal(code): #parametro code tipo INT
    global lCount
    global LOCALES_CODE
    founded = False

    if code <= 0 or code > lCount:
        return -1

    count = 0
    while (count >= 0 and count <= lCount - 1) and not founded:
        if(LOCALES_CODE[count][0] == code):
            founded = True;
        else:
            count += 1

    if LOCALES_CODE[count][0] == code:
        return count
    else:
        return -1


def pedirConfirmacion(texto): #parametro localIndex tipo INT y parametro texto de tipo STRING
    global LOCALES

    opt = input("[?] " + texto + " (S - si, N - no)\n").lower()
    while opt != "s" and opt != "n":
        print("[-] Opcion invalida")
        opt = input("[?] " + texto + " (S - si, N - no)\n").lower()

    return opt == "s"

def activarLocalPrompt(localIndex): #parametro localIndex tipo INT
    global LOCALES
    if pedirConfirmacion("Desea activar nuevamente este local"):
        LOCALES[localIndex][3] = 'A'

def desactivarLocalPrompt(localIndex): #parametro localIndex tipo INT
    global LOCALES
    if pedirConfirmacion("Desea eliminar este local"):
        LOCALES[localIndex][3] = 'B'


def localActivo(localIndex): #parametro localIndex tipo INT
    global LOCALES
    return LOCALES[localIndex][3] == 'A'

def modificarLocal():
    global LOCALES
    global LOCALES_CODE
    global lRubs

    lCode = input("[?] Ingrese el codigo del local\n")
    localIndex = conseguirIndiceLocal(int(lCode))

    while localIndex == -1:
        print("[-] Codigo de local invalido")
        lCode = input("[?] Ingrese el codigo del local\n")
        localIndex = conseguirIndiceLocal(int(lCode))

    if not localActivo(localIndex):
        activarLocalPrompt(localIndex)
    
    if localActivo(localIndex):
        lName = input("[?] Ingrese el nombre del local (ingrese \".\" para salir)\n")

        while nombreInvalido(lName):
            print("[-] Nombre de local en uso")
            lName = input("[?] Ingrese el nombre del local\n")

        lAddress = input("[?] Ingrese la ubicacion del local\n")

        lHeading = input("[?] Ingrese el rubro del local\n").lower()
        while lHeading != "indumentaria" and lHeading != "perfumeria" and lHeading != "comida":
            print("[-] Rubro invalido")
            lHeading = input("[?] Ingrese el rubro del local\n").lower()

        lUserCode = int(input("[?] Ingrese el codigo de usuario del dueño del local\n"))
        while (not isLocalOwner(lUserCode)):
            print("[-] El codigo de usuario ingresado no existe o no pertenece a un dueño de local")
            lUserCode = int(input("[?] Ingrese el codigo de usuario del dueño del local\n"))

        # Si se modifica el rubro, se resta uno al actual y se suma uno al nuevo
        if LOCALES[localIndex][2] != lHeading:
            lRubsCount[conseguirIndiceRub(LOCALES[localIndex][2])] -= 1

            if lHeading == "indumentaria":
                lRubsCount[conseguirIndiceRub("indumentaria")] += 1
            elif lHeading == "perfumeria":
                lRubsCount[conseguirIndiceRub("perfumeria")] += 1
            else: 
                lRubsCount[conseguirIndiceRub("comida")] += 1

        
        LOCALES[localIndex] = [lName, lAddress, lHeading, "A"]
        LOCALES_CODE[localIndex] = [LOCALES_CODE[localIndex][0], lUserCode]
        
        ordenarRubros()
        ordenarAlfabeticamente()

def eliminarLocal():
    global LOCALES
    global LOCALES_CODE

    lCode = input("[?] Ingrese el codigo del local\n")
    localIndex = conseguirIndiceLocal(int(lCode))

    while localIndex == -1:
        print("[-] Codigo de local invalido")
        lCode = input("[?] Ingrese el codigo del local\n")
        localIndex = conseguirIndiceLocal(int(lCode))

    if not localActivo(localIndex):
        print("[-] Este local ya fue dado de baja")

    if localActivo(localIndex):
        desactivarLocalPrompt(localIndex)
        print("[+] Local eliminado")
    
def mapaLocales():
    global LOCALES_CODE
    
    for fila in range(0,10):
        inicio = 5 * fila
        fin = 5 * (fila + 1)
        
        print("+--+--+--+--+--+")
        for local in range(inicio, fin):
            lId = str(LOCALES_CODE[local][0])
            if LOCALES_CODE[local][0] < 10:
                lId = "0"+lId

            if local != fin - 1:
                print("|"+str(lId), end="")
            else:
                print("|"+str(lId)+"|")
    print("+--+--+--+--+--+")
    
# Funcion que muestra el menu de Gestion de locales
def gestionLocales():
    print('''
a) Crear locales
b) Modificar local
c) Eliminar local
d) Mapa de locales
e) Volver
    ''')

    opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()

    while opcion == "" or ord(opcion) != 101: # cuando la opcion sea distinta de E 
        while (opcion == "" or (ord(opcion) < 97 or ord(opcion) > 101)): # Valida que la opcion sea una letra entre A y E
            print("[-] La opcion ingresada no es valida")
            opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()

        match ord(opcion):
            case 97:
                verLocalesPrompt()
                registroLocales()
            case 98:
                verLocalesPrompt()
                modificarLocal()
            case 99:
                verLocalesPrompt()
                eliminarLocal()
            case 100: 
                mapaLocales()
        
        print('''
a) Crear locales
b) Modificar local
c) Eliminar local
d) Mapa de locales
e) Volver
        ''')
        opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()
    

# Funcion que se encarga de mostrar el menu de Gestion de novedades
def gestionNovedades():
    print('''
a) Crear novedades
b) Modificar novedad
c) Eliminar novedad
d) Ver reporte de novedades
e) Volver
    ''')

    opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()
    
    while opcion == "" or ord(opcion) != 101: # cuando la opcion sea distinta de E 
        while (opcion == "" or (ord(opcion) < 97 or ord(opcion) > 101)): # Valida que la opcion sea una letra entre A y E
            print("[-] La opcion ingresada no es valida")
            opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()

        match ord(opcion):
            case 97:
                print("[-] En construccion...")
            case 98:
                print("[-] En construccion...")
            case 99:
                print("[-] En construccion...")
            case 100:
                print("[-] En construccion...")
        
        opcion = input("[?] Ingrese el indice de la opcion requerida\n").lower()


# Funcion que se encarga del menu principal
def menuPrincipal():
    print('''
1. Gestion de locales
2. Crear cuentas de dueños de locales
3. Aprobar / Denegarsolicitud de descuento
4. Gestión de novedades
5. Reporte de utilización de descuentos
0. Salir
    ''')

    opcion = int(input("[?] Ingrese el indice de la opcion requerida\n"))

    while opcion != 0:
        # Creamos un bucle que pida nuevamente la opcion en caso de que 
        # sea incorrecta hasta que una opcion valida sea ingresada.
        while (opcion < 0 or opcion > 5):
            print("[-] La opcion ingresada no es valida")
            opcion = input("[?] Ingrese el indice de la opcion requerida\n")

        match opcion:
            case 1:
                os.system('cls')
                gestionLocales()
            case 2:
                os.system('cls')
                print("[-] En construccion...")
            case 3:
                os.system('cls')
                print("[-] En construccion...")
            case 4:
                os.system('cls')
                gestionNovedades()
            case 5:
                os.system('cls')
                print("[-] En construccion...")

        print('''
1. Gestion de locales
2. Crear cuentas de dueños de locales
3. Aprobar / Denegarsolicitud de descuento
4. Gestión de novedades
5. Reporte de utilización de descuentos
0. Salir
        ''')
        opcion = int(input("[?] Ingrese el indice de la opcion requerida\n"))
        
    print("[-] El programa ha finalizado")

# Funcion que se encarga del menu para dueños de local
def menuDLocal():
    print('''
1. Gestión de Descuentos
    a) Crear descuento para mi local
    b) Modificardescuentodemilocal
    c) Eliminar descuento de mi local
    d) Volver
2. Aceptar / Rechazar pedido de descuento
3. Reporte de uso de descuentos
0. Salir
    ''')

    opcion = ord(input("[?] Ingrese el indice de la opcion requerida\n").lower())

    while opcion != 48:
        # Creamos un bucle que pida nuevamente la opcion en caso de que 
        # sea incorrecta hasta que una opcion valida sea ingresada.
        while ((opcion < 48 or opcion > 51) and (opcion < 97 or opcion > 100)):
            print("[-] La opcion ingresada no es valida")
            opcion = ord(input("[?] Ingrese el indice de la opcion requerida\n")).lower()

        os.system('cls')
        print("[-] En construccion...")

        print('''
1. Gestión de Descuentos
    a) Crear descuento para mi local
    b) Modificardescuentodemilocal
    c) Eliminar descuento de mi local
    d) Volver
2. Aceptar / Rechazar pedido de descuento
3. Reporte de uso de descuentos
0. Salir
        ''')
        opcion = ord(input("[?] Ingrese el indice de la opcion requerida\n").lower())
        
    print("[-] El programa ha finalizado")

# Funcion que se encarga del menu para dueños de local
def menuCliente():
    print('''
1. Registrarme
2. Buscar descuentos en locales
3. Solicitar descuento
4. Ver novedades
0. Salir
    ''')

    opcion = int(input("[?] Ingrese el indice de la opcion requerida\n"))

    while opcion != 0:
        # Creamos un bucle que pida nuevamente la opcion en caso de que 
        # sea incorrecta hasta que una opcion valida sea ingresada.
        while (opcion < 0 or opcion > 4):
            print("[-] La opcion ingresada no es valida")
            opcion = ord(input("[?] Ingrese el indice de la opcion requerida\n"))

        os.system('cls')
        print("[-] En construccion...")

        print('''
1. Registrarme
2. Buscar descuentos en locales
3. Solicitar descuento
4. Ver novedades
0. Salir
        ''')
        opcion = int(input("[?] Ingrese el indice de la opcion requerida\n"))
        
    print("[-] El programa ha finalizado")

# funcion que retorna un booleano dependiendo si el usuario ingresado existe
def loginValido(user, passwd): # parametro user y passwd de tipo string
    global USERS
    global MY_USER_INDEX

    logged = False
    uIndex = 0

    # Recorremos los usuarios hasta terminarlos o hasta encontrar el que fue usado
    while (not logged and uIndex <= 3):
        if USERS[uIndex][0] == user and USERS[uIndex][1] == passwd:
            logged = True
            MY_USER_INDEX = uIndex
        uIndex = uIndex + 1
    
    return logged; 

# Funcion encargada del inicioSesion de usuarios
def loginUser():
    global attempts

    os.system('cls')

    username = input("[?] Ingrese su nombre de usuario: ")
    password = maskpass.askpass("[?] Ingrese su contraseña: ")
    
    while ((not loginValido(username, password)) and attempts <= 3):
        if attempts > 0 and attempts < 3:
            print("[-] Intentos fallidos: " + str(attempts) + "/3")
            username = input("[?] Ingrese su nombre de usuario: ")
            password = maskpass.askpass("[?] Ingrese su contraseña: ")
        elif attempts >= 3:
            os.system('cls')
            print("[-] Demasiados intentos fallidos, el programa se cerrara!")
            
        attempts = attempts + 1

    if MY_USER_INDEX != -1:
        os.system('cls')
        account = USERS[MY_USER_INDEX][2]
        print("[+] Sesion iniciada como " + account)
        match account:
            case "administrador":
                menuPrincipal()
            case "dueñoLocal":
                menuDLocal()
            case "cliente":
                menuCliente()

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
        
    loadFiles()
    authMenu()

entryPoint()
