## ORNL neutronimaging

### Set up

To make sure you have all the packages necessary to run those algorithms, run the following command
> python ./check_install.py


### Algorithm 1 Sliding Window approach 

Input file location is in line 26 its in .XLSX (excel format)

run the script will ask for 2 requirement
1) Window Span eg:0.025\  
2) Threshold value like: 0.0025 for analysis by peak. a threshold is need it at beginning later its dynamically changeable once figure is given


### Algorithm 2 smooth distance based 

requires 4 inputs.

1) input file txt that contains the value later this will be merged to get them direct from the image from step1.ipynb 
input= textin.txt

2)Smoothed Curve Output file: not important just to write and read values after changing threshold to make it more dynamic

Smoothed Curve Output file= text_1.txt

3)Threshold Output file: also not important just to write and read values after changing threshold to make it more dynamic

4)Window size: This value is of vital importance as it sets the analysis area to analyze how wide the area around each and every point it will also affect the fitting procedure currently with Si sample we tested with 0.075 we could set an index for different materials like a sensitivity or accuracy parameter based on experimentation. 


### Algorithm 3 smooth highest peak based calculation

requires 4 inputs 

1) input file txt that contains the value later this will be merged to get them direct from the image from step1.ipynb 
input= textin.txt

2)Smoothed Curve Output file: not important just to write and read values after changing threshold to make it more dynamic

Smoothed Curve Output file= text_1.txt

3)Threshold Output file: also not important just to write and read values after changing threshold to make it more dynamic

4)Window size: This value is of vital importance as it sets the analysis area to analyze how wide the area around each and every point it will also affect the fitting procedure currently with Si sample we tested with 0.075 we could set an index for different materials like a sensitivity or accuracy parameter based on experimentation. 


### Algorithm 4 Genetic Programming

in progress

- zoom to rectangle

To magnify a certain area in the graph, select "zoom to rectangle" and draw a rectangle on desired area to magnify points

- Click Home icon

To get back actual size figure.

