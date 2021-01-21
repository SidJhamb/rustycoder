#include<stdio.h>
int main()
{
    int N,Q,i;
    scanf("%d%d",&N,&Q);
    int* A = (int*)malloc(N*sizeof(int));
    for(i=0;i<N;i++)
    {
        scanf("%d",&A[i]);
    }
    for(i=0;i<Q;i++)
    {
        int operation,X,Y,sum=0;
        scanf("%d%d%d",&operation,&X,&Y);
        if(operation==1)
        {
            A[X]=Y;
        }
        else
        {
            while(X<=Y)
            {
                sum = sum+A[X++];
            }
            printf("%d\n",sum);
        }
        
    }
}