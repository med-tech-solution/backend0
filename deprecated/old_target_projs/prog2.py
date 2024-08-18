import cupy as cp
import time

# Function 1: GPU-based matrix multiplication with increasing size
def gpu_matrix_multiplication(size):
    print(f"Starting GPU matrix multiplication with size {size}x{size}")
    A = cp.random.rand(size, size)
    B = cp.random.rand(size, size)
    result = cp.matmul(A, B)
    cp.cuda.Stream.null.synchronize()  # Ensure computation is finished
    print("GPU matrix multiplication completed.")

# Function 2: GPU-based element-wise operation with increasing array size
def gpu_element_wise_operation(size):
    print(f"Starting GPU element-wise operation on array of size {size}")
    A = cp.random.rand(size)
    B = cp.random.rand(size)
    result = A * B + cp.sin(A)
    cp.cuda.Stream.null.synchronize()  # Ensure computation is finished
    print("GPU element-wise operation completed.")

# Function 3: GPU-based FFT with increasing array size
def gpu_fft(size):
    print(f"Starting GPU FFT on array of size {size}")
    A = cp.random.rand(size)
    result = cp.fft.fft(A)
    cp.cuda.Stream.null.synchronize()  # Ensure computation is finished
    print("GPU FFT completed.")

# Function 4: Infinite loop for continuous GPU computation
def infinite_gpu_computation(size):
    print(f"Starting infinite GPU computation with size {size}")
    A = cp.random.rand(size, size)
    B = cp.random.rand(size, size)
    while True:
        result = cp.matmul(A, B)
        cp.cuda.Stream.null.synchronize()  # Ensure computation is finished
        time.sleep(0.1)  # Add a small delay to simulate processing intervals

# Example usage of functions with increasing GPU load
if __name__ == "__main__":
    # GPU Matrix Multiplication
    gpu_matrix_multiplication(500)
    gpu_matrix_multiplication(1000)
    
    # GPU Element-wise Operation
    gpu_element_wise_operation(10**6)
    gpu_element_wise_operation(10**7)
    
    # GPU FFT
    gpu_fft(10**6)
    gpu_fft(10**7)
    
    # Infinite GPU computation (commented out to avoid running indefinitely)
    # Uncomment the line below to start the infinite loop
    # infinite_gpu_computation(1000)
