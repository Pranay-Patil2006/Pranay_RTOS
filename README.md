# ZenithOS: Custom Preemptive RTOS for ARM Cortex-M4

ZenithOS is a minimal, preemptive Real-Time Operating System (RTOS) designed from scratch for the ARM Cortex-M4 architecture (specifically targeting the STM32F4 series). It serves as an educational dive into kernel internals, context switching, and hardware-level task scheduling.

## Features
*   **Preemptive Task Scheduling**: Utilizes the ARM Cortex-M `SysTick` timer and `PendSV` exception to perform true preemptive context switching.
*   **Priority-based Execution**: Tasks are assigned priorities, allowing critical tasks (like sensor reading or control loops) to preempt lower-priority tasks (like telemetry).
*   **Thread Sleeping & Yielding**: Tasks can cooperatively yield the CPU or sleep for a specific number of OS ticks.
*   **Hardware Abstraction**: Includes basic board support for UART, LEDs, PWM, I2C, and SPI.
*   **Sensor Drivers**: Pre-built integrations for standard IMUs (Accelerometer, Gyroscope, Magnetometer).

## Architecture Internals
To understand how ZenithOS works under the hood, you need to understand three core ARM concepts:
1.  **SysTick Timer**: The heartbeat of the OS. It fires an interrupt every 1ms. If a task has exhausted its time quanta or a higher priority task is ready, the SysTick handler triggers a `PendSV` exception.
2.  **PendSV (Pendable Service Call)**: This is where the actual context switch happens. The assembly routine saves the current task's CPU registers to its individual stack, swaps the stack pointer to the next task's stack, and pops the new registers.
3.  **Task Control Block (TCB)**: Every thread has a TCB that stores its stack pointer, priority, state (READY, SLEEPING), and sleep duration.

## Getting Started

### Hardware Requirements
*   STM32F4-Discovery or STM32 Nucleo-F4xx board.
*   ST-Link V2 (Usually built into the boards).

### Building and Flashing
This project uses a standard `Makefile` and does not rely on heavy IDE abstractions like STM32CubeIDE.
You will need the `arm-none-eabi-gcc` toolchain.

```bash
make
make flash
```

## Portfolio Notes
*This project was built to demonstrate a deep understanding of bare-metal C programming, ARM assembly, and operating system design principles. By avoiding standard libraries like FreeRTOS, this repository proves an ability to manipulate hardware registers directly and design memory-safe architectures in constrained environments.*
