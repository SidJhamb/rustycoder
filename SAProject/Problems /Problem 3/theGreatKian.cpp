#include <iostream>
using namespace std;
 
int main()
{
    long n,a[100000];
    long long v[4];
    cin>>n;
    for(long i=0;i<n;i++)
    {
        cin>>a[i];
        v[i%3]=v[i%3]+a[i];
    }
    cout<<v[0]<<" "<<v[1]<<" "<<v[2];
    return 0;
}