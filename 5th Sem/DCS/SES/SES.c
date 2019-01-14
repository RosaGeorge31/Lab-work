#include <mpi.h>
#include <stdio.h>
#define n 3

struct message
{
	int msg;
	int recv;
	int t[n];
}
int main(int argc,char **argv)
{
	int q[n],i,src,dest,size,rank;
	char *s;
	MPI_Status status;
	
	MPI_Init(&arc,&argv);
	MPI_Comm_size(MPI_COMM_WORLD,&size);
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	struct message mesg;
	for(i=0;i<n;i++)
	{
		mesg->t[i] =0;
	}
	
	
	if(rank==0)
	{
		printf("Enter source and destination:\n");
		scanf("%d %d",&src,&dest);
		printf("Enter the message\n");
		scanf("%d",s);
	}
	if(rank==source)
	{
		mesg->t[source]+=1;
		mesg->msg = s;
		mesg->recv=dest;
		MPI_Send(&mesg,sizeof(mesg),MPI_INT,dest,20,MPI_COMM_WORLD);
	}
	if(rank==dest)
	{
		MPI_Recv(&mesg,sizeof(mesg),MPI_INT,dest,20,MPI_COMM_WORLD,&status);
	}

	MPI_Finalize();

	return 0;
}
