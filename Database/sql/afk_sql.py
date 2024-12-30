import threading
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, DateTime, UnicodeText
from sqlalchemy.exc import SQLAlchemyError
from Database.sql import BASE, SESSION  # Import BASE and SESSION from Database.sql
import logging

# Setup logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Thread lock for thread-safe operations
INSERTION_LOCK = threading.RLock()

# Dictionary to cache AFK user data
AFK_USERS = {}


class AFK(BASE):
    __tablename__ = "afk_user"

    user_id = Column(BigInteger, primary_key=True)
    is_afk = Column(Boolean, default=True)
    reason = Column(UnicodeText, nullable=True)
    time = Column(DateTime, default=datetime.now)

    def __init__(self, user_id: int, reason: str = "", is_afk: bool = True):
        self.user_id = user_id
        self.reason = reason
        self.is_afk = is_afk
        self.time = datetime.now()

    def __repr__(self):
        return f"AFK status for {self.user_id}"


# Ensure the table is created if it doesn't exist
AFK.__table__.create(checkfirst=True, bind=SESSION.bind)


def is_afk(user_id: int) -> bool:
    """Check if a user is AFK."""
    return user_id in AFK_USERS


def check_afk_status(user_id: int):
    """Retrieve the AFK status of a user from the database."""
    try:
        return SESSION.query(AFK).get(user_id)
    except SQLAlchemyError as e:
        logger.error(f"Error checking AFK status for {user_id}: {e}")
    finally:
        SESSION.close()


def set_afk(user_id: int, reason: str = ""):
    """Set a user as AFK with an optional reason."""
    with INSERTION_LOCK:
        try:
            curr = SESSION.query(AFK).get(user_id)
            if not curr:
                curr = AFK(user_id, reason, True)
            else:
                curr.is_afk = True
                curr.reason = reason

            AFK_USERS[user_id] = {"reason": reason, "time": curr.time}

            SESSION.add(curr)
            SESSION.commit()
        except SQLAlchemyError as e:
            SESSION.rollback()
            logger.error(f"Error setting AFK for {user_id}: {e}")
        finally:
            SESSION.close()


def rm_afk(user_id: int) -> bool:
    """Remove a user's AFK status."""
    with INSERTION_LOCK:
        try:
            curr = SESSION.query(AFK).get(user_id)
            if curr:
                if user_id in AFK_USERS:  # Sanity check
                    del AFK_USERS[user_id]

                SESSION.delete(curr)
                SESSION.commit()
                return True
        except SQLAlchemyError as e:
            SESSION.rollback()
            logger.error(f"Error removing AFK for {user_id}: {e}")
        finally:
            SESSION.close()
        return False


def toggle_afk(user_id: int, reason: str = ""):
    """Toggle a user's AFK status."""
    with INSERTION_LOCK:
        try:
            curr = SESSION.query(AFK).get(user_id)
            if not curr:
                curr = AFK(user_id, reason, True)
            elif curr.is_afk:
                curr.is_afk = False
            else:
                curr.is_afk = True
                curr.reason = reason

            AFK_USERS[user_id] = {"reason": reason, "time": curr.time}
            SESSION.add(curr)
            SESSION.commit()
        except SQLAlchemyError as e:
            SESSION.rollback()
            logger.error(f"Error toggling AFK for {user_id}: {e}")
        finally:
            SESSION.close()


def __load_afk_users():
    """Load all AFK users into the cache."""
    global AFK_USERS
    try:
        all_afk = SESSION.query(AFK).all()
        AFK_USERS = {
            user.user_id: {"reason": user.reason, "time": user.time}
            for user in all_afk
            if user.is_afk
        }
    except SQLAlchemyError as e:
        logger.error(f"Error loading AFK users: {e}")
    finally:
        SESSION.close()


def refresh_afk_cache():
    """Refresh the AFK cache."""
    __load_afk_users()


# Load AFK users on startup
__load_afk_users()
            
