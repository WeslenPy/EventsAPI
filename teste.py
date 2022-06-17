from datetime import datetime

datetime.strptime('2020-03-03', "%Y-%m-%d").date()

print(datetime.strptime('2020,3,3', "%Y,%m,%d").date())