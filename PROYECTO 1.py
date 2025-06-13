
from datetime import datetime
import json
import os

if os.path.exists("inventario.json"):
    with open("inventario.json", "r") as archivo:
        inventario = json.load(archivo)
else:
    inventario = {
        "autos":231,
        "camionetas":124,
        "motos":133
    }

precios={
    "autos":15000,
    "camionetas":25000,
    "motos":5000
}

if os.path.exists("usuarios.json"):
    with open("usuarios.json", "r") as archivo:
        usuarios = json.load(archivo)
else: 
    usuarios={}    

def guardar_datos():
    with open("inventario.json", "w") as archivo:
        json.dump(inventario, archivo)
    with open("usuarios.json", "w") as archivo:
        json.dump(usuarios, archivo)


def ingresar():
    while True:
        try: opción=int(input())
        except ValueError:
            print("Por favor, seleccione una opción válida")
            continue
        if opción==3:
            print("Saliendo de la tienda... Gracias por visitarnos!")
            guardar_datos()
            continue
        print("Por favor ingresa tu nombre")
        nombre=input()
        print("Por favor ingresa tu apellido")
        apellido=input()
        nombreCompleto=nombre +" "+ apellido

        if opción==1:
            if nombreCompleto not in usuarios:
                print("Usuario no encontrado. Por favor, regístrese primero.")
                print("-----------------------------------------------------")
                print("1. Iniciar sesión")
                print("2. Registrarse")
                print("3. Salir")
                continue
            else: 
                usuario_actual= nombreCompleto
                print(f"Bienvenido de nuevo, {nombreCompleto}! Gracias por visitarnos.")
                return usuario_actual
        elif opción==2:
            if nombreCompleto in usuarios:
                print("Ese usuario ya existe. Intente iniciar sesión")
                continue
            else:
                usuario_actual= nombreCompleto
                usuarios[nombreCompleto]={"carrito":{},"historial_de_compras":[]}
                print(f"Usuario registrado correctamente. Gracias por visitarnos, {nombreCompleto}!")
                return usuario_actual
        elif opción==3:
            print("Saliendo de la tienda... Gracias por visitarnos!")
            break
        else: 
            print("Ingrese una opción válida.")
            continue  

def totalDeVehiculos():
    vehiculos = 0
    for valores in inventario.values():
        vehiculos += valores
    return vehiculos

def mostrarInventario():
    print("**********INVENTARIO**********")
    print("Actualmente disponemos de:")
    for llaves,valores in inventario.items():
        print(f'    {valores} {llaves}')
    print ("Tenemos un total de",totalDeVehiculos(),"vehículos en venta disponibles.")

def menuOpcionesCompra(usuario_actual):
    carrito=usuarios[usuario_actual]["carrito"]
    historial_de_compras=usuarios[usuario_actual]["historial_de_compras"]
    while True:
        print("========================================")
        print("Seleccione una opción para continuar:")
        print("1. Ver carrito de compra")
        print("2. Continuar comprando")
        print("3. Confirmar la compra.")
        try: res=int(input())
        except ValueError:
            print("Por favor seleccione una opción válida")
            continue
        if res==2:
            print("Volviendo atrás...")
            break
        elif res==1:
            verCarrito(usuario_actual)
        elif res==3:
            recibo=confirmarCompra(usuario_actual,carrito)
            if recibo:
                historial_de_compras.append(recibo)
            carrito.clear()
            guardar_datos()
            break

def comprarVehículo(usuario_actual):
    carrito=usuarios[usuario_actual]["carrito"]
    vehiculo=""
    while True:
        print("¿Qué tipo de vehículo le gustaría adquirir?")
        print("1. Auto")
        print("2. Camioneta")
        print("3. Moto")
        print("4. cancelar")
        
        try: res= int(input())
        except ValueError:
            print("Por favor, ingrese una opción válida.")
            continue
        
        if res==4:
            print("Operación cancelada.")
            return "salir"
        elif res==1: vehiculo="autos"
        elif res==2: vehiculo="camionetas"
        elif res==3: vehiculo="motos"
        else: 
            print(f'Por favor, seleccione una opción válida.')
            continue

        if inventario[vehiculo]==0:
            print(f'Lo sentimos, actualmente no tenemos unidades disponibles. Por favor, seleccione otra opción o vuelva a intentarlo más tarde')
            continue

        print("¿Cuantas unidades va a comprar?")
        try: res2= int(input())
        except ValueError:
            print("Por favor, ingrese un valor válido.")
            continue
        
        if res2==(0):
            print("Por favor, ingrese un valor válido.")
            continue
        elif inventario[vehiculo] < res2:
            print(f'Lo sentimos, actualmente solo contamos con {inventario[vehiculo]} {vehiculo}. Por favor ingrese una cantidad válida o revise el catálogo más tarde.')
            continue
        else:
            agregarAlCarrito(usuario_actual,vehiculo,res2)
            print("Artículo agregado al carrito.")
            menuOpcionesCompra(usuario_actual)
            return

def agregarAlCarrito(usuario_actual,vehiculo:str,cantidadDeUnidades:int):
    carrito=usuarios[usuario_actual]["carrito"]

    if vehiculo in carrito:
        carrito[vehiculo]+=cantidadDeUnidades
    else: carrito[vehiculo] = cantidadDeUnidades

def verCarrito(usuario_actual):
    carrito=usuarios[usuario_actual]["carrito"]
    
    while True:
        subtotal_vehiculo=0
        total=0
        if len(carrito)==0:
            print(f'Actualmente el carrito está vacío.')
            return 
        else: 
            print("********* CARRITO *********")
            for vehiculos, cantidades in carrito.items():
                precios_unitarios= precios[vehiculos]
                subtotal_vehiculo = precios_unitarios * cantidades
                total += subtotal_vehiculo
                print(f'{cantidades} {vehiculos} - Precio unitario: ${precios_unitarios} - Subtotal: ${subtotal_vehiculo}')
            
            print(f'El total es de ${total}')
            print("---------------------------")    
        print("¿Desea eliminar algún artículo en el carrito?")
        print("1. Si")
        print("2. No")
        try: res=int(input())
        except ValueError:
            print("Por favor seleccione una opción válida")
            continue
        if res==1:
            print("¿Que vehiculo desea eliminar? (Escriba el nombre, ej: autos)")
            vehiculo=input().lower()
            if vehiculo in carrito: 
                del carrito[vehiculo]
                print(f'Se eliminó {vehiculo} del carrito')
                return
            else:
                print(f'Actualmente {vehiculo} no se encuentra en el carrito')
                continue
        else: break

def confirmarCompra(usuario_actual,carrito:dict):
    carrito=usuarios[usuario_actual]["carrito"]
    historial_de_compras=usuarios[usuario_actual]["historial_de_compras"]
    if not carrito:
        print(f'No se pudo realizar la operación, el carrito está vacío.')
        return
    precio_total=0
    itemsComprados=[]
    fecha=datetime.now()

    for vehiculo,cantidad in carrito.items():
        restarUnidadesVendidas(vehiculo,cantidad)
        
        precio_total += precios[vehiculo] * cantidad
        itemsComprados.append(f'{cantidad} {vehiculo}')
    recibo = {
    "fecha": str(fecha),
    "items": itemsComprados,
    "total": precio_total
    }
    
    print("========================================")
    print("==          RECIBO DE COMPRA          ==")
    print("")
    print(usuario_actual)
    print(f"Fecha: {fecha}")
    print("Usted ha adquirido:")
    print(f'    {itemsComprados}')
    print("----------------------------------------")
    print(f"    MONTO TOTAL: ${precio_total}")
    print("----------------------------------------")
    print("¡Gracias por su compra!")
    print("========================================")

    return recibo

def restarUnidadesVendidas(vehiculo:str,cantidadDeUnidades:int):
    inventario[vehiculo]-= cantidadDeUnidades

def mostrarHistorial(usuario_actual):
    historial_de_compras = usuarios[usuario_actual]["historial_de_compras"]
    print("=============================")
    print("==  HISTORIAL DE COMPRAS   ==")
    print("=============================")

    if not historial_de_compras:
        print("No hay compras realizadas.")
        return

    for i, recibo in enumerate(historial_de_compras, 1):
        print(f"Compra #{i}")
        print(f"Fecha: {recibo["fecha"]}")
        print("Vehículos adquiridos:")
        for item in recibo["items"]:
            print(f"   - {item}")
        print(f"Total de la compra: ${recibo["total"]}")
        print("-----------------------------")

###################

print("****************************")
print("**      BIENVENIDO A      **")
print("**    LA CONCESIONARIA    **")
print("****************************")
print("1. Iniciar sesión")
print("2. Registrarse")
print("3. Salir")

usuario_actual=ingresar()

while True:
    print("*************************************")
    print("Por favor seleccione una opción:")
    print("1. Revisar el catálogo")
    print("2. Adquirir un vehículo")
    print("3. Ver historial de compras")
    print("4. Salir")
    print("*************************************")

    try: res= int(input())
    except ValueError:
        print("Por favor, seleccione una opción válida.")
        continue

    if res==4:
        print("Saliendo de la tienda... Gracias por visitarnos!")
        guardar_datos()
        break
    elif res== 1:
        mostrarInventario()
    elif res== 2:
        comprarVehículo(usuario_actual)
    elif res==3:
        mostrarHistorial(usuario_actual)
    else:
        print("Opción no válida. Por favor, seleccione 1, 2 o 3.")



