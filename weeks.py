import csv
from datetime import date, timedelta

def weeks_of_year(year):
    # Find the first Monday of the year
    d = date(year, 1, 1)
    d += timedelta(days=(7 - d.weekday()) % 7)
    d -= timedelta(days=7)  # Start from the week before first Monday of the year
    week_num = 1
    weeks = []
    month = None
    while d.year <= year or (d.year == year + 1 and d.isocalendar()[1] == 1):
        week_start = d
        week_end = d + timedelta(days=6)
        new_month = week_end.month
        weeks.append([(week_num-1) % 52 + 1, week_end.strftime('%B') if month is None or new_month != month else ''])
        month = new_month
        for i in range(7):
            weeks[-1].append((week_start + timedelta(days=i)).day)
        d += timedelta(days=7)
        week_num += 1
        if week_end.year > year and week_start.year > year:
            break
    return weeks

def write_weeks_csv(filename, year):
    weeks = weeks_of_year(year)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Month', 'M', 'T', 'W', 'R', 'F', 'S', 'S'])
        writer.writerows(weeks)

if __name__ == "__main__":
    year = 2025  # Change this to the desired year
    write_weeks_csv('weeks.csv', year)
    print("weeks.csv generated.")