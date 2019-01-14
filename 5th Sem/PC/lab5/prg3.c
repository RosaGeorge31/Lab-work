#include <stdio.h>
#include <omp.h>
#include <stdlib.h>
#include <time.h>
#define MAX 1000000
int main()
{
	int arr[MAX],u=1000000,l=50,i,Min=1000000;
	srand(time(NULL));
	for(i=0;i<MAX;i++)
	{
		arr[i] = (rand()%(u-l+1))+l;
	}
	double t1 = omp_get_wtime();
	#pragma omp parallel for schedule(static) reduction(min:Min)
	for(i=0;i<MAX;i++)
	{
		if(arr[i]<Min)
			Min=arr[i];
	}
	double t2 = omp_get_wtime();
	printf("\nMin: %d\nTime taken: %f\n",Min,t2-t1 );
	return 0;
}