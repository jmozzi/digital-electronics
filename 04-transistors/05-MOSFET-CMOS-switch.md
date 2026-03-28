I've learnt about N-type and P-type material in [[01-conductors-insulators]], now we use that to build transistors:
# MOSFET switch
- `metal-oxide-semiconductor field-effect transistor`
- there are several types of MOSFET that use different voltage levels and polarities
- basic material: doped silicon (see [[01-conductors-insulators]]
- main conduction path through a MOSFET is the `channel`, which is connected between the `source` and the `drain` (output) terminals
- the `gate` (input) is made from the opposite type of semiconductor and controls the conductivity through the channel
# CMOS switch (FinFet)
> Modern processors (Intel, AMD, Apple, etc.) now use **FinFETs** or **GAAFETs**, which are still _MOSFETs_ — just with 3D geometries for better electrostatic control

- `complementary metal-oxide semiconductor`
- how NMOS and PMOS are combined to build logic gates

In CMOS:
- Each logic gate uses **both** `NMOS` and `PMOS` transistors.
> `PMOS transistors` pull the output **high** (to Vdd) when the logic requires it.
> `NMOS transistors` pull the output **low** (to ground) when required.
- This arrangement drastically reduces power consumption because in steady states (logic 1 or 0), **no DC current flows** through the gate (only a small leakage current).

see 06-logic-gates