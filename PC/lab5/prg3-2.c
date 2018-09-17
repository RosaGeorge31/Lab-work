#include <stdio.h>
#include <omp.h>
#include <stdlib.h>
#include <time.h>
#define MAX 1000000
int main()
{
	long long arr[MAX],u=100000,l=50,i,Min=1000000;
	srand(time(NULL));
	for(i=0;i<MAX;i++)
	{
		arr[i] = (rand()%100);
	}
	double t1 = omp_get_wtime();

	for(i=0;i<MAX;i++)
	{
		if(arr[i]<Min)
			Min=arr[i];
	}
	double t2 = omp_get_wtime();
	printf("\nTime taken: %f\n",t2-t1 );
	return 0;
}