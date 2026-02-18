# 🦠 Simulação de Dinâmicas Epidêmicas via Autômatos Celulares (Modelo SIRS)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)

> Este projeto implementa uma simulação computacional baseada em **Autômatos Celulares (AC)** para modelar a propagação de doenças infecciosas. O foco é a comparação entre **estados endêmicos naturais** (formação de espirais) e **cenários pandêmicos** (como a COVID-19) com intervenção vacinal.

Desenvolvido como parte da disciplina de Computação Gráfica/Modelagem na **UFRPE**.

---

## 📸 Visualização dos Resultados

### 1. Cenário Endêmico (Sem Vacina)
A doença se auto-organiza em **ondas espirais**. Os focos de infecção giram em torno de núcleos imunes, mantendo a doença viva indefinidamente (estado meta-estável).

![Ondas Espirais](assets/espiral.png)
*(Exemplo da formação de espirais no modelo Greenberg-Hastings)*

### 2. Cenário Pandêmico & Vacinação (COVID-19)
Simulação de ondas recorrentes (variantes) e o impacto de uma **campanha de vacinação**. Os pontos azuis (vacinados) criam barreiras que quebram a propagação do vírus (pontos vermelhos).

![Vacinação e Extinção](assets/vacina_final.png)
*(Visualização do efeito de percolação: a vacina bloqueia o vírus e extingue a epidemia)*

---

## 🧪 Fundamentação Teórica

O projeto utiliza o modelo de **Greenberg-Hastings** para meios excitáveis, adaptado para a epidemiologia espacial **SIRS** (Suscetível $\to$ Infectado $\to$ Recuperado $\to$ Suscetível).

A dinâmica é regida por regras locais em uma grade $L \times L$:
- **Suscetível (Verde):** Pode ser infectado por vizinhos (contágio local) ou espontaneamente (variantes).
- **Infectado (Vermelho/Branco):** Transmite a doença e torna-se imune no próximo passo.
- **Recuperado (Cinza):** Imunidade temporária que decai com o tempo.
- **Vacinado (Azul):** Barreira permanente que impede a propagação (bloqueio de percolação).

---

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de ter o Python instalado. As dependências são apenas `numpy` (para a matemática da grade) e `matplotlib` (para a animação).

```bash
pip install numpy matplotlib
