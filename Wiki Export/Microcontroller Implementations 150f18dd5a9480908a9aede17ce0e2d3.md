# Microcontroller Implementations

Author: Aaliyah Yan
Branch: Hardware
Hidden: No
Parent page: Development Resources (Development%20Resources%2014bf18dd5a9480dcb4cbfec87e0cb38b.md)

## **Overview**

Typically any system that requires any sort of controls, computing, and telemetry will need some sort of microcontroller or system on chip (SoC). These come in a few different form factors with varying levels of customizability. This page will focus solely on choosing what form of microcontroller to implement.

## **Bare MCU or Carrier Board?**

### Bare MCU

The term “bare-metal programming” refers to programming without any operating system or resources to aid in the running of your program; although you gain fast access to register information and memory, there aren’t any safeguards or optimizations in place to aid your program in running.

When I refer to a “bare MCU,” I am referring to a microcontroller unit implemented directly on a custom PCB, like in the picture below. I.e. you make the PCB and directly slap the chip on there and route/set up all the IO of the chip.

![image.png](Microcontroller%20Implementations%20150f18dd5a9480908a9aede17ce0e2d3/image.png)

This reduces form factor incredibly and can result in much lower power draws, as well as being able to directly configure the IO of the chip to suit your needs. However, this adds additional complexity in implementation and flashing. This is also typically how most professional companies will end up doing it since they have the manpower to drive this additional complexity in development. You might also want to weigh the difficulty in manufacturing and try and spec an MCU that is relatively easy to solder (i.e. through drag soldering).

### Carrier Board

With microcontroller development boards, like an STM32 Nucleo board or a Teensy 4.1 (shown in pictures below), the bare MCU has already been implemented for you and all you need to do is route the IO of the board itself. The routing of the IO can be done through a “carrier” board.

With microcontroller development boards, like an STM32 Nucleo board or a Teensy 4.1 (shown in pictures below), the bare MCU has already been implemented for you and all you need to do is route the IO of the board itself. The routing of the IO can be done through a “carrier” board.

![image.png](Microcontroller%20Implementations%20150f18dd5a9480908a9aede17ce0e2d3/image%201.png)

![image.png](Microcontroller%20Implementations%20150f18dd5a9480908a9aede17ce0e2d3/image%202.png)

These development boards typically have a bunch of safety circuits and other chips onboard to aid development, such as an EEPROM, onboard activity LED, reset button, and maybe even an IC to handle flashing the chip. All of that would need to be manually implemented with a bare MCU. However, you lose out on the configurability, have to work with a much larger form factor, and usually end up with an overspec’ed microcontroller board because there are things that you will never need onboard.

![“Carrier” board for an STM32 dev board using vertical connectors, but can just be soldered in place to reduce height at the cost of ease of disassembly](Microcontroller%20Implementations%20150f18dd5a9480908a9aede17ce0e2d3/image%203.png)

“Carrier” board for an STM32 dev board using vertical connectors, but can just be soldered in place to reduce height at the cost of ease of disassembly