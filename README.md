# Aprendizado Gamificado da Operação do Sistema Elétrico Brasileiro: Uma experiência prática e interativa

## Descrição

Este projeto consiste em um simulador interativo que permite ao usuário desempenhar o papel de um Operador do Sistema Interligado Nacional (SIN). O objetivo é equilibrar a geração e o consumo de energia de diferentes fontes, otimizando os custos operacionais e garantindo a estabilidade do sistema. O simulador é desenvolvido utilizando **Python** com a biblioteca **Tkinter** para a interface gráfica e **Matplotlib** para a geração dos gráficos interativos.

## Objetivo

O objetivo deste simulador é:
1. Proporcionar uma experiência educacional sobre a operação do sistema elétrico brasileiro.
2. Simular os desafios reais de um operador do SIN, equilibrando a geração e a demanda de energia.
3. Otimizar o custo de operação, respeitando os limites operacionais e evitando violações de segurança.

## Tecnologias Utilizadas

- **Linguagem de Programação**: Python
- **Interface Gráfica**: Tkinter
- **Visualização de Dados**: Matplotlib
- **Manipulação de Imagens**: PIL (Python Imaging Library)

## Funcionalidades

- **Gerenciamento de Carga e Geração**: O jogador ajusta a geração de energia de diferentes fontes (hidrelétrica, eólica, solar, térmica e nuclear) para atender à demanda em tempo real.
- **Variações de Fontes Intermitentes**: As fontes de energia eólica e solar apresentam variações naturais que simulam sua intermitência, tornando o jogo mais desafiador.
- **Monitoramento de Frequência**: A estabilidade do sistema elétrico depende do equilíbrio entre geração e consumo, mantendo a frequência próxima a 60 Hz.
- **Gráficos Interativos**: Gráficos que mostram a previsão de carga e a disponibilidade de geração ao longo do dia, permitindo ao jogador planejar e ajustar suas ações.
- **Controle de Custos**: O simulador calcula o custo total da operação com base no despacho de geração de cada fonte de energia.
- **Diagrama Unifilar**: Uma segunda tela mostra graficamente o fluxo de energia nas linhas de transmissão e os níveis de tensão nos barramentos, permitindo o controle do sistema em maior detalhe.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

1. **`main.py`**: Arquivo principal que contém a implementação do simulador, incluindo a lógica do jogo, interface gráfica e gráficos interativos.
2. **Dados de Geração e Carga**: Valores pré-definidos de geração e consumo de energia que simulam o comportamento real do sistema elétrico brasileiro ao longo do dia.
3. **Imagens**: O projeto inclui o uso de uma imagem de mapa (`mapaGeracoesCargas.png`) que exibe graficamente as usinas e as linhas de transmissão.

## Como Executar

1. Clone este repositório:
    ```bash
    git clone https://github.com/seu-usuario/simulador-sin.git
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd simulador-sin
    ```

3. Instale as dependências necessárias:
    ```bash
    pip install ...
    ```

4. Execute o arquivo principal:
    ```bash
    python main.py
    ```

## Requisitos

- **Python 3.8+**
- **Tkinter** (geralmente já incluído na instalação do Python)
- **Matplotlib**
- **Pillow** (PIL)

## Como Funciona

1. O jogador ajusta os valores de geração de diferentes fontes de energia utilizando barras deslizantes.
2. A carga do sistema varia ao longo do dia, exigindo ajustes constantes na geração.
3. O simulador calcula em tempo real o balanço entre geração e consumo, apresentando gráficos de previsão de carga, geração disponível e frequência do sistema.
4. Violações de segurança (frequência muito alta ou baixa) e o custo operacional são monitorados constantemente.
5. Ao final do jogo, um resumo das operações realizadas e o custo total da operação é apresentado ao jogador.

## Resultados

- O simulador permite que o usuário compreenda de maneira prática os desafios de equilibrar a geração de energia de diferentes fontes com a demanda do sistema elétrico.
- Fornece feedback em tempo real sobre o custo operacional e a estabilidade do sistema, ajudando a desenvolver habilidades de tomada de decisão sob pressão.

## Lições Aprendidas

- **Gamificação na Educação**: A gamificação se mostrou uma ferramenta poderosa para o ensino de conceitos complexos, como a operação de sistemas elétricos, de forma interativa e envolvente.
- **Desafios de Fontes Intermitentes**: A variação natural das fontes de energia solar e eólica adiciona uma camada de dificuldade, simulando com precisão as condições reais do setor elétrico.

