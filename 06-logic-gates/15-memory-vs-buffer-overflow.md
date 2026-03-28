# memory overflow vs buffer overflow
## Integer overflow (arithmetic issue)
ADDERs operate on fixed-width binary values (e.g. 16-bit integers), not memory layout.
- if a number is too big to fit in the data type (16-bit signed integer)
- that could trigger an unhandled software exception and system crash
- this is NOT about memory corruption, but wrong arithmetic assumptions

## Buffer overflow (memory corruption)
A **buffer overflow is a logical/software-level failure**, not a transistor-level mechanism.
- it is a software bug that results in unintended memory writes
- program allocates a fixed-size buffer (64 bytes for input)
- user provides more than that, cause code doesn't check (missing bounds checks)
- extra bytes overflow into adjacent memory which could contain
	- return addresses
	- function pointers
	- other variables or control data  

If exploited carefully, this **can allow attackers to hijack program control flow** (e.g. run shellcode, overwrite variables, redirect to malicious code).
