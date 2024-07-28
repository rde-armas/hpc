import matplotlib.pyplot as plt

# Datos
experimentos = ["24 cod_var"] * 5
nro_procesadores = [24, 16, 8, 4, 1]
maestro = [1, 1, 1, 1, 1]
esclavos = [24, 12, 4, 2, 1]
tiempo_ejecucion = [1155.84, 1921.5, 4264.9, 7038.5, 12733.0]

# Crear la gráfica
plt.figure(figsize=(10, 6))
plt.plot(nro_procesadores, tiempo_ejecucion, marker='o', linestyle='-', color='b')

# Añadir títulos y etiquetas
plt.title('Número de Procesadores vs Tiempo de Ejecución')
plt.xlabel('Número de Procesadores')
plt.ylabel('Tiempo de Ejecución (s)')
plt.grid(True)

# Mostrar la gráfica
plt.show()
