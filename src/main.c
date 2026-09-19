#include "kernel.h"
#include <stdio.h>

// ---------------------------------------------------------
// ZenithOS - Minimal Preemptive RTOS for ARM Cortex-M
// Personalized for your GitHub portfolio!
// ---------------------------------------------------------

void task_sensor_read();
void task_control_loop();
void task_telemetry();

// Global variables for dummy sensor data
volatile short sensor_x = 0;
volatile short sensor_y = 0;
volatile short sensor_z = 0;

int main(void) {
    // 1. Initialize the Kernel
    kernelInit();

    // 2. Initialize Hardware / Board Support
    BSP_LED_Init();
    USART2_Init();
    
    // Print a cool startup banner
    USART2_send_str("\r\n==================================\r\n");
    USART2_send_str("        Booting ZenithOS...       \r\n");
    USART2_send_str(" Minimal Preemptive RTOS Kernel   \r\n");
    USART2_send_str("==================================\r\n");

    // 3. Add Threads (Tasks) to the Scheduler
    // kernelAddThreads(function_pointer, priority)
    kernelAddThreads(&task_sensor_read, 1);
    kernelAddThreads(&task_control_loop, 2);
    kernelAddThreads(&task_telemetry, 3);

    USART2_send_str("[SYSTEM] All tasks loaded. Launching scheduler...\r\n");

    // 4. Launch Kernel (hands over control to the scheduler)
    kernelLaunch();

    // The system should never reach here
    return 0;
}

// ---------------------------------------------------------
// Task Definitions
// ---------------------------------------------------------

// Task 1: Simulates reading from an I2C/SPI sensor at a high frequency
void task_sensor_read() {
    while(1) {
        // In a real scenario, you would read I2C here:
        // accelGetValues(&sensor_x, &sensor_y, &sensor_z);
        
        sensor_x = (sensor_x + 1) % 100; // Dummy data
        
        // Yield to allow other tasks of same/lower priority to run
        threadYield(); 
    }
}

// Task 2: Simulates a control loop (like a PID controller)
void task_control_loop() {
    while (1) {
        // Toggle an LED to show the control loop is alive
        BSP_LED_redToggle();
        
        // Simulate some processing time
        busy_wait(10); 
        
        threadYield();
    }
}

// Task 3: Prints telemetry data over UART periodically
void task_telemetry() {
    while (1) {
        BSP_LED_greenToggle();
        
        // Send telemetry out via UART
        USART2_send_str("[TELEMETRY] Sensor X: ");
        USART2_send_int(sensor_x);
        USART2_send_str("\r\n");
        
        // Wait before sending next telemetry packet
        threadSleep(500); 
    }
}
