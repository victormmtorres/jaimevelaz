from models import disburment
import date.datetime

today = datetime.now()
disburment.calculate_disburment(today)
