import xlwt


def excel_format(x, y, outputfile):

    workbook = xlwt.Workbook(encoding='ascii') 
    sheet = workbook.add_sheet("Sheet") 
    sheet.write(0, 0, "(Raw-OB)/OB")    
    sheet.write(0, 1, "wavelength (angs)")
    for i in range(len(x)):
        sheet.write(i+1, 0, x[i])        
        sheet.write(i+1, 1, y[i])    
    workbook.save(outputfile)