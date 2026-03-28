video: Capacitors are terrible at remembering data
https://www.youtube.com/watch?v=7WnbIeMgWYA
https://www.youtube.com/watch?v=7J7X7aZvMXQ&t=535s

DRAM = working memory = main memory
cause CPU only works with instructions once they're loaded into RAM (from SSDs)
# Intro
DRAM:
- 2D arrays
- temporarily stores 1 bit per memory cell (capacitor)
- composed of billions of tiny capacitor memory cells
- gigabytes of working memory
- temporary storage
- read/write speed ca 17 nanoseconds, which is 3000 times faster than SSD speeds
- like supersonic jet vs a tortoise
- DRAM stick with 8 chips holds 16 gigabytes of data
> needs power to continuously store and refresh the data held in capacitors

SSD:
- 3D massive arrays
- composed of a trillion memory cells
- SSD sticks smaller than DRAM, but can hold so much more data (terabytes)
- terabytes of storage
- read/write speed ca 50 microseconds
> permanent storage

Prefetching
- moving data from SSD to DRAM before its needed
# How CPU moves data from SSD to DRAM
- stick of memory is also called `Dual Inline Memory Module` or `DIMM`
- on my CRUCIAL DRAM stick there are 8 x DRAM chips
- motherboards often have 4 x DRAM slots
- when plugged in, the DRAM is directly connected to the CPU via 2 x memory channels that run through the mother board
- inside the CPU is the DRAM interface, a memory controller which manages and communicates with DRAM
- for DDR5, each memory channel is divided into 2 parts, `Channel A`, and `Channel B`
![Pasted image 20251105213220](../images/Pasted%20image%2020251105213220.png)
- these memory channels independently transfer 32 bits at a time using 32 data wires
- there are 21 additional wires, each memory channel carries and address specifying where to read or write data and
- using 7 control signals wires, to relay commands
- 
# how DRAM memory cells are organised - 1T1C cell
`1T1C` means 1 transistor + 1 capacitor per bit

![Pasted image 20251107103330](../images/Pasted%20image%2020251107103330.png)

has 2 parts:
- capacitor
	- stores *one bit of data* in form of electrical charge
	- shaped like deep trench
	- dug into silicon, composed of 2 conductive surfaces, separated by a dielectric insulator which stops flow of electrons, but allows electric fields to pass through

![Pasted image 20251107103539](../images/Pasted%20image%2020251107103539.png)

- transistor
	- to access and read or write data
	- the wordline wire (rows)
		- connects to the gate of the transistor
	- the bitline wire (columns)
		- connects to the other side of the transistor's channel
	- applying voltage to the wordline 
		- turns on the transistor, and it connects the capacitor to the bitline
		- allowing us to access and charge up the capacitor to write a `1`
		- or discharge the capacitor to write a `0`
		- and we can `read` the capacitor by measuring the amount of charge
	- over time, electrons leak across the channel cause it's so small, and capacitor needs to be refreshed to recharge the leaked electrons

![Pasted image 20251107103723](../images/Pasted%20image%2020251107103723.png)

So, the wordline turns the transistor on
and the transistor allows the bitline to charge the capacitor
![Pasted image 20251107104309](../images/Pasted%20image%2020251107104309.png)

- when wordline is one, all capacitors in that row are connected to respective bitlines
- activating all memory cells in that row

![Pasted image 20251107104441](../images/Pasted%20image%2020251107104441.png)

The Row Decoder and Column Multiplexer
- is responsible for the `column selection`
- from a 31-bit address, 
	- the first 5 bits are to select the bank
	- next 16 bits are sent to row decoder 
		- to select just that one single wordline row (and turning on all transistors in that row and connecting all capacitors in that row to their bitlines)
	- remaining 10 bits of address go to the column multiplexer
		- connects a specific group of 8 bitlines depending on that 10-bit address
		- to the 8 input and output wires at the bottom. 

Row Decoder:

![Pasted image 20251107104828](../images/Pasted%20image%2020251107104828.png)

Column Multiplexer:

![Pasted image 20251107105155](../images/Pasted%20image%2020251107105155.png)

> now we can access any 8 bit active 1T1C cells in the big array
# How data is written/read from memory cells
- for this we need to add 2 elements to our layout:
	- sense amplifier at the bottom of each bitline
	- and read/write driver outside of the column multiplexer
## reading from memory cells
So, if we read from a group of memory cells, then this happens:
- the read command and 31-bit address are sent from CPU to DRAM
- the first 5 bits select specific bank
- then turn off all wordlines in that bank, thereby isolating all capacitors
- then precharge all bitlines to 0.5 volts
- next the 16-bit row address turns on a row and all capactors in that row are on and connected to their bitlines
- if an individual capacitor holds a `1` and is charged to `1 volt`, then some charge flows from that capacitor onto the 0.5 volt bitlines and the voltage on the bitline increases
- the sense amplifier detects this slight change of voltage on the bitline, amplifies tha change and pushes the voltage on the bitline all the way up to 1 volt
- but if `0` is stored in the capacitor, charge flows from the bitline into the capactor, and the 0.5 volt bitline decreases in voltage
- the sense amplifier detects this slight change of voltage on the bitline, amplifies it and drives the bitline voltage down to `0` volt or ground.
- now all bitlines are driven to `1V` or `0V` corresponding to the stored charge in the capacitors of the activated row
	- and this row is considered open
![Pasted image 20251107114612](../images/Pasted%20image%2020251107114612.png)

- next the `column select multiplexer` uses the 10-bit column address to connect the corresponding 8 bitlines to the read driver 
![Pasted image 20251107114814](../images/Pasted%20image%2020251107114814.png)

- which then sends these 8 values and voltages over the 8 data wires to the CPU
![Pasted image 20251107114914](../images/Pasted%20image%2020251107114914.png)

## writing to memory cells


# Optimisation
- burst buffer
- folded DRAM layouts
- optimisations differ in different devices (or GPU DRAM called VRAM)
- DDR5 (different generations of DRAM)
- 
# How DRAM fits into the CPU pipeline
- Takes the _virtual address_ (`0x7FFF_FF00`),
    
- Checks the **TLB** for a cached mapping,
    
- If not found, walks the **page tables** (in RAM),
    
- Checks protection bits,
    
- Produces a **physical address** (e.g. `0x0023_FF00`),
    
- Sends that to the **memory controller**, which then activates the correct **DRAM row, bank, and column**.