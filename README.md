# Report economico Campionati Nazionali sport individuali

La dashboard riguarda esclusivamente le Finali dei Campionati Nazionali degli sport individuali.

## File
- `index.html`: sito completo.
- `data.json`: dati del foglio `conti`.
- `update_data.py`: aggiorna `data.json` e i dati incorporati in `index.html`.
- `logo_csi.jpg`: logo dell'intestazione.
- `Report_incassi_quote_pivot_sistemata.xlsx`: sorgente Excel.

## Aggiornamento
1. Sostituire il file Excel nella cartella.
2. Verificare che esista il foglio `conti`.
3. Eseguire `python update_data.py`.

Lo script usa automaticamente il file più recente che inizia con `Report_incassi_quote_pivot_sistemata`.
I dati sono incorporati anche nell'HTML, quindi il sito funziona aprendolo direttamente senza server locale.
