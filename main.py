from ocrReader import OcrReader
from datetime import datetime

def main():
    print("Iniciando...")
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
    print(data_e_hora_em_texto)

    ocr = OcrReader("./teste", "127.0.0.1","jrdutra", "1234", "ocrpmm")
    ocr.convert_all_pdf_to_jpg()
    ocr.generate_ocr_all_img("jpg")

    print("Finalizando...")
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
    print(data_e_hora_em_texto)
    

if __name__ == '__main__':
    main()