import concurrent.futures
import math
import pickle

import numpy as np
from characteristicParameters.measurementProcedure import MeasurementProcedure, MeasuredStokesVector
from characteristicParameters.muellerCalculus import linearly_polarized_light, optical_equivalent_model

# Settings
stepsize = math.radians(45)
# y-axis
omegas = np.arange(0, math.pi + stepsize / 2, stepsize)
# x-axis
deltas = np.arange(0, math.pi + stepsize / 2, stepsize)

# Two orientations angles for the incident linearly polarized light:
phi_1 = 0
phi_2 = math.radians(45)

# Store the values here:
true_values = []  # true characteristic values
measurements: list[MeasurementProcedure] = []  # measured Stokes parameters
measured_values = []  # measured characteristic values

for delta in deltas:
    for omega in omegas:
        theta = delta / 6

        true_values.append((delta, theta, omega))

        # Measured Stokes parameters
        model = optical_equivalent_model(delta=delta, theta=theta, omega=omega)
        # Incident light:
        S_in_phi1 = linearly_polarized_light(phi_1)
        S_in_phi2 = linearly_polarized_light(phi_2)

        S_out_phi1 = np.matmul(model, S_in_phi1)
        S_out_phi2 = np.matmul(model, S_in_phi2)

        OutgoingStokes1 = MeasuredStokesVector(phi=phi_1,
                                               stokes_vector=S_out_phi1)
        OutgoingStokes2 = MeasuredStokesVector(phi=phi_2,
                                               stokes_vector=S_out_phi2)
        measurements.append(MeasurementProcedure([OutgoingStokes1, OutgoingStokes2]))


# Define a function that can be run parallel:
def find_parameters_1(measurement: MeasurementProcedure) -> (float, float, float):
    parameters = measurement.find_characteristic_parameters(
        lb_delta=0, ub_delta=math.pi,
        lb_theta=0, ub_theta=math.pi / 2,
        lb_omega=0, ub_omega=math.pi,
        strategy="best1bin"
    )
    return parameters.delta, parameters.theta, parameters.omega


def find_parameters_2(measurement: MeasurementProcedure) -> (float, float, float):
    parameters = measurement.find_characteristic_parameters(
        lb_delta=0, ub_delta=math.pi,
        lb_theta=0, ub_theta=math.pi,
        lb_omega=0, ub_omega=2 * math.pi,
        strategy="best1bin"
    )
    return parameters.delta, parameters.theta, parameters.omega


def find_parameters_3(measurement: MeasurementProcedure) -> (float, float, float):
    parameters = measurement.find_characteristic_parameters(
        lb_delta=0, ub_delta=math.pi,
        lb_theta=0, ub_theta=math.pi / 2,
        lb_omega=0, ub_omega=math.pi,
        strategy="rand1exp"
    )
    return parameters.delta, parameters.theta, parameters.omega


def find_parameters_4(measurement: MeasurementProcedure) -> (float, float, float):
    parameters = measurement.find_characteristic_parameters(
        lb_delta=0, ub_delta=math.pi,
        lb_theta=0, ub_theta=math.pi,
        lb_omega=0, ub_omega=2 * math.pi,
        strategy="rand1exp"
    )
    return parameters.delta, parameters.theta, parameters.omega


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
        pass
        # 1
        measured_values = list(executor.map(find_parameters_1, measurements))
        with open("data/S_fig1_measured_values_1_new.pickle", "wb") as handle:
            pickle.dump(measured_values, handle)

        # 2
        measured_values = list(executor.map(find_parameters_2, measurements))
        with open("data/S_fig1_measured_values_2_new.pickle", "wb") as handle:
            pickle.dump(measured_values, handle)

        # 3
        measured_values = list(executor.map(find_parameters_3, measurements))
        with open("data/S_fig1_measured_values_3_new.pickle", "wb") as handle:
            pickle.dump(measured_values, handle)

        # 4
        measured_values = list(executor.map(find_parameters_4, measurements))
        with open("../figures_supplemental/data/S_fig1_measured_values_4_new.pickle", "wb") as handle:
            pickle.dump(measured_values, handle)

    with open("../figures_supplemental/data/S_fig1_true_values_new.pickle", "wb") as handle:
        pickle.dump(true_values, handle)
