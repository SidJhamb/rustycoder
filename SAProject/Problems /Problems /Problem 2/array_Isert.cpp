#include <bits/stdc++.h>
using namespace std;
 
int main()
{
    int n,q;
    cin>>n>>q;
    vector <int> v;
    int elem;
    for(int i=0;i<n;i++){
        cin>>elem;
        v.push_back(elem);
    }
    int t,x,y;
    while(q--){
        cin>>t>>x>>y;
        if(t==1){
            v[x] = y;
        }
        else {
            int sumx = 0;
            for(int i=x;i<=y;i++) sumx+=v[i];
            cout<<sumx<<endl;
        }
    }
    return 0;
}