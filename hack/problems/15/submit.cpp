      
#include<bits/stdc++.h>
using namespace std;

int maxima(int a,int b,int c){
    /* Write your code here */
int maxi = a;
if(b>maxi)
maxi = b;

if(c>maxi)
maxi = c;

return maxi;

}
int main(int argc, char const *argv[])
{
    int t;
    int a,b,c;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>a>>b>>c;
    result = maxima(a,b,c);
    cout<<result<<endl;
    }
 	
 	
 	return 0;
} 

    