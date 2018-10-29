#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
int main()
{
	double arr[500];
    double min_val=111110.0;
    int i;

    for( i=0; i<500; i++)
        arr[i] = random()%(100000-500+1)+50;

    double t1 = omp_get_wtime();
    for( i=0;i<500; i++)
    {
        
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

