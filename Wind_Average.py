#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Taking the longitudinally, time averaged E-W wind speed over the entire orbit for two different models and then comparing the difference in the E-W wind structure
#Takes in 180 fort.26 files (90 from each model) corresponding to 90 orbital phases

#file input structure

path='/home/whouck/scratch.komacek-prj/Willow/Models/' #sets the path in the directory to the models
runnames=['0G_yeseccen/Planet_Restart3','3G_yeseccen/Planet_Restart2'] #folders for each of the models
cm_data2 = np.loadtxt("/home/whouck/scratch.komacek-prj/Willow/Models/ScientificColourMaps8/cork/cork.txt") #sets the colorbar colors
cm_data2=np.flip(cm_data2,axis=0) #makes the colorbar flip which way the colors go
mymap2 = mcolors.LinearSegmentedColormap.from_list('my_colormap', cm_data2) #sets the color scheme of the plot to be the same as the colorbar

savename=path+'/'+'Difference_3G_vs_0G'+'.png' #sets where the file will be saved as and what name it will be saved under

#parameters

caption=False   #set equal to true to have a caption
cap='P=2.578 days'  #caption in top right
freeze=False         #adds a black line at water freezing temperature,useful for earth only works for plot=0
zeros=False #draw a contour line at 0
oom=7 #orders of magnitude the model spans
surfp=100 #surface pressure
LastOrbit_=False

#prints extra information
OLR_=False
verbose=False
ver=False

prot = 4.14 #rotational period in days
porb = 5.86 #orbital period in days
plot=1   #0 to plot temps, 1 to plot E-W winds, 2=N-S winds. (USUALLY ONLY T AND E-W USED) 
rotate = False
longavg=False       #if True, longavg
long_pl=0.0         #if longavg=True, ignored, otherwise longitude to plot at
units_a=1           #1=degrees, 0=radians, lat lon units. INPUT is already in degrees
units_t=0           #0=Kelvin, 1=Celsius, 2=Farhenheit - FOR plot=0 only
units_w=1           #0=m/s 1=km/s 2=mph, FOR plot=1 or =2 only


cbarL=0#useful for multiple plots --- force lower limit of colorbars. SET 0 otherwise
cbarM=0 #useful for multiple plots --- force upper limit of colorbars
ex=0           # if you want to extend the colorbar. Default is 1 for temperature

cbar_even=True     #for Winds, center colorbar so that 0 is middle.
ncolors=0  #0,sets so that each color step =1 in whatever units. otherwise =multiple of that

lo=False 
savefig=True

get_ipython().run_line_magic('matplotlib', 'inline')
fig, axs=plt.subplots(1, 3, sharex=True, sharey=True,figsize=(15,7), gridspec_kw={'hspace': .25, 'wspace': 0}) #creating a 1x3 figure

#Beginning the averaging function and other plotting

for i in range(3): #goes through the loop 3 teams, once for each panel in the figure
    if i != 2: #if were are not calculating the difference
        windavg = np.zeros((65,48,90)) #creates a zero-filled array the same size as the plt.data so that we can fill it with the correect values and take an average of them later
        for j in range(90): #goes through each of the orbital phase fortran files
            if j < 10: #need to have an if statement in case there is a single digit fortran file that needs a 0 in front of it
                fort_file = 'fort.260' + str(j)
                fort_64 = 'fort.640' + str(j)
            else: #for all other double digit fortran files that don't need a zero in front
                fort_file = 'fort.26' + str(j)
                fort_64 = 'fort.64' + str(j)
            
            #load_data and plotting scripts written previously by Erin May and Hayley Beltz with small edits made for this use
            runname2,lon_arr,lat_arr,oom,surfp,p_BAR,data_26,data_lo,data_olr=load_data(path,runnames[i],oom,surfp,LastOrbit_,OLR_,verbose,fort_file,fort_64,rotate,prot,porb,caption) #reading in the data using an external script
            LAT,PRESS_P,plt_data,cbar_levs,mymap=press_Plot_nograph(plot,lon_arr,lat_arr,p_BAR,data_26,units_a,units_t,units_w,freeze, caption, cap,savefig,savename,zeros,ver,cbarL,cbarM,cbar_even,ex,ncolors,longavg,long_pl,lo,oom) #reading in the plotting data using an external script
            windavg[:,:,j] = plt_data #assigns the wind data to the windavg array
        plt_data = np.mean(windavg, axis=2) #takes an average of all of the E-W wind data across all 90 orbital phases so we can get an idea of the wind structure of the planet, reducing noise and artifacts
        cbar_levs=np.linspace(-6,6,50) #sets levels for colorbar
        if i==0:
            cimg=axs[0].contourf(LAT,PRESS_P,plt_data,levels=cbar_levs,cmap=mymap,zorder=0,alpha=1.0) 
            
        #drawing from the plotting data
        axs[i].contourf(LAT,PRESS_P,plt_data,levels=cbar_levs,cmap=mymap,zorder=0,alpha=1.0) #plots the filled contours for the wind colors
        axs[i].contour(LAT,PRESS_P,plt_data,levels=[0],colors='black',zorder=0,alpha=1.0) #plots the black contour lines
        axs[i].tick_params(labelsize=15) #setting the size of the ticks
        axs[i].set_ylim(np.nanmax(p_BAR),np.nanmin(p_BAR)) #setting the y axis to have the same min and max as the pressure bar
        axs[i].set_xlim(np.nanmin(lat_arr),np.nanmax(lat_arr)) #setting the x axis to have the same min and max as the latitude range
        axs[i].set_yscale('log') #making it a log plot
        
    #beginning the averaging + differencing function
    if i == 2: #for the third panel, where we will be calculating the difference between the previous 2 panels/models
        windavgdiff = np.zeros((65,48,90))
        for j in range(90):
            if j < 10:
                fort_file = 'fort.260' + str(j)
                fort_64 = 'fort.640' + str(j)
            else:
                fort_file = 'fort.26' + str(j)
                fort_64 = 'fort.64' + str(j)
                
            #load_data and plotting scripts written previously by Erin May and Hayley Beltz with small edits made for this use
            runname2,lon_arr,lat_arr,oom,surfp,p_BAR,data_26,data_lo,data_olr=load_data(path,runnames[0],oom,surfp,LastOrbit_,OLR_,verbose,fort_file,fort_64,rotate,prot,porb,caption) #reading in the first set of data using an external script
            LAT,PRESS_P,plt_data,cbar_levs,mymap=press_Plot_nograph(plot,lon_arr,lat_arr,p_BAR,data_26,units_a,units_t,units_w,freeze, caption, cap,savefig,savename,zeros,ver,cbarL,cbarM,cbar_even,ex,ncolors,longavg,long_pl,lo,oom) #reading in the first set of plotting data using an external script
            plt_data0G = plt_data #creating a variable to hold just the first model's wind data
            runname2,lon_arr,lat_arr,oom,surfp,p_BAR,data_26,data_lo,data_olr=load_data(path,runnames[1],oom,surfp,LastOrbit_,OLR_,verbose,fort_file,fort_64,rotate,prot,porb,caption) #reading in the second set of data using an external script
            LAT,PRESS_P,plt_data,cbar_levs,mymap=press_Plot_nograph(plot,lon_arr,lat_arr,p_BAR,data_26,units_a,units_t,units_w,freeze, caption, cap,savefig,savename,zeros,ver,cbarL,cbarM,cbar_even,ex,ncolors,longavg,long_pl,lo,oom) #reading in the second set of plotting data using an external script
            plt_data3G = plt_data #creating a variable to hold the second model's wind data
            windavgdiff[:,:,j] = plt_data3G - plt_data0G #instead of just assigning the wind data to the array, we're assigning the difference between the two sets of wind data to the array 
        plt_data_diff = np.mean(windavgdiff, axis=2) #calculating the average of the wind difference data
        cbar_levs=np.linspace(-6,6,50)
        axs[2].contourf(LAT,PRESS_P,plt_data_diff,levels=cbar_levs,cmap=mymap,zorder=0,alpha=1.0)
        axs[2].contour(LAT,PRESS_P,plt_data_diff,levels=[0],colors='black',zorder=0,alpha=1.0)
        axs[2].tick_params(labelsize=15)
        axs[2].set_ylim(np.nanmax(p_BAR),np.nanmin(p_BAR))
        axs[2].set_xlim(np.nanmin(lat_arr),np.nanmax(lat_arr))
        axs[2].set_yscale('log')
axs[0].set_xlabel('Latitude [degrees]',fontsize=22) #setting the x axis label for all the panels
axs[1].set_xlabel('Latitude [degrees]',fontsize=22)
axs[2].set_xlabel('Latitude [degrees]',fontsize=20)
axs[0].set_ylabel('Pressure [bars]',fontsize=22) #setting the y axis label
axs[0].set_title('0G Eccentric',fontsize=22) #titling each of the panels accordingly
axs[1].set_title('3G Eccentric',fontsize=22)
axs[2].set_title('Difference',fontsize=22)
cbar=plt.colorbar(cimg,ax=axs,orientation='vertical') #actually plotting the colorbar
cbar.set_label('E-W Wind Speed [km/s]', size=22) #labeling the colorbar
fig.savefig(savename) #saving the figure under the savename defined above

