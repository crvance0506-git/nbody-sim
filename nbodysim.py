import numpy as np
import matplotlib.pyplot as plt

class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = position
        self.velocity = velocity

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
    sun = Body(1.989e30, np.array([0, 0]), np.array([0, 0]))
    
    # Earth: mass, position, velocity
    earth = Body(5.972e24, np.array([1.5e11, 0]), np.array([0, 29780]))

    # Mars:
    mars = Body(6.418e23, np.array([2.27987e11, 0]), np.array([0, 24000]))
                 
    dt = 86400 # Step 1 day represented with seconds
    num_steps = 730 # Simulate 2 earth years

    bodies = [earth, mars, sun]
    position_history = [[] for _ in bodies]

    for timestep in range(num_steps):
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
    for i, body in enumerate(bodies):
        x_positions = [pos[0] for pos in position_history[i]]
        y_positions = [pos[1] for pos in position_history[i]]
        plt.plot(x_positions, y_positions, label=f'Body {i}')
    plt.axis('equal')
    plt.xlabel('x(m)')
    plt.ylabel('y(m)')
    plt.title('N-Body orbit')
    plt.legend()
    plt.show()

    return 0

if __name__ == "__main__":
    main()