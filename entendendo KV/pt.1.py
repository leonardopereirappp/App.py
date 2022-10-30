# Antes de começar a explicação, gostaria de dizer que é importante ler e revisar TODOS OS PASSOS, não escrevi isso à toa

# No Kivy, sempre se faz algo assim:

ex1 = """

Label: ( Isso é como no HTML com a tag div, na dúvida chama de objeto )
    text: "Hello World"  ( O text é a propriedade do Label, e depois dos dois pontos, o que essa propriedade vai receber ( valor ) )

Image:
    arquivo: "c://..."
    posicao: "..."

Button:
    text: "Inscrever-se"
    quando_clicar: "roda uma função..."

"""

# O .kv sempre tem o objeto pai, e se tu colocar dois objetos pais, o código quebra, então o código acima (ex1) não funcionaria

# As tags pais mais recomendadas são o GridLayout e o FloatLayout

# O problema é que o GridLayout não é tão fácil, no sentido de: coloca o item na esquerda com 20% de margin-left, pra isso tu deveria separar o app em 18 colunas e colocar na última coluna, primeira linha
# Ou seja, muito trabalho, nesse caso o FloatLayout faz esse papel muito bem

ex2 = """
GridLayout:
    Label: ( Isso é como no HTML com a tag div, na dúvida chama de objeto )
        text: "Hello World"  ( O text é a propriedade do Label, e depois dos dois pontos, o que essa propriedade vai receber ( valor ) )

    Image:
        arquivo: "c://..."
        posicao: "..."
    
    Button:
        text: "Inscrever-se"
        quando_clicar: "roda uma função..."
"""

# Esse código (ex2), embora feio, já funcionaria se tivesse todas as funções

# Observação: O objeto sempre tem um nome em Capitalize ( primeira letra maiúscula ) ex:[Label, Image, Button, ...], já as propriedades sempre estarão em .lower() ( todas as letras em minúsculo ) [text, position, ...]
