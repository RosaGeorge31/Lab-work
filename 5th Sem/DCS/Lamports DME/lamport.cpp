#include <mpi.h>
#include <stdio.h>
#include <omp.h>
#include <stdlib.h>
#include <algorithm>
#include <iostream>
#include <vector>
#include <cstdlib>
#include <limits.h>  

using namespace std;

#define SET 1
#define MAX(a,b) a>b?a:b
#define REL 0
#define REQ 2
#define ACK 1

void receive(vector< pair<int,int> > &q ,int &l_clock, int &recvLock, int &sendLock, int world_rank)
{
    MPI_Status status;
    int counter=0;
    
    while(true)
    {
        int msg[2];
        
        MPI_Recv(msg, 8, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
        while(sendLock);
        //cout<<"Clock val: "<<world_rank<<"="<<l_clock<<endl;
        #pragma omp critical
        {
            
            l_clock=((msg[1]>l_clock)?msg[1]:l_clock);
            l_clock+=1;
        }
        cout<<"Process: "<<world_rank<<" received message from "<<status.MPI_SOURCE<<" ("<<msg[0]<<","<<msg[1]<<") "<<endl;;

        if(msg[0]==0)
        {
        	printf("prev value was : %d\n", q[status.MPI_SOURCE].first);
            //Msg is of type release
            #pragma omp critical
            {
                q[status.MPI_SOURCE].first=0;
                q[status.MPI_SOURCE].second=msg[1];
            }
        }
        else if(msg[0]==1)
        {
            //Msg is of type ack
            counter+=1;

            #pragma omp critical
            {
                if(q[status.MPI_SOURCE].first!=2)
                {
                    q[status.MPI_SOURCE].first=1;
                    q[status.MPI_SOURCE].second=msg[1];
                    //cout<<"Adding to queue"<<q[status.MPI_SOURCE].first<<" "<<q[status.MPI_SOURCE].second<<endl;
                }
            }
            if(counter==2)
            { 
                recvLock=0;
                counter=0;
            }
        }
        else
        {	
        	printf("hey rosa :  %d\n", status.MPI_SOURCE);
            //Msg is of type request
            #pragma omp critical
            {

                q[status.MPI_SOURCE].first=2;
                q[status.MPI_SOURCE].second=msg[1];
            }
            msg[0]=1;
            msg[1]=l_clock;
            cout<<"Process: "<<world_rank<<" sending ACK to "<<status.MPI_SOURCE<<endl;
            MPI_Send(msg,8,MPI_INT, status.MPI_SOURCE, 0, MPI_COMM_WORLD); // sending reply back
        }
    }
}

int minQ(vector< pair<int,int> > q)
{
    int min=10000000;
    int min_i;
    for(int i=0;i<q.size();i++)
    {
        if(q[i].first==1)
        {
            if(q[i].second<min)
            {
                min_i=i;
                min=q[i].second;
            }
        }
    }
    return min_i;
}

void enter_cs(vector< pair<int,int> > &q ,int &l_clock,int &recvLock, int &sendLock,int world_rank)
{

    l_clock+=1;
    int msg[2];
    //Take lock
    sendLock=1;
    for(int i=0;i<3;i++)
    {
        if(i==world_rank)continue;
        //Send request to all processes
        msg[0]=2;
        msg[1]=l_clock;
        cout<<"Process "<<world_rank<<" sending  REQ to "<<i<<" with clock val: "<<l_clock<<endl;
        MPI_Send(msg,8,MPI_INT, i, 0, MPI_COMM_WORLD);
    }
    //Release lock
    sendLock=0;

    q[world_rank].first=2;
    q[world_rank].second=l_clock;
    while(recvLock);
    #pragma omp critical
    {
        recvLock=1;
    }

    for(long int i=0;i<1000000000;i++);
    
    //Query the queue
    while(q[minQ(q)].second<q[world_rank].second);
    cout<<"Contents of queue of process: "<<world_rank<<endl;
    for(int i=0;i<q.size();i++)
    {
      cout<<q[i].first<<" "<<q[i].second<<endl;
    }
    return;
}

void exit_cs(vector< pair<int,int> > &q ,int &l_clock, int world_rank)
{
    #pragma omp atomic
        l_clock+=1;
    int msg[2];
    for(int i=0;i<3;i++)
    {
        if(i==world_rank)continue;
        //Send release to all processes
        msg[0]=0;
        msg[1]=l_clock;
        MPI_Send(&msg,8,MPI_INT, i, 0, MPI_COMM_WORLD);
    }
    q[world_rank].first=0;
    q[world_rank].second=l_clock;
}

int main(int argc, char** argv) {
    MPI_Init(NULL, NULL);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    MPI_Status status;

    //Message codes: 0:REL. 1:ACK. 2:REQ
    int l_clock=world_rank;
    vector< pair<int,int> > q(world_size);
    for(int i=0;i<q.size();i++)
    {
        q[i].first=0;
        q[i].second=0;
    }

    if (world_rank == 0)
    {
        int recvLock=1;
        int sendLock=0;
        #pragma omp parallel num_threads(2)
        {
            int tid=omp_get_thread_num();
            if(tid==0)
            {
                //Receiver thread
                receive(q, l_clock, recvLock,sendLock,world_rank);
            }
            else
            {
                //Sender thread
                cout<<"Process: "<<world_rank<<" requesting access to CS clock val:"<<l_clock<<endl;
                enter_cs(q, l_clock, recvLock,sendLock,world_rank);
                cout<<"Process: "<<world_rank<<" entered CS "<<endl;
                exit_cs(q, l_clock, world_rank);
                cout<<"Process: "<<world_rank<<" exits CS"<<endl;
            }
        }
    }

    if (world_rank == 1)
    {
        int recvLock=1;
        int sendLock=0;
        #pragma omp parallel num_threads(2)
        {
            int tid=omp_get_thread_num();
            if(tid==0)
            {
                //Receiver thread
                receive(q, l_clock, recvLock,sendLock,world_rank);
            }
            else
            {
                //Sender thread
                cout<<"Process: "<<world_rank<<" requesting access to CS clock val:"<<l_clock<<endl;
                enter_cs(q, l_clock, recvLock,sendLock,world_rank);
                cout<<"Process: "<<world_rank<<" entered CS "<<endl;
                exit_cs(q, l_clock, world_rank);
                cout<<"Process: "<<world_rank<<" exits CS"<<endl;
            }
        }
    }

    if (world_rank == 2)
    {
        int recvLock=1;
        int sendLock=0;
        #pragma omp parallel num_threads(1)
        {
            int tid=omp_get_thread_num();
            if(tid==0)
            {
                //Receiver thread
                receive(q, l_clock, recvLock,sendLock,world_rank);
            }
            // else
            // {
            //     //Sender thread
            //     enter_cs(q, l_clock, recvLock,world_rank);
            //     cout<<"Process "<<world_rank<<"Entered CS"<<endl;
            //     exit_cs(q, l_clock, world_rank);
            // }
        }
    }
    MPI_Finalize();
}
