# Schematic Best Practices

Author: Aaliyah Yan
Branch: Hardware
Hidden: No
Parent page: Development Resources (Development%20Resources%2014bf18dd5a9480dcb4cbfec87e0cb38b.md)

> “Electricity is really just organized lightning” - George “Andrew Abrego” Carlin
> 

## **Preface**

This document will show you how to set up your KiCAD schematic pages to look as professional as possible, as well as give you some good design practices when implementing circuitry.

![image.png](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image.png)

## **Keeping Your Schematic Organized**

### Selecting the Correct Page Size

Typically when you begin a schematic, KiCAD will open a page that resembles the following:

![image.png](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image%201.png)

KiCAD schematics generate with a **Size A** page by default, which most of the time will be too small to fit a significant amount of circuitry on.

We can change this by zooming in on the box in the bottom right of the schematic page and selecting the box related to page size.

![image.png](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image%202.png)

Clicking this box will open a menu where you will be able to alter the page size of the schematic. Industry-standard schematics are **Size B**, although in certain situations will go up to **Size C or D**.

![image.png](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image%203.png)

Make sure to also fill out the Issue Date, Revision, and Title fields

## **Schematic Organization**

Organize your schematic by functionality

![Organization of power architecture in a KiCAD schematic](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image%204.png)

Organization of power architecture in a KiCAD schematic

One of the main goals when creating a schematic is to allow other engineers to easily read and understand the work that you’ve done, and interpret (from a circuitry standpoint) the purpose of each part of the circuit. One of the ways that we can do this is by **grouping components by functionality**.

**Grouping components by functionality** means organizing your schematic in such a way that all IC’s and passive components (Resistors, Capacitors, etc) are grouped together. Popular grouping includes the following:

<aside>
💡

**Power architecture:** How your project is powered:

- This page should include callouts as to how much power is being used and the current draw on each of the power supplies
</aside>

As we can see from the image above, the voltage levels that the IC’s are regulating are called out explicitly in blue (1.2V and 3.3V switching supplies)

Shown below is another good example of useful notes to include when listing out power architecture

![image.png](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image%205.png)

This image shows both USB-C power transfer circuitry as well as architecture to regulate voltage. Pay attention to how the notes in blue and red **call out exactly what the circuit does and what voltage level it is operating at or regulating.**

<aside>
💡

**Control architecture:**

- Another common way of organizing a schematic is having differente sections dedicated to different methods of control.
- Examples of this include having anything that is on a shared I2C line or anything that exists as its own architecture (such as a microcontroller and associated passive components) in their own sections
</aside>

![image.png](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image%206.png)

As we can see from this image, the power supply LDO IC, MCU, and header pins are all placed close to one another and have their nets labeled. This helps us to identify which pins go where.

## **Reference Designators**

Another important thing to consider when designing a schematic is having clean and consistent labeling for the various components and ICs. This includes:

- Using proper reference designators for all components. Here are some of the most common reference designators that you might encounter in Generate, along with other information that should be visible:
    - **R:** Resistor (resistance value)
    - **C:** Capacitor (capacitance value and voltage rating)
    - **L:** Inductor/ferrite bead (inductance value and voltage rating)
    - **U/IC:** Integrated Circuit (IC), U is more common, but IC is still acceptable (part number and manufacturer)
    - **Q:** Transistor (part number)
    - **J:** Terminal/connector (part number)
    - **B:** Battery (part number and voltage rating)
    - **D:** Diode (part number)
    - **S:** Switch (part number)
    - **TP:** Test point
- Making sure that reference designators are in visible locations, and are not covered by other text or symbols
- **Ground and power lines should be indicated with power flags**
    - Ground flags should always point down
    - Power flags should always point up

![image.png](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image%207.png)

## **Other Important Considerations**

The following tips are important considerations to take into account when designing schematics, but are not large enough to warrant their own sections (but are however, still crucial to follow when designing a schematic)

- **Ensure that every net has a meaningful name. Also, keep net names reasonably short and only use uppercase letters**
    - A net is the connection between the pins of two or more devices
    - When doing layout, the software will use the nets from the schematic to determine which pins on which devices will be allowed to connect to each other
        - If pins that are supposed to be connected are labeled with different net names, the layout software will not allow you to connect the pins together (technically you can manually override this, but it’ll still throw an error when checking the layout

![This image shows a schematic where every net is named, meaning that connections will be made between the pins with the same nets](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image%208.png)

This image shows a schematic where every net is named, meaning that connections will be made between the pins with the same nets

- **Arrange pins according to function: It’s ok for the schematic symbol for a component not to match exactly with the footprint of the part if it means that the schematic will be neater or easier to understand**
- **Direct connections should be used when reasonable (ie when drawing lines directly from pin-to-pin won’t result in the schematic being harder to understand). Otherwise, use net names to keep the schematic neat and easy to understand.**
- **If you are using any chips that utilize I2C for communication with a main microcontroller, be sure to call out the specific I2C address that the device uses**

![image.png](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image%209.png)

## **Example Schematics**

![image.png](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image%2010.png)

![image.png](Schematic%20Best%20Practices%20150f18dd5a94803d8723fd92ffd4b363/image%2011.png)