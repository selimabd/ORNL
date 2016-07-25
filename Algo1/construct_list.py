import math


"""Method to capture Normalized Absolute Differences Sum of each element in Y_Coordinates a.k.a (Raw - OB)/OB values""" 
def construct_Alphalist(window_Span, x_coordinates, y_coordinates, alpha_list):
    for i in range(0, len(x_coordinates)):
        temp_Sum = 0                #Intermediate Sum Value
        count = 0                   #Count to Normalize Absolute Differences Sum
        for j in range(0, len(x_coordinates)):
            if (x_coordinates[j] >= x_coordinates[i]-window_Span) and \
            (x_coordinates[j] <= x_coordinates[i]+window_Span) and \
            (y_coordinates[j]!=y_coordinates[i]):
                count += 1                
                temp_Sum  += math.fabs(y_coordinates[i] - y_coordinates[j])        
        alpha_list.append(temp_Sum/float(count))
    return alpha_list

"""Method to populate beta_list elements"""
def construct_Betalist(alpha_list, beta_list):
    beta_list.append(math.fabs(alpha_list[0]-alpha_list[1]))    
    
    for i in range(0, len(alpha_list)):        
        if i-1 >= 0 and i+1 < len(alpha_list):
            beta_list.append(math.fabs(alpha_list[i]- \
                                       alpha_list[i-1])+math.fabs(alpha_list[i]-alpha_list[i+1]))

    beta_list.append(math.fabs(alpha_list[-1]-alpha_list[-2]))
    return beta_list