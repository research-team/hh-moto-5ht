import nest
import pylab
import numpy


def plot_parameter(device, param_to_display, label, style='-'):
    status = nest.GetStatus(device)[0]
    events = status['events']
    times = events['times']
    pylab.plot(times, events[param_to_display], style, label=label)


nest.Install("research_team_models")
nest.SetKernelStatus(dict(resolution=0.1))

neuron = nest.Create(
    'hh_moto_5ht', params={
        "I_e": 700.0,  # pA
        "C_m": 200.0,  # pF
        "t_ref": 0.0,
    }
)
multimeter = nest.Create(
    'multimeter',
    params={
        "record_from": [
            "V_m",
            "Ca_in",
            "Act_m",
            "Act_h",
            "Inact_n",
            "Act_p",
            "Act_mc",
            "Act_hc",
        ],
        "withtime": True,
        "interval": 0.1
    }
)

nest.Connect(multimeter, neuron)
nest.Simulate(150.)

pylab.figure()
pylab.title('Nest iclamp sim')

pylab.subplot(4, 1, 1)
pylab.ylabel('Membrane Voltage')
plot_parameter(multimeter, 'V_m', 'V_m')
pylab.legend()

pylab.subplot(4, 1, 2)
pylab.ylabel('Ca inside')
pylab.yticks(numpy.arange(0.0001, 0.0010, 0.0002))
plot_parameter(multimeter, 'Ca_in', 'Ca_in')
pylab.legend()

pylab.subplot(4, 1, 3)
pylab.ylim(0, 1)
pylab.ylabel('h, m, n particles')
plot_parameter(multimeter, 'Act_h', 'h', 'r')
plot_parameter(multimeter, 'Act_m', 'm', 'g')
plot_parameter(multimeter, 'Inact_n', 'n', 'b')
pylab.legend()

pylab.subplot(4, 1, 4)
pylab.ylim(0, 1)
pylab.ylabel('p, mc, hc particles')
plot_parameter(multimeter, 'Act_p', 'p', 'r')
plot_parameter(multimeter, 'Act_mc', 'mc', 'g')
plot_parameter(multimeter, 'Act_hc', 'hc', 'b')
pylab.legend()

pylab.show()
