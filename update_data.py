from pathlib import Path
import json, re
from artifact_tool import Blob, SpreadsheetFile

BASE=Path(__file__).resolve().parent
HTML_PATH=BASE/"index.html"
JSON_PATH=BASE/"data.json"

def find_excel():
    files=sorted(BASE.glob("Report_incassi_quote_pivot_sistemata*.xlsx"),key=lambda p:p.stat().st_mtime,reverse=True)
    if not files: raise FileNotFoundError("File Excel non trovato.")
    return files[0]

def main():
    excel=find_excel()
    wb=SpreadsheetFile.import_xlsx(Blob.load(str(excel)))
    result=wb.inspect({"kind":"table","range":"conti!A1:D5000","include":"values,formulas","table_max_rows":5000,"table_max_cols":4})
    values=json.loads(result.ndjson)["values"]
    rows=[]; current=None
    for row in values[3:]:
        event,committee,companies,amount=(row+[None]*4)[:4]
        event=event.strip() if isinstance(event,str) else event
        committee=committee.strip() if isinstance(committee,str) else committee
        if event:
            if event=="Totale complessivo" or event.endswith(" Totale"): continue
            current=event
        if not current or not committee: continue
        try: rows.append({"campionato":current,"comitato":committee,"numero_societa":int(companies or 0),"importo":float(amount or 0)})
        except (TypeError,ValueError): pass
    data={"titolo":"Finali dei Campionati Nazionali Sport Individuali","sottotitolo":"Report economico delle quote di partecipazione","anno":2026,"fonte":f"{excel.name} · foglio conti","dati":rows}
    JSON_PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    html=HTML_PATH.read_text(encoding="utf-8")
    embedded=json.dumps(data,ensure_ascii=False).replace("</script>","<\\/script>")
    html,n=re.subn(r'(<script id="embedded-data" type="application/json">).*?(</script>)',lambda m:m.group(1)+embedded+m.group(2),html,count=1,flags=re.S)
    if n!=1: raise RuntimeError("Blocco embedded-data non trovato.")
    HTML_PATH.write_text(html,encoding="utf-8")
    print(f"Aggiornati data.json e index.html: {len(rows)} righe da {excel.name}")

if __name__=="__main__": main()
