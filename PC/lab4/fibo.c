#include <stdio.h>
#include <omp.h>
int fibo(int n);
void main()
{
	int n,fib;
	double t1,t2;
	printf("Enter the value of n:\n");
	scanf("%d",&n);
	t1 = omp_get_wtime();
	#pragma omp parallel shared(n)
	{
		#pragma omp single
		{
			fib = fibo(n);
		}
	}
	t2 = omp_get_wtime();
	printf("Fib is %d\n",fib);
	printf("Time taken is %f s\n", t2-t1);
}
int fibo(int n)
{
	int a,b;
	if(n<2)
		return n;
	else{
		#pragma omp task shared(a)
		{
			printf("Task in a\n");
			printf("Task Created by Thread %d  for n: %d\n",omp_get_thread_num(),n-1);
			a=fibo(n-1);
			printf("n = %d Task Executed by Thread %d \ta=%d\n",n,omp_get_thread_num(),a);
		}
		#pragma omp task shared(b)
		{
			printf("Task in b\n");
			printf("Task Created by Thread %d  for n: %d\n",omp_get_thread_num(),n-2);
			b = fibo(n-2);
			printf("n = %d Task Executed by Thread %d b=%d\n",n,omp_get_thread_num(),b);	
		}
	#pragma omp taskwait 
		return a+b;
	}
}