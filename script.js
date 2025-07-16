// Função para escapar HTML e prevenir XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Mostrar campo customizado se necessário
document.getElementById('data-type').addEventListener('change', function() {
    const customDiv = document.getElementById('custom-selector-div');
    if (this.value === 'custom') {
        customDiv.style.display = 'block';
    } else {
        customDiv.style.display = 'none';
    }
});

document.getElementById('scraping-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const url = document.getElementById('url').value;
    const query = document.getElementById('query').value;
    const dataType = document.getElementById('data-type').value;
    const customSelector = document.getElementById('custom-selector').value;
    const outputFormat = document.getElementById('output-format').value;

    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<em>Executando scraping...</em>';

    const payload = {
        url,
        query,
        data_type: dataType,
        custom_selector: customSelector,
        output_format: outputFormat
    };

    try {
        const response = await fetch('/scrape', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        
        // Verificar se a resposta foi bem-sucedida
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`);
        }
        
        if (outputFormat === 'csv' || outputFormat === 'json') {
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = outputFormat === 'csv' ? 'resultados.csv' : 'resultados.json';
            document.body.appendChild(a);
            a.click();
            a.remove();
            resultsDiv.innerHTML = '<b>Download iniciado!</b>';
        } else {
            const data = await response.json();
            
            // Verificar se há erro na resposta
            if (data.error) {
                resultsDiv.innerHTML = '<b>Erro:</b> ' + data.error;
                return;
            }
            
            // Verificar se results existe e é um array
            if (!data.results || !Array.isArray(data.results)) {
                resultsDiv.innerHTML = '<b>Erro:</b> Resposta inválida do servidor';
                return;
            }
            
            // Verificar se há resultados
            if (data.results.length === 0) {
                resultsDiv.innerHTML = '<b>Nenhum resultado encontrado.</b>';
                return;
            }
            
            if (outputFormat === 'table') {
                let html = '<table><thead><tr><th>#</th><th>Resultado</th></tr></thead><tbody>';
                data.results.forEach((item, idx) => {
                    html += `<tr><td>${idx+1}</td><td>${escapeHtml(item)}</td></tr>`;
                });
                html += '</tbody></table>';
                resultsDiv.innerHTML = html;
            } else if (outputFormat === 'list') {
                let html = '<ul>';
                data.results.forEach(item => {
                    html += `<li>${escapeHtml(item)}</li>`;
                });
                html += '</ul>';
                resultsDiv.innerHTML = html;
            } else {
                resultsDiv.innerHTML = '<b>Formato não suportado para visualização.</b>';
            }
        }
    } catch (err) {
        console.error('Erro detalhado:', err);
        resultsDiv.innerHTML = '<b>Erro ao executar scraping:</b> ' + err.message + '<br><small>Verifique se a URL está correta e acessível.</small>';
    }
});