from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import hashlib, os
from pathlib import Path

######### Config #########
project_root = Path(__file__).resolve().parent.parent
DB_PATH = project_root / 'database/processed/sql/authentication_data.db'

Base = declarative_base()
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Session = sessionmaker(bind=engine)

######### TABLES #########
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)

    password = relationship("UserPassword", uselist=False, back_populates="user", cascade="all, delete")

class UserPassword(Base):
    __tablename__ = 'user_passwords'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    password_hash = Column(String, nullable=False)

    user = relationship("User", back_populates="password")



######### Utilities #########
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authentication_db():
    if not DB_PATH.exists():
        os.makedirs(DB_PATH.parent, exist_ok=True)
    Base.metadata.create_all(engine)

def create_user(username, full_name, email, password, role="user"):
    session = Session()

    hashed_pw = hash_password(password)
    user = User(username=username, full_name=full_name, email=email, role=role)
    session.add(user)
    session.commit()

    pw = UserPassword(user_id=user.id, password_hash=hashed_pw)
    session.add(pw)
    session.commit()
    session.close()
    print(f"User '{username}' created with role '{role}'.")


def login_user(identifier: str, password: str):
    """
    Attempt to login using either email or username.
    
    :param identifier: Email or username
    :param password: Plain-text password
    :return: User object if authenticated, None otherwise
    """
    session = Session()
    hashed_pw = hash_password(password)

    # Try to find user by username or email
    user = session.query(User).filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()

    if user and user.password and user.password.password_hash == hashed_pw:
        # print(f"Login successful for user: {user.username}")
        session.close()
        return user
    else:
        # print("Login failed: Invalid credentials.")
        session.close()
        return None

# Run for testing
if __name__ == "__main__":
    authentication_db()
    
    # Try logging in
    login_user("jdoe", "test123")          # Login with username
    login_user("jdoe@example.com", "test123")  # Login with email
    login_user("jdoe", "wrongpassword")    # Should fail
