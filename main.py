# main.py
from pdf_processor import process_pdfs_in_folder
from text_processor import apply_domain_adjustments

def main():
    folder_path = r"C:\Users\Priyanshi Tomar\Desktop\pdfs" 
    process_pdfs_in_folder(folder_path)
    apply_domain_adjustments()

if __name__ == "__main__":
    main()
