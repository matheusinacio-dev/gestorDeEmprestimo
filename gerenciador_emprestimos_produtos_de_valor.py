'''
Gerenciamento de empréstimo de produtos com grande valor agregado, 
como equipamentos de informática, ferramentas, etc.
Envolvendo 
- Cadastro (com nome detalhado, descrição e estado)
- Empréstimo (informações do cadastro com adicionais de nome do cliente, funcionário responsável, data de empréstimo e data prevista para devolução)
- Visualização (filtragem por estado)
'''

'''
Importar da biblioteca datetime a parte "datetime"
Explicação do uso em código:
Criamos a variável data_hora para armazenar as informações de data e horário.
Atribuimos a ela o valor datetime.now() 
    - que dentro da biblioteca datetime pega as informações do momento presente, isso é do prenchimento das perguuntas.
Depois formatamos os dados capturados usando o método com a seguinte ordem:
    .strftime("Dia/Mês/Ano")
'''

from datetime import datetime

'''
Função validar_prenchimento recebe o parametro mensagem, que é prenchido pelo usuário.
Nessa função, temos um loop infinito com uma simples validação de valor não vazio. 
Se o valor é prenchido, o return confirma o resultado e sai do loop. 
Se não, exibe um aviso no terminal e o loop infinito roda de novo. 
Assim o usuário pode prencher o campo.
'''

def validar_prenchimento(mensagem):
    while True:
        valor = ""
         # O método strip() remove os espaços em branco no início e no fim da string. quando nenhum parâmetro é passado.
         # Garantindo que as comparações sejam feitas com os valores tratados e assim, evitando erros. 
        valor = input(mensagem).strip()

        if valor:
            return valor

        print("Erro: o campo não pode ficar vazio.")



# Lista que vai guardar os produtos e seus dados

# Explicação do produtos = {} dentro do while
'''
        Cria um dicionário novo a cada volta do loop. Sem que os dados persistam depois de usados.
            - Devido ao "coletor de lixo" do python, que verá a lista produtos como a única referência.
        Evitando que os valores das próximas voltas sejam sobre-escritos pelos valores da volta 1. 
        Caso criassemos uma variável global, teríamos um único endereço de informações para ser ocupado. 
            - Então as informações repetiriam a cada volta do loop.
        Já com a variável local, a cada volta um novo endereço é criado.
 '''


'''
Função cadastro de novo produto - única entrada para produtos novos
- Novo objeto a cada vez
- Gera:
    -  ID - váriavel global próximo_id, que será puxada para o escopo local da função cadastro_produto(), 
            usando "global proximo_id", para dizer que proximo_id é a variável global.
            Por fim, incrementa à váriavel +1 a cada volta do loop, antes de preencher o dicionário. 
            Como o valor inicial é 0, o id atribuido ao primeiro produdo é 1, e assim por diante.
- Pergunta:
    - Nome com detalhes
    - Descrição do produto
- Colocar na lista principal produtos + exibir a lista produtos
- Quebrar o loop (break dentro da função cadastrar produto) 
- Questionar se deseja cadastrar outro produto (bloco match/case - caso 1)
    - sim - rodar mais uma vez o cadastro
    - não - voltar para o menu principal
'''
proximo_id = 0
produtos = []


def cadastro_produto():
     
     while True:
          produto = {}
          global proximo_id
          proximo_id += 1
          nome_produto = validar_prenchimento("Nome do Produto com detalhes: ")
          descricao_produto = validar_prenchimento("Descrição do Produto (ex.: local de uso,...): ")
          estado = "disponível"
          produto.update({
        "id": proximo_id,
        "nome_produto": nome_produto,
        "descricao_produto": descricao_produto,
        "estado": estado
        })
          produtos.append(produto)
          print(produtos)
          break

'''
Função para emprestar o produto

1 - verificar a disponibilidade
    criar lista "disponiveis" vazia
    rodar um for que percorrerá a lista produtos, que tem como itens os produtos cadastrados
    verificar se a chave "estado" do dicionário "produto" == "disponível" (todos os produtos cadastrados são de estado "disponível")
    acrescentar a lista "disponíveis"
    após o loop for, caso a lista "disponíveis" continue vazia, o que quer dizer que não existem produtos cadastrados, aparece uma mensagem no terminal
    return - encerra a execução da função, voltar ao "menu de opções" (sobre o return abaixo)
    
    return - tem dois usos 
        encerrar a execução da função (a função executa até o return)
        retornar um valor (o valor está ao lado do return)
    
2 - exibir os produtos que podem ser emprestados 
    loop for percorrer a lista de disponíveis, exibindo no terminal id, nome e descrição de cada produto

3 - escolha de produto a ser emprestado
    pedir pro usuário escolher um id, armazenado no "id_escolhido"  
    for percorre a lista principal "produtos" - dicionários "produto" foram "cadastrados"
        se o "id_escolhido" == valor da chave "id" daquele produto, perguntasse as seguintes informações:
            - funcionário responsável pelo empréstimo
            - cliente
            - prazo do empréstimo/devolução
        depois, o produto, na lista principal "produtos" é atualizado com as chaves e valores novos, e o seu "estado" é modificado para "em uso".
            nota-se que as chaves e valores do "cadastro" são mantidas pelo método .update(), desde que não modificadas.

        debug - print da lista produtos
        mensagem no terminal de empréstimo bem sucedido
        return - interromper o restante da função

        se o if não for execultado até o final do loop for (condição == False), o return não é executado
            ao final do loop for mal sucedido (todos os casos condição == False) exibição da mensagem no terminal - "Produto não encontrado"

'''
def emprestar_produto():

    disponiveis = []

    for produto in produtos:
        if produto["estado"] == "disponível":
            disponiveis.append(produto)

    if len(disponiveis) == 0:
        print("Não existem produtos disponíveis.")
        return

    for produto in disponiveis:
        print(f'ID: {produto["id"]} - {produto["nome_produto"]} - {produto["descricao_produto"]} ')

    id_escolhido = int(validar_prenchimento("Digite o ID do produto: "))

    for produto in produtos:

        if (produto["id"] == id_escolhido and produto["estado"] == "disponível"):
            funcionario = validar_prenchimento("Qual o seu nome? ")
            cliente = validar_prenchimento("Nome do cliente: ")
            prazo = validar_prenchimento("Data prevista para devolução (dd/mm/aaaa): ")

            produto.update({
                "estado": "em uso",
                "funcionario": funcionario,
                "cliente": cliente,
                "data_emprestimo": datetime.now().strftime("%d/%m/%Y"),
                "data_devolucao": prazo
            })

            print(produtos)  # debug

            print("Produto emprestado com sucesso.")
            return
    
    print("Produto não encontrado.")
    
'''
Função devolver produto - "em uso" e expirarante hoje -> "disponível"
1 - checar se há produtos que expiram hoje. Se sim, informa os dados chave, se não, avisa que não tem.
2 - pedir para selecionar um "id".
3 - roda uma verificação na lista principal - centralizar os dados.
    caso o id digitado não for encontrado -> mensagem no terminal "produto não encontrado"
4 - alterar o estado para "disponível" e deletar os dados do empréstimo
5 - mostrar a lista de produtos atualizada
6 - mensagem do terminal de sucesso da operação

'''
def devolver_produto():
    prazos_expirantes_hoje = []
    for produto in produtos :
        # checar se há produtos expirantes hoje e se não, avisar
        if produto["estado"] == "em uso" and produto["data_devolucao"] == datetime.now().strftime("%d/%m/%Y"):
            prazos_expirantes_hoje.append(produto)
            print(f'{produto["id"]} - {produto["nome_produto"]} - {produto["descricao_produto"]} - Expira hoje: {produto["data_devolucao"]} ')
        
    if len(prazos_expirantes_hoje) == 0:
        print("Nenhum produto espirante hoje!!!")
        return

    id_escolhido = int(validar_prenchimento("Digite o ID do produto que deseja devolver: "))

    ## Modificar os produtos devolvidos
    for produto in produtos :
        if produto["estado"] == "em uso" and produto["data_devolucao"] == datetime.now().strftime("%d/%m/%Y") and produto["id"] == id_escolhido:

            ## .pop() exclui a chave do dicionário e retorna (return) o valor do segundo parâmetro, nesse caso None.
            produto.pop("funcionario", None)
            produto.pop("cliente", None) 
            produto.pop("data_emprestimo", None)
            produto.pop("data_devolucao", None)  
            produto.update({
                "estado": "disponível",
            })

            print(produtos)  # debug

            print("Produto devolvido com sucesso.")
            return
        
    print("Produto não encontrado.")




'''
Função checar vencimentos - mesmo mês e ano 
- produto[data_devolucao][3:] == datetime.now().strftime("%m/%Y")
    O formato da string é: "dd/mm/aaaa" -> [3:] corta essa string do quarto caracter ao final (índice 3) para o formato "mm/aaaa"
Checar quais são os prazos de empréstimo em vencimento ou vencidos do mês
1 - cria uma variável para ver se tem ou não vencimentos mensais. 
    Se sim, salva na variável e printa dados chave. 
    Se não, printa um aviso de que não há vencimentos nesse mês.

'''
def checar_vencimentos():
    prazos_vencimento_mensais = []

    for produto in produtos:
        if produto["estado"] == "em uso" and produto["data_devolucao"][3:] == datetime.now().strftime("%m/%Y") :
            prazos_vencimento_mensais.append(produto)
            print(f'ID: {produto["id"]} - {produto["nome_produto"]} - {produto["descricao_produto"]} - Cliente: {produto["cliente"]}  - Vence esse mês: {produto["data_devolucao"]} ')
    if len(prazos_vencimento_mensais) == 0:
        print("Nenhum produto espirante este mês!!!")
        return


'''
1 - "posicionando" uma lista para receber os valores filtrados - criada depois

    Analogia - "Em casa com goteira, [ ] seca a poça. Já o .clear() tampa a fonte (goteira)"
2 -  método .clear() limpa todos os valores da lista da memória, ideal para vários endereços ("variáveis") com os "mesmos valores" da "mesma fonte (objeto)" .
        O uso é diferente de limpar uma lista com [ ], pois nesse caso os valores são substituidos pelo [ ]. 
        O que significa que caso os valores tenha/estejam em mais de um endereço (variáveis), eles irão continuar existido.
        Logo, a limpeza com [ ] para mais de uma variável com o "mesmo valor" vindo da "mesma fonte (objeto)" não funciona.

3 - percorrer todos os elementos (dicionários) da lista produtos um a um
4 - "variável temporária" produto se torna um dicionário
5 - acessar uma chave do dicionário e verificar se o seu valor corresponde ao estado filtrado
6 - Caso corresponda (True) - adicionar dicionário em uma lista de valores filtrados
'''
def filtrar_estado(nova_lista, estado):
    nova_lista.clear() # Explicação no tópico 2 acima
    for produto in produtos:
        if produto["estado"] == estado:
            nova_lista.append(produto)


while True:
    atividade = validar_prenchimento(f'''========================================================
Qual ação você deseja executar?
1 - Cadastro de novo produto
2 - Emprestar produto já cadastrado
3 - Devolver produto emprestado que expira hoje
4 - Checar vencimentos mensais
5 - Visualização de produtos emprestados ("em uso")
6 - Visualização de produtos disponíveis ("disponível")
                                     
Digite o número da ação desejada:''')
    
    # Dentro do loop infinito, cria uma lógica de navegação centralizada em um menu guiado por números.
    # Em que cada número leva a uma "atividade" diferente definida em cases no match/case
    match atividade:
        case "1":
            while True :

                cadastro_produto()  
                quer_continuar = validar_prenchimento("Você deseja cadastrar outro produto? (S) - Sim | (N) - Não: ")
                if quer_continuar.lower() == "s":
                    continue
                elif quer_continuar.lower() == "n" :
                    break
             
        case "2":
            emprestar_produto()

        case "3":
            devolver_produto()

        case "4":
            checar_vencimentos()

        case "5":
              '''
              Explicação na linha 189
              - aqui o paramêtro nova_lista antes "posicionado" recebe a lista produtos_emprestados criada
              '''
              produtos_emprestados = []
              filtrar_estado(produtos_emprestados, "em uso")
              print(f"Essa é a lista de produtos emprestados:\n{produtos_emprestados}")   

        case "6":
              '''
              Explicação na linha 189
              - aqui o paramêtro nova_lista antes "posicionado" recebe a lista produtos_disponiveis criada
              '''
              produtos_disponiveis = []
              filtrar_estado(produtos_disponiveis, "disponível")
              
              print(f"Essa é a lista de produtos disponíveis:\n{produtos_disponiveis}")

         case "0":
              # Salva mais uma vez por segurança (caso algo tenha ficado pendente) e encerra o loop infinito
              salvar_produtos()
              print("Dados salvos. Encerrando o programa...")
              break










