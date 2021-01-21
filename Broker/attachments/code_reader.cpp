    #include<iostream>
    using namespace std;
    int main()
    {
    	long long int N,min,max,*w,*b,*z,k=0;
    	long long int odd=0,even=0;
    	int tc;
    	cin>>tc;
    	while(tc)
    	{
    	
    	cin>>N>>min>>max;
    	int size=max-min+1;
    	z=new long long int[size];
    	w=new long long int[N];
    	b= new long long int[N];
    	for(int i=0;i<N;i++)
    	{
    		cin>>w[i]>>b[i];
     }
    	
    		for(int j=min;j<=max;j++)
    		{
    			int y=0;
    			int s;
    			 s=(w[y]*j)+b[y];
    			 if(N==1)
    			 {
    			 	z[k++]=s;
    			 }
    			 y++;
    			 if(y<N)
    			 {
    			 z[k++]=(w[y]*s)+b[y];
    			}
    	}
    	for(int i=0;i<max-min+1;i++)
    	{
    		if(z[i]%2==0)
    		even++;
    		else
    		odd++;
    	}
    	cout<<even<<" "<<odd;
    	tc--;
    }
    }
     