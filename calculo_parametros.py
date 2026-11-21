"""
Cálculo dos parâmetros do estudo — "Praia ou Montanha?"

Mesmas contas da apresentação (praia-montanha.html), separadas em Python puro
(só biblioteca padrão, sem numpy).

Uso:
    python calculo_parametros.py                     # pergunta os valores
    python calculo_parametros.py --N 15000000 --conf 95 --eps 3
    python calculo_parametros.py --N 15000000 --conf 95 --eps 3 --pA 55
"""

import argparse
import math
from statistics import NormalDist


def calcular_parametros(N, conf, eps, p=0.5):
    """
    N    : tamanho da população
    conf : nível de confiança em % (ex.: 95)
    eps  : margem de erro desejada em pontos percentuais (ex.: 3)
    p    : proporção usada no planejamento (0,5 = pior caso, variabilidade máxima)
    """
    alpha = 1 - conf / 100                       # significância
    z = NormalDist().inv_cdf(1 - alpha / 2)      # valor crítico z_(α/2)
    e = eps / 100                                # margem em proporção

    n0 = p * (1 - p) / e ** 2 * z ** 2           # n0 = p(1−p)/ε² · z²
    n = min(N, math.ceil(n0 - 1e-9))             # arredonda sempre para cima
    fracao = n / N                               # fração amostral n/N

    return {
        "N": N, "conf": conf, "alpha": alpha, "z": z, "eps": e,
        "p": p, "variabilidade": p * (1 - p),
        "n0": n0, "n": n, "fracao": fracao,
    }


def resultado_pesquisa(n, conf, pA, nomeA="Praia", nomeB="Montanha"):
    """
    Resultado observado: a opção com maior proporção vira a referência (X = 1).
    pA : porcentagem observada para a opção A (a opção B recebe 100 − pA)
    """
    z = NormalDist().inv_cdf(1 - (1 - conf / 100) / 2)
    pa, pb = pA / 100, 1 - pA / 100
    if pa >= pb:
        lider, outro, p_hat = nomeA, nomeB, pa
    else:
        lider, outro, p_hat = nomeB, nomeA, pb

    k = round(n * p_hat)                         # votos da opção à frente
    ep = math.sqrt(p_hat * (1 - p_hat) / n)      # erro padrão
    margem = z * ep
    ic_lider = (p_hat - margem, p_hat + margem)
    ic_outro = (1 - p_hat - margem, 1 - p_hat + margem)
    empate = p_hat == 0.5 or ic_lider[0] <= 0.5  # intervalos se sobrepõem

    return {
        "lider": lider, "outro": outro, "p_hat": p_hat, "k": k,
        "ep": ep, "margem": margem, "ic_lider": ic_lider, "ic_outro": ic_outro,
        "empate": empate,
    }


# ---------- formatação em pt-BR ----------
def br(x, d=0):
    return f"{x:,.{d}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def pedir(texto, tipo=float):
    while True:
        valor = input(texto).strip().replace(",", ".")
        try:
            v = tipo(float(valor))
            if v > 0:
                return v
        except ValueError:
            pass
        print("  Valor inválido, tente de novo.")


def main():
    ap = argparse.ArgumentParser(description="Parâmetros do estudo de amostragem")
    ap.add_argument("--N", type=int, help="tamanho da população")
    ap.add_argument("--conf", type=float, help="nível de confiança em %% (ex.: 95)")
    ap.add_argument("--eps", type=float, help="margem de erro em p.p. (ex.: 3)")
    ap.add_argument("--pA", type=float, help="%% observada para a opção A (opcional)")
    ap.add_argument("--nomeA", default="Praia")
    ap.add_argument("--nomeB", default="Montanha")
    a = ap.parse_args()

    N = a.N or pedir("Tamanho da população (N): ", int)
    conf = a.conf or pedir("Nível de confiança (%): ")
    eps = a.eps or pedir("Margem de erro (p.p.): ")

    P = calcular_parametros(N, conf, eps)
    print("\n=== Parâmetros do estudo ===")
    print(f"População N           : {br(P['N'])}")
    print(f"Nível de confiança    : {br(P['conf'], 1)}%  (α = {br(P['alpha'], 3)})")
    print(f"Valor crítico z       : {br(P['z'], 3)}")
    print(f"Margem de erro ε      : ±{br(eps, 1)} p.p.  ({br(P['eps'], 3)})")
    print(f"Variabilidade p(1−p)  : {br(P['variabilidade'], 2)}  (p = 0,5, pior caso)")
    print(f"n0 = p(1−p)/ε² · z²   : {br(P['n0'], 2)}")
    print(f"Tamanho da amostra n  : {br(P['n'])} pessoas")
    print(f"Fração amostral n/N   : {br(P['fracao'] * 100, 4)}%")

    if a.pA is not None:
        R = resultado_pesquisa(P["n"], conf, a.pA, a.nomeA, a.nomeB)
        print("\n=== Resultado da pesquisa ===")
        print(f"À frente              : {R['lider']} com {br(R['p_hat'] * 100, 1)}% ({br(R['k'])} votos)")
        print(f"Erro padrão           : {br(R['ep'] * 100, 2)} p.p.")
        print(f"Margem real           : ±{br(R['margem'] * 100, 1)} p.p.")
        print(f"IC {R['lider']:<18}: [{br(R['ic_lider'][0] * 100, 1)}%; {br(R['ic_lider'][1] * 100, 1)}%]")
        print(f"IC {R['outro']:<18}: [{br(R['ic_outro'][0] * 100, 1)}%; {br(R['ic_outro'][1] * 100, 1)}%]")
        print("Conclusão             : " + ("empate técnico" if R["empate"] else f"{R['lider']} lidera"))


if __name__ == "__main__":
    main()
