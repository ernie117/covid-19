from webapp.etl.covid_19_date_data import Covid19DateDataETL
from webapp.etl.mongo_dao import MongoDAO

top_transformer = Covid19DateDataETL()
top_transformer.execute_etl()

# mongo = MongoDAO("dates")
# data = mongo.get_all_dates_by_country()
# for
