import toml
import os

# Cargar configuración desde configpy.toml
config = toml.load("configpy.toml")

# Configurar el entorno según las opciones en el TOML
for key, value in config["environment"].items():
    match key:
        case "PYTHONPATH":
            os.environ["PYTHONPATH"] = value
            print(f"✅ PYTHONPATH configurado: {value}")

        case "MODULES":
            for module in value:
                module_path = os.path.join(os.environ["PYTHONPATH"], module)
                if module_path not in os.sys.path:
                    os.sys.path.append(module_path)
                    print(f"🔄 Módulo agregado al sys.path: {module}")

        case _:
            print(f"⚠️ Opción desconocida en configpy.toml: {key}")

print("🚀 Configuración completada.")
