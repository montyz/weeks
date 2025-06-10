import csv
from datetime import date, timedelta
from fpdf import FPDF

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

def write_weeks_pdf(filename, year):
    weeks = weeks_of_year(year)
    pdf = FPDF(orientation='P', unit='in', format='Letter')
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    col_widths = [0.4, 0.8] + [0.2]*7
    headers = ['Week', 'Month', 'M', 'T', 'W', 'R', 'F', 'S', 'S']

    # Table header
    # for i, header in enumerate(headers):
    #     pdf.cell(col_widths[i], 0.3, header, border=1, align='C')
    # pdf.ln(0.3)
    # Title line with the year
    pdf.set_font("Arial", "B", 14)
    pdf.cell(sum(col_widths), 0.4, f"{year}", border=0, align='C')
    pdf.ln(0.3)
    pdf.set_font("Arial", size=10)

    # Table rows
    for row in weeks:
        for i, cell in enumerate(row):
            pdf.cell(col_widths[i], 0.3, str(cell), border=0, align='C')
        pdf.ln(0.175)

    pdf.output(filename)

if __name__ == "__main__":
    year = 2025  # Change this to the desired year
    write_weeks_csv('weeks.csv', year)
    write_weeks_pdf('weeks.pdf', year)
    print("weeks.csv generated.")