import sqlite3
import os

db_name = "spacetraders.db"


def init_db() -> None:
    if os.path.exists(db_name):
        os.remove(db_name)

    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("CREATE TABLE user(callsign, faction, token, active, accountid, headquarters, credits)")
    con.commit()


def inactivate_all_agents():
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("update user set active = 1 where 1=1")
    con.commit()


def insert_agent(callsign, faction, token, account_id, headquarters, credit_amt):
    inactivate_all_agents()
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("insert into user (callsign, faction, token, active, accountid, headquarters, credits) "
                + "values (?, ?, ?, 1, ?, ?, ?)",
                (callsign, faction, token, account_id, headquarters, credit_amt))
    con.commit()


def get_bearer_token() -> str:
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    res = cur.execute("SELECT token from user where active = 1")
    return res.fetchone()[0]
