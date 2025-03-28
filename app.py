import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from models.invoice import InvoiceData
from services.scraping import download_xml, setup_driver
from services.processing import process_nfe_xml
from services.storage import upload_json_to_minio, BUCKET_NAME

app = FastAPI(title="API de Processamento de Notas Fiscais")

@app.post("/process_invoice")
def process_invoice_endpoint(invoice: InvoiceData, background_tasks: BackgroundTasks):
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    driver = setup_driver(download_dir)
    try:
        xml_file = download_xml(driver, "https://meudanfe.com.br/", invoice.chave_acesso, download_dir)
    except Exception as e:
        driver.quit()
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        nfe_data = process_nfe_xml(xml_content)
    except Exception as e:
        driver.quit()
        raise HTTPException(status_code=500, detail="Erro ao processar o XML da nota fiscal.")
    
    background_tasks.add_task(upload_json_to_minio, nfe_data, BUCKET_NAME, f"{invoice.chave_acesso}.json")
    
    driver.quit()
    return {
        "message": "Nota fiscal processada com sucesso e arquivo JSON enviado ao MinIO.",
        "nfe_data": nfe_data,
        "categoria": invoice.categoria
    }
