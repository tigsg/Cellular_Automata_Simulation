import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap, BoundaryNorm

# ==========================================
# PARÂMETROS: CAMPANHA DE VACINAÇÃO
# ==========================================
L = 100                 
T_STEPS = 1000          # Tempo longo para ver o antes e depois
K_REFRACTORY = 20       
INFECTION_PROB = 1.0    
SPONTANEOUS_PROB = 0.001 
INITIAL_INFECTED = 0.01 

# Configuração da Campanha
VAC_START_STEP = 300    # A vacina só chega no passo 300 (Quando o caos já reina)
VAC_SPEED = 0.005       # 0.5% da população é vacinada por passo (Logística)
MAX_VAC_RATE = 0.85     # Meta: Vacinar 85% da população

# ==========================================
# LÓGICA DO MODELO
# ==========================================
def update(frame, img, grid, ax_curve, s_line, i_line, r_line, v_line, s_data, i_data, r_data, v_data):
    new_grid = grid.copy()
    N, M = grid.shape
    
    # --- LÓGICA DA CAMPANHA DE VACINAÇÃO ---
    # Se já passou do tempo de início e ainda não atingiu a meta
    current_vac_pct = np.sum(grid == 99) / (N * M)
    if frame >= VAC_START_STEP and current_vac_pct < MAX_VAC_RATE:
        # Seleciona aleatoriamente células para vacinar
        # Vacina N células por vez baseado na velocidade
        num_to_vaccinate = int((N * M) * VAC_SPEED)
        for _ in range(num_to_vaccinate):
            rx, ry = np.random.randint(0, N, 2)
            # Só vacina quem não é vacinado E NÃO ESTÁ INFECTADO (vacina preventiva)
            # Se quiser simular cura, tire a condição '!= 1'
            if new_grid[rx, ry] != 99 and new_grid[rx, ry] != 1:
                new_grid[rx, ry] = 99

    # --- LÓGICA DA DOENÇA ---
    for i in range(N):
        for j in range(M):
            state = grid[i, j]
            
            if state == 99: continue # Vacinado é parede

            elif state == 0:  # Suscetível
                infected_neighbors = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0: continue
                        ni, nj = (i + di) % N, (j + dj) % M
                        if grid[ni, nj] == 1:
                            infected_neighbors += 1
                
                if infected_neighbors > 0:
                    if np.random.random() < INFECTION_PROB:
                        new_grid[i, j] = 1
                elif np.random.random() < SPONTANEOUS_PROB:
                    new_grid[i, j] = 1
                        
            elif state == 1: # Infectado -> Recuperado
                new_grid[i, j] = 2
                
            elif state >= 2 and state < 99: # Imunidade Natural (Decai)
                if state < K_REFRACTORY:
                    new_grid[i, j] += 1
                else:
                    new_grid[i, j] = 0 

    grid[:] = new_grid[:]
    img.set_data(grid)
    
    # Dados para gráfico
    total = N * M
    s_data.append(np.sum(grid == 0) / total)
    i_data.append(np.sum(grid == 1) / total)
    r_data.append(np.sum((grid > 1) & (grid < 99)) / total)
    v_data.append(np.sum(grid == 99) / total)
    
    x = range(len(s_data))
    s_line.set_data(x, s_data)
    i_line.set_data(x, i_data)
    r_line.set_data(x, r_data)
    v_line.set_data(x, v_data)
    
    # Adiciona uma linha vertical no gráfico marcando o início da vacinação
    if frame == VAC_START_STEP:
        ax_curve.axvline(x=VAC_START_STEP, color='blue', linestyle='--', alpha=0.5, label='Início Vacinação')
        ax_curve.legend()

    ax_curve.set_xlim(0, max(100, len(s_data) + 10))
    
    return img, s_line, i_line, r_line, v_line

# ==========================================
# VISUALIZAÇÃO
# ==========================================
grid = np.zeros((L, L), dtype=int)

# Inicia apenas com infecção (SEM VACINA AINDA)
infection_mask = np.random.random((L, L)) < INITIAL_INFECTED
grid[infection_mask] = 1

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Verde(S), Vermelho(I), Cinza(R), Azul(V)
cmap = ListedColormap(['#abf7b1', '#ff0000', '#505050', '#0000FF']) 
bounds = [0, 1, 2, K_REFRACTORY+1, 100]
norm = BoundaryNorm(bounds, cmap.N)

img = ax1.imshow(grid, cmap=cmap, norm=norm, interpolation='nearest')
ax1.set_title("Simulação em Tempo Real: Doença vs Vacina")
ax1.axis('off')

ax2.set_title("Efeito da Intervenção Vacinal")
ax2.set_xlabel("Tempo")
ax2.set_ylabel("População")
ax2.set_ylim(0, 1.0)
ax2.grid(True, linestyle='--', alpha=0.6)

s_data, i_data, r_data, v_data = [], [], [], []
s_line, = ax2.plot([], [], label='Suscetíveis', color='#abf7b1', linewidth=2)
i_line, = ax2.plot([], [], label='Infectados', color='red', linewidth=2.5)
r_line, = ax2.plot([], [], label='Recuperados (Nat)', color='gray', linewidth=1)
v_line, = ax2.plot([], [], label='Vacinados', color='blue', linewidth=2)
ax2.legend()

ani = animation.FuncAnimation(fig, update, fargs=(img, grid, ax2, s_line, i_line, r_line, v_line, s_data, i_data, r_data, v_data),
                              frames=T_STEPS, interval=50, blit=False, repeat=False)

plt.tight_layout()
plt.show()