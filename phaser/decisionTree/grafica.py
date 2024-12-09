
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cargar los datos desde el CSV especificando que la primera fila es un encabezado
df = pd.read_csv('C:/Users/HUAWEI/Documents/ITM/ISC 11Onceavo/IA/phaser/decisionTree/game_training_data.csv', header=None, names=['x1', 'x2', 'target'], dtype=float)
# Crear la figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Graficar puntos con target=0
ax.scatter(df[df['target'] == 0]['x1'], df[df['target'] == 0]['x2'], df[df['target'] == 0]['target'],
           c='blue', marker='o', label='target=0')
# Graficar puntos con target=1
ax.scatter(df[df['target'] == 1]['x1'], df[df['target'] == 1]['x2'], df[df['target'] == 1]['target'],
           c='red', marker='x', label='target=1')
# Etiquetas de los ejes
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('Target')
# Mostrar leyenda
ax.legend()
# Mostrar el gráfico
plt.show()




