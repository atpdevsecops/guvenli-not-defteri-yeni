from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Şimdilik notları hafızada tutalım (Güvenli değil, ama başlangıç için!)
notes = []

# HTML Şablonu (XSS açığı içerebilir!)
HTML_TEMPLATE = """
<!doctype html>
<title>Güvenli Not Defteri</title>
<h1>Notlarım</h1>
<form method=post action="/add">
  <input type=text name=note_text size=30>
  <input type=submit value="Not Ekle">
</form>
<h2>Eklenen Notlar:</h2>
<ul>
  {% for note in notes %}
    <li>{{ note | safe }}</li> {# <--- DİKKAT: Burada potansiyel XSS var! #}
  {% endfor %}
</ul>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    note = request.form.get('note_text')
    if note:
        notes.append(note)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) # Debug modunu açık bırakıyoruz (Bu da bir güvenlik riskidir!)