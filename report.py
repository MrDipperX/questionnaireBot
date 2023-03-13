from db.db import PgConn
import pandas as pd
from pyexcel.cookbook import merge_all_to_a_book
from config.constants import REGIONS_UZ

import glob


def get_report_by_school():
    db_conn = PgConn()
    question_dict = {key: value for key, value in db_conn.get_all_questions()}

    results = pd.DataFrame(db_conn.get_result_by_school())
    if results.empty is True:
        return "Empty"
    results[3] = results[3].head(1)
    results = results.rename(columns={0: "Maktab", 1: "Savol", 2: "O'rtacha baho", 3: "Ishtirokchilar soni"})
    results = results.replace({"Savol": question_dict})

    results.to_csv("files/report_school.csv", index=False)
    merge_all_to_a_book(glob.glob("files/report_school.csv"), "files/report_school.xlsx")


def get_report_by_region():
    db_conn = PgConn()
    question_dict = {key: value for key, value in db_conn.get_all_questions()}

    results = pd.DataFrame(db_conn.get_result_by_region())
    if results.empty is True:
        return "Empty"
    results[3] = results[3].head(1)
    results = results.rename(columns={0: "Viloyat", 1: "Savol", 2: "O'rtacha baho", 3: "Ishtirokchilar soni"})
    results = results.replace({"Savol": question_dict})
    results = results.replace({"Viloyat": REGIONS_UZ})

    results.to_csv("files/report_region.csv", index=False)
    merge_all_to_a_book(glob.glob("files/report_region.csv"), "files/report_region.xlsx")


def get_all_report():
    db_conn = PgConn()
    question_dict = {key: value for key, value in db_conn.get_all_questions()}

    results = pd.DataFrame(db_conn.get_all_results())
    if results.empty is True:
        return "Empty"
    results[2] = results[2].head(1)
    results = results.rename(columns={0: "Savol", 1: "O'rtacha baho", 2: "Ishtirokchilar soni"})
    results = results.replace({"Savol": question_dict})

    results.to_csv("files/report.csv", index=False)
    merge_all_to_a_book(glob.glob("files/report.csv"), "files/report.xlsx")
