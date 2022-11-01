import numpy as np 
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def clean_up_datafile(filepath):
    data = np.loadtxt(filepath, skiprows=23, delimiter="\t").T
    omega_unique = np.unique(data[1])
    r_unique = np.unique(data[2])
    postdata = []
    for i in range(omega_unique.shape[0]): 
        for j in range(r_unique.shape[0]):
            ind = np.where(data[1:3].T == [omega_unique[i],r_unique[j]])
            #print(data[1:3].T[ind])
            measured_omega = np.mean(data[3][ind[0]])
            measured_r = np.mean(data[4][ind[0]])
            measured_power = np.mean(data[5][ind[0]])
            measured_voltage = np.mean(data[6][ind[0]])
            measured_current = np.mean(data[7][ind[0]])
            postdata.append([omega_unique[i], r_unique[j], measured_omega,measured_r, measured_power, measured_voltage, measured_current])
    postdata = np.array(postdata)
    header = "Nominal Omega [RPM]\tNominal R [Ohm]\tMeasured Omega [RPM]\tMeasured R [Ohm]\t Measured Power [W]\t Measured Voltage [V]\tMeasured Current [A]"
    np.savetxt("postdata.txt", postdata, delimiter="\t", fmt="%10.5f", header=header)

def plots():

    data = np.loadtxt("postdata.txt", delimiter="\t",skiprows=1).T
    omega_unique = np.unique(data[0])
    r_unique = np.unique(data[1])
    omega = data[0].reshape(omega_unique.shape[0], r_unique.shape[0])
    r = data[1].reshape(omega_unique.shape[0], r_unique.shape[0])
    P = data[4].reshape(omega_unique.shape[0], r_unique.shape[0])
    fig = make_subplots(rows=2, cols=2, start_cell="top-left")
    fig = make_subplots(
        rows=3, cols=2,
        column_widths=[0.5, 0.5],
        row_heights=[1, 1, 1],
        specs=[[{"type": "surface", "rowspan": 2}, {"type": "scatter"}],
                [        None                    , {"type": "scatter"}],
                [{"type": "scatter"}             , {"type": "scatter"}]],
        subplot_titles=("Power surface", "Power vs Resistance", "Power vs Angular Speed", "Power vs Voltage", "Current vs Voltage"))
    
    
    fig.add_trace(go.Surface(x=omega,y=r,z=P,
                    colorbar=dict(x=0.425, y=0.72,len=0.5)), row=1,col=1)
    
    Vvec = np.sort(data[5]) 
    Pvec = data[4][np.argsort(data[5])]
    Ivec = data[6][np.argsort(data[5])]


    for i in range(omega.shape[1]): 
        fig.add_trace(go.Scatter(x=omega[:,i], y=P[:,i]), row=1,col=2)
    for i in range(r.shape[0]):
        fig.add_trace(go.Scatter(x=r[i], y=P[i]), row=2,col=2)

    fig.add_trace(go.Scatter(x=Pvec, y=Vvec), row=3,col=1)
    fig.add_trace(go.Scatter(x=Vvec, y=Ivec), row=3,col=2)

    fig.update_layout(title='Wind Turbine Graphs and Curves', 
                      autosize=True,
                      height=1250)

    fig.update_layout(scene = dict(xaxis_title='Angular Speed [RPM]',
                                   yaxis_title='Resistance [Ohm]',
                                   zaxis_title='Power [W]'))

    # Update xaxis properties
    fig.update_xaxes(title_text= "Resistance[Ohm]", row=1, col=2)
    fig.update_xaxes(title_text= "Omega [RPM]", row=2, col=2)
    fig.update_xaxes(title_text= "Power [W]", row=3, col=1)
    fig.update_xaxes(title_text= "Voltage[V]", row=3, col=2)

    # Update yaxis properties
    fig.update_yaxes(title_text= "Power [W]", row=1, col=2)
    fig.update_yaxes(title_text= "Power [W]", showgrid=False, row=2, col=2)
    fig.update_yaxes(title_text= "Voltage [V]", row=3, col=1)
    fig.update_yaxes(title_text= "Current [A]", row=3, col=2)
    
    fig.update_xaxes(rangeslider=dict(visible=False)) 

    fig.show()
