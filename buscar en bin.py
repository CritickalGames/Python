import webbrowser

def buscar_en_edge(busquedas):
    edge_path = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s'
    for termino in busquedas:
        url = f"https://www.bing.com/search?q={termino}"
        webbrowser.get(edge_path).open(url)
        print(f"Búsqueda realizada: {termino}")

def main():
    busquedas = [
        "Best books to read in 2024",
        "Upcoming video game releases",
        "DIY home improvement projects",
        "Top universities in the world",
        "How to learn coding for free",
        "Tips for financial planning",
        "History of the Great Wall of China",
        "Benefits of drinking green tea",
        "How to write a resume",
        "Best travel destinations in Europe",
        "Basics of quantum computing",
        "Famous speeches in history",
        "How to bake a perfect cake",
        "Importance of mental health",
        "Exercises to improve flexibility",
        "Best practices for time management",
        "Top programming languages to learn",
        "Guide to digital marketing",
        "How to play the guitar",
        "Latest advancements in biotechnology",
        "How to start a podcast",
        "Tips for a successful job interview",
        "History of the Internet",
        "How to create a budget",
        "Benefits of regular exercise",
        "How to study effectively",
        "Top science fiction novels",
        "Ways to reduce carbon footprint",
        "How to draw realistic portraits",
        "Understanding blockchain technology"
    ]


    
    while True:
        print("\nOpciones:")
        print("1. Realizar búsquedas en Edge")
        print("0. Salir")

        opcion = input("Ingrese la opción deseada: ")

        if opcion == '1':
            buscar_en_edge(busquedas)
        elif opcion == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, ingrese 1 o 0.")

if __name__ == "__main__":
    main()
