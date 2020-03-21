from webapp.etl.covid_19_date_data import Covid19DateDataETL

top_transformer = Covid19DateDataETL()
top_transformer.execute_etl()