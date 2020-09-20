from ocrReader import OcrReader


def main():
    print("Iniciando...")
    ocr = OcrReader("./teste")
    #print(str(ocr.get_quantity_pdf_exists()))
    #print(str(ocr.get_quantity_img_exists("jpg")))
    #ocr.convert_pdf_to_jpg("./teste", "(LC-223-2013)_LC 223-2013.pdf")
    ocr.convert_all_pdf_to_jpg()
    ocr.generate_ocr_all_img("jpg")
    

if __name__ == '__main__':
    main()