import matplotlib.pyplot as plt

# Datos
procesadores = [4, 8, 16, 24]
masters = [1, 1, 1, 1]
slaves = [2, 4, 12, 24]
tiempo = [7038.5, 4264.9, 1921.5, 1155.8]
paralelicibilidad = [1.81, 2.99, 6.63, 11.02]

# Crear la gráfica
plt.figure(figsize=(10, 6))
plt.plot(procesadores, paralelicibilidad, '-o', label='Paralelicibilidad')

# Agregar la recta y=x en rojo
plt.plot(procesadores, procesadores, 'r--', label='y = x')

# Configurar los ticks del eje x
plt.xticks(procesadores)

plt.xlabel('Número de Procesadores')
plt.ylabel('Paralelicibilidad')
plt.title('Paralelicibilidad en función de Procesadores')
plt.grid(True)
plt.legend()

# Guardar la gráfica como un archivo PNG
plt.savefig('paralelicibilidad_vs_procesadores.png')

# Mostrar la gráfica
plt.show()


