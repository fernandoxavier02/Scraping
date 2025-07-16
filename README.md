# Web Scraping Personalizável

Uma aplicação web completa que permite configurar e executar web scrapings personalizados de forma intuitiva.

## 🚀 Funcionalidades

- **Configuração Flexível**: Escolha qualquer URL, termo de busca e tipo de dados
- **Múltiplos Tipos de Extração**: Títulos, parágrafos, links, imagens ou seletores CSS customizados
- **Formatos de Saída**: Visualização em tabela/lista ou download em CSV/JSON
- **Interface Responsiva**: Design moderno e amigável para desktop e mobile
- **Filtros de Busca**: Filtre resultados por termos específicos

## 📁 Estrutura do Projeto

```
├── index.html          # Interface web principal
├── style.css           # Estilos e responsividade
├── script.js           # Lógica frontend e requisições
├── app.py              # Backend Flask para scraping
├── requirements.txt    # Dependências Python
└── README.md           # Este arquivo
```

## 🛠️ Instalação e Uso

### Pré-requisitos
- Python 3.7+
- pip

### Instalação
1. Clone ou baixe todos os arquivos do projeto
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python app.py
```

4. Acesse no navegador: `http://localhost:5000`

## 🎯 Como Usar

1. **URL do Site**: Insira a URL completa do site que deseja fazer scraping
2. **Termo de Busca**: (Opcional) Filtre resultados por palavra-chave específica
3. **Tipo de Informação**: Escolha o que extrair:
   - Títulos (h1, h2, h3, etc.)
   - Parágrafos
   - Links
   - Imagens
   - Seletor CSS customizado
4. **Formato de Saída**: Como visualizar os resultados:
   - Tabela (visualização web)
   - Lista (visualização web)
   - Download CSV
   - Download JSON

## 🔧 Exemplos de Uso

### Extrair Títulos
- URL: `https://news.ycombinator.com`
- Tipo: Títulos
- Formato: Tabela

### Buscar Parágrafos sobre IA
- URL: `https://pt.wikipedia.org/wiki/Inteligência_artificial`
- Termo: "inteligência"
- Tipo: Parágrafos
- Formato: Lista

### Seletor CSS Customizado
- URL: `https://example.com`
- Tipo: Customizado
- Seletor: `.article-title, .post-title`
- Formato: CSV

## 🚀 Deploy em Produção

### Heroku
1. Crie um `Procfile`:
```
web: python app.py
```

2. Configure a porta no app.py:
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Docker
1. Crie um `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Servidor VPS
1. Instale dependências
2. Use gunicorn para produção:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## ⚠️ Considerações Importantes

- **Respeite robots.txt**: Sempre verifique se o site permite scraping
- **Rate Limiting**: Evite fazer muitas requisições simultâneas
- **Termos de Uso**: Respeite os termos de serviço dos sites
- **Dados Pessoais**: Não colete informações pessoais sem consentimento

## 🛡️ Limitações

- Alguns sites podem bloquear requisições automatizadas
- Sites com muito JavaScript podem não funcionar perfeitamente
- CAPTCHAs e autenticação não são suportados
- Timeout de 15 segundos por requisição

## 🔧 Personalização

### Adicionar Novos Tipos de Extração
Edite a função `extract_data()` em `app.py`:

```python
elif data_type == 'custom_type':
    for tag in soup.find_all('your_selector'):
        # Sua lógica aqui
        results.append(processed_data)
```

### Modificar Interface
- Edite `style.css` para alterar aparência
- Modifique `script.js` para nova funcionalidade frontend
- Atualize `index.html` para novos campos

## 📝 Licença

Este projeto é de código aberto. Use livremente respeitando as boas práticas de web scraping.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Adicionar novas funcionalidades
- Melhorar documentação