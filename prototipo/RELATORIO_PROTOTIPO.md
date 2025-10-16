# RELATÓRIO TÉCNICO - PROTÓTIPO DO SIMULADOR DE MEDIDOR DE VENTURI

## INTRODUÇÃO

O presente relatório apresenta o desenvolvimento de um protótipo funcional de um simulador interativo para medidores de Venturi, desenvolvido como ferramenta educacional para o ensino de mecânica dos fluidos e instrumentação industrial. O protótipo foi construído utilizando tecnologias web modernas, especificamente a biblioteca Streamlit do Python, combinada com bibliotecas científicas como NumPy e Matplotlib para processamento numérico e visualização de dados.

## DESCRIÇÃO DO PROTÓTIPO

O protótipo desenvolvido consiste em uma aplicação web interativa que simula o comportamento de medidores de Venturi, permitindo aos usuários configurar parâmetros geométricos e de escoamento para calcular e visualizar os resultados correspondentes. A aplicação oferece dois modos de operação distintos: o modo simulação, onde o usuário define uma vazão volumétrica e o sistema calcula o desnível manométrico resultante, e o modo medidor, onde o usuário fornece um desnível manométrico medido e o sistema calcula a vazão correspondente.

As principais funcionalidades implementadas incluem uma interface gráfica intuitiva com controles deslizantes para ajuste de parâmetros, cálculos automáticos baseados na equação de Bernoulli, visualizações esquemáticas do medidor de Venturi, representação gráfica de manômetros diferenciais em U, e exibição de resultados numéricos organizados. A interface foi projetada com foco na usabilidade, utilizando um layout responsivo com abas organizadas que separam as diferentes visualizações e informações.

## CONTEÚDOS E CONCEITOS ABORDADOS

O protótipo abrange conceitos fundamentais da mecânica dos fluidos, especificamente os princípios da equação de Bernoulli aplicados ao escoamento em condutos. Os conceitos principais incluem a conservação de energia em escoamentos incompressíveis, a relação entre velocidade e pressão em seções de diferentes áreas, e a aplicação prática desses princípios na medição de vazão através de dispositivos de restrição.

A aplicação também aborda conceitos de instrumentação industrial, particularmente o funcionamento de medidores de pressão diferencial e a utilização de manômetros em U para medição de diferenças de pressão. Os conceitos de densidade de fluidos, propriedades manométricas, e a relação entre pressão e altura de coluna de líquido são fundamentais para o funcionamento do simulador.

Do ponto de vista tecnológico, o protótipo demonstra a aplicação de programação científica em Python, utilizando bibliotecas especializadas para cálculos numéricos e visualização de dados. A integração entre backend de cálculos e frontend de visualização através do framework Streamlit representa uma abordagem moderna para desenvolvimento de aplicações educacionais interativas.

## APLICAÇÃO TÉCNICA DOS CONCEITOS

A implementação técnica do protótipo baseia-se na equação de Bernoulli simplificada, aplicada entre duas seções do medidor de Venturi. O cálculo da velocidade na garganta é realizado através da equação de continuidade, considerando a conservação de massa entre as seções de entrada e garganta. A diferença de pressão é calculada utilizando a relação entre as velocidades e as densidades dos fluidos envolvidos.

A classe VenturiSimulator implementa os cálculos fundamentais, incluindo a determinação das áreas das seções transversais, o cálculo das velocidades de escoamento, e a aplicação da equação de Bernoulli para determinar a diferença de pressão. O sistema permite a configuração de diferentes densidades de fluidos e propriedades manométricas, simulando condições reais de operação.

A visualização gráfica é implementada através de funções especializadas que utilizam a biblioteca Matplotlib para criar diagramas esquemáticos e representações de manômetros. A função plotar_diagrama_venturi gera uma representação visual do medidor, incluindo as dimensões principais e pontos de medição, enquanto a função plotar_manometro cria uma representação detalhada do manômetro diferencial em U, mostrando o desnível de líquido manométrico e as pressões correspondentes.

## COMPARAÇÃO ENTRE PROTÓTIPO E TRABALHO FINAL

O protótipo atual representa aproximadamente 30% da funcionalidade planejada para o trabalho final, focando nos aspectos fundamentais de cálculo e visualização básica. As funcionalidades já implementadas incluem a interface de usuário completa, os cálculos básicos da equação de Bernoulli, a visualização esquemática do medidor, e a representação do manômetro diferencial. O sistema de navegação por abas e a organização dos resultados numéricos também estão completamente funcionalizados.

As principais limitações do protótipo atual incluem a ausência de cálculos avançados que considerem perdas por atrito, a falta de análise do regime de escoamento através do número de Reynolds, e a inexistência de exemplos práticos pré-configurados. O protótipo não inclui funcionalidades de análise de sensibilidade, exportação de dados, ou geração de relatórios automáticos.

Para o trabalho final, estão planejadas implementações que expandirão significativamente as capacidades do sistema. A Fase 1 incluirá a implementação da equação de Bernoulli completa com consideração de perdas por atrito, o cálculo do número de Reynolds para determinação do regime de escoamento, e a incorporação do coeficiente de descarga para simulações mais realistas. A Fase 2 adicionará visualizações avançadas, incluindo gráficos de perfil de pressão ao longo do Venturi, curvas de calibração, e análises de sensibilidade de parâmetros.

A Fase 3 do trabalho final incluirá a implementação de cinco exemplos práticos pré-configurados, demonstrando diferentes cenários de aplicação e facilitando o uso educacional do sistema. A Fase 4 adicionará funcionalidades profissionais, incluindo análise estatística dos resultados, exportação de dados em formatos CSV e Excel, geração automática de relatórios em PDF, e simulação de diferentes tipos de fluidos. A Fase 5 finalizará o desenvolvimento com a implementação de uma interface profissional completa, incluindo dashboard avançado, temas personalizáveis, sistema de ajuda contextual, histórico de simulações, e funcionalidades de comparação de cenários.

## CONCLUSÃO

O protótipo desenvolvido demonstra com sucesso a viabilidade técnica e educacional do projeto proposto, oferecendo uma base sólida para o desenvolvimento do sistema completo. A implementação atual comprova a aplicabilidade das tecnologias escolhidas e a eficácia da abordagem metodológica adotada. O protótipo serve como validação conceitual do projeto, demonstrando que os objetivos educacionais podem ser alcançados através de uma interface interativa e visualmente atrativa.

A arquitetura modular implementada facilita a expansão futura do sistema, permitindo a adição gradual de funcionalidades mais avançadas sem comprometer a estabilidade do código existente. A separação clara entre lógica de cálculo, visualização e interface de usuário estabelece uma base sólida para o desenvolvimento iterativo do trabalho final.

O protótipo representa um marco importante no desenvolvimento do projeto, fornecendo uma demonstração concreta das capacidades do sistema e validando a abordagem educacional proposta. A transição para o trabalho final será baseada na expansão sistemática das funcionalidades existentes, mantendo a qualidade e usabilidade já estabelecidas no protótipo atual.
