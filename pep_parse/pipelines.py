from datetime import datetime as dt
from pathlib import Path

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

BASE_DIR = Path(__file__).parent.parent
DT_FORMAT = "%Y-%m-%d_%H-%M-%S"

status_summary = {}

Base = declarative_base()


class Pep(Base):
    __tablename__ = "pep"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    name = Column(String(250))
    status = Column(String(50))


class PepParsePipeline:
    def open_spider(self, spider):
        engine = create_engine("sqlite:///pep_lists.db")
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        if item["status"] not in status_summary:
            status_summary[item["status"]] = 1
        else:
            status_summary[item["status"]] += 1
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
        total = 0
        with open(file_name, mode="w", encoding="utf-8") as file:
            file.write("Status,Quantity\n")
            for key, value in status_summary.items():
                file.write(f"{key},{value}\n")
                total += value
            file.write(f"Total,{total}")
        self.session.close()
