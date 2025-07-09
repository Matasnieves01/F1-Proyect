from use_cases import services

if __name__ == "__main__":
    # Agregamos algunos corredores
    services.registrar_corredor("Lewis Hamilton", "Reino Unido", "Mercedes", 44, 210, "admin/img/hamilton.png", edad=39, podios=195, victorias=103)
    services.registrar_corredor("Max Verstappen", "Países Bajos", "Red Bull", 1, 255, "admin/img/verstappen.png", edad=26, podios=98, victorias=62)

    # Listamos los corredores
    corredores = services.listar_corredores()
    for corredor in corredores:
        print(corredor)

    # Buscar un corredor específico
    print("\nBuscando a Max Verstappen:")
    print(services.mostrar_corredor("Max Verstappen"))
