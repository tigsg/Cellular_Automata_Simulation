import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

# ==========================================
# CONFIGURAÇÕES (AJUSTADAS PARA VISUALIZAÇÃO MELHOR)
# ==========================================
L = 100                 # Tamanho da grade (100x100)
T_STEPS = 1000          # Mais tempo para ver as espirais
K_REFRACTORY = 8        # Reduzi de 15 para 8 (Imunidade dura menos, facilita ondas)
INFECTION_PROB = 1.0    # Altamente contagioso (garante frentes de onda sólidas)
SPONTANEOUS_PROB = 0.0005 # CHANCE DE RE-IGNIÇÃO (Impede que a doença suma totalmente)

# ==========================================
# LÓGICA DO MODELO (SIRS / GREENBERG-HASTINGS)
# ==========================================
def update(frame, img, grid, ax_curve, s_line, i_line, r_line, s_data, i_data, r_data):
    # Copia a grade para atualização síncrona
    new_grid = grid.copy()
    N, M = grid.shape
    
    # Percorre a grade
    for i in range(N):
        for j in range(M):
            state = grid[i, j]
            
            if state == 0:  # SUSCETÍVEL
                # Conta vizinhos infectados (Vizinhança de Moore)
                infected_neighbors = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0: continue
                        ni, nj = (i + di) % N, (j + dj) % M
                        if grid[ni, nj] == 1:
                            infected_neighbors += 1
                
                # REGRA 1: Contágio por vizinho
                if infected_neighbors > 0:
                    if np.random.random() < INFECTION_PROB:
                        new_grid[i, j] = 1
                
                # REGRA EXTRA: Infecção Espontânea (Mantém a simulação viva)
                elif np.random.random() < SPONTANEOUS_PROB:
                    new_grid[i, j] = 1
                        
            elif state == 1: # INFECTADO -> RECUPERANDO
                new_grid[i, j] = 2
                
            elif state >= 2: # RECUPERADO (Imune) -> CONTAGEM REGRESSIVA
                if state < K_REFRACTORY:
                    new_grid[i, j] += 1
                else:
                    new_grid[i, j] = 0 # Volta a ser Suscetível

    # Atualiza os dados
    grid[:] = new_grid[:]
    img.set_data(grid)
    
    # Coleta estatísticas para o gráfico
    total = N * M
    s_data.append(np.sum(grid == 0) / total)
    i_data.append(np.sum(grid == 1) / total)
    r_data.append(np.sum(grid > 1) / total)
    
    # Atualiza as linhas do gráfico
    x = range(len(s_data))
    s_line.set_data(x, s_data)
    i_line.set_data(x, i_data)
    r_line.set_data(x, r_data)
    
    # Ajusta o eixo X do gráfico para acompanhar o tempo
    ax_curve.set_xlim(0, max(100, len(s_data) + 10))
    
    return img, s_line, i_line, r_line

# ==========================================
# VISUALIZAÇÃO
# ==========================================
grid = np.zeros((L, L), dtype=int)

# Inicializa com vários focos aleatórios para criar "caos" inicial
mask = np.random.random((L, L)) < 0.05
grid[mask] = 1

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Cores: Verde (Suscetível), Branco (Infectado - Destaque), Preto (Recuperado)
# Essa combinação (Preto/Branco/Verde) costuma dar um contraste melhor para artigos
cmap = ListedColormap(['#006400', '#FFFFFF', '#404040']) 
bounds = [0, 1, 2, K_REFRACTORY+1]
norm = plt.Normalize(vmin=0, vmax=K_REFRACTORY)

img = ax1.imshow(grid, cmap=cmap, norm=norm, interpolation='nearest')
ax1.set_title("Mapa de Calor da Infecção (SIRS)\nBranco=Infectado | Verde=Suscetível | Cinza=Imune")
ax1.axis('off')

# Configuração do Gráfico de Linhas
ax2.set_title("Evolução da População")
ax2.set_xlabel("Tempo")
ax2.set_ylabel("Proporção")
ax2.set_ylim(0, 1.0)
ax2.grid(True, linestyle='--', alpha=0.6)

s_data, i_data, r_data = [], [], []
# Cores das linhas combinando com o mapa
s_line, = ax2.plot([], [], label='Suscetíveis (S)', color='green', linewidth=2)
i_line, = ax2.plot([], [], label='Infectados (I)', color='orange', linewidth=2, linestyle='--') # Laranja para destacar
r_line, = ax2.plot([], [], label='Recuperados (R)', color='gray', linewidth=2)
ax2.legend(loc='upper right')

# AQUI CONTROLA A VELOCIDADE: interval=100 (quanto maior, mais lento)
ani = animation.FuncAnimation(fig, update, fargs=(img, grid, ax2, s_line, i_line, r_line, s_data, i_data, r_data),
                              frames=T_STEPS, interval=100, blit=False, repeat=False)

plt.tight_layout()
plt.show()