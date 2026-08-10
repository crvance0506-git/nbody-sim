import numpy as np
import matplotlib.pyplot as plt

def gravitational_force(pos1, mass1, pos2, mass2, G=6.674e-11):
    r_vec = pos2 - pos1
    r_mag = np.linalg.norm(r_vec)
    r_hat = r_vec / r_mag

    force_mag = (G*mass1*mass2) / r_mag**2
    force_vec = force_mag * r_hat

    return force_vec

def main():

    # SI Units
    # Sun: mass, position, velocity
    sun_mass = 1.989e30
    sun_pos = np.array([0, 0])
    sun_vel = np.array([0, 0])

    # Earth: mass, position, velocity
    earth_mass = 5.972e24
    earth_pos = np.array([1.5e11, 0])
    earth_vel = np.array([0, 29780])

    dt = 86400
    num_steps = 365 # Simulate a year

    positions = []

    for timestep in range(num_steps):
        force = gravitational_force(earth_pos, earth_mass, sun_pos, sun_mass)
        acceleration = force / earth_mass
        earth_pos = (earth_vel * dt) + earth_pos
        earth_vel = (acceleration * dt) + earth_vel
        positions.append(earth_pos)

    # Visualize
    x_positions = [pos[0] for pos in positions]
    y_positions = [pos[1] for pos in positions]

    plt.plot(x_positions, y_positions)
    plt.axis('equal')
    plt.xlabel('x(m)')
    plt.ylabel('y(m)')
    plt.title('Earth orbit (Euler integration)')
    plt.show()

    return 0

if __name__ == "__main__":
    main()