# Learn2Slither

```bash
./snake -h
```
| Argumento | Funcionamiento |
| --- | --- |
| `-sessions N` | Ejecuta exactamente N partidas. |
| `-save PATH` | Guarda el modelo final al terminar. |
| `-load PATH` | Carga Q-table, epsilons y episodios antes de empezar. |
| `-visual on/off` | Activa o desactiva completamente la interfaz gráfica. |
| `-dontlearn` | Evalúa sin modificar Q-table, epsilons ni contador de entrenamiento. |
| `-step-by-step` | En visual, espera Espacio o Enter antes de cada movimiento. |
| `-show-vision` | Muestra en terminal la visión completa de la serpiente. |
| `-width N` | Cambia el ancho jugable del tablero (mínimo 3, por defecto 10). |
| `-height N` | Cambia el alto jugable del tablero (mínimo 3, por defecto 10). |
| `-h` | Muestra la ayuda. |

```bash
./snake -load models/model_100000.pkl -dontlearn -sessions 10 -width 16 -height 8 -visual off
```
