import sqlite3
from colorama import Fore

# Funcion para crear la base de datos y la tabla de los productos
def create_database():
  with sqlite3.connect('inventario.db') as conn:
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS PRODUCTS (
      id INTEGER PRIMARY KEY AUTOINCREMENT, 
      name TEXT NOT NULL, 
      description TEXT, 
      stock INTEGER NOT NULL,
      price REAL NOT NULL,
      category TEXT
    );""")
    conn.commit()
    print(Fore.YELLOW + "Tabla producto creada con exito.")
  #  No necesitamos cerrar la conexión explícitamente, ya que `with` se encarga de ello.

# Funcion para agregar productos
def add_product():
  try:
    name_product = input('Ingrese el nombre del producto a agregar: ').strip().capitalize()
    description = input('Ingrese la descripcion del producto: ').strip().capitalize()
    stock_product = int(input('Ingrese el stock del producto: '))
    price_product = float(input('Ingrese el precio del producto: '))
    category_product = input('Ingrese la categoria del producto: ').strip().capitalize()
    
    sql = """INSERT INTO PRODUCTS(name,description,stock,price,category) VALUES(?,?,?,?,?)"""
    
    with sqlite3.connect('inventario.db') as conn:
      cursor = conn.cursor()
      cursor.execute(sql, [name_product, description, stock_product, price_product, category_product])
      conn.commit()
      print(Fore.YELLOW + "Se agrego el producto correctamente.")
    #  No necesitamos cerrar la conexión explícitamente, ya que `with` se encarga de ello.

  except ValueError as ve:
    # Si ocurre un error de conversión de tipo (por ejemplo, al ingresar valores no numéricos para stock o precio)
    print(Fore.RED + f"Error de tipo: {ve}. Asegúrate de ingresar números válidos para el stock y el precio.")

# Funcion para mostrar todos los productos
def show_products():
  
  with sqlite3.connect('inventario.db') as conn:
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM PRODUCTS""")
    all_products = cursor.fetchall()
    if(len(all_products) == 0):
      print(Fore.RED + 'No hay productos registrados.')
    else:
      print_products(all_products)
  #  No necesitamos cerrar la conexión explícitamente, ya que `with` se encarga de ello.

# Actualizar la cantidad del producto
def update_product():
  
  try:
    id = int(input("ingrese el id del producto para modificar: "))
    sql = """UPDATE PRODUCTS SET stock=? WHERE id = ?"""
    
    with sqlite3.connect('inventario.db') as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM PRODUCTS WHERE id = ?", [id])
      product = cursor.fetchone()  # Esto devuelve una tupla con los datos del producto si existe
      
      check_id = not_exist_id(product)
      
      if check_id:
        return
      
      stock_product = int(input('Ingrese el nuevo stock del producto: '))
      cursor.execute(sql, (stock_product, id))
      print(Fore.YELLOW + f"Se actualizo con exito el producto!!")
      conn.commit()
    # No necesitamos cerrar la conexión explícitamente, ya que `with` se encarga de ello.
  except ValueError as ve:
    # Si ocurre un error de conversión de tipo (por ejemplo, al ingresar valores no numéricos para stock o precio)
    print(Fore.RED + f"Error de tipo: {ve}. Asegúrate de ingresar id válido.")

# Eliminar un producto
def delete_product():
  
  try:
    id = int(input("ingrese el id del producto para eliminar: "))
    sql = """DELETE FROM PRODUCTS WHERE id = ?"""
    
    with sqlite3.connect('inventario.db') as conn:
      
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM PRODUCTS WHERE id = ?", [id])
      product = cursor.fetchone()  # Esto devuelve una tupla con los datos del producto si existe
      
      check_id = not_exist_id(product)
      
      if check_id:
        return
      
      cursor.execute(sql, [id])
      
      print(Fore.YELLOW + f"Se borro con exito el producto!!")
      conn.commit()
    # No necesitamos cerrar la conexión explícitamente, ya que `with` se encarga de ello.
  except ValueError as ve:
    # Si ocurre un error de conversión de tipo (por ejemplo, al ingresar valores no numéricos para stock o precio)
    print(Fore.RED + f"Error de tipo: {ve}. Asegúrate de ingresar id válido.")

# Buscar un producto
def search_product():
  
  option_search = input("Ingrese si desea buscar por id/nombre/categoria: ").strip().lower()
  
  try:
    with sqlite3.connect('inventario.db') as conn:
      cursor = conn.cursor()
      if option_search == 'id':
        id = int(input("ingrese el id del producto para buscarlo: "))
        cursor.execute("SELECT * FROM PRODUCTS WHERE id = ?", [id])
        all_products = cursor.fetchall()
        print_products(all_products)
      elif option_search == 'nombre':
        name = input("ingrese el nombre del producto para buscarlo: ")
        cursor.execute("SELECT * FROM PRODUCTS WHERE name LIKE ?", ('%' + name + '%',))
        all_products = cursor.fetchall()
        print_products(all_products)
      elif option_search == 'categoria':
        category = input("ingrese la categoria que quiere buscar: ")
        cursor.execute("SELECT * FROM PRODUCTS WHERE category LIKE ?", ('%' + category + '%',))
        all_products = cursor.fetchall()
        print_products(all_products)
      else:
        print(Fore.RED + 'Busqueda incorrecta!!!!')
    # No necesitamos cerrar la conexión explícitamente, ya que `with` se encarga de ello.
  except ValueError as ve:
    # Si ocurre un error de conversión de tipo (por ejemplo, al ingresar valores no numéricos para stock o precio)
    print(Fore.RED + f"Error de tipo: {ve}. Asegúrate de ingresar id válido.")

# Reporte de bajo stock
def low_stock_report():
  
  low_stock = int(input('Ingrese el low stock para obtener los productos con esta cantidad o menos: '))
  sql = """SELECT * FROM PRODUCTS WHERE stock <= ?"""
  
  with sqlite3.connect('inventario.db') as conn:
    cursor = conn.cursor()
    cursor.execute(sql, [low_stock])
    all_products = cursor.fetchall()
    if(len(all_products) == 0):
      print(Fore.RED + 'No hay productos con stocks bajos.')
    else:
      print_products(all_products)
    conn.commit()
  # No necesitamos cerrar la conexión explícitamente, ya que `with` se encarga de ello.

# Funcion para comprobar que exista el id.
def not_exist_id(product):
  if product is None:
    # Si el producto no existe, notificamos al usuario
    print(Fore.RED + "Error: El ID ingresado no existe en la base de datos.")
    return True
  return False

# funcion para hacer un print de todos los productos
def print_products(all_products):
  for product in all_products:
    print(Fore.MAGENTA + f"id: {product[0]}\nNombre: {product[1]}\nDescripcion: {product[2]}\nStock: {product[3]}\nPrecio: {product[4]}\nCategoria: {product[5]}\n")