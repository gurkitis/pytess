from ocrParsing import processOcr
from validation import validate
import pandas as pd

pages = ['14lpp', '151lpp', '397lpp', '665lpp', '996lpp']
thresholds = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

error_data = []
extra_work_data = []
for threshold in thresholds:
    _error_data, _extra_work_data = [], []
    for page in pages:
        conf = processOcr(page, include_img=True, threshold=threshold)
        error, extra_work = validate(page)
        _error_data.append(error)
        _extra_work_data.append(extra_work)
        print(threshold, page, 'done')
    error_data.append(_error_data)
    extra_work_data.append(_extra_work_data)

error_df = pd.DataFrame(error_data, columns=pages, index=thresholds)
extra_work_df = pd.DataFrame(extra_work_data, columns=pages, index=thresholds)
writer = pd.ExcelWriter('results.xlsx')
error_df.to_excel(writer, sheet_name='error')
extra_work_df.to_excel(writer, sheet_name='extra_work')
writer.close()

for page in pages:
    error, extra_work = validate(page, target_suffix='Abby.txt')
    print(page, 'error', error, 'extra_work', extra_work)
