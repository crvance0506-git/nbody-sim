import numpy as np
import matplotlib.pyplot as plt

class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = position
        self.velocity = velocity

def kinetic_energy(bodies):
    total_kinetic = 0
    for body in bodies:
        total_kinetic += 0.5 * body.mass * (np.linalg.norm(body.velocity)**2)

    return total_kinetic

def potential_energy(bodies, G=6.674e-11):
    total_potential = 0
    for i, body_i in enumerate(bodies):
        for j, body_j in enumerate(bodies):
            if j > i:
                r_vec = body_j.position - body_i.position
                r_mag = np.linalg.norm(r_vec)
                total_potential += (G * body_i.mass * body_j.mass) / r_mag

    return total_potential * -1

def gravitational_force(body1, body2, G=6.674e-11):
    r_vec = body2.position - body1.position
    r_mag = np.linalg.norm(r_vec)
    r_hat = r_vec / r_mag

    force_mag = (G*body1.mass*body2.mass) / r_mag**2
    force_vec = force_mag * r_hat

    return force_vec

def main():

    # SI Units
    # Sun: mass, position, velocity
    sun = Body(1.889e30, np.array([0, 0]), np.array([0, 0]))
    
    # Earth: mass, position, velocity
    earth = Body(1.989e30, np.array([1.496e11, 0]), np.array([0, 29780]))

    # Mars:
    mars = Body(2.189e30, np.array([-1.496e11, 0]), np.array([0, -35780]))
                 
    dt = 86400 # Step 1 day represented with seconds
    YEARS_TO_SIMULATE = 5
    num_steps = int(365 * YEARS_TO_SIMULATE) # Modify YEARS_TO_SIMULATE rather than this variable for an easier time

    bodies = [earth, mars, sun]
    position_history = [[] for _ in bodies] # Stores the position of each body at each time step
    energy_history = [] # Stores the total energy of the system at each time step

    for timestep in range(num_steps):
        # I'm going to calculate the total energy before the update.
        # I believe there are slight differences between calculating before vs after,
        # but I prefer before just to have the true initial energy of the system.
        total_energy = kinetic_energy(bodies) + potential_energy(bodies)
        energy_history.append(total_energy)

        net_forces = []

        for i, body_i in enumerate(bodies):
            net_force = np.array([0.0, 0.0])
            for j, body_j in enumerate(bodies):
                if i != j:
                    net_force += gravitational_force(body_i, body_j)
            net_forces.append(net_force)

        # Must update all new forces AFTER calculations are done
        for i, body in enumerate(bodies):
            acceleration = net_forces[i] / body.mass
            body.velocity = (acceleration * dt) + body.velocity
            body.position = (body.velocity * dt) + body.position
            position_history[i].append(body.position)


    # Visualize

    # Trajectory plot
    plt.figure()
    for i, body in enumerate(bodies):
        x_positions = [pos[0] for pos in position_history[i]]
        y_positions = [pos[1] for pos in position_history[i]]
        plt.plot(x_positions, y_positions, label=f'Body {i}')
    plt.axis('equal')
    plt.xlabel('x(m)')
    plt.ylabel('y(m)')
    plt.title('N-Body orbit')
    plt.legend()

    # Total energy plot
    # Here, i wanted to plot total energy just to see how accurate this simulation can conserve energy.
    # Ideally, the system conserves all energy we started with, but the calculations could cause discrepancies, which I would like to graph.
    plt.figure()
    plt.plot(energy_history)
    plt.xlabel('time(days)')
    plt.ylabel('total energy (J)')
    plt.title('Total Energy in System')
    
    plt.show()

    return 0

if __name__ == "__main__":
    main()