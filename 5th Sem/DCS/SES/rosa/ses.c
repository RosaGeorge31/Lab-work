#include<mpi.h>
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#define max(a,b)     (((a) > (b)) ? (a) : (b))

int checkcontain(int size,int receive[][size],int des)
{
    for(int i=0;i<size;i++)
    {
        if(receive[des][i]!=0){
            return 1;
        }
    }
    return 0;
}

int isless(int V_M[],int vector[],int size)
{
    int strict=0;
    int less=1;
    for(int i=0;i<size;i++)
    {
        if(V_M[i]<=vector[i])
        {
            if(V_M[i]<vector[i])
            {
                strict=1;
            }
        }
        else
        {
            less=0;
            break;
        }
    }
    if(less==1 && strict==1)
    {
        return 1;
    }
    else if(less==1)
    {
        return 2;
    }
    int g=0,gstrict=1;
    for(int i=0;i<size;i++)
    {
        if(V_M[i]>=vector[i])
        {
            if(V_M[i]>vector[i])
            {
                gstrict=1;
            }
        }
        else
        {
            g=0;
            break;
        }
    }
    if(g==1)
    {
        return 3;
    }
    else
    {
        return 4;
    }
}

void updateBuffer(int size,int receive[size][size],int local[size+1][size],int dest){
    for(int i=0;i<size;i++)
        local[dest][i]=0;
    for(int i=0;i<size;i++)
    {
        if(isless(local[i],receive[i],size)==3){
            for(int j=0;j<size;j++){
                local[i][j]=receive[i][j];             //copying updated value of local
            }
        }
    }
    for(int i=0;i<size;i++){
        local[size][i]=max(local[size][i],receive[size][i]);
    }
}
void main(int argc,char **argv){
    
    int rank,size,i,src,dest;
    i=3;
    int receive[5][4]={0},local[5][4]={0};
    MPI_Status status;
    int buffer[4][4][4];
    for(int i=0;i<4;i++)
        buffer[i][0][0]=0;

    MPI_Init(&argc,&argv);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    while(i)
    {
        i--;
        src=-1;dest=-1;
        if(rank==0)
        {
            printf("Enter the source and destination\n");
            scanf("%d%d",&src,&dest);
        }
        
        MPI_Bcast(&src,1,MPI_INT,0,MPI_COMM_WORLD);
        MPI_Bcast(&dest,1,MPI_INT,0,MPI_COMM_WORLD);
        MPI_Barrier(MPI_COMM_WORLD);

        if(rank==src)
        {
            local[size][src]+=1;
            MPI_Send(local,(size+1)*size,MPI_INT,dest,0,MPI_COMM_WORLD);

            for(int j=0;j<size;j++)
            {
                local[dest][j]=local[size][j]; 
            }
           
        }
        if(rank==dest)
        {
            MPI_Recv(receive,(size+1)*size,MPI_INT,src,0,MPI_COMM_WORLD,&status);
            if(checkcontain(size,receive,dest)==0)
            {
                local[size][dest]+=1;
                updateBuffer(size,receive,local,dest);
                printf("Received messege from %d to %d vector clock:",src,dest);
                
                for(int i=0;i<size;i++)
                {
                    printf("%d ",local[size][i]);
                }
                printf("\n");                
            }
            else
            {
                if(isless(receive[dest],local[size],size)==1 ||isless(receive[dest],local[size],size)==2)
                {
                    local[size][dest]+=1;
                    updateBuffer(size,receive,local,dest);
                    printf("Received messege from %d to %d vector clock:",src,dest);
                    for(int i=0;i<size;i++)
                    {
                        printf("%d ",local[size][i]);
                    }
                    printf("\n");
                }
                else{
                    //to buffer
                    printf("Buffered since previous message in buffer\n");
                    if(buffer[dest][0][0]==-1)
                    {
                        for(int i=0;i<size;i++)
                        {
                            for(int j=0;j<size;j++)
                            {
                                buffer[dest][i][j]=receive[i][j];
                            }
                        }
                    }
                }
            }
            
            for(int i=0;i<size;i++)
            {
                int flag=0;
                for(int i=0;i<size;i++)
                {
                    if(buffer[i][0][0]!=-1 && isless(buffer[i][i],local[size],size)==1)
                    {
                        
                        flag=1;
                        local[size][dest]+=1;
                        updateBuffer(size,buffer[i],local,dest);
                        buffer[i][0][0]=-1;
                        printf("received messege from %d to %d vector clock:",src,dest);
                        for(int i=0;i<size;i++)
                            printf("%d ",local[size][i]);
                        printf("\n");
                    }
                }
                if(flag==0)
                break;
            }
        }
    }
    MPI_Finalize();
}