import json
import os

# --- Clase Producto ---
# Define la entidad básica del sistema con sus atributos y métodos de acceso.
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        # Uso de guion bajo para indicar atributos protegidos (encapsulamiento)
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # Métodos para obtener valores de los atributos (Getters)
    def get_id(self): return self._id
    def get_nombre(self): return self._nombre
    def get_cantidad(self): return self._cantidad
    def get_precio(self): return self._precio

    # Métodos para modificar valores de los atributos (Setters)
    def set_cantidad(self, nueva_cantidad): self._cantidad = nueva_cantidad
    def set_precio(self, nuevo_precio): self._precio = nuevo_precio

    # Retorna una cadena formateada que representa al producto
    def __str__(self):
        return f"ID: {self._id:<5} | Nombre: {self._nombre:<15} | Cantidad: {self._cantidad:<5} | Precio: ${self._precio:.2f}"


# --- Clase Inventario ---
# Clase principal encargada de la lógica de negocio y gestión de los artículos.
class Inventario:
    def __init__(self):

        # --- Integración de Colecciones ---
        # Se implementa un diccionario como estructura principal para garantizar
        # búsquedas de productos por ID con una complejidad de tiempo eficiente.
        self._productos = {}

        self._nombre_archivo = "inventario_tienda.json"
        self._cargar_datos()

    def añadir_producto(self, producto):
        """Inserta un nuevo objeto Producto en el diccionario usando el ID como clave."""
        if producto.get_id() in self._productos:
            print("Error: Ya existe un registro con ese identificador.")
        else:
            self._productos[producto.get_id()] = producto
            print(f"Producto '{producto.get_nombre()}' agregado exitosamente.")
            self._guardar_datos()

    def eliminar_producto(self, id_producto):
        """Remueve un producto de la colección basándose en su identificador único."""
        if id_producto in self._productos:
            del self._productos[id_producto]
            print("Registro eliminado satisfactoriamente.")
            self._guardar_datos()
        else:
            print("Error: El ID proporcionado no coincide con ningún producto.")

    def actualizar_producto(self, id_producto, cant=None, prec=None):
        """Actualiza selectivamente la cantidad o el precio de un producto existente."""
        if id_producto in self._productos:
            p = self._productos[id_producto]
            if cant is not None: p.set_cantidad(cant)
            if prec is not None: p.set_precio(prec)
            print("Información actualizada correctamente.")
            self._guardar_datos()
        else:
            print("Error: No se encontró el producto para actualizar.")

    def buscar_por_nombre(self, nombre):
        """Realiza una búsqueda filtrada permitiendo coincidencias parciales (case-insensitive)."""
        encontrados = [p for p in self._productos.values() if nombre.lower() in p.get_nombre().lower()]
        if encontrados:
            print("\nCoincidencias encontradas:")
            for p in encontrados: print(p)
        else:
            print("No se encontraron productos con ese criterio de búsqueda.")

    def mostrar_todos_los_productos(self):
        """Itera sobre la colección para mostrar el estado actual de todos los registros."""
        if not self._productos:
            print("El inventario se encuentra vacío.")
        else:
            print("\nListado completo de productos:")
            for p in self._productos.values():
                print(p)


# --- Almacenamiento en Archivos ---
    def _guardar_datos(self):
        """Proceso de serialización: convierte los objetos en formato JSON para su persistencia."""
        try:
            # Transformación de objetos Producto a una lista de diccionarios planos
            datos_mapeados = [
                {'id': p.get_id(), 'nombre': p.get_nombre(),
                 'cantidad': p.get_cantidad(), 'precio': p.get_precio()}
                for p in self._productos.values()
            ]
            with open(self._nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_mapeados, f, indent=4)
            print("... Cambios guardados en el archivo exitosamente.")
        except Exception as e:
            print(f"Error de escritura en disco: {e}")

    def _cargar_datos(self):
        """Proceso de deserialización: restaura los objetos Producto desde el archivo JSON."""
        if os.path.exists(self._nombre_archivo):
            try:
                with open(self._nombre_archivo, 'r', encoding='utf-8') as f:
                    datos_cargados = json.load(f)
                    for item in datos_cargados:
                        # Reconstrucción de la instancia de clase a partir de datos serializados
                        p = Producto(item['id'], item['nombre'], item['cantidad'], item['precio'])
                        self._productos[p.get_id()] = p
            except (json.JSONDecodeError, IOError):
                print("Aviso: No se pudo procesar el archivo existente. Se iniciará un inventario limpio.")


# --- Interfaz de Usuario ---
def mostrar_menu():
    """Punto de entrada del programa que gestiona el flujo de interacción por consola."""
    inv = Inventario()
    while True:
        print("\n" + "="*40)
        print("    SISTEMA DE GESTIÓN DE INVENTARIO")
        print("="*40)
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad o precio")
        print("4. Buscar y mostrar productos por nombre")
        print("5. Mostrar todos los productos en el inventario")
        print("6. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == '1':
            id_p = input("ID: ")
            nom = input("Nombre: ")
            try:
                can = int(input("Cantidad: "))
                pre = float(input("Precio: "))
                inv.añadir_producto(Producto(id_p, nom, can, pre))
            except ValueError:
                print("Error: Use números para cantidad y precio.")

        elif opcion == '2':
            id_eliminar = input("Ingrese el ID del producto a eliminar: ")
            inv.eliminar_producto(id_eliminar)

        elif opcion == '3':
            id_p = input("ID del producto a actualizar: ")
            print("(Deje vacío si no desea modificar el valor actual)")
            c_input = input("Nueva cantidad: ")
            p_input = input("Nuevo precio: ")

            # Conversión condicional: solo si el usuario escribió algo
            n_can = int(c_input) if c_input.strip() else None
            n_pre = float(p_input) if p_input.strip() else None
            inv.actualizar_producto(id_p, n_can, n_pre)

        elif opcion == '4':
            busqueda = input("Ingrese el nombre o parte del nombre a buscar: ")
            inv.buscar_por_nombre(busqueda)

        elif opcion == '5':
            inv.mostrar_todos_los_productos()

        elif opcion == '6':
            print("Saliendo del SISTEMA DE GESTIÓN DE INVENTARIO... ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    mostrar_menu()
