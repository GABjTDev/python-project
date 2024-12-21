#importamos la libreria
from colorama import Fore, init

#importe de funciones
from utils import create_database, add_product, show_products, update_product, delete_product, search_product, low_stock_report

# Función principal para el sistema de inventario (NO ELIMINAR)
def main():
  # AQUÍ PUEDES COMENZAR A DESARROLLAR LA SOLUCIÓN
  init(autoreset=True)
  
  # Al correr el codigo se crea la base de datos y la tabla.
  create_database()
  
  while (True):
    print(Fore.CYAN + "\n--- Menú de Inventario ---")
    print('1 - Agregar producto')
    print('2 - Mostrar todos los productos')
    print('3 - Actualizar producto')
    print('4 - Eliminar producto')
    print('5 - Buscar producto')
    print('6 - Reporte de bajo stock')
    print('7 - Salir')
    
    option_menu = int(input(Fore.GREEN + 'Ingrese la opción que desea utilizar: '))
    
    if isinstance(option_menu, int) and option_menu <= 7:
      
      if option_menu == 1:
        add_product()
      elif option_menu == 2:
        show_products()
      elif option_menu == 3:
        update_product()
      elif option_menu == 4:
        delete_product()
      elif option_menu == 5:
        search_product()
      elif option_menu == 6:
        low_stock_report()
      elif option_menu == 7:
        print(Fore.BLUE + '\n--- ¡Saliste con éxito del programa! ---')
        break
      
    else:
      print(Fore.RED + '\n--- Ingresaste un dato inválido. ¡Vuelve a intentarlo! ---')


# Ejecución de la función main() - (NO ELIMINAR)
if __name__ == "__main__":
    main()
