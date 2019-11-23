import matplotlib.pyplot as plt
import numpy as np

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

def live_plotter(x_vec, y1_data, line1, titulo1, y2_data, line2, titulo2, y3_data, line3, titulo3, y4_data, line4, titulo4, identifier='', pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(14,8))
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(223)
        ax4 = fig.add_subplot(224)
        ax1.set_title(titulo1)
        ax2.set_title(titulo2)
        ax3.set_title(titulo3)
        ax4.set_title(titulo4)
        # create a variable for the line so we can later update it
        line1, = ax1.plot(x_vec,y1_data,'',alpha=0.8)
        line2, = ax2.plot(x_vec,y2_data,'',alpha=0.8)
        line3, = ax3.plot(x_vec,y3_data,'',alpha=0.8)
        line4, = ax4.plot(x_vec,y4_data,'',alpha=0.8)
        #update plot label/title
        #plt.ylabel('Y Label')
        plt.title(titulo4)
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    line2.set_ydata(y2_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])

    if np.min(y2_data)<=line1.axes.get_ylim()[0] or np.max(y2_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y2_data)-np.std(y2_data),np.max(y2_data)+np.std(y2_data)])

    if np.min(y3_data)<=line1.axes.get_ylim()[0] or np.max(y3_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y3_data)-np.std(y3_data),np.max(y3_data)+np.std(y3_data)])

    if np.min(y4_data)<=line1.axes.get_ylim()[0] or np.max(y4_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y4_data)-np.std(y4_data),np.max(y4_data)+np.std(y4_data)])

    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1, line2, line3, line4

# the function below is for updating both x and y values (great for updating dates on the x-axis)
def live_plotter_xy(x_vec,y1_data,line1,identifier='',pause_time=0.01):
    if line1==[]:
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        line1, = ax.plot(x_vec,y1_data,'r-o',alpha=0.8)
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()
        
    line1.set_data(x_vec,y1_data)
    plt.xlim(np.min(x_vec),np.max(x_vec))
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])

    plt.pause(pause_time)
    
    return line1