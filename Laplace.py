import time
from mpi4py import MPI 
import numpy as np
import math
import matplotlib.pyplot as plt

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

ROWS, COLUMNS = 1000, 1000
MAX_TEMP_ERROR = 0.01

pe_rows = ROWS//size  #no. of rows each PE is assigned

temperature      = np.empty((pe_rows+2, COLUMNS+2))
temperature_last = np.empty((pe_rows+2, COLUMNS+2))

start_time = time.time()

def initialize_temperature(temp, rank):
    temp[:,:] = 0

    #we need to split this between the PE's, saving the last PE for the bottom boundary

    #right side boundary condition
    for i in range(1, pe_rows+2): 
        global_i = i + rank * pe_rows 
        temp[i, COLUMNS+1] = 100 * math.sin(((3.14159/2)/ROWS) * global_i)  

    #bottom boundary condition
    if rank == size - 1:  
        for i in range(COLUMNS+2):
            temp[pe_rows+1, i] = 100 * math.sin(((3.14159/2)/COLUMNS) * i)

initialize_temperature(temperature_last, rank)

max_iterations = None
if rank == 0:
    max_iterations = int(input("Enter iterations: "))

max_iterations = comm.bcast(max_iterations, root=0)

dt = 100
iteration = 1

while (dt > MAX_TEMP_ERROR) and (iteration < max_iterations):  

    #send and receive boundary rows to and from neighboring processes
    if rank > 0:
        comm.Send(temperature_last[1, :], dest = rank - 1)
        comm.Recv(temperature_last[0, :], source = rank - 1)
    if rank < size - 1:
        comm.Send(temperature_last[pe_rows, :], dest = rank + 1) 
        comm.Recv(temperature_last[pe_rows+1, :], source = rank + 1)    
    comm.Barrier() 

    for i in range(1, pe_rows+1):
        for j in range(1, COLUMNS+1):
            temperature[i, j] = 0.25*( 
                temperature_last[i+1,j] + 
                temperature_last[i-1,j] +
                temperature_last[i,j+1] + 
                temperature_last[i,j-1]   
            )

    #since the send and recieve functions work with individual PE's, we also calculate the corresponding 'dt' individually
    dt_individual = 0
    for i in range(1, pe_rows+1): 
        for j in range(1, COLUMNS+1):
            dt_individual = max(dt_individual, abs(temperature[i,j] - temperature_last[i,j]))
            temperature_last[i, j] = temperature [i, j]

    dt = comm.allreduce(dt_individual, op=MPI.MAX)  #allreduce- collecting the individual data and making it global

    if rank == 0:
        print(f"Iteration {iteration}, dt = {dt}", flush=True)
    iteration += 1

# gathering for the full grid
grid_individual = temperature_last[1:pe_rows+1, 1:COLUMNS+1].flatten()  #first collecting for the individual grids
if rank == 0:
    grid_full = np.zeros((ROWS, COLUMNS))
else:
    grid_full = None
comm.Gather(grid_individual, grid_full, root=0)

if rank == 0:  
    grid_full = np.reshape(grid_full, (ROWS, COLUMNS))
    plt.imshow(grid_full)
    plt.colorbar()
    plt.show()
    plt.savefig("plate.png")

end_time = time.time()  
if rank == 0:
    print(f"Execution time: {end_time - start_time} seconds")