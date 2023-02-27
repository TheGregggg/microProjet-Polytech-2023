import get_points
import get_points_2
import get_points_3
import get_points_4

import time


def benchmark_module(size: int, module, n_times: int):
    times = []
    for i in range(n_times):
        start_time = time.time()
        result = module.get_points(size)
        end_time = time.time()
        times.append(end_time-start_time)
        module.already_done_node = []

    moyenne = 0
    for d_time in times:
        moyenne += d_time
    moyenne = moyenne/len(times)

    return moyenne


def run_benchmarks(list_modules, list_sizes, repeats=1):
    final_output = "\n"
    for module in list_modules:
        final_output += f"Benchmark for {module.__name__}\n"
        final_output += f"| grid size |  time  |\n|:---------:|:------:|\n"
        for size in list_sizes:
            mtime = benchmark_module(size, module, repeats)
            final_output += f"|     {size}     | {mtime:.3f}s |\n"
        final_output += "\n"

    return(final_output)


if __name__ == "__main__":
    results = run_benchmarks(
        [get_points_4, get_points_3], [4], 10)
    print(results)
