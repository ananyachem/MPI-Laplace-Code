# Laplace Equation in Parallel

This code was written in Python using the MPI library, to parallelise the Laplace equation to simulate heating a metal plate. The process was divided ampong 4 PE's (Parallel Environments) to heat up a plate of 1000 x 1000 units. 

## Image of the Output:
![plate](https://github.com/user-attachments/assets/dfd7b41d-f276-4cf5-a76e-ea3a3186181c)

## Differences in Run-Time:

### Serial
<img width="1295" alt="run-time-serial" src="https://github.com/user-attachments/assets/5eac9bd3-cad0-4b0c-88d3-8b29d1c6274c" />

This code took around 2 hours to converge. Now let's compare it with the parallel output.

### Parallel
<img width="1296" alt="run-time-parallel" src="https://github.com/user-attachments/assets/fa4d0f0a-cd8b-4baa-86b8-973cbfeb8d1f" />

If you see this output, the code converged in around 30 minutes. This shows that the parallel code ran 4 times faster than the serial code, which can essentially end up saving computation cost and power. 
