"""Method to smooth the curve where beta_list elements exceed the threshold limit""" 
def smoothing_Plot(total_Span, threshold, x_coordinates, y_coordinates, beta_list):
    x_smooth1   = []            #List to hold all the beta_listelements greater than threshold
    x_smooth2   = []            #List to hold all the adjoining elements that fall into the window length of each element in X_Smooth1, including them
    temp_listY  = []            #List to hold all the elements of Y_Coordinates that fall into window length of each element in X_Smooth2
    smooth_y_coordinates = []   #Smoothed Values of each element in X_Smooth2
    
    for i in beta_list:
        if i > threshold:
            x_smooth1.append(x_coordinates[beta_list.index(i)])

    for i in x_smooth1:
        for j in x_coordinates:
            if (j >= i-total_Span) and (j <= i+total_Span):
                x_smooth2.append(j)

    for i in x_coordinates:        
        if i in x_smooth2:
            temp_listY = []    
            for j in x_coordinates:
                if (j >= i-total_Span) and (j <= i+total_Span):        
                    temp_listY.append(y_coordinates[x_coordinates.index(j)])            
            smooth_y_coordinates.append(sum(temp_listY)/len(temp_listY))            
        else:
            smooth_y_coordinates.append(y_coordinates[x_coordinates.index(i)])               
        
    return {'x_smooth1': x_smooth1, 'x_smooth2': x_smooth2, 'smooth_y_coordinates': smooth_y_coordinates}
        
