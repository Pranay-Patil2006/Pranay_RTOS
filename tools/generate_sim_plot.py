import matplotlib.pyplot as plt
import numpy as np
import random

# Generate simulated data exactly like the dashboard
time_points = np.linspace(0, 10, 200)
y_data = []

for t in time_points:
    # Simulating the sawtooth wave from our main.c dummy data
    val = int(t * 10) % 100
    # Add some noise
    val += random.uniform(-2, 2)
    y_data.append(val)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(time_points, y_data, lw=2, color='#00ffcc')

# Styling
ax.set_facecolor('#1e1e1e')
fig.patch.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.title('ZenithOS Live Telemetry Simulation', color='white', pad=20, fontsize=14)
plt.xlabel('Time (s)', color='white', fontsize=12)
plt.ylabel('Sensor Value', color='white', fontsize=12)
plt.ylim(-10, 110)
plt.xlim(0, 10)
plt.grid(True, color='#333333', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot
plt.savefig('docs/simulation_demo.png', facecolor=fig.get_facecolor(), edgecolor='none', dpi=150)
print("Simulation plot saved to docs/simulation_demo.png")
