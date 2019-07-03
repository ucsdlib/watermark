from PyPDF2 import PdfFileWriter, PdfFileReader
import sys
import getopt


def get_scale(in_page, wm_height, wm_width):
        # Set proper scale
        page_width = in_page.mediaBox[2]
        page_height = in_page.mediaBox[3]
        width_scale = page_width/wm_width
        height_scale = page_height/wm_width
        # height_scale = page_height/wm_height
        return width_scale, height_scale, page_height, page_width


def create_watermark(input_pdf, output, watermark):
    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)

    # Get the width and height of the watermark page
    wm_width = watermark_page.mediaBox[2]
    wm_height = watermark_page.mediaBox[3]

    # Read in the input file
    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)

        w_scale, h_scale, page_h, page_w = get_scale(page, wm_height=wm_height, wm_width=wm_width)

        # Is page portrait or landscape
        if page_w >= page_h:
            # x_translation to center in landscape
            if (float(page_w)/2) - (wm_width/2) > 0:
                x_tranlation = (float(page_w)/2) - (wm_width/2)
            else:
                x_tranlation = 0
            page.mergeScaledTranslatedPage(watermark_page, min(w_scale, 1), x_tranlation, 0)
        else:
            # y_translation to center in portrait
            if (float(page_h)/2) - (wm_width/2) > 0:
                y_tranlation = (float(page_h)/2) - (wm_width/2)
            else:
                y_tranlation = 0
            page.mergeRotatedScaledTranslatedPage(watermark_page, -90, min(h_scale, 1), 0, float(page_h)-float(y_tranlation))

        # Add page to pdf writer
        pdf_writer.addPage(page)

    with open(output, 'wb') as out:
        pdf_writer.write(out)


def get_args(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('pdf_watermarker.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pdf_watermarker.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    return inputfile, outputfile

if __name__ == '__main__':
    in_file, out_file = get_args(sys.argv[1:])
    create_watermark(
        input_pdf=in_file,
        output=out_file,
        watermark='VRR_SCA_watermark.pdf'
        )
