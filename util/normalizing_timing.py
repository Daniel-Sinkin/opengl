import time

import glm
import numpy as np

# Number of vectors to generate
num_vectors = 1_000_000

# Generate 100,000 glm::vec3 vectors with vx and vy as -1 or 1, and vz as 0
vectors = [
    glm.vec3(np.random.choice([-1, 1]), np.random.choice([-1, 1]), 0)
    for _ in range(num_vectors)
]

# Global sqrt(2) value
sqrt2 = glm.sqrt(2)


# Function to normalize vectors by dividing by dynamically computed sqrt(2)
def normalize_div_sqrt2_dynamic(vectors):
    return [v / glm.sqrt(2) for v in vectors]


# Function to normalize vectors by dividing by precomputed sqrt(2)
def normalize_div_sqrt2_global(vectors):
    return [v / sqrt2 for v in vectors]


# Function to normalize vectors using glm.normalize
def normalize_glm(vectors):
    return [glm.normalize(v) for v in vectors]


# Measure time for normalizing by dynamically computing sqrt(2)
start_time = time.perf_counter()
normalized_div_sqrt2_dynamic = normalize_div_sqrt2_dynamic(vectors)
end_time = time.perf_counter()
time_div_sqrt2_dynamic = end_time - start_time

# Measure time for normalizing by using precomputed sqrt(2)
start_time = time.perf_counter()
normalized_div_sqrt2_global = normalize_div_sqrt2_global(vectors)
end_time = time.perf_counter()
time_div_sqrt2_global = end_time - start_time

# Measure time for normalizing using glm.normalize
start_time = time.perf_counter()
normalized_glm = normalize_glm(vectors)
end_time = time.perf_counter()
time_glm = end_time - start_time

# Print the results
print(
    f"Time taken to normalize by dynamically computing sqrt(2): {time_div_sqrt2_dynamic:.6f} seconds"
)
print(
    f"Time taken to normalize by using precomputed sqrt(2): {time_div_sqrt2_global:.6f} seconds"
)
print(f"Time taken to normalize using glm.normalize: {time_glm:.6f} seconds")
