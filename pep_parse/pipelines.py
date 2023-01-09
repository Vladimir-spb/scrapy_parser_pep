import csv
from datetime import datetime as dt
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from pep_parse.model import Pep

BASE_DIR = Path(__file__).parent.parent
DT_FORMAT = "%Y-%m-%d_%H-%M-%S"

status_summary = {}

Base = declarative_base()


class PepParsePipeline:
    def open_spider(self, spider):
        engine = create_engine("sqlite:///pep_lists.db")
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        status_summary[item["status"]] = (
            status_summary.get(item["status"], 0) + 1
        )
        pep = Pep(
            number=item["number"], name=item["name"], status=item["status"]
        )
        self.session.add(pep)
        self.session.commit()
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / "results"
        results_dir.mkdir(exist_ok=True)
        now_time = dt.now().strftime(DT_FORMAT)
        file_name = results_dir / f"status_summary_{now_time}.csv"
        with open(file_name, mode="w", encoding="utf-8", newline='') as file:
            writer = csv.writer(
                file,
                delimiter=";"
            )
            writer.writerows([
                ("Status", "Quantity"),
                *status_summary.items(),
                ('Total', sum(status_summary.values()))
            ])
        self.session.close()
