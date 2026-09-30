# benchmark_core.mojo
# Mojo kernel for high-speed statistical metric calculation

fn calculate_tokens_per_sec(total_tokens: Int, total_time_sec: Float64) -> Float64:
    if total_time_sec == 0.0:
        return 0.0
    return Float64(total_tokens) / total_time_sec

fn process_latencies(latencies_sum: Float64, count: Int) -> Float64:
    if count == 0:
        return 0.0
    return latencies_sum / Float64(count)

fn main():
    print("Mojo High-Performance Benchmarking Kernel Initialized.")