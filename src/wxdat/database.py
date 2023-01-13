"""Database connection and models for wxdat."""
import logging

import sqlalchemy as sql
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)


MagicTable = declarative_base()
MagicSession = sessionmaker()


class CurrentConditions(MagicTable):
    """Define data fields for current conditions."""

    __tablename__ = "current_conditions"

    timestamp = sql.Column(sql.DateTime(True), primary_key=True)
    provider = sql.Column(sql.String(256), primary_key=True)
    station_id = sql.Column(sql.String(256), primary_key=True)

    temperature = sql.Column(sql.Float())
    feels_like = sql.Column(sql.Float())
    dew_point = sql.Column(sql.Float())

    wind_speed = sql.Column(sql.Float())
    wind_gusts = sql.Column(sql.Float())
    wind_bearing = sql.Column(sql.Float())

    humidity = sql.Column(sql.Float())

    precip_hour = sql.Column(sql.Float())
    precip_day = sql.Column(sql.Float())
    precip_week = sql.Column(sql.Float())
    precip_month = sql.Column(sql.Float())
    precip_year = sql.Column(sql.Float())

    rel_pressure = sql.Column(sql.Float())
    abs_pressure = sql.Column(sql.Float())

    cloud_cover = sql.Column(sql.Float())
    visibility = sql.Column(sql.Float())
    uv_index = sql.Column(sql.Float())
    ozone = sql.Column(sql.Float())

    solar_lux = sql.Column(sql.Float())
    solar_rad = sql.Column(sql.Float())

    remarks = sql.Column(sql.Text())


class WeatherDatabase:
    def __init__(self, url):
        """Connect to a database specified by the connection URL."""

        logger.debug("Connecting to database: %s", url)
        self.engine = sql.create_engine(url)

        self.migrate()

        # configure the session class to use our engine
        MagicSession.configure(bind=self.engine)

    def migrate(self):
        # TODO create / migrate schema as needed
        MagicTable.metadata.create_all(self.engine)

    def session(self):
        """Starts a new session with the database engine."""
        return MagicSession()

    def save(self, entry: MagicTable):
        with self.session() as session:

            try:
                session.merge(entry)
                session.commit()

            except SQLAlchemyError:
                logger.exception("Error saving entry; rolling back")
                session.rollback()
                return False

        return True
