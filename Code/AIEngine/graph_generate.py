import matplotlib.pyplot as plt
import numpy as np

# Generate random data
x = np.arange(1, 11)  # X values (1 to 10)
y = np.random.randint(1, 100, 10)  # Random Y values between 1 and 100

# Create the plot
plt.figure(figsize=(6, 4))
plt.plot(x, y, marker='o', linestyle='-', color='b', label='Successful Alerts')
plt.title('Analysis Graph: Datapoints for Effective Alerts Over Scientific Year')
plt.xlabel('Time')
plt.ylabel('Effective Alerts')
plt.legend()

# Save the graph as an image
plt.savefig('graph.png')
plt.close()
