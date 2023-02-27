# Benchmark results

Results are generated from benchmark.py

Each module is tested 10 times on each size

## Explanations of the differences

- The first version (get_points), is the basic version.

- The second one tries to reduces the time by implementing a light modification ine the algorithme.

- The third is the same but with another implementation.

- The fourth is an optimisation of the third

## Results

Benchmark for get_points
| grid size | time |
|:---------:|:------:|
| 2 | 0.002s |
| 3 | 0.143s |

Benchmark for get_points_2
| grid size | time |
|:---------:|:------:|
| 2 | 0.002s |
| 3 | 0.139s |

Benchmark for get_points_3
| grid size | time |
|:---------:|:------:|
| 2 | 0.002s |
| 3 | 0.133s |

## Analyse

We can see that in average, the third version of the algorithm is slightly faster.

## Second run with algo 4

Benchmark for get_points_1
| grid size | time |
|:---------:|:------:|
| 3 | 0.182s |

Benchmark for get_points_2
| grid size | time |
|:---------:|:------:|
| 3 | 0.151s |

Benchmark for get_points_3
| grid size | time |
|:---------:|:------:|
| 3 | 0.135s |

Benchmark for get_points_4
| grid size | time |
|:---------:|:------:|
| 3 | 0.085s |

## Analyse

The fourth algorithm is the best.
