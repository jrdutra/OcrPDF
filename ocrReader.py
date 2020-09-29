import os
from fnmatch import fnmatch
import os.path
import pytesseract as ocr
from PIL import Image
from jsonFile import JsonFile
from mysqlConnector import MysqlConnector
from pdf2image import convert_from_path


class OcrReader:

    def __init__(self, _root, _host, _user, _pass, _dataBase):
        self.root = _root
        self.qt_arq = 0
        self.qt_lida = 0
        self.porcento = 0
        self.current_data = JsonFile("current_data")
        self.mysqlConnector = MysqlConnector(_host, _user, _pass, _dataBase)

    #------------------------------------------------------------
    #  CONTADORES, tanto de imagens, quanto de PDFs
    #------------------------------------------------------------
    def get_quantity_img_to_gen(self, img_extension):
        self.qt_arq = 0
        for path, subdirs, files in os.walk(self.root):
            subdirs
            for name in files:
                # se nome do arquivo do subdir tiver a extensao
                if fnmatch(name, '*.' + img_extension):
                    current_dir = os.path.join(path, name)
                    # se nao existir o .txt com texto, cria
                    if os.path.isfile(current_dir + ".txt") == 0:
                        self.qt_arq += 1
        return self.qt_arq
    
    def get_quantity_pdf_to_gen(self):
        self.qt_arq = 0
        for path, subdirs, files in os.walk(self.root):
            subdirs
            for name in files:
                # se nome do arquivo do subdir tiver a extensao
                if fnmatch(name, '*.pdf') or fnmatch(name, '*.PDF'):
                    current_dir = os.path.join(path, name)
                    # se nao existir o diretorio com as imagens, conta como passivel de conversao
                    if os.path.exists(current_dir[0:-4]) == 0:
                        self.qt_arq += 1     
        return self.qt_arq

    def get_quantity_pdf_exists(self):
        self.qt_arq = 0
        for path, subdirs, files in os.walk(self.root):
            subdirs
            path
            for name in files:
                # se nome do arquivo do subdir tiver a extensao
                if fnmatch(name, '*.pdf') or fnmatch(name, '*.PDF'):
                    self.qt_arq += 1        
        return self.qt_arq
    
    def get_quantity_img_exists(self, img_extension):
        self.qt_arq = 0
        for path, subdirs, files in os.walk(self.root):
            subdirs
            path
            for name in files:
                # se nome do arquivo do subdir tiver a extensao
                if fnmatch(name, '*.' + img_extension):
                    self.qt_arq += 1        
        return self.qt_arq

    #------------------------------------------------------------
    #               Conversor de pdf para jpg
    #------------------------------------------------------------

    def convert_pdf_to_jpg(self, filePath, fileName):
        try:
            #Lê arquivo pdf do diretorio passado
            pages = convert_from_path(filePath + "/" + fileName, 500)
            #corre todas as páginas do arquivo convetendo
            for index, page in enumerate(pages, start=0):
                #cria o nome do novo diretorio onde serão salvas as imagens, sem espaço
                pagesDirectory = fileName[0:-4].replace(" ", "_").replace(".PDF", ".pdf")
                #renomeia o arquivo pdf original substituindo os espaços
                os.rename(filePath + "/" + fileName, filePath + "/" + fileName.replace(" ", "_"))
                #substitui os espaços da variável fileName
                fileName = fileName.replace(" ", "_")
                #Se o subdiretorio para salvar não existe, cria, se já existe, ignora
                if os.path.exists(filePath + "/" + pagesDirectory) == 0:
                    os.mkdir(filePath + "/" + pagesDirectory)
                    #print("Dir created: " + filePath + "/" + pagesDirectory)
                #Testa se o arquivo não existe
                imgPageName = filePath + "/" + pagesDirectory + "/" +str(index) + '.jpg'
                if os.path.isfile(imgPageName) == 0:
                    print("pág. " + str(index))
                    page.save(imgPageName, 'JPEG')
        except:
            print("Arquivo não encontrado: " + filePath + "/" + fileName)

    #------------------------------------------------------------
    #  GERADOR DE OCR - Recebe o diretório da imagem e gera
    #------------------------------------------------------------
    def generate_ocr(self, current_dir):
        texto = ocr.image_to_string(Image.open(current_dir), lang='por')
        arq = open(current_dir + ".txt", "w")
        texto = texto.strip()
        #Record in a text file
        arq.write(texto)
        arq.close()
        #record in the database
        self.mysqlConnector.record(current_dir, texto)

    #------------------------------------------------------------
    #  EXECUTORES DE DIRETORIOS COMPLETOS
    #------------------------------------------------------------
    def generate_ocr_all_img(self, img_extension):
        self.qt_lida = 0
        if self.qt_arq == 0:
            self.qt_arq = self.get_quantity_img_to_gen(img_extension)
        for path, subdirs, files in os.walk(self.root):
            subdirs
            for name in files:
                # se nome do arquivo do subdir tiver a extensao
                if fnmatch(name, '*.' + img_extension):
                    current_dir = os.path.join(path, name)
                    # se nao existir o .txt com texto, cria
                    if os.path.isfile(current_dir + ".txt") == 0:
                        self.qt_lida += 1
                        print("Converting " + img_extension + " to txt[" + str(self.qt_lida) +
                              " from " + str(self.qt_arq) + "] | DIR: " + current_dir)
                        self.generate_ocr(current_dir)
                        self.current_data.json_img_txt_details_conversion(
                            self.qt_arq, self.qt_lida, current_dir)
        self.qt_arq = 0

    def convert_all_pdf_to_jpg(self):
        self.qt_lida = 0
        if self.qt_arq == 0:
            self.qt_arq = self.get_quantity_pdf_to_gen()
        for path, subdirs, files in os.walk(self.root):
            subdirs
            for name in files:
                # se nome do arquivo do subdir tiver a extensao
                if fnmatch(name, '*.pdf') or fnmatch(name, '*.PDF'):
                    current_dir = os.path.join(path, name)
                    # se nao existir o .txt com texto, cria
                    if os.path.exists(current_dir[0:-4]) == 0:
                        self.qt_lida += 1
                        print("Converting pdf to jpg [" + str(self.qt_lida) +
                              " from " + str(self.qt_arq) + "] | DIR: " + current_dir)
                        self.convert_pdf_to_jpg(path, name)
                        self.current_data.json_img_txt_details_conversion(
                            self.qt_arq, self.qt_lida, current_dir)
        self.qt_arq = 0
