# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from cryptography.fernet import Fernet
from flask_talisman import Talisman
from datetime import datetime

# YENİ: Kullanıcı kimlik doğrulama için importlar
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# --- Yapılandırma ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

KEY_FILE = os.path.join(BASE_DIR, 'secret.key')
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'rb') as f:
        ENCRYPTION_KEY = f.read()
else:
    ENCRYPTION_KEY = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(ENCRYPTION_KEY)
    print(f"UYARI: Yeni bir şifreleme anahtarı oluşturuldu ve '{KEY_FILE}' dosyasına kaydedildi. Bu dosyayı güvenli bir şekilde saklayın ve yedekleyin!")

cipher_suite = Fernet(ENCRYPTION_KEY)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'cok-gizli-bir-anahtar-bunu-kesinlikle-degistir')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'notes.db')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Güvenlik Başlıkları
Talisman(app, content_security_policy=None) # Üretimde CSP yapılandırılmalı

# YENİ: --- Flask-Login Yapılandırması ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Giriş yapılmamışsa yönlendirilecek sayfanın adı (route fonksiyon adı)
login_manager.login_message = "Bu sayfayı görüntüleyebilmek için lütfen giriş yapın."
login_manager.login_message_category = "info" # Flash mesaj kategorisi

# --- Modeller (Veritabanı Tabloları) ---
class User(db.Model, UserMixin): # YENİ: UserMixin eklendi
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # YENİ: Parola hash'i için
    notes = db.relationship('Note', backref='author', lazy=True)

    # YENİ: Parola işlemleri için metotlar
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, default="Başlıksız Not")
    encrypted_content = db.Column(db.LargeBinary, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now()) # Oluşturulma zamanı
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now()) # Güncellenme zamanı
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def content(self):
        try:
            return cipher_suite.decrypt(self.encrypted_content).decode('utf-8')
        except Exception as e:
            print(f"Hata: Not çözülemedi (ID: {self.id}) - {e}")
            return "[İçerik Çözülemedi]"

    @content.setter
    def content(self, text_content):
        self.encrypted_content = cipher_suite.encrypt(text_content.encode('utf-8'))

    def __repr__(self):
        return f'<Note {self.id} - "{self.title}" by User {self.user_id}>'

# YENİ: --- Flask-Login için Kullanıcı Yükleyici Fonksiyonu ---
@login_manager.user_loader
def load_user(user_id):
    """Flask-Login'in kullanıcı oturumunu yönetmek için kullandığı fonksiyon."""
    return User.query.get(int(user_id))

# --- Formlar (Flask-WTF ile) ---
class NoteForm(FlaskForm):
    title = StringField('Başlık:', validators=[DataRequired(message="Başlık boş olamaz!"), Length(min=1, max=200)])
    note_text = TextAreaField('Notunuz:', validators=[DataRequired(message="Not boş olamaz!"), Length(min=1, max=5000)])
    submit = SubmitField('Kaydet')

class DeleteNoteForm(FlaskForm):
    submit = SubmitField('Sil')

# --- Yardımcı Fonksiyonlar ---
# get_or_create_default_user fonksiyonu daha sonra kaldırılacak veya değiştirilecek.
# Şimdilik, uygulama başlangıçta ve rotalarda hata vermemesi için bırakıyoruz.
# Ancak, User modelinde password_hash artık zorunlu olduğu için bu fonksiyonun
# varsayılan kullanıcıyı oluşturma şekli değişmeli veya geçici olarak kaldırılmalı.
# En iyisi, init_db içinden çağrısını ve rotalardaki kullanımını yorum satırına alalım.
def get_or_create_default_user():
    # Bu fonksiyon artık password_hash olmadan kullanıcı oluşturamaz.
    # Gerçek kullanıcı sistemi geldiğinde bu tamamen kaldırılacak.
    # Şimdilik, eğer veritabanında hiç kullanıcı yoksa bir tane oluşturmaya çalışalım
    # ama parola ayarlamadan. Bu, login sistemi gelene kadar bazı hatalara yol açabilir.
    # VEYA: Bu fonksiyonu tamamen yorum satırına alıp, rotalarda current_user kullanmaya başlayana kadar
    # uygulama bazı yerlerde hata verecektir.
    # **Geçici çözüm: Sadece ID döndürsün veya hata versin.**
    # return 1 # Çok kaba bir geçici çözüm, sadece ID döndürür.
    print("UYARI: get_or_create_default_user fonksiyonu kullanımdan kalkacak. Gerçek kullanıcı girişi gerekli.")
    # Eğer bir kullanıcı varsa onu döndür, yoksa None.
    # user = User.query.first()
    # return user.id if user else None
    # En güvenlisi bu fonksiyonun rotalardan çağrısını kaldırana kadar hata vermesini engellemek
    # veya geçici olarak None döndürmesini sağlamak ve rotaları hemen current_user'a göre güncellemek.
    # Şimdilik, test için 1 döndürmeye devam etsin ama bu login ile değişecek.
    user = User.query.get(1)
    if not user:
        print("Varsayılan kullanıcı bulunamadı. Lütfen kayıt sistemiyle bir kullanıcı oluşturun.")
        # Geliştirme aşamasında bir varsayılan kullanıcı oluşturabiliriz (parolalı)
        # VEYA init_db'de oluşturalım.
    return 1 # Bu satır, rotalar güncellenene kadar sorun çıkaracak.

# --- Rotalar (Routes) ---
# Rotalar, bir sonraki adımda current_user ve @login_required ile güncellenecek.
@app.route('/', methods=['GET'])
def index():
    # current_user_id = get_or_create_default_user() # Bu satır değişecek
    # Şimdilik test için bırakalım ama current_user.is_authenticated kontrolü eklenecek
    if current_user.is_authenticated:
        user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
    else:
        user_notes = [] # Giriş yapılmamışsa boş liste
        flash("Notlarınızı görmek için lütfen giriş yapın.", "info") # Ekstra bilgilendirme

    note_form = NoteForm()
    delete_form = DeleteNoteForm()
    # current_user objesi otomatik olarak şablona geçer (Flask-Login sayesinde)
    return render_template('index.html', notes=user_notes, form=note_form, delete_form=delete_form)

@app.route('/add', methods=['POST'])
@login_required # YENİ: Bu rota artık giriş gerektiriyor
def add_note():
    # current_user_id = get_or_create_default_user() # Artık current_user.id kullanılacak
    form = NoteForm()

    if form.validate_on_submit():
        note_title = form.title.data
        note_text = form.note_text.data
        
        new_note = Note(
            user_id=current_user.id, # YENİ: Giriş yapmış kullanıcının ID'si
            title=note_title
        )
        new_note.content = note_text
        
        try:
            db.session.add(new_note)
            db.session.commit()
            flash('Not başarıyla eklendi!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Not eklenirken bir hata oluştu: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                field_label = getattr(form, field).label.text if hasattr(getattr(form, field), 'label') else field
                flash(f"{field_label}: {error}", 'danger')
    return redirect(url_for('index'))

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required # YENİ: Bu rota artık giriş gerektiriyor
def edit_note(note_id):
    # current_user_id = get_or_create_default_user() # Artık current_user.id kullanılacak
    # Sadece kendi notunu düzenleyebilmeli
    note_to_edit = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    
    form = NoteForm(obj=note_to_edit)

    if form.validate_on_submit():
        note_to_edit.title = form.title.data
        note_to_edit.content = form.note_text.data
        note_to_edit.updated_at = datetime.utcnow()
        try:
            db.session.commit()
            flash('Not başarıyla güncellendi!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Not güncellenirken bir hata oluştu: {str(e)}', 'danger')
        return redirect(url_for('index'))

    if request.method == 'GET':
        form.title.data = note_to_edit.title
        form.note_text.data = note_to_edit.content
    
    delete_form = DeleteNoteForm()
    return render_template('edit_note.html', form=form, note_id=note_id, delete_form=delete_form, note=note_to_edit)


@app.route('/delete/<int:note_id>', methods=['POST'])
@login_required # YENİ: Bu rota artık giriş gerektiriyor
def delete_note(note_id):
    # current_user_id = get_or_create_default_user() # Artık current_user.id kullanılacak
    form = DeleteNoteForm() 

    if form.validate_on_submit():
        # Sadece kendi notunu silebilmeli
        note_to_delete = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
        try:
            db.session.delete(note_to_delete)
            db.session.commit()
            flash('Not başarıyla silindi.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Not silinirken bir hata oluştu: {str(e)}', 'danger')
    else:
        flash('Geçersiz istek veya CSRF token hatası.', 'danger')
    return redirect(url_for('index'))

# init_db fonksiyonu, varsayılan kullanıcıyı artık parola olmadan oluşturamayacağı için güncellenmeli
# veya test için geçici olarak bir varsayılan kullanıcı (parolalı) oluşturmalı.
# Şimdilik, get_or_create_default_user çağrısını init_db'den kaldıralım.
# Kullanıcılar kayıt sistemi üzerinden oluşturulacak.
def init_db():
    with app.app_context():
        db.create_all()
        # get_or_create_default_user() # YENİ: Bu satır kaldırıldı veya düzenlendi.
        print("Veritabanı tabloları oluşturuldu/kontrol edildi.")
        # İlk kullanıcıyı manuel olarak eklemek isterseniz (test için):
        if not User.query.first(): # Eğer hiç kullanıcı yoksa
             test_user = User(username='testkullanici')
             test_user.set_password('testparola123')
             db.session.add(test_user)
             db.session.commit()
             print("Test kullanıcısı (testkullanici/testparola123) oluşturuldu.")


if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)