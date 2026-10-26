from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Новый правильный синтаксис для свежих версий FastAPI
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/check", response_class=HTMLResponse)
def check_meds(request: Request, medications: str = Form(...)):
    med_names = [m.strip() for m in medications.split(",") if m.strip()]
    
    conn = sqlite3.connect("polypharmacy.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    found_meds = []
    unknown_meds = []
    
    for name in med_names:
        cursor.execute("SELECT id, name FROM active_ingredients WHERE name_lower = ?", (name.lower(),))
        row = cursor.fetchone()
        if row:
            if row["id"] not in [m["id"] for m in found_meds]:
                found_meds.append(row)
        else:
            unknown_meds.append(name)

    beers_alerts = []
    for m in found_meds:
        cursor.execute("SELECT category, rationale, recommendation FROM beers_criteria WHERE ingredient_id = ?", (m["id"],))
        for rule in cursor.fetchall():
            beers_alerts.append({"med": m["name"], "cat": rule["category"], "why": rule["rationale"], "rec": rule["recommendation"]})

    interaction_alerts = []
    for i in range(len(found_meds)):
        for j in range(i + 1, len(found_meds)):
            id1, name1 = found_meds[i]["id"], found_meds[i]["name"]
            id2, name2 = found_meds[j]["id"], found_meds[j]["name"]
            cursor.execute("""
                SELECT severity, description FROM drug_interactions 
                WHERE (ingredient_id_1 = ? AND ingredient_id_2 = ?) OR (ingredient_id_1 = ? AND ingredient_id_2 = ?)
            """, (id1, id2, id2, id1))
            for rule in cursor.fetchall():
                interaction_alerts.append({"med1": name1, "med2": name2, "sev": rule["severity"], "desc": rule["description"]})

    conn.close()

    # Новый правильный синтаксис для передачи данных в HTML
    return templates.TemplateResponse(
        request=request, 
        name="result.html", 
        context={
            "found": found_meds, 
            "unknown": unknown_meds,
            "beers": beers_alerts, 
            "interactions": interaction_alerts
        }
    )