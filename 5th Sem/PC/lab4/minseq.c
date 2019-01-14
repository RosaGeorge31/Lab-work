#include <stdio.h>
#include <sys/time.h>
#include <omp.h>
#include <stdlib.h>
int main()
{
	double arr[10];
    omp_set_num_threads(4);
    double min_val=111110.0;
    int i;
    for( i=0; i<10; i++)
        arr[i] = 2.0 + i;
    double t1 = omp_get_wtime();
    #pragma omp parallel for reduction(min : min_val)
    for( i=0;i<10; i++)
    {
        //printf("thread id = %d and i = %d\n", omp_get_thread_num(), i);
        if(arr[i] < min_val)
        {
            min_val = arr[i];  
        }
    }
  	double t2 = omp_get_wtime();
    printf("\nmin_val = %f\n", min_val);
    printf("Time taken : %f\n", t2-t1);
    return 0;

}

