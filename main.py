import math

def main():
    camera = Camera(Ponto(0, 0, 0), Ponto(0, 0, -1), Vetor(0, 1, 0), 1.0, 800, 600)

    esfera = Esfera(Ponto(0, 0, -5), 1, Vetor(1, 0, 0))
    plano = Plano(Ponto(0, -1, 0), Vetor(0, 1, 0), Vetor(0, 1, 0))

    raio = Raio(camera.posicao, Vetor(0, 0, -1))

    intersecao_esfera = esfera.intersectar(raio)
    if intersecao_esfera:
        print(f"Raio intersecta a esfera em: {intersecao_esfera}")
    else:
        print("Sem interseção com a esfera")

    intersecao_plano = plano.intersectar(raio)
    if intersecao_plano:
        print(f"Raio intersecta o plano em: {intersecao_plano}")
    else:
        print("Sem interseção com o plano")

if __name__ == "__main__":
    main()