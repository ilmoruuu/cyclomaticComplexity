from radon.complexity import cc_visit
import os
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

PROJECT_PATH = PROJECT_PATH = "" #Aqui o Path do Projeto

#Aqui vai ser lido todos os arquivos
def get_python_files(path):
    py_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


def analyze_complexity(path):
    files = get_python_files(path)
    results = []
    total_complexity = 0
    total_functions = 0

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()
        analysis = cc_visit(code)
        for item in analysis:
            results.append({
                "file": file,
                "name": item.name,
                "complexity": item.complexity
            })
            total_complexity += item.complexity
            total_functions += 1

    avg_complexity = total_complexity / total_functions if total_functions else 0

    print("\n📊 RESULTADOS GERAIS")
    print(f"Arquivos analisados: {len(files)}")
    print(f"Total de funções: {total_functions}")
    print(f"Soma da complexidade: {total_complexity:.2f}")
    print(f"Média por função: {avg_complexity:.2f}")

    results.sort(key=lambda x: x["complexity"], reverse=True)
    top = results[:920]

    print("\n| Funções mais complexas: |")
    for r in top:
        print(f"{r['name']} ({r['file']}) → V(G) = {r['complexity']}")

    # Gráfico de barras
    nomes = [f"{os.path.basename(r['file'])}\n{r['name']}" for r in top]
    valores = [r["complexity"] for r in top]

    plt.figure(figsize=(15,300))
    plt.barh(nomes, valores, color="steelblue")
    plt.xlabel("Complexidade Ciclomática (V(G))")
    plt.ylabel("Função")
    plt.gca().invert_yaxis()
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

    # Gerar Relatório com Mathplotlib
    with open("relatorio_complexidade.txt", "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE COMPLEXIDADE CICLOMÁTICA (Radon)\n\n")
        f.write(f"Arquivos analisados: {len(files)}\n")
        f.write(f"Total de funções: {total_functions}\n")
        f.write(f"Soma da complexidade: {total_complexity:.2f}\n")
        f.write(f"Média por função: {avg_complexity:.2f}\n\n")
        f.write("Top 15 funções mais complexas:\n")
        for r in top:
            f.write(f" - {r['name']} ({r['file']}) → V(G) = {r['complexity']}\n")

    print("\n📁 Relatório salvo em: relatorio_complexidade.txt")


if __name__ == "__main__":
    analyze_complexity(PROJECT_PATH)
