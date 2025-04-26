from app import create_app, db
from app.models import Doctor, APIKey
import secrets

app = create_app()
with app.app_context():
    doctor = Doctor.query.filter_by(email='admin@cema.com').first()
    if not doctor:
        doctor = Doctor(name='Dr. Admin', email='gideon.macharia@student.moringaschool.com',is_admin=True)
        db.session.add(doctor)
        db.session.commit()
        print("Doctor seeded.")

    if not doctor.api_keys:
        key = secrets.token_hex(32)
        api_key = APIKey(key=key, doctor=doctor)
        db.session.add(api_key)
        db.session.commit()
        print("API Key seeded:", key)
    else:
        print("Existing API Key:", doctor.api_keys[0].key)
