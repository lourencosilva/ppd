import time
import requests
import concurrent.futures

#Função que realiza uma requisição http para uma url.
#Recebemos a resposta e verificamos qual é o status_code.
#Se for 200, sabemos que a página existe. Se for 404 a página não existe.
#Para maiores informações sobre o pacote requests(https://docs.python-requests.org/en/master/)
#Para instalar o pacote requests utilize o comando # pip install requests
def get_wiki_page_existence(wiki_page_url, timeout=10):
    response = requests.get(url=wiki_page_url, timeout=timeout)

    page_status = "unknown"
    if response.status_code == 200:
        page_status = "exists"
    elif response.status_code == 404:
        page_status = "does not exist"

    return wiki_page_url + " - " + page_status


#A ideia deste código é verificar se a wikipedia possui as páginas para os números
#de 1 a 50. (https://en.wikipedia.org/wiki/1, https://en.wikipedia.org/wiki/2, etc)
#Para cada página será necessário fazer uma requisição http para o servidor e aguardar a resposta.
#Porém iremos utilizar threads, para fazer as consultas em paralelo. Este é um exemplo de tarefa
#I/O bound, pois o tempo de I/O é maior que o tempo de processamento (CPU)

if __name__ == '__main__':

    print("Executando com threads:")
     
    #forma mais concisa de fazer a inicialização das urls
    wiki_page_urls = ["https://en.wikipedia.org/wiki/" + str(i) for i in range(50)]

    #o código acima produz o mesmo resultado que o código abaixo.
    #wiki_page_urls = []
    #for i in range(50):
    #   wiki_page_urls.append("https://en.wikipedia.org/wiki/" + str(i))

    #armazenamos o tempo no momento do início da execução das consultas http
    # inicio = time.time()
    
    #criando um gerenciador para executar as threads. Note que é possível indicar 
    #o número máximo de tarefas concorrentes.

    arquivo = open('musicas.txt', 'w')
    cont=14
    while (cont<=15):
        inicio = time.time()
        print(f"Trabalhando com {cont} threads.")
        arquivo.write(str("Trabalhando com {} ".format(cont)+" threads"))
        arquivo.write("=====================================")

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=cont)
        #lista para armazenar as respostas de cada requisição
        respostas = []
        resultado = ""
        for url in wiki_page_urls:
            #para cada url é submetida uma nova tarefa através do método executor.submit. Note
            #que estamos armazenando o resultado de cada tarefa. O retorno do submit é um obejto do
            #tipo Future, que representa um dado que somente estará disponível após um tempo.
            # arquivo.write(str(executor.submit(get_wiki_page_existence,wiki_page_url=url))+"\n")
            respostas.append(executor.submit(get_wiki_page_existence,wiki_page_url=url))

        print("Tarefas submetidas...")

        #indicamos que a submissão de tarefas foi finalizada e iremos aguardar o encerramento de todas
        #as requisições.
        executor.shutdown(wait=True)

        #como a lista de respostas contém objetos do tipo Future, 
        #é necessário verificar se todas foram completadas.
        # for future  in concurrent.futures.as_completed(respostas):
        # #utilizamos o método result para acessar o resultado da execução da tarefa
        # #    arquivo.write(str(future.result()+"\n"))
        #     print(future.result())

        fim = time.time()
        #mostramos o tempo total da execução
        print(f"Tempo de execução em paralelo:{fim - inicio}\n")
        arquivo.write(str(fim-inicio))
        cont+=1
    arquivo.close()
#ref: https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3-pt 