# Economia delle Finali 2026

Dashboard dedicata alle **Finali dei Campionati Nazionali degli sport individuali**.

## Origine dei dati

Il sito non utilizza più il foglio pivot `conti`. I dati sono letti direttamente dal foglio:

`file_cassa_individuali`

Colonne utilizzate:

- **B**: Campionato nazionale
- **G**: codice società
- **L**: tipologia di incasso
- **N**: importo complessivo
- **O**: Comitato
- **R**: quota pagata successivamente tramite Link da portale

La quota della colonna R viene sottratta dalla modalità indicata in L e classificata separatamente come **Link da portale**.

## File del progetto

- `index.html`: dashboard completa, con dati incorporati.
- `data.json`: dati elaborati.
- `update_data.py`: rigenera `data.json` e aggiorna i dati incorporati nell'HTML.
- `logo_csi.jpg`: logo dell'intestazione.
- `Report_incassi_quote_pivot_sistemata.xlsx`: file Excel sorgente.

## Aggiornamento

1. Sostituire il file Excel nella cartella.
2. Eseguire:

```bash
python update_data.py
```

3. Caricare su GitHub almeno:
   - `index.html`
   - `data.json`

Il selettore standard “Mostra 25 elementi” è stato rimosso per evitare il difetto grafico e rendere l'interfaccia più pulita.
