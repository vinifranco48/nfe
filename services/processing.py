import xml.etree.ElementTree as ET
from datetime import datetime
import logging

def process_nfe_xml(xml_content: str) -> dict:
    try:
        root = ET.fromstring(xml_content)
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        nfe_data = {
            'numero_nota': root.find('.//nfe:nNF', ns).text,
            'chave_acesso': root.find('.//nfe:chNFe', ns).text,
            'data_emissao': datetime.strptime(root.find('.//nfe:dhEmi', ns).text.split('T')[0], '%Y-%m-%d').strftime('%d/%m/%Y'),
            'fornecedor': root.find('.//nfe:emit/nfe:xNome', ns).text,
            'cnpj_fornecedor': root.find('.//nfe:emit/nfe:CNPJ', ns).text,
            'valor_total': float(root.find('.//nfe:vNF', ns).text),
            'itens': []
        }
        for det in root.findall('.//nfe:det', ns):
            quantidade = float(det.find('.//nfe:qCom', ns).text)
            valor_unitario = float(det.find('.//nfe:vUnCom', ns).text)
            valor_total_sem_desconto = quantidade * valor_unitario
            desconto_element = det.find('.//nfe:vDesc', ns)
            desconto = float(desconto_element.text) if desconto_element is not None else 0
            valor_total_com_desconto = valor_total_sem_desconto - desconto
            item = {
                'numero': det.get('nItem'),
                'descricao': det.find('.//nfe:xProd', ns).text,
                'quantidade': quantidade,
                'unidade': det.find('.//nfe:uCom', ns).text,
                'valor_unitario': valor_unitario,
                'valor_total_sem_desconto': valor_total_sem_desconto,
                'desconto': desconto,
                'valor_total_com_desconto': valor_total_com_desconto,
                'ncm': det.find('.//nfe:NCM', ns).text
            }
            nfe_data['itens'].append(item)
        logging.info("XML da nota fiscal processado com sucesso.")
        return nfe_data
    except Exception as e:
        logging.error(f"Erro ao processar XML da nota fiscal: {e}")
        raise
