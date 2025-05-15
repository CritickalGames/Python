import os

def print_tree(start_path, indent="", output_file=None, ignorar = False):
    """Imprime la estructura del proyecto en forma de árbol y la guarda en DOCUMENTACIÓN/árbol.txt."""
    lines =[]
    if not ignorar:
        raiz = f"{os.path.basename(start_path)}"  # Nombre de la raíz
        lines = [raiz]  # La primera línea guardada será la raíz
        print(raiz)  # Muestra la raíz en consola

    items = sorted(os.listdir(start_path))  # Ordena archivos y carpetas alfabéticamente

    for index, item in enumerate(items):
        path = os.path.join(start_path, item)
        is_last = index == len(items) - 1  # Detecta si es el último elemento

        prefix = "└── " if is_last else "├── "
        lines.append(indent + prefix + item)

        print(indent + prefix + item)  # Muestra en consola

        # Si es un directorio (y no está oculto), explora su contenido
        if os.path.isdir(path) and not item.startswith("."):
            next_indent = indent + ("    " if is_last else "│   ")
            lines.extend(print_tree(path, next_indent, None, True))

    # Guardar en archivo si es la primera llamada
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    return lines  # Retorna las líneas para llamadas recursivas

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_file = os.path.join(project_root, "DOCUMENTACIÓN", "árbol.txt")

    # Crear carpeta DOCUMENTACIÓN si no existe
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print_tree(project_root, "", output_file)

    print(f"\n✅ Estructura guardada en: {output_file}")
