from PIL import Image
import pytesseract
import cv2
from dominate.tags import *
import os


# bgr
def calcColor(conf):
    conf -= 50
    diff = abs(conf) * 255 / 50
    if conf > 0:
        return 0, 255, 255 - diff
    else:
        return 0, 255 - diff, 255

def processOcr(name, lang='lav', threshold=75, color_words=False, include_img=True, create_color_map=False,
               tesseract_config='--psm 6'):
    img_path = './' + name + '/' + name + '_cropMan.jpeg'
    image = cv2.imread(img_path)

    # OCR processing
    text_data = pytesseract.image_to_data(Image.open(img_path), lang=lang, output_type='data.frame',
                                          config=tesseract_config)
    text_data.to_csv('data.csv')
    text_data = text_data[text_data['text'].notnull()]

    html = ''
    avg_conf = 0
    processed_text = ''

    # Output processing
    row_index = (1, 1)
    for index, row in text_data.iterrows():
        color = calcColor(row['conf'])

        # New line check
        if not row_index == (row['par_num'], row['line_num']):
            row_index = (row['par_num'], row['line_num'])
            html += br().render()
            processed_text += '\n'
        else:
            processed_text += ' '
            html += span(' ').render()

        if row['conf'] < threshold and include_img:
            # Replace by image
            # Insert img tag in html
            crop_image = image[(row['top']):(row['top'] + row['height']), (row['left']):(row['left'] + row['width'])]
            img_name = './' + name + '/img/img' + str(index) + '.png'
            src = os.getcwd() + '/' + img_name
            cv2.imwrite(img_name, crop_image)
            if crop_image.shape[0] > 14:
                html += img(src=src, style='height: 14px;').render()
            else:
                html += img(src=src, style='width: 14px; padding-bottom: ' + str(
                    (14 - crop_image.shape[0] / 2) / 2) + 'px;').render()

            # Insert img tag in output text
            processed_text += '<img' + row['text'] + '/>'
        else:
            # Include text in html
            text = span(row['text'])
            if color_words:
                text['style'] = 'color: rgb(' + str(color[2]) + ',' + str(color[1]) + ',' + str(color[0]) + ');'
            html += text.render()

            # Insert text in output text
            processed_text += row['text']

        if create_color_map:
            image = cv2.rectangle(image, (row['left'], row['top']),
                                  (row['left'] + row['width'], row['top'] + row['height']), color, 2)
        avg_conf += row['conf']

    with open(name + '/' + name + 'Output.txt', 'w') as f:
        processed_text = processed_text[1:]
        processed_text += '\n'
        f.write(processed_text)

    with open(name + '/' + name + '.html', 'w') as f:
        f.write(html)

    avg_conf /= len(text_data.index)

    if create_color_map:
        cv2.imwrite(name + 'ColorMap' + '.jpeg', image)

    return avg_conf
