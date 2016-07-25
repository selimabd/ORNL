import xlrd
import os


"""Method to read input dataset (Wavelength (angs) values and (Raw - OB)/OB values) into X_Coordinates and Y_Coordinates"""
def read_Input(x_coordinates, y_coordinates):

    wb = xlrd.open_workbook(os.path.join(r'Si_plot.xlsx'))
    wb.sheet_names()
    sh = wb.sheet_by_index(0)
    for i in range(1,1486):
        if sh.cell(i,6).value>=1.4 and sh.cell(i,6).value<=4.4:   #Considering Wavelength values that are in [1.4, 4.4] 
            x_coordinates.append(sh.cell(i,6).value)
            y_coordinates.append(sh.cell(i,3).value)

    return {'x':x_coordinates, 'y':y_coordinates}