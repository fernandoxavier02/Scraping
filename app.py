from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import csv
import io
import json
import os

app = Flask(__name__)
CORS(app)

# 🐛 Debug: Log todas as requisições
@app.before_request
def log_request_info():
    print(f"🔍 DEBUG: Requisição recebida:")
    print(f"   - Método: {request.method}")
    print(f"   - URL: {request.url}")
    print(f"   - Path: {request.path}")
    print(f"   - Headers: {dict(request.headers)}")
    print(f"   - Data: {request.get_data()}")

def extract_data(soup, data_type, custom_selector=None):
    results = []
    if data_type == 'titles':
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = tag.get_text(strip=True)
            if text:
                results.append(text)
    elif data_type == 'paragraphs':
        for tag in soup.find_all('p'):
            text = tag.get_text(strip=True)
            if text:
                results.append(text)
    elif data_type == 'links':
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            text = tag.get_text(strip=True)
            if text:
                results.append(f"{text} ({href})")
            else:
                results.append(href)
    elif data_type == 'images':
        for tag in soup.find_all('img', src=True):
            src = tag['src']
            alt = tag.get('alt', '')
            results.append(f"{alt} ({src})" if alt else src)
    elif data_type == 'custom' and custom_selector:
        for tag in soup.select(custom_selector):
            text = tag.get_text(strip=True)
            if text:
                results.append(text)
    return results

# ✅ ROTA ESPECÍFICA PRIMEIRO
@app.route('/scrape', methods=['POST'])
def scrape():
    print("🎯 DEBUG: Rota /scrape foi alcançada com sucesso!")
    print(f"🎯 DEBUG: Método da requisição: {request.method}")
    
    try:
        data = request.json
        print(f"🎯 DEBUG: Dados JSON recebidos: {data}")
        
        if not data:
            print("❌ DEBUG: Nenhum dado JSON fornecido")
            return jsonify({'error': 'Dados JSON não fornecidos'}), 400
            
        url = data.get('url')
        if not url:
            print("❌ DEBUG: URL não fornecida")
            return jsonify({'error': 'URL é obrigatória'}), 400
            
        query = data.get('query', '')
        data_type = data.get('data_type')
        custom_selector = data.get('custom_selector')
        output_format = data.get('output_format', 'table')
        
        print(f"✅ DEBUG: Configurações processadas:")
        print(f"   - URL: {url}")
        print(f"   - Query: {query}")
        print(f"   - Data Type: {data_type}")
        print(f"   - Output Format: {output_format}")
        
    except Exception as e:
        print(f"❌ DEBUG: Erro ao processar dados: {str(e)}")
        return jsonify({'error': f'Erro ao processar dados: {str(e)}'}), 400

    try:
        print(f"🌐 DEBUG: Iniciando scraping da URL: {url}")
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; SunaBot/1.0)'}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        print(f"✅ DEBUG: Resposta HTTP recebida: {resp.status_code}")
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        print(f"✅ DEBUG: HTML parseado com sucesso")

        results = extract_data(soup, data_type, custom_selector)
        print(f"✅ DEBUG: {len(results)} resultados extraídos")
        
        if query:
            original_count = len(results)
            results = [r for r in results if query.lower() in r.lower()]
            print(f"✅ DEBUG: Filtro aplicado: {original_count} -> {len(results)} resultados")

        if output_format == 'csv':
            print("📁 DEBUG: Gerando arquivo CSV")
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['Resultado'])
            for item in results:
                writer.writerow([item])
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name='resultados.csv'
            )
        elif output_format == 'json':
            print("📁 DEBUG: Gerando arquivo JSON")
            return send_file(
                io.BytesIO(json.dumps({'results': results}, ensure_ascii=False, indent=2).encode('utf-8')),
                mimetype='application/json',
                as_attachment=True,
                download_name='resultados.json'
            )
        else:
            print("📋 DEBUG: Retornando resultados como JSON")
            return jsonify({'results': results})
            
    except requests.exceptions.RequestException as e:
        print(f"❌ DEBUG: Erro de requisição: {str(e)}")
        return jsonify({'error': f'Erro ao acessar URL: {str(e)}'}), 500
    except Exception as e:
        print(f"❌ DEBUG: Erro interno: {str(e)}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

# ✅ ROTAS GENÉRICAS DEPOIS
@app.route('/')
def index():
    print("🏠 DEBUG: Rota / (index) foi alcançada")
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    print(f"📁 DEBUG: Rota genérica /<path> foi alcançada para arquivo: {filename}")
    return send_from_directory('.', filename)

# 🐛 Debug: Log de todas as rotas registradas
@app.before_first_request
def log_routes():
    print("🗺️  DEBUG: Rotas registradas no Flask:")
    for rule in app.url_map.iter_rules():
        print(f"   - {rule.rule} -> {rule.methods} -> {rule.endpoint}")

if __name__ == '__main__':
    print("🚀 DEBUG: Iniciando servidor Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)
