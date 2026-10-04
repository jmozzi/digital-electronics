Source:
CoreDumped https://www.youtube.com/watch?v=rM9BjciBLmg  -> conceptual info via gated latches
Microchip Tech: https://www.youtube.com/watch?v=kU2SsUUsftA&t=16s   -> more realistic 6T cells

# Summary
**SRAM (Static RAM)** does _not_ use capacitors like DRAM.

- It stores each bit using a **flip-flop circuit** (typically **6 transistors per bit**, called a 6T cell)
- This is essentially a tiny **bistable latch** (two cross-coupled inverters)
- As long as power is supplied, the circuit **holds its state indefinitely** — no refresh needed

**Key contrast:**

- DRAM -> capacitor + periodic refresh (leaks charge)
- SRAM -> transistor latch -> stable while powered, no refresh

**Trade-offs:**

- SRAM: faster, lower latency, but **larger + more expensive**
- DRAM: slower, needs refresh, but **much denser + cheaper**

That’s why SRAM is used for **CPU caches**, DRAM for **main memory**.

# Details
