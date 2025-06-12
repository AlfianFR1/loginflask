from app import create_app, db, bcrypt
from app.models.role import Role
from app.models.user import User

app = create_app()

with app.app_context():
    # Cek dan buat role
    admin_role = Role.query.filter_by(name='admin').first()
    user_role = Role.query.filter_by(name='user').first()

    if not admin_role:
        admin_role = Role(name='admin')
        db.session.add(admin_role)
    if not user_role:
        user_role = Role(name='user')
        db.session.add(user_role)

    db.session.commit()

    # Cek dan buat admin user
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(username='admin', password_hash=hashed_pw, role=admin_role)
        db.session.add(admin_user)

    db.session.commit()

    print("Seeder selesai: role dan admin user sudah dibuat.")
