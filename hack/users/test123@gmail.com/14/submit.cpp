          
#include<bits/stdc++.h>
using namespace std;

int square(int x){
    /* Write your code here */
return 25 + x;
}
int main(int argc, char const *argv[])
{
    int t;
    int x;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>x;
    result = square(x);
    cout<<result<<endl;
    }
 	
 	
 	return 0;
} 
        