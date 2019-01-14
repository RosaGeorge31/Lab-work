#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#define chunksize 5
#define N 100
void main(int argc, char const *argv[])
{
	int nthreads, tid, i, chunk;
	float a[N], b[N], c[N];
	for(i=0;i<N;i++)
		a[i] = b[i] = 1.0 * i;
	chunk = chunksize;
	#pragma omp parallel shared(a,b,c,nthreads,chunk) private(i,tid)
	{
	
		tid = omp_get_thread_num();
		if(tid==0)
		{
			nthreads = omp_get_num_threads();
			printf("Number of threads = %d\n",nthreads );
		}
		printf("Thread %d starting...\n", tid );
		#pragma omp for schedule(guided,chunk)
		for(i=0;i<N;i++)
		{
			c[i] = a[i] + b[i];
			printf("Thread %d: c[%d] = %f\n",tid,i,c[i] );
		}
	}

}