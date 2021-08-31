      
#include<bits/stdc++.h>
using namespace std;

int prime(int x){
    /* Write your code here */
   for(int i=2;i<=x/2;i++){
    if(x%i == 0)
          return 0;
}
return 1;

}
int main(int argc, char const *argv[])
{
    int t;
    int x;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>x;
    result = prime(x);
    cout<<result<<endl;
    }
 	
 	
 	return 0;
} 

    