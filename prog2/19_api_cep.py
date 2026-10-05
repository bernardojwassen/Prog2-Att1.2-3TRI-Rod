"""Exercício 19 — Requisição GET na API pública ViaCEP (somente biblioteca padrão)."""
import json
import urllib.error
import urllib.request


def consultar_cep(cep: str) -> dict:
    cep = "".join(c for c in cep if c.isdigit())
    if len(cep) != 8:
        raise ValueError("O CEP deve ter 8 dígitos.")
    url = f"https://viacep.com.br/ws/{cep}/json/"      # URL utilizada
    with urllib.request.urlopen(url, timeout=10) as resposta:   # método GET
        if resposta.status != 200:                      # código de resposta
            raise RuntimeError(f"Resposta inesperada: HTTP {resposta.status}")
        dados = json.load(resposta)                     # interpreta o JSON
    if dados.get("erro"):
        raise LookupError("CEP não encontrado.")
    return dados


def main():
    cep = input("Digite um CEP: ")
    try:
        d = consultar_cep(cep)
        print(f"Logradouro: {d['logradouro']}\nBairro: {d['bairro']}\nCidade: {d['localidade']}-{d['uf']}")
    except ValueError as e:
        print("Entrada inválida:", e)
    except LookupError as e:
        print(e)
    except urllib.error.HTTPError as e:
        print("Erro HTTP:", e.code)
    except urllib.error.URLError as e:
        print("Falha de conexão:", e.reason)


if __name__ == "__main__":
    main()
