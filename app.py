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

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dados JSON não fornecidos'}), 400
            
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL é obrigatória'}), 400
            
        query = data.get('query', '')
        data_type = data.get('data_type')
        custom_selector = data.get('custom_selector')
        output_format = data.get('output_format', 'table')
        
        print(f"Processando scraping para: {url}")
        
    except Exception as e:
        return jsonify({'error': f'Erro ao processar dados: {str(e)}'}), 400

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; SunaBot/1.0)'}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        results = extract_data(soup, data_type, custom_selector)
        if query:
            results = [r for r in results if query.lower() in r.lower()]

        if output_format == 'csv':
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
            return send_file(
                io.BytesIO(json.dumps({'results': results}, ensure_ascii=False, indent=2).encode('utf-8')),
                mimetype='application/json',
                as_attachment=True,
                download_name='resultados.json'
            )
        else:
            return jsonify({'results': results})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro ao acessar URL: {str(e)}'}), 500
    except Exception as e:
        print(f"Erro interno: {str(e)}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)