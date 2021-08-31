      
#include<bits/stdc++.h>
using namespace std;

void checkEvenOdd(int x){
    /* Write your code here */
    if (x % 2 == 0)
    cout<<x<<" is even number"<<endl;
    else
 cout<<x<<" is odd number"<<endl;

}
int main(int argc, char const *argv[])
{
    int t;
    int x;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>x;
    checkEvenOdd(x);
    }
 	
 	
 	return 0;
} 

    