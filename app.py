from pathlib import Path
import shutil as sh
import json, os, sys, logging 

PathFolder = Path()
config_arc_name = "config.json"
CONFIGS = {}
not_has_category = []


#Função principal
def __main__():
    global PathFolder

    logging.basicConfig(#Configurações do log
        format='%(asctime)s - %(levelname)s: "%(message)s"', 
        level=logging.DEBUG, 
        filename="register.log", 
        encoding='utf-8'
    )
    logging.info("---Programa iniciado!---")

    try:
        #lê o config.json e carrega as configuração na fariavel CONFIG
        with open(get_source_path(config_arc_name), 'r') as arc:
            CONFIGS = json.load(arc)
    except FileNotFoundError:
        #Finaliza o programa se não encontrar o config.json
        logging.critical(f"O arquivo *{config_arc_name} não foi encontrado!!")
        return


    while True:
        path_input = input("Caminho: ")#recebe o caminho
        path_input = path_input.replace("\\", "/")#corrige o caminho

        if Path(path_input).is_dir():#se o caminho for de uma pasta segue
            logging.info(f'Caminho da pasta - "{path_input}"')
            PathFolder = Path(path_input)
            break
        else:
            logging.error(f'Caminho invalido - "{path_input}"')
            print(f'Caminho invalido - "{path_input}"')


    for arc in PathFolder.iterdir():#percorre todos os items dentro da pasta

        extension = arc.suffix.lower()#Extenção do arquivo
        category = get_category(extension, CONFIGS)#Categoria de acordo com as configs

        if category:#se tiver categoria move o arquivo
            mov_arc(arc, category)
        elif not arc.is_dir():# Se NÃO for uma pasta ele vai informar
            not_has_category.append(arc.name)#se não tem uma categoria entra na lista dos mesmos

    logging.warning(f'Os seguintes arquivos não estão em nenhuma categoria: {not_has_category}')#faz o log dos arquivos sem categoria


def sort_folder():
    pass

#Recoonhecer o caminho do arquivo config
def get_source_path(relative_path):
    if hasattr(sys, "_MEIPASS"):#Se é um execultavel do pyinstaller
        return os.path.join(sys._MEIPASS, relative_path)#retorna o caminho ate a pasta temporaria

    return os.path.join(os.path.abspath("."), relative_path)#se não retorna o caminho onde o arquivo esta sendo execultado


#Busca a categoria do arquivo
def get_category(extension, configs):
    for category, extensions in configs.items():#Verifica se a extenção faz parte de alguma categoria

        if extension in extensions:#Se fizer parte de alguma categoria ele retorna o nome =
            return category

    return None


#move arquivo para pasta
def mov_arc(arc, category):
    
    categoryf_path : Path = PathFolder / category.upper()#caminho até a pasta

    if not categoryf_path.exists():#se não tiver a pasta referente a categoria, sera criada"
        categoryf_path.mkdir()
        logging.info(f"Pasta {categoryf_path} foi criada!")

    if categoryf_path.is_dir():#se realmente for uma pasta ele vai mover o arquivo para a pasta
        sh.move(
            arc,
            categoryf_path
        )
        logging.info(f'{arc.name} foi movido para "{categoryf_path}"!')

__main__()
print("---Programa finalizado!---")
logging.info("---Programa finalizado!---")