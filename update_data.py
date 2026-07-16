from pathlib import Path
import json, re
from artifact_tool import Blob, SpreadsheetFile

BASE=Path(__file__).resolve().parent
HTML_PATH=BASE/"index.html"
JSON_PATH=BASE/"data.json"

def find_excel():
    files=sorted(BASE.glob("Report_incassi_quote_pivot_sistemata*.xlsx"),key=lambda p:p.stat().st_mtime,reverse=True)
    if not files:
        raise FileNotFoundError("Nessun file Report_incassi_quote_pivot_sistemata*.xlsx trovato.")
    return files[0]

def read_column(wb,col,last_row,chunk=60):
    out=[]
    for start in range(1,last_row+1,chunk):
        end=min(last_row,start+chunk-1)
        obj=json.loads(wb.inspect({
            "kind":"table",
            "range":f"file_cassa_individuali!{col}{start}:{col}{end}",
            "include":"values",
            "table_max_rows":chunk+5,
            "table_max_cols":1
        }).ndjson)
        vals=obj.get("values",[])
        if len(vals)!=(end-start+1):
            raise RuntimeError(f"Lettura incompleta della colonna {col}, righe {start}-{end}.")
        out.extend([r[0] if r else None for r in vals])
    return out

def main():
    excel=find_excel()
    wb=SpreadsheetFile.import_xlsx(Blob.load(str(excel)))
    sheet_lines=wb.inspect({"kind":"sheet","include":"id,name"}).ndjson.splitlines()
    source_sheet=None
    for line in sheet_lines:
        info=json.loads(line)
        if info.get("name")=="file_cassa_individuali":
            source_sheet=info
            break
    if not source_sheet:
        raise RuntimeError("Foglio file_cassa_individuali non trovato.")
    match=re.search(r":R(\d+)$", source_sheet.get("range",""))
    if not match:
        raise RuntimeError("Impossibile determinare l'ultima riga del foglio sorgente.")
    last_row=int(match.group(1))
    cols={c:read_column(wb,c,last_row) for c in ["B","G","L","N","O","R"]}
    rows=[]
    for i in range(1,last_row):
        camp,company,payment,total,committee,link=(cols[c][i] for c in ["B","G","L","N","O","R"])
        if not camp or not committee or total is None:
            continue
        total=float(total or 0); link=float(link or 0)
        if link<0 or link>total:
            raise ValueError(f"Importo 'da_link' non valido alla riga Excel {i+1}: {link} su totale {total}.")
        rows.append({
            "campionato":str(camp).strip(),
            "societa":str(company) if company is not None else "",
            "comitato":str(committee).strip(),
            "tipoincasso":str(payment).strip() if payment else "Non indicato",
            "importo_totale":total,
            "importo_principale":total-link,
            "importo_link":link
        })
    data={
        "titolo":"Finali dei Campionati Nazionali Sport Individuali",
        "sottotitolo":"Report economico delle quote di partecipazione",
        "anno":2026,
        "fonte":f"{excel.name} · foglio file_cassa_individuali",
        "nota_pagamenti":"L'importo totale deriva dalla colonna N. L'eventuale quota indicata in colonna R è riclassificata come Link da portale e sottratta dalla modalità indicata in colonna L.",
        "dati":rows
    }
    JSON_PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    html=HTML_PATH.read_text(encoding="utf-8")
    embedded=json.dumps(data,ensure_ascii=False).replace("</script>","<\\/script>")
    html,n=re.subn(r'(<script id="embedded-data" type="application/json">).*?(</script>)',lambda m:m.group(1)+embedded+m.group(2),html,count=1,flags=re.S)
    if n!=1:
        raise RuntimeError("Blocco embedded-data non trovato in index.html.")
    HTML_PATH.write_text(html,encoding="utf-8")
    print(f"Aggiornati data.json e index.html: {len(rows)} registrazioni da {excel.name}")

if __name__=="__main__":
    main()
