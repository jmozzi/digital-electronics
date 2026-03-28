# full adder - overflow signal
- can deal with 2 bits being added
- and the carry from a previous addition
- basically has 2x half adders in it

![Pasted image 20251103110402](../images/Pasted%20image%2020251103110402.png)

![Pasted image 20251103110421](../images/Pasted%20image%2020251103110421.png)

- the `carry output` of each `FULL ADDER` feeds directly into the `carry INPUT` of the next `FULL ADDER`

![Pasted image 20251103110513](../images/Pasted%20image%2020251103110513.png)
## 8-bit ADDER
> **to add n digits, n full adders are needed**
- Example for adding 2x 8-bit numbers, we need 8 full adders:

![Pasted image 20251103110619](../images/Pasted%20image%2020251103110619.png)

- 8-bit adder has an `overflow` signal and two 8-bit numbers as input
	- this is basically a `carry` output of the last `full adder` 
	- and the output is another 8-bit number

![Pasted image 20251103110634](../images/Pasted%20image%2020251103110634.png)

- the `overflow` is essential because it tells us whether storage capacity is adequate or not, aka whether 8 bits are enough to store the output or whether we need another byte/8bit to adequately represent the output
- monitoring the `overflow` means we can recognise the need to add an extra byte

![Pasted image 20251103110651](../images/Pasted%20image%2020251103110651.png)

- if we don't do that, we get the wrong output namely just `00000000` which can lead to undefined behaviour with potentially serious results
*Example: Rocket failure in 1996, Ariane 5 flight 501*
- cause: integer overflow in `IRS` (inertial reference system) of the rocket
	- The software attempted to convert a **64-bit floating point number (representing horizontal velocity)** to a **16-bit signed integer** (Whole number that **can be negative or positive**).
	- However, **the value was too large** for a 16-bit integer (max: 32,767), resulting in an **overflow**.
	- This triggered a **software exception** and failure not handled safely
# 8-bit Incrementer
- a circuit that increments an input value by `1`
- use full adder
- set the second input to always be `1`