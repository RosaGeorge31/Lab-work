#include <omp.h>
#include <stdio.h>
void main()
{
	int n=2,i,j,k;
	int a[2][2],b[2][2],c[2][2];
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			a[i][j] = i+j;
			b[i][j] = i*j;
		}
	}


double t1 = omp_get_wtime();
#pragma omp parallel for private(k,j)
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			c[i][j] =0;
			for(k=0;k<n;k++)
			{
				c[i][j]+=a[i][k]*b[k][j];
			}
		}
	}

	double t2 = omp_get_wtime();
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			printf("%d \n",c[i][j] );
		}
		printf("\n");
	}
	printf("Time taken: %f s\n", t2-t1 );
}