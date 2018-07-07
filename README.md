# Value Range Analysis

Jen-tse Huang, Haotang Liu

This is the course project of Compiler Design in 17-18 spring semester. Given the range of arguments, the value range analysing system should calculate the range of the return value. The programs are provided in .ssa form. Our group works together on GitHub.

# Requirement

- Python 3.7
- re module

# Usage

Use the following command to run the range analysis. main.py is in the src file.

	python3 main.py
	
Then follow the instrucion printed on the screen. 

\* it may takes some time to process the range analysis. Please wait until the answer appears on the screen. 

# Method

We could split the analysing process into 3 steps. 

### Step1: Basic Block Dividing and Function Inline
Jen-tse Huang

- Define function and basic\_block class. 
- Save the source code in functions. 
Each funcion has a basic\_block list that saves all the basic blocks in this function.
- Inline the callees to the "foo" function.

### Step2: Basic Block Parsing
Haotang Liu

- Initialize the symbol table.
- Design the data flow analysis algorithm, including dataflow equations and transfer functions.
- Implement forward analysis and simplified 'widen-ft-narrow' method.

### Step3: Interactive Interface
Jen-tse Huang and Haotang Liu

- Determine which argument needs range input and output.



# Testing Output

- If the metric is EXACT MATCH, correctness: 7/10

- Our system output range all cover the correct range.  

1. finish analysing, the answer is: 
return range = [ 100 , 100 ] \(Correct\)

2. finish analysing, the answer is: 
return range = [ 200 , 300 ] \(Correct\)

3. finish analysing, the answer is: 
return range = [ 20 , 50 ] \(Correct\)

4. finish analysing, the answer is: 
return range = [ 0 , inf ] \(Correct\)

5. finish analysing, the answer is: 
return range = [ 0 , 210 ] \(Half-Correct\)

6. finish analysing, the answer is: 
return range = [ -9 , 10 ] \(Correct\)

7. finish analysing, the answer is: 
return range = [ 16 , 30 ] \(Correct\)

8. finish analysing, the answer is: 
return range = [ -3.2192304691619382 , 5.9423080203095955 ] \(Correct\)

9. finish analysing, the answer is: 
return range = [ -10 , inf ] \(Incorrect\)

10. finish analysing, the answer is: 
return range = [ -49 , inf ] \(Incorrect\)

# Feature
The first case is identical to the case in the slides. 
By using our method, the range in the process are all the same.

# Reference
Rodrigues, Raphael Ernani, Victor Hugo Sperle Campos, and Fernando Magno Quintao Pereira. "A fast and low-overhead technique to secure programs against integer overflows." Code Generation and Optimization (CGO), 2013 IEEE/ACM International Symposium on. IEEE, 2013.
