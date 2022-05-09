#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>
#include <pthread.h>

// 将进程锁定在某个固定CPU上
void lockCpu(int cpuId)
{
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(cpuId, &mask);
    if (sched_setaffinity(0, sizeof(mask), &mask) < 0)
    {
        fprintf(stderr, "set thread affinity failed\n");
    }
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        fprintf(stderr, "Usage: ./tlb pages trials");
        exit(EXIT_FAILURE);
    }

    // 将进程锁定在CPU0上
    lockCpu(0);

    // 申请页的数量
    int page_numebr = atoi(argv[1]);
    int trials = atoi(argv[2]);

    if (page_numebr <= 0)
    {
        fprintf(stderr, "Invaild Input");
        exit(EXIT_FAILURE);
    }

    int jump = sysconf(_SC_PAGE_SIZE) / sizeof(int);

    struct timespec start, end;
    struct timespec start_hit, end_hit;

    int sum_miss = 0;
    int sum_hit = 0;

    int cnt = 0;

    while (trials--)
    {
        for (int step = 0; step < page_numebr * jump; step += jump)
        {
            cnt++;
            int *array = calloc(page_numebr, getpagesize());

            // 计算TLB miss的时间
            clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
            array[step] += 0;
            clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
            sum_miss += end.tv_nsec - start.tv_nsec;

            // 计算TLB hit的时间
            clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start_hit);
            array[step + 1] += 0;
            clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end_hit);
            sum_hit += end_hit.tv_nsec - start_hit.tv_nsec;
            free(array);
        }
    }
    int miss_average = sum_miss / cnt;
    int hit_average = sum_hit / cnt;

    printf("Time per access(TLS miss): %d\n", miss_average);
    printf("Time per access(TLS hit): %d\n", hit_average);

    return 0;
}