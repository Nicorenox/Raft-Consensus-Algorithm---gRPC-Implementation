
import requests

proxy_url = "http://proxy:5004"  # Cambia según tu configuración de red

def write_operation(data):
    response = requests.post(f"{proxy_url}/write", json=data)
    if response.status_code == 200:
        print("Write operation successful:", response.json())
    else:
        print("Write operation failed:", response.json())

def read_operation():
    response = requests.get(f"{proxy_url}/read")
    if response.status_code == 200:
        print("Read operation successful:", response.json())
    else:
        print("Read operation failed:", response.json())

if __name__ == "__main__":
    while True:
        choice = input("¿Deseas realizar una operación de escritura (w) o lectura (r)? (q para salir): ").strip().lower()

        if choice == 'w':
            key = input("Introduce la clave para escribir: ")
            value = input("Introduce el valor para escribir: ")
            write_data = {"key": key, "value": value}
            write_operation(write_data)

        elif choice == 'r':
            read_operation()

        elif choice == 'q':
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Por favor elige 'w' para escritura, 'r' para lectura o 'q' para salir.")

