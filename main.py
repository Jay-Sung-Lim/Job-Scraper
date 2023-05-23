from flask import Flask, render_template, request, redirect, send_file
from extractors.wwr import extract_wwr_jobs
from extractors.remoteok import extract_remoteok_jobs
from file import save_to_file

app = Flask("JobScrapper")

@app.route("/")
def home():
  return render_template("home.html", name="Jaesung")


db_wwr = {}
db_remoteok = {}

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword in db_wwr or db_remoteok:
    wwr = db_wwr[keyword]
    remoteok = db_remoteok[keyword]
  else:
    wwr = extract_wwr_jobs(keyword)
    remoteok = extract_remoteok_jobs(keyword)
    db_wwr[keyword] = wwr
    db_remoteok[keyword] = remoteok
  return render_template("search.html", keyword=keyword, wwr=wwr, remoteok=remoteok)

@app.route("/export-wwr")
def export_wwr():
  platform = "wwr"
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword not in db_wwr:
    return redirect(f"/search?keyword={keyword}")    
  save_to_file(platform, keyword, db_wwr[keyword])
  return send_file(f"{platform}_{keyword}.csv", as_attachment=True)
  
@app.route("/export-remoteok")
def export_remoteok():
  platform = "remoteok"
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword not in db_remoteok:
    return redirect(f"/search?keyword={keyword}")    
  save_to_file(platform, keyword, db_remoteok[keyword])
  return send_file(f"{platform}_{keyword}.csv", as_attachment=True)


app.run("0.0.0.0")