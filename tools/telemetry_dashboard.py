import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse
import random

# -----------------------------------------------------------------------------
# ZenithOS Telemetry Dashboard
# This script connects to the STM32 via UART and plots real-time sensor data.
# If no board is connected, use --simulate to generate dummy data.
# -----------------------------------------------------------------------------

parser = argparse.ArgumentParser(description="ZenithOS Real-Time Telemetry")
parser.add_argument('--port', type=str, default='COM3', help='Serial port (e.g., COM3 or /dev/ttyUSB0)')
parser.add_argument('--baud', type=int, default=115200, help='Baud rate')
parser.add_argument('--simulate', action='store_true', help='Simulate data if board is not connected')
args = parser.parse_args()

x_data = []
y_data = []
start_time = time.time()

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2, color='#00ffcc')
ax.set_facecolor('#1e1e1e')
fig.patch.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
plt.title('ZenithOS Live Telemetry', color='white')
plt.xlabel('Time (s)', color='white')
plt.ylabel('Sensor Value', color='white')

# Initialize serial connection
ser = None
if not args.simulate:
    try:
        ser = serial.Serial(args.port, args.baud, timeout=1)
        print(f"Connected to ZenithOS on {args.port}")
    except Exception as e:
        print(f"Error connecting to serial port: {e}")
        print("Falling back to simulation mode...")
        args.simulate = True

def init():
    ax.set_ylim(-10, 110)
    ax.set_xlim(0, 10)
    return line,

def update(frame):
    current_time = time.time() - start_time
    val = 0
    
    if args.simulate:
        # Simulate the sawtooth wave from our main.c dummy data
        val = int(current_time * 10) % 100
        # Add some noise
        val += random.uniform(-2, 2)
        time.sleep(0.05) # Simulate UART delay
    else:
        if ser and ser.in_waiting:
            line_data = ser.readline().decode('utf-8').strip()
            if "Sensor X:" in line_data:
                try:
                    val = int(line_data.split(":")[-1].strip())
                except ValueError:
                    pass

    x_data.append(current_time)
    y_data.append(val)
    
    # Keep only the last 100 points
    if len(x_data) > 100:
        x_data.pop(0)
        y_data.pop(0)
        
    # Dynamically adjust X axis
    if current_time > 10:
        ax.set_xlim(current_time - 10, current_time)

    line.set_data(x_data, y_data)
    return line,

ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=50)
plt.show()
