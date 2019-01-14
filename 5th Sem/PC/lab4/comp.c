/**The details of an employ with employ id and employ salary is stored in a two
dimensional array. The company would like to raise the salary of all its employees
by 6%. If the increase in salary is more for reductiothan 5,000 Rs, the company would like to
put tax of 2% on the increased amount more than 5,000 Rs. Calculate the total extra
amount the company need spend by increasing the salary 6%.**/
#include <omp.h>
#include <stdio.h>
void main()
{
	int n,i,j,extrasum=0;
	printf("enter number of employees");
	scanf("%d",&n);
	int a[n][2];
	for(i=0;i<n;i++)
	{
		printf("Enter employee id\n");
		scanf("%d",&a[i][0]);

		printf("Enter employee salary\n");
		scanf("%d",&a[i][1]);
	}
	double t1= omp_get_wtime();
	#pragma omp parallel shared(a)
	{
		
		#pragma omp for reduction(+:extrasum)
		for(i=0;i<n;i++)
		{
			double val = 1.06 * (float)a[i][1];
			if(val - a[i][1] > 5000)
			{
				val = 0.80 * val;
			}
			extrasum+=val-a[i][1];
			a[i][1]=(int)val;
		}
	}
	double t2 = omp_get_wtime();
	printf("Sum = %d\n",extrasum);
	
	printf("Time taken: %f s\n", t2-t1 );
}