#include <stdio.h>
#include <omp.h>
void main(int argc, char const *argv[])
{
	int i,n;
	double t2,t1;
	printf("Enter the value of n\n");
	scanf("%d",&n);
	t1 = omp_get_wtime();
	#pragma omp parallel num_threads(4)
	{
		int tid = omp_get_thread_num();
		#pragma omp for nowait
		for(i=0;i<n;i++)
			printf("Thread %d: value of i: %d\n", tid,i);
		printf("\n I am Thread %d NO WAIT EFFECT\n",tid);
	}
	t2=  omp_get_wtime();
	printf("Time taken is %f\n",t2-t1 );
}