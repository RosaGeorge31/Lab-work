#include <stdio.h>
#include <omp.h>
void main()
{
	int i,j,a[2][2];
	int cs[2],rs[2];
	for(i=0;i<2;i++)
	{
		for(j=0;j<2;j++)
		{
			a[i][j] = i+j;
		}
	}

	#pragma omp parallel shared(a)
	{
		#pragma omp for collapse(2)
			for(i=0;i<2;i++)
			{
				for(j=0;j<2;j++)
				{
					cs[i]+=a[i][j];
					rs[i]+=a[j][i];
				}
			}
	}

for(i=0;i<2;i++)
	
{
	printf("cs : %d\n",cs[i]);
	printf("rs : %d\n",rs[i]);
}}