# Praia ou Montanha — Estatística e Amostragem em Python

Repositório com implementações em Python que acompanham o estudo de caso **Praia ou Montanha**, abordando dimensionamento amostral, inferência estatística, simulações de Monte Carlo, verossimilhança e intervalos de confiança para proporções.

O projeto é composto por um notebook interativo voltado para visualização e exploração didática e por um script de linha de comando em Python puro para cálculos rápidos de parâmetros amostrais.

---

## Estrutura do Repositório

| Arquivo | Descrição | Dependências |
| :--- | :--- | :--- |
| `praia_montanha.ipynb` | Notebook completo com cálculos, gráficos, simulações de Monte Carlo, curvas de verossimilhança e painel interativo. | `numpy`, `pandas`, `matplotlib`, `scipy`, `ipywidgets` |
| `calculo_parametros.py` | Script CLI em Python puro para cálculo de tamanho de amostra, fração amostral e avaliação de resultados observados. | Apenas biblioteca padrão do Python (`argparse`, `math`, `statistics`) |

---

## Fundamentação Estatística

Os códigos implementam os seguintes conceitos e formulações matemáticas:

* **Tamanho mínimo da amostra (pior caso $p = 0{,}5$):**
  $$n_0 = \frac{z_{\alpha/2}^2 \cdot p(1 - p)}{\varepsilon^2}$$

* **Correção para população finita (implementada no notebook):**
  $$n = \frac{n_0}{1 + \frac{n_0 - 1}{N}}$$

* **Erro padrão e margem de erro real:**
  $$EP = \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}, \qquad \text{margem} = z_{\alpha/2} \cdot EP$$

* **Diferença entre proporções e empate técnico (implementada no notebook):**
  Para $D = \hat{p}_B - \hat{p}_A = 2\hat{p} - 1$, o erro padrão da diferença é $EP_D = 2 \cdot EP$. Caso o intervalo de confiança $[D - z \cdot EP_D;\; D + z \cdot EP_D]$ contenha zero, caracteriza-se empate técnico.

* **Verossimilhança relativa e Informação Observada:**
  $$L_{\text{rel}}(p) = \frac{L(p)}{L(\hat{p})}, \qquad I(\hat{p}) = \frac{n}{\hat{p}(1 - \hat{p})}, \qquad EP = \frac{1}{\sqrt{I(\hat{p})}}$$

* **Poder estatístico (80%):**
  Estimativa do tamanho de amostra necessário para desempatar estatisticamente uma diferença observada $D$ com poder de $80\%$.

---

## 1. Notebook Interativo (`praia_montanha.ipynb`)

O notebook organiza a análise em 10 seções sequenciais, com formatação numérica no padrão brasileiro (separador de milhar por ponto e decimal por vírgula):

1. **Parâmetros e cálculos:** Função central `calcular()` que computa valor crítico $z$, $n_0$, $n$ corrigido, erro padrão, margem de erro, intervalo de confiança da diferença, veredito e $n$ para poder de $80\%$, exibidos em tabela via `resumo()`.
2. **Amostragem de população:** Sorteio aleatório de 40 indivíduos em uma grade de 400 pessoas para ilustrar a variação de $\hat{p}$ em torno de $p$.
3. **Os pilares do tamanho da amostra:** Gráficos dedicados à variabilidade $p(1 - p)$, à distribuição Normal padrão (áreas de confiança e rejeição $\alpha$) e ao decaimento da margem de erro em função de $\sqrt{n}$ (escala logarítmica).
4. **Pesquisa realizada:** Gráfico de barras comparativo entre Praia e Montanha com barras de erro correspondentes à margem real.
5. **Bernoulli para Binomial:** Distribuição exata de probabilidade $K \sim \text{Binomial}(n, p)$ sobreposta à aproximação Normal.
6. **Simulação de Monte Carlo:** Execução de $10.000$ pesquisas simuladas demonstrando a distribuição amostral de $\hat{p}$, a cobertura empírica do intervalo de confiança e a convergência do desvio padrão observado para o erro padrão teórico.
7. **Verossimilhança:** Curvas de verossimilhança relativa e log-verossimilhança com linha de corte do intervalo de confiança e tabela de plausibilidade para valores candidatos de $p$.
8. **Curvatura e Erro Padrão:** Comparação de curvas de verossimilhança para diferentes tamanhos de amostra ($n/10$, $n/4$, $n$, $4n$, $16n$) acompanhada de tabela de Informação Observada $I(\hat{p})$.
9. **Intervalo de Confiança da Diferença:** Visualização lado a lado dos intervalos individuais e do intervalo da diferença $D = \text{Montanha} - \text{Praia}$.
10. **Painel interativo:** Interface com `ipywidgets` permitindo ajustar ao vivo o nível de confiança ($80\%$ a $99{,}9\%$), margem de erro ($0{,}5$ a $10$ p.p.), proporção observada, população $N$ e tamanho de amostra $n$.

### Como executar o notebook

**No Google Colab:**
1. Abra o arquivo `.ipynb` no Google Colab.
2. No menu superior, acesse **Ambiente de execução -> Executar tudo**.

**Localmente (Jupyter):**
```bash
pip install numpy pandas matplotlib scipy ipywidgets
jupyter notebook praia_montanha.ipynb