# 🎓 Roteiro de Apresentação: Simulador de Venturi

**Tempo Estimado:** 10 a 15 minutos
**Objetivo:** Demonstrar o domínio dos conceitos de Fenômenos de Transporte através de uma aplicação prática de simulação.

---

## 🛠️ 1. Preparação (Antes de começar)

1.  **Abra o VS Code** na pasta do projeto.
2.  **Abra o Terminal** e execute o simulador:
    ```bash
    streamlit run app.py
    ```
3.  Deixe o **Navegador** (com o simulador aberto) e o **VS Code** (com o código) prontos para alternar (Alt+Tab).
4.  No VS Code, deixe abertos os arquivos: `app_modules/simulator.py` e `app_modules/plots.py`.

---

## 🗣️ 2. Roteiro Passo a Passo

### Parte 1: Introdução (1-2 min)
*Foco: Apresentar o problema e a solução.*

*   **O que falar:**
    > "Bom dia/Boa noite. Meu trabalho consiste no desenvolvimento de um simulador interativo para um Medidor de Venturi.
    > O objetivo foi aplicar os conhecimentos teóricos da disciplina — como equações de conservação, estática dos fluidos e perda de carga — em uma ferramenta prática que permite visualizar esses fenômenos acontecendo em tempo real.
    > Em vez de apenas resolver exercícios no papel, o software permite testar milhares de cenários e ver a física 'ganhando vida'."

### Parte 2: A Física no Código (3-4 min)
*Foco: Mostrar que você sabe ONDE a teoria está implementada. Alterne para o VS Code.*

*   **Ação:** Abra `app_modules/simulator.py`.
*   **O que falar:**
    > "Todo o motor físico do simulador está nesta classe `VenturiSimulator`. Eu mapeei os conteúdos da ementa diretamente em métodos Python:"

    1.  **Propriedades dos Fluidos:** (Mostre as linhas 16-17)
        > "Aqui definimos a densidade do fluido de trabalho e do fluido manométrico, fundamentais para os cálculos de pressão."
    2.  **Continuidade:** (Mostre as linhas 40-41 ou 52-53)
        > "Aqui aplicamos a Equação da Continuidade. Como a vazão é constante, calculamos as velocidades $v_1$ e $v_2$ baseadas na redução da área."
    3.  **Bernoulli e Hidrostática:** (Mostre as linhas 35-38)
        > "Este é o coração do medidor. Usamos a equação de Bernoulli combinada com a hidrostática do manômetro em U para relacionar o desnível $\Delta h$ com a vazão."
    4.  **Escoamento em Dutos (Perda de Carga):** (Mostre o método `_calcular_perda_carga` na linha 69)
        > "Para tornar a simulação realista, implementei a equação de Darcy-Weisbach para calcular a perda de carga por atrito, algo que modelos ideais ignoram."

### Parte 3: Demonstração Prática (5-6 min)
*Foco: Provar que funciona. Alterne para o Navegador.*

**Cenário A: O Princípio de Bernoulli (Modo Ideal)**
1.  **Ação:** Selecione "Simulação Interativa" > Modo "Ideal".
2.  **Ação:** Aumente a Vazão (Q).
3.  **O que mostrar:** Aponte para o gráfico de "Perfil de Pressão".
4.  **O que falar:**
    > "Observem que conforme o fluido acelera na garganta (pela continuidade), a pressão cai drasticamente. Isso é a visualização direta do Princípio de Bernoulli: a energia de pressão é convertida em energia cinética."

**Cenário B: Hidrostática e Manometria (Modo Medidor)**
1.  **Ação:** Mude para o Modo "Medidor".
2.  **Ação:** Mexa no slider de "Desnível ($\Delta h$)".
3.  **O que mostrar:** O desenho do Manômetro em U mudando e o valor da Vazão sendo recalculado.
4.  **O que falar:**
    > "Aqui invertemos o problema. Simulamos o que acontece na indústria: o operador lê o desnível no manômetro (Hidrostática) e o software calcula a vazão correspondente. Isso cobre o tópico de Forças Hidrostáticas da ementa."

**Cenário C: Realidade vs Ideal (Perda de Carga e Reynolds)**
1.  **Ação:** Volte para Modo "Realista".
2.  **Ação:** Vá na aba "Energia".
3.  **O que mostrar:** A linha de energia (LE) decaindo.
4.  **O que falar:**
    > "Diferente dos livros teóricos, aqui consideramos o atrito. A linha roxa (Energia Total) não é reta, ela cai. Essa queda é o $h_L$ (perda de carga).
    > Além disso, o sistema calcula o Número de Reynolds em tempo real (mostre o valor no painel), indicando se o escoamento é Laminar ou Turbulento."

### Parte 4: Conclusão (1 min)
*   **O que falar:**
    > "Concluindo, este trabalho não apenas substitui a prova teórica, mas demonstra a aplicação integrada de todos os tópicos do semestre: Propriedades, Estática, Cinemática e Dinâmica dos Fluidos. O software serve agora como uma ferramenta de verificação para qualquer exercício da disciplina."

---

## ❓ Perguntas Prováveis (FAQ)

**P: Como você calculou o fator de atrito 'f'?**
R: "Nesta simulação, o 'f' é um parâmetro de entrada (input) para permitir testar diferentes rugosidades, mas ele é usado na fórmula de Darcy-Weisbach ($h_L = f \cdot (L/D) \cdot v^2/2g$)."

**P: Onde entra a Equação de Euler?**
R: "A Equação de Euler é a base diferencial que, quando integrada ao longo de uma linha de corrente, gera a Equação de Bernoulli que usei na linha 58 do código."

**P: Por que a pressão recupera depois da garganta?**
R: "Porque a velocidade diminui na seção divergente (a área aumenta), então a energia cinética volta a se converter em pressão (Recuperação de Pressão), menos as perdas por atrito."
