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

NEW_TEXT_LENGHT = 200
NEW_TYPE_LENGHT = 20

# Declaramos variables de los tipos de usuarios existentes
USER_TYPE_ADMIN = "administrador"
USER_TYPE_CLIENT = "cliente"
USER_TYPE_LOCALOWNER = "dueñoLocal"

# Declaramos las variables de los tipos de locales que existen
LOCAL_TYPE_FOOD = "comida"
LOCAL_TYPE_PERFUME = "perfume"
LOCAL_TYPE_FASHION = "indumentaria"

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
    exists = False 

    if not os.path.exists(filePath):
        logicFile = open(filePath, "w+b")
    else:
        logicFile = open(filePath, "r+b")
        exists = True

    return logicFile, exists

# funcion para cargar archivos
def loadFiles():
    global userFile, localsFile, promsFile, promsUseFile, newsFile
    
    # crea la carpeta del tp3 si no existe 
    os.makedirs(mainPath, 775, True)

    userFile, exists = openFile(userFilePath)
    if not exists:
        loadAdmin()

    localsFile, exists = openFile(localsFilePath)
    if exists: 
        loadLocals()

    promsFile, _ = openFile(promsFilePath)
    promsUseFile, _ = openFile(promsUseFilePath)
    newsFile, _ = openFile(newsFilePath)

# funcion para cerrar archivos
def unloadFiles():
    userFile.close()
    localsFile.close()
    promsFile.close()
    promsUseFile.close()
    newsFile.close()

# funcion para guardar un usuario en el archivo
def saveUser(user):
    user.tipoUsuario = user.tipoUsuario.ljust(USER_TYPE_LENGHT)
    user.claveUsuario = user.claveUsuario.ljust(USER_PASS_LENGHT)
    user.nombreUsuario = user.nombreUsuario.ljust(USER_NAME_LENGHT)

    pickle.dump(user, userFile)
    userFile.flush()

# funcion para guardar un local en el archivo
def saveLocal(local):
    local.nombreLocal = local.nombreLocal.ljust(LOCAL_NAME_LENGHT)
    local.ubicacionLocal = local.ubicacionLocal.ljust(LOCAL_ADDR_LENGHT)
    local.rubroLocal = local.rubroLocal.ljust(LOCAL_CATG_LENGHT)

    pickle.dump(local, localsFile)
    localsFile.flush()

# funcion para guardar una novedad en el archivo
def saveNew(new):
    new.textoNovedad = new.textoNovedad.ljust(NEW_TEXT_LENGHT)
    new.tipoUsuario = new.tipoUsuario.ljust(NEW_TYPE_LENGHT)
    pickle.dump(new, newsFile)
    newsFile.flush()

# funcion para la carga de usuario
def loadAdmin():
    adminUser = Usuario()
    adminUser.codUsuario = 1
    adminUser.nombreUsuario = "admin@shopping.com"
    adminUser.tipoUsuario = USER_TYPE_ADMIN
    adminUser.claveUsuario = "12345"
    
    saveUser(adminUser)

# funcion para cargar la cantidad de locales por rubro en lCategories
def loadLocals():
    fileSize = os.path.getsize(localsFilePath)
    localsFile.seek(0,0)

    while localsFile.tell() < fileSize:
        localsFile.tell()
        local = pickle.load(localsFile)
        addToCategory(local.rubroLocal)

# funcion para leer opciones numericas en rango
def optionRange(inicio, fin):
    opc = int(input('Elije una opcion: '))
    while opc > fin or opc < inicio:
        opc = int(input('Elije una opcion valida: '))
    return opc 

# funciones para el menu de autenticacion:FL
def authMenuOpts():
    print('1. Ingresar con usuario registrado')
    print('2. Registrarse como cliente')
    print('3. Salir')

def authMenu():    
    authMenuOpts()
    opc = optionRange(1,3)

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
    
    user.nombreUsuario = mail
    user.claveUsuario = input('Ingrese una contraseña nueva(tiene que tener '+str(USER_PASS_LENGHT)+' caracteres): ')
    
    while len(user.claveUsuario) != USER_PASS_LENGHT:
        user.claveUsuario = input('La contraseña que acaba de ingresar no tiene '+str(USER_PASS_LENGHT)+' caracteres, ingrese otra: ')
    
    user.tipoUsuario = USER_TYPE_CLIENT
    saveUser(user)
    print('Registrado correctamente')

# funciones para buscar un local
def searchLocalEnginge(searchFunc, param):
    T = os.path.getsize(localsFilePath)
    pos = -1 
    locals = Locales()
    localsFound = False
    localsFile.seek(0,0)

    while not localsFound and localsFile.tell() < T:
        # lee puntero
        p = localsFile.tell()

        # carga contenido
        tmp = pickle.load(localsFile)
        
        # chequea si el nombre es igual al mail
        if searchFunc(tmp, param):
            pos = p
            locals = tmp
            localsFound = True
    
    return locals, pos

def searchLocalByCodeCondition(local, code):
    return local.codLocal == code

def searchLocalByCode(code):
    return searchLocalEnginge(searchLocalByCodeCondition, code)

# funciones para buscar un usuario en base a ciertos datos
def searchUserEnginge(searchFunc, param):
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
        if searchFunc(tmp, param):
            usr = tmp
            usrFound = True
    return usr

def searchUserByMailCondition(usr, mail):
    return usr.nombreUsuario.strip() == mail

def searchUserByMail(mail):
    return searchUserEnginge(searchUserByMailCondition, mail)

def searchUserByCodeCondition(usr, code):
    return usr.codUsuario.strip() == code

def searchUserByCode(code):
    return searchUserEnginge(searchUserByCodeCondition, code)

# funcion para conseguir la cantidad de locales
def getLocalsQuantity():
    fileSize = os.path.getsize(localsFilePath)
    localsFile.seek (0, 0)
    _ = pickle.load(localsFile)
    regSize = localsFile.tell() 
    total = int(fileSize / regSize)  
        
    return total

# funcion para validar si el nombre del local es valido
def invalidLocalName(nombre):
    inicio = 0
    fin = getLocalsQuantity() - 1
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
    local = Locales()
    T = os.path.getsize(localsFilePath)
    localsFile.seek(0)
    local = pickle.load(localsFile)
    singleT = localsFile.tell()
    quantityOfLocals = T // singleT
    if quantityOfLocals > 0:
        confirm = input('Desea ver los locales guardados hasta el momento?')
        if confirm.lower() == 'si' and T != 0:
            for i in range(quantityOfLocals):
                print(f"============ LOCAL Nº {str(i)} ============")
                print(f'Codigo local: {local.codLocal}\nNombre: {local.nombreLocal.strip()}\nUbicacion: {local.ubicacionLocal.strip()}\nRubro: {local.rubroLocal.strip()}\nEstado: {local.estado} ')
                print(f"===========================================")
                local = pickle.load(localsFile)

# funcion para ordenar locales por nombre
def orderLocalsByName():
    fileSize = os.path.getsize(localsFilePath)
    localsFile.seek (0, 0)
    _ = pickle.load(localsFile)
    regSize = localsFile.tell() 
    total = int(fileSize / regSize)  

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
    founded = False
    rubIdx = 0
    while (not founded and rubIdx <= len(lCategories) - 1):
        if lCategories[rubIdx] == rub:
            founded = True
        else:
            rubIdx += 1
    
    return rubIdx

# funcion para añadir uno a la cuenta de la categoria
def addToCategory(cat):
    global lCategoriesCount
    lCategoriesCount[getCategoryIndex(cat)] += 1

# funcion para restar uno a la cuenta de la categoria
def removeFromCategory(cat):
    global lCategoriesCount
    lCategoriesCount[getCategoryIndex(cat)] +- 1

# Function para registrar locales
def newLocals():
    os.system('cls')
    global lCategories
    
    localsFile.seek(0,0)
    locals = Locales()
    locals = pickle.load(localsFile)
    locals.nombreLocal = input("[?] Ingrese el nombre del local (ingrese \".\" para salir)\n")

    # Se saca el número de locales para poder poner el codigo de del mismo de manera secuencial
    localQty = getLocalsQuantity()
    registeredLocals = 0

    while locals.nombreLocal != ".":
        while invalidLocalName(lName):
            print("[-] Nombre de local en uso")
            locals.nombreLocal = input("[?] Ingrese el nombre del local\n")

        locals.ubicacionLocal = input("[?] Ingrese la ubicacion del local\n")
        locals.codLocal = localQty + 1
        registeredLocals = registeredLocals + 1

        locals.rubroLocal = input(f"[?] Ingrese el rubro del local ({LOCAL_TYPE_FASHION}, {LOCAL_TYPE_FOOD}, {LOCAL_TYPE_PERFUME})\n").lower()
        while locals.rubroLocal != LOCAL_TYPE_FASHION and locals.rubroLocal != LOCAL_TYPE_PERFUME and locals.rubroLocal != LOCAL_TYPE_FOOD:
            print("[-] Rubro invalido")
            locals.rubroLocal = input(f"[?] Ingrese un rubro de local valido ({LOCAL_TYPE_FASHION}, {LOCAL_TYPE_FOOD}, {LOCAL_TYPE_PERFUME})\n").lower()

        locals.codUsuario = int(input("[?] Ingrese el codigo de usuario del dueño del local\n"))
        while (searchUserByCode(locals.codUsuario).tipoUsuario != USER_TYPE_LOCALOWNER):
            print("[-] El codigo de usuario ingresado no existe o no pertenece a un dueño de local")
            locals.codUsuario = int(input("[?] Ingrese el codigo de usuario del dueño del local\n"))

        # sumar uno a la categoria
        addToCategory(locals.rubroLocal)

        # Se guarda el nuevo local en archivo con la función "saveLocal"
        saveLocal(locals)
        orderLocalsByName()

        os.system('cls')
        lName = input("[?] Ingrese el nombre del siguiente local (ingrese \".\" para salir)\n")

    #valida que al menos se haya ejecutado una vez el while
    if registeredLocals > 0:
        # Si se ingreso al menos un local nuevo se reordenan las categorias
        orderCategories()

        os.system('cls')
        print("[+] Locales por rubro: ")

        for rubro in range(0, len(lCategories)):
            print(" " + lCategories[rubro] + ": " + str(lCategoriesCount[rubro]))


def pedirConfirmacion(texto): #parametro localIndex tipo INT y parametro texto de tipo STRING
    global LOCALES

    opt = input("[?] " + texto + " (S - si, N - no)\n").lower()
    while opt != "s" and opt != "n":
        print("[-] Opcion invalida")
        opt = input("[?] " + texto + " (S - si, N - no)\n").lower()

    return opt == "s"

def activarLocalPrompt(localData, posL): #parametro localIndex tipo INT
    if pedirConfirmacion("Desea activar nuevamente este local"):
        localData.estado = 'A'
        localsFile.seek(posL,0)
        pickle.dump(localData, localsFile)
        localsFile.flush()


def desactivarLocalPrompt(localData, posL): #parametro localIndex tipo INT
    if pedirConfirmacion("Desea eliminar este local"):
        localData.estado = 'B'
        localsFile.seek(posL,0)
        pickle.dump(localData, localsFile)
        localsFile.flush()

def modifyLocal():
    lCode = input("[?] Ingrese el codigo del local\n")
    localData, pos = searchLocalByCode(int(lCode))

    while pos == -1:
        print("[-] Codigo de local invalido")
        lCode = input("[?] Ingrese el codigo del local\n")
        localData, pos = searchLocalByCode(int(lCode))

    localsFile.seek(pos,0)

    if localData.estado != "A":
        activarLocalPrompt(localData, pos)
    
    if localData.estado == "A":
        localData.nombreLocal = input("[?] Ingrese el nombre del local (ingrese \".\" para salir)\n")

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

        
        LOCALES[localIndex] = [lName, lAddress, lHeading, "A"]
        LOCALES_CODE[localIndex] = [LOCALES_CODE[localIndex][0], lUserCode]
        
        orderCategories()
        orderLocalsByName()

def eliminarLocal():
    global LOCALES
    global LOCALES_CODE

    lCode = input("[?] Ingrese el codigo del local\n")
    localIndex = searchLocalByCode(int(lCode))

    while localIndex == -1:
        print("[-] Codigo de local invalido")
        lCode = input("[?] Ingrese el codigo del local\n")
        localIndex = searchLocalByCode(int(lCode))

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
def localManage():
    
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
                listLocals()
                NewLocals()
            case 98:
                listLocals()
                modifyLocal()
            case 99:
                listLocals()
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
def newsManage():
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
def adminMenu():
    print('''
1. Gestion de locales
2. Crear cuentas de dueños de locales
3. Aprobar / Denegarsolicitud de descuento
4. Gestión de novedades
5. Reporte de utilización de descuentos
0. Salir·
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
                localManage()
            case 2:
                os.system('cls')
                print("[-] En construccion...")
            case 3:
                os.system('cls')
                print("[-] En construccion...")
            case 4:
                os.system('cls')
                newsManage()
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
def loginValido(mail, passwd): # parametro mail y passwd de tipo string
    global MY_USER
    logged = False

    user = searchUserByMail(mail)
    if user.nombreUsuario == "":
        return logged

    if user.claveUsuario == passwd.strip():
        logged = True
        MY_USER = user

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

    if MY_USER.nombreUsuario != "":
        os.system('cls')
        print("[+] Sesion iniciada como " + MY_USER.tipoUsuario)
        
        match MY_USER.tipoUsuario.strip():
            case "administrador":
                adminMenu()
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
    unloadFiles()

entryPoint()
