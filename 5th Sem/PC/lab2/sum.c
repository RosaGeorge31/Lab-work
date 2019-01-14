#include <stdio.h>
#include <omp.h>

void main()
{
	int i,n,sum = 0;
	printf("Enter the value of n\n");
	scanf("%d",&n);
	int a[n];
	for(i=0;i<n;i++)
		scanf("%d",&a[i]);
	#pragma omp parallel
	{
		int id = omp_get_thread_num();
		#pragma omp for lastprivate(i)
		for(i=0;i<n;i++)
		{
			printf("Thread %d: Value of i :%d\n",id,i );
			sum = sum +a[i];
			
		}
	}
	printf("Sum is %d\n",sum);
}