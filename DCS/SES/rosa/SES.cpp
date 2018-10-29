#include <bits/stdc++.h>
using namespace std;
#include <omp.h>
#include <stdio.h>
int main()
{
	int q,ts;
	vector<pair<int,int> > buffer;
	int time_stamp=0,prevt=0;
	printf("Enter number of queries\n");
	cin>>q;
	int n;
	printf("Enter number of processes\n");
	cin>>n;
	int send,rec,th_wait,th_send;
	th_send=-1;
	int wait;
	vector<vector<pair<int,int>>>each_process;
	for(int i=0;i<n;i++){
		vector<pair<int,int> > v;
		each_process.push_back(v);
		}
	vector<int> times;
	for(int i=0;i<n;i++){
		times.push_back(0);
	}
	#pragma omp parallel num_threads(n) shared(each_process) 
	{
		for(int i=0;i<q;i++)
		{
			#pragma omp single 
			{
			printf("Enter the sending process number\n");
			cin>>send;
			printf("Enter the receiving process id\n");
			cin>>rec;
			printf("Enter time after which message was sent\n");
			cin>>ts;
			}
			int th_num = omp_get_thread_num();
			if(th_num==send){
				int flag=0;
				for(int i=0;i<each_process[send].size();i++){
					if(each_process[send][i].first == rec){
						for(int k=0;k<buffer.size();k++){
							if(buffer[k].first==rec && buffer[k].second==send){
								printf("Previous process %d has received message with time_stamp %d from process %d\n",rec,times[each_process[send][i].second], each_process[send][i].second);
								times[send]=times[send]+10*send;
								if(send==0){
									times[send]=times[send]+1;
								}
								each_process[send][i].first=rec;
								each_process[send][i].second=send;
								buffer.erase(buffer.begin()+k);
								pair<int,int> pp;
								pp.first=rec;
								pp.second=send;
								buffer.push_back(pp);
							}
						}
						flag=1;
					}

				}
				for(int i=0;i<buffer.size();i++){
					
					if(buffer[i].first==rec){
						flag=2;
						printf("Previous process %d has received message from process %d with timestamp %d\n",rec,buffer[i].second,times[buffer[i].second]);
					}
					for(int j=0;j<each_process[buffer[i].second].size();j++){
						if(each_process[buffer[i].second][j].first==rec){
							each_process[buffer[i].second].erase(each_process[buffer[i].second].begin()+j);
						}
					}
					buffer.erase(buffer.begin()+i);
					pair<int,int> p;
					p.first=rec;
					p.second= send;
					buffer.push_back(p);
				}

				if(flag==0 && ts>2)
				{
					vector<pair<int,int> > v = each_process[send];
					pair<int,int> p;
					p.first=rec;
					p.second= send;
					v.push_back(p);
					each_process[send]=v;
					printf("Process %d is  sent to process %d\n",send ,rec);
					times[send]=10*send+times[send];
					if(send==0)
					{
							times[send]=times[send]+1;
					}
					times[rec]=times[send];
					for(int i=0;i<v.size()-1;i++)
					{
						each_process[rec].push_back(v[i+1]);
					}

				}
				else if(flag==0)
				{
					vector<pair<int,int> > v = each_process[send];
					pair<int,int> p;
					p.first=rec;
					p.second= send;
					v.push_back(p);
					each_process[send]=v;
					buffer.push_back(p);
					
					times[send]=10*send+times[send];
					if(send==0)
					{
							times[send]=times[send]+1;
					}
				}
			if(flag==2)
			{
					vector<pair<int,int> > v = each_process[send];
					pair<int,int> p;
					p.first=rec;
					p.second= send;
					v.push_back(p);
					each_process[send]=v;
			}
			
			}	
	}
		#pragma omp single
		{
			for(int i=0;i<buffer.size();i++)
			{
				times[buffer[i].second]=10*buffer[i].second+times[buffer[i].second];
				if(times[buffer[i].second])
				{
					times[buffer[i].second]=times[buffer[i].second]+1;
				}
					times[buffer[i].first]=times[buffer[i].second];
				printf("Process %d is received from process %d with timestamp %d\n", rec,send,times[rec]);
			}
		}	
	}
	return 0;
}