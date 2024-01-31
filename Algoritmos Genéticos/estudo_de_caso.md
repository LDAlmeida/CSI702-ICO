# Um algoritimo memético para a otimização de quantizadores vetorias.

## Qual o problema?
A codificação eficiente de sinais. O artigo visa melhorar a Quantização Vetorial (QV) [1,2] que é utilizado em imagens [6-8], identificação vocal [10], esconder
informações em imagem [11].

## O que são algoritmos de otimização
Algoritmos de otimização podem ser usados para melhorar o desempenho de quantizadores vetoriais.

## O que é um algoritmo genético
No contexto do artigo, um AG [27] recebe como entrada dicionários
gerados por algum algoritmo de projeto de dicionários e tenta obter um melhor dicionário mediante aplicações sucessivas de
operadores, tais como, recombinação (ou cruzamento) e mutação, em um processo evolutivo

## O algoritmo LBG
O algoritmo Linde-Buzo-Gray (LBG) [13], também conhecido como Algoritmo de Lloyd Generalizado, constitui-se
na técnica mais utilizada para o projeto de dicionários. 

## A implementação do artigo

No presente artigo, um AG híbrido modificado é utilizado para a otimização de dicionários projetados com o
algoritmo LBG. O AG modificado é composto de um módulo de otimização local. Especificamente, as soluções encontradas
ao final de cada geração do AG são atualizadas de acordo com o método de Lee et al. [28], o qual consiste em uma versão
acelerada do LBG. 

## Diferença do AM para o AG
A estratégia de integração de módulos de busca local a algoritmos evolutivos, como aqui se propõe,
constitui-se em uma característica inerente a Algoritmos Meméticos [29].

## Como foi utilizado o algoritmo memético para resolver o problema

O algoritmo proposto no presente artigo deriva da estratégia AG + LBG, ou seja, aplicar o LBG à saída do AG. Foram contudo modificados 4 items:

i. modificou-se a estratégia de recolocação de forma a aceitar todos os filhos que representam melhores soluções em relação àquelas já conhecidas;
ii. com probabilidade 1 – pacc (em que pacc é a probabilidade de aceitação), rejeitam-se as soluções produzidas que não obtiverem ganhos sobre o pior indivíduo presente na população. Quando aceito, um filho irá sempre substituir o pior
indivíduo;
iii. substituiu-se o algoritmo LBG convencional pela versão acelerada proposta em [28] para o módulo de otimização
local
iv. em vez de aplicar o LBG acelerado ao melhor indivíduo a cada geração, aplica-se o algoritmo à nova solução gerada